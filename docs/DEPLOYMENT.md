# Cloudflare Pages deployment

Cloudflare Pages owns the build and deployment pipeline through its GitHub integration with `iMagdy/astro90.com`. GitHub Actions independently builds and validates the website. It has read-only repository permissions, no hosting credentials, and no deployment steps.

## Pages settings

Configure these settings through the authenticated Cloudflare MCP connection, using the repository's existing Cloudflare GitHub app installation:

| Setting | Value |
| --- | --- |
| Repository | `iMagdy/astro90.com` |
| Production branch | `main` |
| Automatic production deployments | Enabled after Access verification |
| Build command | `bash scripts/build_pages.sh` |
| Build output | `public` |
| Root directory | Repository root |
| Build system | Version 3 |
| Production and preview variable | `ZOLA_VERSION=0.23.4` |
| Initial production and preview variable | `ASTRO90_BUILD_MODE=bootstrap` |
| After Access verification | `ASTRO90_BUILD_MODE=site` |

The build script runs Zola's content checks, checks presentation JavaScript syntax, builds the site, and verifies the generated routes, links, assets and metadata. Any failed check prevents Cloudflare from publishing that build. GitHub and Cloudflare run the same build validation independently; Cloudflare does not wait for the GitHub check to finish.

Production uses `https://astro90.com`. Preview builds use Cloudflare's `CF_PAGES_URL` so their navigation, images and canonical URLs stay on that preview. Keep automatic branch previews disabled until the wildcard Access application has been verified, then they can be enabled.

## Connect hosting safely

Use Cloudflare MCP to inspect the account, the active `astro90.com` zone, existing Pages projects, the GitHub integration and Access applications before changing them. Reuse matching resources. Create a Git-integrated Pages project when none exists; a Direct Upload project cannot be converted into a Git-integrated project.

For the first build, keep `ASTRO90_BUILD_MODE=bootstrap` in both production and preview. The script also defaults to bootstrap when that variable is absent on Cloudflare. This copies only `scripts/cloudflare-bootstrap/`: a minimal Worker returning HTTP 403 on every request and a generic missing-page fallback. No website content is included.

Connect `astro90.com` and, if used, `www.astro90.com` to the Pages project. Preserve mail and unrelated DNS records. Wait for the custom-domain certificates to become active before adding Access to those hostnames, as required by Cloudflare's domain verification.

Then configure and verify owner-only Access for all entry points:

- `astro90.com` and every additional custom hostname attached to the project.
- The project's actual `pages.dev` hostname.
- `*.<project-hostname>.pages.dev`, covering immutable deployments and branch aliases.

Use one allow policy containing exactly the owner email supplied for the private preview. Keep that private address in Cloudflare's policy rather than this public repository. Use the email one-time-code identity provider and a 24-hour session. Reuse an existing provider when possible. Do not add email-domain rules, Everyone, service-token exceptions, or bypass paths.

Read back the application hostnames, identity provider and complete policy rules. Inspect any more-specific overlapping applications that could override the intended restriction. Anonymous requests to the homepage, a nested page, a static asset, a missing route, the Pages hostname and an actual deployment URL must reach the account's Access login. Complete an owner login separately to verify the authenticated experience.

Only after those checks pass, set `ASTRO90_BUILD_MODE=site` for the protected environments, enable automatic production deployments, and trigger a new Cloudflare build. Check its commit and deployment status, then repeat the anonymous access checks. The Zola output contains no Worker, so the deployment replaces the temporary bootstrap with static hosting.

The build-mode variable controls which files are built; Cloudflare Access enforces authentication. Neither that variable nor the preview `X-Robots-Tag` header replaces an Access policy.

## Local verification

```sh
bash scripts/build_pages.sh .local/pages-production
CF_PAGES=1 ASTRO90_BUILD_MODE=site CF_PAGES_BRANCH=preview CF_PAGES_URL=https://preview.astro90.pages.dev bash scripts/build_pages.sh .local/pages-preview
CF_PAGES=1 ASTRO90_BUILD_MODE=bootstrap bash scripts/build_pages.sh .local/pages-bootstrap
```

Normal builds need Zola 0.23.4, Python 3.11+ and Node for JavaScript syntax validation. Node does not bundle the website or install application dependencies. The bootstrap output must contain only its two source files. It must never include the site's HTML, artwork or fonts.

Cloudflare Pages uses the generated `404.html` for missing routes and returns HTTP 404 after authentication. `static/_headers` applies a preview indexing preference plus standard response headers.

## Public release later

Keep Access enabled until the owner explicitly requests the public release. Make a reviewed change to remove the preview `X-Robots-Tag` header, then remove only the Astro90 Access applications for the hostnames intended to become public. Keep Pages and branch previews protected unless their release is also intended. Preserve shared identity providers and unrelated account settings.

Verify anonymous homepage and asset access, a real HTTP 404 for a missing route, and continued protection on any private preview URLs. Cloudflare's Git integration and the build-only GitHub workflow continue unchanged.

## References

- [Cloudflare Pages Git integration](https://developers.cloudflare.com/pages/configuration/git-integration/)
- [Zola build configuration](https://developers.cloudflare.com/pages/framework-guides/deploy-a-zola-site/)
- [Pages Access and custom-domain limitations](https://developers.cloudflare.com/pages/platform/known-issues/)
