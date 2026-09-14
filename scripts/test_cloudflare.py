"""Security checks for the conditions which permit a private deployment."""
from copy import deepcopy
from io import BytesIO
import unittest
from unittest.mock import patch

from cloudflare import SetupError, access_redirect, site_destination, validate_owner_policy

OWNER = "owner@example.com"
POLICY = {"decision": "allow", "include": [{"email": {"email": OWNER}}]}


class OwnerPolicyTests(unittest.TestCase):
    def test_only_the_owner_is_accepted(self):
        validate_owner_policy(POLICY, OWNER)

    def test_bypass_and_service_auth_are_rejected(self):
        for decision in ("bypass", "non_identity", "deny"):
            with self.subTest(decision=decision), self.assertRaises(SetupError):
                validate_owner_policy({**POLICY, "decision": decision}, OWNER)

    def test_additional_email_or_everyone_is_rejected(self):
        for extra in ({"email": {"email": "another@example.com"}}, {"everyone": {}}):
            policy = deepcopy(POLICY)
            policy["include"].append(extra)
            with self.subTest(extra=extra), self.assertRaises(SetupError):
                validate_owner_policy(policy, OWNER)

    def test_domain_and_group_allow_rules_are_rejected(self):
        for rule in ({"email_domain": {"domain": "example.com"}}, {"group": {"id": "group"}}):
            with self.subTest(rule=rule), self.assertRaises(SetupError):
                validate_owner_policy({**POLICY, "include": [rule]}, OWNER)

    def test_conditions_that_lock_out_the_owner_are_rejected(self):
        with self.assertRaises(SetupError):
            validate_owner_policy({**POLICY, "exclude": POLICY["include"]}, OWNER)


class DestinationTests(unittest.TestCase):
    def test_paths_and_deployment_aliases_are_in_scope(self):
        for domain in ("astro90.com/public", "www.astro90.com", "astro90.pages.dev",
                       "*.astro90.pages.dev", "a1b2.astro90.pages.dev/private"):
            self.assertTrue(site_destination(domain, "astro90.pages.dev"))

    def test_similar_names_are_not_our_domains(self):
        for domain in ("evilastro90.com", "astro90.com.example.com", "evilastro90.pages.dev"):
            self.assertFalse(site_destination(domain, "astro90.pages.dev"))


class EdgeCheckTests(unittest.TestCase):
    def response(self, status, location):
        response = BytesIO(b"")
        response.status = status
        response.headers = {"Location": location}
        return response

    def test_requires_a_real_https_access_redirect(self):
        team = "studio.cloudflareaccess.com"
        for status, location, accepted in (
            (302, f"https://{team}/cdn-cgi/access/login/astro90.com", True),
            (200, f"https://{team}/cdn-cgi/access/login/astro90.com", False),
            (403, "", False),
            (302, f"http://{team}/cdn-cgi/access/login/astro90.com", False),
            (302, "https://studio.cloudflareaccess.com.example.com/cdn-cgi/access/login/", False),
            (302, f"https://{team}/unrelated", False),
        ):
            with self.subTest(status=status, location=location), patch("cloudflare.build_opener") as opener:
                opener.return_value.open.return_value = self.response(status, location)
                self.assertEqual(access_redirect("https://astro90.com/", team), accepted)


if __name__ == "__main__":
    unittest.main()
