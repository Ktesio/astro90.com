"""Provision and verify Astro90's private Pages deployment through Cloudflare's API.

Wrangler creates the Pages project and uploads files. This script manages the
DNS and Access resources which Wrangler does not expose. No credentials or
owner email are stored in the repository.
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.cloudflare.com/client/v4"
PROJECT = "astro90"
DOMAIN = "astro90.com"
CUSTOM_HOSTS = (DOMAIN, f"www.{DOMAIN}")
POLICY_NAME = "Astro90 private preview owner"
APP_PREFIX = "Astro90 private: "


class SetupError(RuntimeError):
    pass


def load_local_environment():
    path = ROOT / ".env.cloudflare"
    if path.is_file() and not os.environ.get("CI"):
        # Parse values as data; never execute an environment file as shell code.
        for line in path.read_text().splitlines():
            key, separator, value = line.strip().partition("=")
            if separator and key in {"CLOUDFLARE_API_TOKEN", "ASTRO90_ACCESS_EMAIL"}:
                os.environ.setdefault(key, value.strip().strip("\"'"))


class Cloudflare:
    def __init__(self):
        self.token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
        self.owner = os.environ.get("ASTRO90_ACCESS_EMAIL", "").strip().lower()
        if not self.token:
            raise SetupError("CLOUDFLARE_API_TOKEN is required.")
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", self.owner):
            raise SetupError("ASTRO90_ACCESS_EMAIL must contain the owner's email address.")
        zones = self.list("/zones", name=DOMAIN)
        if len(zones) != 1 or zones[0]["name"] != DOMAIN:
            raise SetupError("The token must have access to exactly the astro90.com zone.")
        zone = zones[0]
        if zone["status"] != "active":
            raise SetupError("astro90.com is not an active Cloudflare zone yet.")
        self.zone_id = zone["id"]
        self.account_id = zone["account"]["id"]
        self.account = f"/accounts/{self.account_id}"
        self.project_path = f"{self.account}/pages/projects/{PROJECT}"
        self.pages_host = f"{PROJECT}.pages.dev"

    def request(self, method, path, body=None, *, missing_ok=False, envelope=False):
        request = Request(
            API + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"},
            method=method,
        )
        try:
            with urlopen(request, timeout=30) as response:
                result = json.load(response)
        except HTTPError as error:
            if missing_ok and error.code == 404:
                return None
            try:
                details = json.load(error).get("errors", [])
                codes = ", ".join(str(item.get("code")) for item in details)
            except (ValueError, AttributeError):
                codes = "unavailable"
            # API responses can contain private configuration: report only codes.
            raise SetupError(f"Cloudflare {method} {path.split('?')[0]}: HTTP {error.code}, codes {codes}") from None
        if not result.get("success"):
            raise SetupError(f"Cloudflare rejected {method} {path.split('?')[0]}")
        return result if envelope else result.get("result")

    def list(self, path, **filters):
        result, page = [], 1
        while True:
            data = self.request("GET", path + "?" + urlencode({**filters, "page": page, "per_page": 50}), envelope=True)
            items = data.get("result") or []
            if not isinstance(items, list):
                raise SetupError(f"Unexpected list response from {path}")
            result.extend(items)
            info = data.get("result_info") or {}
            if page >= info.get("total_pages", 1):
                return result
            page += 1

    def project(self):
        project = self.request("GET", self.project_path, missing_ok=True)
        if project:
            self.pages_host = project["subdomain"]
            if not re.fullmatch(r"[a-z0-9-]+\.pages\.dev", self.pages_host):
                raise SetupError("Cloudflare returned an unexpected Pages hostname.")
            if project.get("source"):
                raise SetupError("The existing project uses Git integration; review it before switching to CI uploads.")
            if project.get("production_branch") != "main":
                raise SetupError("The existing Pages production branch must be main.")
        return project

    def wrangler(self, *arguments):
        subprocess.run(
            ["npx", "--no-install", "wrangler", *arguments], cwd=ROOT, check=True,
            env={**os.environ, "CLOUDFLARE_ACCOUNT_ID": self.account_id, "WRANGLER_SEND_METRICS": "false"},
        )

    @property
    def hosts(self):
        return (*CUSTOM_HOSTS, self.pages_host, f"*.{self.pages_host}")

    def organization(self):
        organization = self.request("GET", f"{self.account}/access/organizations", missing_ok=True)
        if not organization or not organization.get("auth_domain"):
            raise SetupError("This account needs a Cloudflare Access organization before setup can continue.")
        return organization

    def setup(self):
        # Confirm Access is available before changing any hosting or DNS.
        self.organization()
        if not self.project():
            self.wrangler("pages", "project", "create", PROJECT, "--production-branch", "main")
        project = self.project()
        domains = {item["name"]: item for item in self.list(f"{self.project_path}/domains")}
        if project.get("canonical_deployment") and any(host not in domains for host in CUSTOM_HOSTS):
            raise SetupError("An existing deployment needs review before new hostnames can be safely attached.")
        if not project.get("canonical_deployment"):
            print("Publishing the empty 403 bootstrap; no website content is included.", flush=True)
            self.wrangler("pages", "deploy", "scripts/cloudflare-bootstrap", "--project-name", PROJECT,
                          "--branch", "main", "--commit-message", "Private hosting bootstrap", "--commit-dirty=true")

        for host in CUSTOM_HOSTS:
            # Pages must issue the certificate before an Access application is
            # added for a new custom hostname. The bootstrap denies all requests.
            if host not in domains:
                self.request("POST", f"{self.project_path}/domains", {"name": host})
            self.ensure_dns(host)
        self.wait_for_domains()
        self.ensure_access()
        self.verify()
        self.verify_edge()
        print("Private Pages hosting is ready for the website deployment.")

    def ensure_dns(self, host):
        records = self.list(f"/zones/{self.zone_id}/dns_records", name=host)
        web_records = [record for record in records if record["type"] in {"A", "AAAA", "CNAME"}]
        desired = {"type": "CNAME", "name": host, "content": self.pages_host, "proxied": True, "ttl": 1}
        if len(web_records) > 1:
            raise SetupError(f"Multiple web DNS records exist for {host}; review their migration first.")
        if web_records:
            record = web_records[0]
            if all(record.get(key) == value for key, value in desired.items()):
                return
            self.request("PATCH", f"/zones/{self.zone_id}/dns_records/{record['id']}", desired)
        else:
            self.request("POST", f"/zones/{self.zone_id}/dns_records", desired)
        print(f"DNS points {host} to Pages; mail records are preserved.", flush=True)

    def wait_for_domains(self):
        for attempt in range(24):
            pending = []
            for host in CUSTOM_HOSTS:
                domain = self.request("GET", f"{self.project_path}/domains/{host}")
                if domain.get("status") != "active":
                    pending.append(host)
            if not pending:
                return
            if attempt % 4 == 0:
                print("Waiting for domain certificates: " + ", ".join(pending), flush=True)
            time.sleep(10)
        raise SetupError("Domain activation is still pending. The bootstrap remains closed; rerun setup later.")

    def ensure_access(self):
        idps = self.list(f"{self.account}/access/identity_providers")
        otp = next((idp for idp in idps if idp["type"] == "onetimepin"), None)
        if not otp:
            otp = self.request("POST", f"{self.account}/access/identity_providers",
                               {"name": "Email code", "type": "onetimepin", "config": {}})
        policies = self.list(f"{self.account}/access/policies")
        matching = [policy for policy in policies if policy["name"] == POLICY_NAME]
        if len(matching) > 1:
            raise SetupError("Duplicate Astro90 owner policies need review.")
        policy = matching[0] if matching else self.request("POST", f"{self.account}/access/policies", {
            "name": POLICY_NAME, "decision": "allow",
            "include": [{"email": {"email": self.owner}}], "exclude": [], "require": [],
        })
        validate_owner_policy(policy, self.owner)
        apps = self.list(f"{self.account}/access/apps")
        for host in self.hosts:
            name = APP_PREFIX + host
            matching = [app for app in apps if app.get("domain") == host or app.get("name") == name]
            if matching:
                if len(matching) != 1 or matching[0].get("name") != name:
                    raise SetupError(f"An existing Access application for {host} needs review before adoption.")
                # Existing applications are verified rather than overwritten:
                # drift must never silently weaken protection or other settings.
                continue
            self.request("POST", f"{self.account}/access/apps", {
                "name": name, "domain": host, "type": "self_hosted", "session_duration": "24h",
                "allowed_idps": [otp["id"]], "auto_redirect_to_identity": False,
                "app_launcher_visible": False, "allow_authenticate_via_warp": False,
                "policies": [{"id": policy["id"], "precedence": 1}],
            })
            print(f"Owner-only Access application created for {host}.", flush=True)

    def verify(self):
        if not self.project():
            raise SetupError("The Pages project has not been provisioned; run setup first.")
        organization = self.organization()
        idps = {item["id"]: item for item in self.list(f"{self.account}/access/identity_providers")}
        apps = self.list(f"{self.account}/access/apps")
        exact = {app.get("domain"): app for app in apps if app.get("domain") in self.hosts}
        if set(exact) != set(self.hosts):
            raise SetupError("Missing Access protection for: " + ", ".join(set(self.hosts) - set(exact)))
        for app in apps:
            destinations = application_domains(app)
            if not any(site_destination(value, self.pages_host) for value in destinations):
                continue
            if app.get("type") != "self_hosted":
                raise SetupError("An overlapping Access application has an unexpected type.")
            policies = self.list(f"{self.account}/access/apps/{app['id']}/policies")
            if len(policies) != 1:
                raise SetupError("Each Astro90 Access application must have exactly one owner-only policy.")
            validate_owner_policy(policies[0], self.owner)
            allowed = app.get("allowed_idps") or []
            if not allowed or any(idps.get(key, {}).get("type") != "onetimepin" for key in allowed):
                raise SetupError("Astro90 Access must authenticate through the email-code provider only.")
            if app.get("allow_authenticate_via_warp"):
                raise SetupError("Astro90 Access must require direct email authentication.")
        for host in CUSTOM_HOSTS:
            domain = self.request("GET", f"{self.project_path}/domains/{host}")
            if domain.get("status") != "active":
                raise SetupError(f"The custom domain {host} is not active.")
            records = self.list(f"/zones/{self.zone_id}/dns_records", name=host)
            records = [record for record in records if record["type"] in {"A", "AAAA", "CNAME"}]
            if len(records) != 1 or records[0]["type"] != "CNAME" or records[0]["content"] != self.pages_host or not records[0]["proxied"]:
                raise SetupError(f"{host} must have one proxied CNAME pointing to this Pages project.")
        print("Verified owner-only Access policies, email authentication, custom domains and DNS.", flush=True)
        return organization["auth_domain"]

    def verify_edge(self):
        team_host = self.organization()["auth_domain"]
        urls = {f"https://{host}/" for host in (*CUSTOM_HOSTS, self.pages_host)}
        urls.update(f"https://{DOMAIN}{path}" for path in (
            "/about/", "/contact/", "/media/night-coast-960.webp", "/js/site.js", "/missing-page-check/"))
        for deployment in self.list(f"{self.project_path}/deployments"):
            urls.add(deployment["url"].rstrip("/") + "/")
            for alias in deployment.get("aliases") or []:
                urls.add(alias.rstrip("/") + "/")
        for url in sorted(urls):
            parsed = urlsplit(url)
            if parsed.scheme != "https" or not site_destination(parsed.hostname or "", self.pages_host):
                raise SetupError("A deployment returned a URL outside the Astro90 hosts.")
            protected = False
            for attempt in range(6):
                if access_redirect(url, team_host):
                    protected = True
                    break
                time.sleep(5)
            if not protected:
                raise SetupError(f"Anonymous request did not reach Cloudflare Access: {url}")
        print(f"Verified {len(urls)} anonymous requests reach Access, including deployment aliases and static assets.", flush=True)

    def deploy(self, output):
        self.verify()
        self.verify_edge()
        subprocess.run([sys.executable, "scripts/check_site.py", output], cwd=ROOT, check=True)
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        self.wrangler("pages", "deploy", output, "--project-name", PROJECT, "--branch", "main", "--commit-hash", commit)
        self.verify()
        self.verify_edge()


def validate_owner_policy(policy, owner):
    expected = [{"email": {"email": owner.lower()}}]
    if policy.get("decision") != "allow" or policy.get("include") != expected:
        raise SetupError("The Access allow policy must include only the configured owner email.")
    if policy.get("exclude") or policy.get("require") or policy.get("approval_required"):
        raise SetupError("Unexpected additional conditions in the owner Access policy.")


def application_domains(app):
    domains = [app.get("domain", ""), *(app.get("self_hosted_domains") or [])]
    domains.extend(item.get("uri", "") for item in app.get("destinations") or [])
    return domains


def site_destination(value, pages_host):
    host = value.removeprefix("https://").removeprefix("http://").split("/", 1)[0]
    return host in CUSTOM_HOSTS or host == pages_host or host.endswith("." + pages_host)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        return None


def access_redirect(url, team_host):
    try:
        response = build_opener(NoRedirect).open(Request(url, headers={"User-Agent": "Astro90-deployment-check"}), timeout=20)
    except HTTPError as error:
        response = error
    except (URLError, TimeoutError):
        return False
    with response:
        destination = urlsplit(response.headers.get("Location", ""))
        return response.status in {302, 303, 307, 308} and destination.scheme == "https" and destination.hostname == team_host and destination.path.startswith("/cdn-cgi/access/login/")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["inspect", "configure-ci", "setup", "verify", "deploy"])
    parser.add_argument("--output", default="public")
    args = parser.parse_args()
    load_local_environment()
    client = Cloudflare()
    if args.command == "configure-ci":
        # Send secrets on stdin, never in command arguments or workflow files.
        for name, value in (("CLOUDFLARE_API_TOKEN", client.token), ("ASTRO90_ACCESS_EMAIL", client.owner)):
            subprocess.run(["gh", "secret", "set", name, "--repo", "iMagdy/astro90.com"],
                           input=value, text=True, check=True, cwd=ROOT)
        print("Stored the deployment token and owner email as GitHub Actions secrets.")
    elif args.command == "inspect":
        project = client.project()
        organization = client.organization()
        print(json.dumps({"zone": DOMAIN, "account_id": client.account_id,
                          "project_exists": bool(project), "pages_hostname": client.pages_host,
                          "access_team": organization["auth_domain"]}, indent=2))
    elif args.command == "setup":
        client.setup()
    elif args.command == "verify":
        client.verify()
        client.verify_edge()
    else:
        client.deploy(args.output)


if __name__ == "__main__":
    try:
        main()
    except (SetupError, URLError, subprocess.CalledProcessError) as error:
        print(f"Cloudflare setup stopped: {error}", file=sys.stderr)
        sys.exit(1)
