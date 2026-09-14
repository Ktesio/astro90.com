# Cloudflare Pages deployment

The site is deployed with Wrangler from GitHub Actions. Zola **0.23.4** builds the HTML and assets; Wrangler **4.131.1** uploads them to the Direct Upload Pages project named `astro90`. The normal website has no server-side functions.

The deployment workflow is in `.github/workflows/check.yml`. Pull requests and branches run validation. Pushes to `main` also deploy after the protection checks pass. A manual run on `main` can provision the infrastructure first by enabling the `setup` input. Deployments run sequentially and are never cancelled halfway through by a newer push.

## Private preview

The intended custom hostnames are `astro90.com` and `www.astro90.com`. Access also protects the project's actual `pages.dev` hostname and its wildcard, which covers immutable deployment URLs and branch aliases. Each application uses a single reusable policy that allows exactly the owner email held in the `ASTRO90_ACCESS_EMAIL` secret. Email one-time codes are the only login method enabled for these applications. Sessions last 24 hours.

No broad email-domain rules, service-token exceptions, IP bypasses, or public paths are added. Existing account settings and unrelated applications are left alone. The script stops for conflicting resources rather than adopting them silently.

Before every upload, CI reads back the applications and policies, checks the domains and proxied DNS records, then makes anonymous requests to the site, assets, and every existing deployment alias. Those requests must redirect to this account's Access login. The checks run again after upload. An unavailable API, missing policy, changed owner rule, or failed edge check stops the workflow.

`static/_headers` also sends `X-Robots-Tag: noindex, nofollow, noarchive` during the preview. This header is an indexing preference; Access provides the actual restriction.

## Credentials

Create a Cloudflare API token scoped to the account containing Astro90 with these permissions:

| Resource | Permission |
| --- | --- |
| Account | Cloudflare Pages — Edit |
| Account | Access: Apps and Policies — Edit |
| Account | Access: Organizations, Identity Providers, and Groups — Edit |
| Zone: `astro90.com` only | Zone — Read |
| Zone: `astro90.com` only | DNS — Edit |

Keep the token and owner email in GitHub Actions secrets named `CLOUDFLARE_API_TOKEN` and `ASTRO90_ACCESS_EMAIL`. The account and zone IDs are discovered from the exact `astro90.com` zone, so no account ID is hardcoded. Neither secret is made available to pull-request deployment steps.

For local setup, create the ignored `.env.cloudflare` file:

```dotenv
CLOUDFLARE_API_TOKEN=<your scoped token>
ASTRO90_ACCESS_EMAIL=<the owner's email>
```

The script reads that file as data, without executing shell expressions. Do not commit it or paste tokens into issues or workflow logs. Wrangler OAuth login alone does not provide the DNS and Access permissions required here.

With GitHub CLI authenticated, the following stores both values through stdin without exposing them in command arguments:

```sh
python3 scripts/cloudflare.py configure-ci
```

## First deployment

Requirements: Zola 0.23.4, Node 22+, Python 3.11+, an active Cloudflare zone for `astro90.com`, and an existing Cloudflare Access organization.

```sh
npm ci
python3 scripts/cloudflare.py inspect
python3 scripts/cloudflare.py setup
bash scripts/build_pages.sh .local/pages-production
python3 scripts/cloudflare.py deploy --output .local/pages-production
```

Setup creates the Pages project with Wrangler and initially uploads only `scripts/cloudflare-bootstrap/`. Its small Worker returns HTTP 403 on every request; it contains no website content. Setup then connects both custom domains, updates only their web DNS records, waits for certificates, and creates the Access applications. This ordering accommodates Cloudflare's requirement to validate a custom domain before enabling Access on that hostname.

The real site can be uploaded only after Access passes both configuration and anonymous-request checks. The Zola output contains no `_worker.js`, so that upload replaces the temporary Worker with static hosting. If domain verification takes longer than four minutes, setup stops with the closed bootstrap still in place; rerun after DNS and certificates have settled.

An existing deployment with missing custom hostnames requires review before attachment, to prevent exposing its content on a new unprotected URL. Multiple existing A/AAAA/CNAME records for a hostname also require a reviewed DNS migration. MX and TXT records are preserved.

## Routine checks

```sh
python3 scripts/cloudflare.py verify
python3 -m unittest discover -s scripts -p 'test_cloudflare.py'
```

The first command verifies live protection without uploading content. It does not send login codes or sign in as the owner. Complete an owner login separately to verify the authenticated experience. Access blocks missing pages too; after authentication, Cloudflare Pages uses the generated `404.html` and returns HTTP 404.

To validate a prospective preview build locally:

```sh
CF_PAGES=1 CF_PAGES_BRANCH=preview CF_PAGES_URL=https://preview.astro90.pages.dev bash scripts/build_pages.sh .local/pages-preview
```

Preview HTML uses its own origin for navigation, images and canonical URLs. CI currently deploys only `main`; the wildcard Access application protects the immutable URLs that Pages creates for those production uploads.

## Public release later

Keep Access enabled until the owner explicitly requests the public release. The current CI script deliberately has no public or bypass switch.

For release, make a reviewed change to remove the private-only deployment checks and the preview `X-Robots-Tag` header. Keep normal site validation. Then remove only the Astro90 Access applications for the public custom hostnames through the API. Keep the Pages hostname and wildcard private unless there is a reason to publish those URLs too. Remove the reusable owner policy only if nothing still references it, and keep the shared identity provider and account settings intact.

Verify anonymous access to the homepage and assets, verify HTTP 404 for a missing route, and check that preview aliases still require authentication if they remain private. Reduce the CI token permissions once it no longer manages Access or DNS.

## References

- [Cloudflare Pages with external CI](https://developers.cloudflare.com/pages/how-to/use-direct-upload-with-continuous-integration/)
- [Zola build configuration](https://developers.cloudflare.com/pages/framework-guides/deploy-a-zola-site/)
- [Pages Access and custom-domain limitations](https://developers.cloudflare.com/pages/platform/known-issues/)
- [Access policy examples](https://developers.cloudflare.com/cloudflare-one/access-controls/policies/common-policies/)
