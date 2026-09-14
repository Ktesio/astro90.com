# Astro90

An independent development studio making mobile games, agentic AI software, and tools for developers. **Built from curiosity.**

This repository contains the Astro90 website, the selected identity, and its design sources. The website is built with [Zola](https://www.getzola.org/), the Rust static site generator. The visual direction is cinematic and dark by default, with saffron as the accent.

## Run locally

Use Zola **0.23.4**. With [mise](https://mise.jdx.dev/):

```sh
mise trust
mise install
mise run dev
```

Open <http://127.0.0.1:1111>. Zola compiles the Sass and Tera 2 components directly. Normal builds need no Node step or application server. Fonts and artwork are served locally.

With Zola already installed:

```sh
zola serve --interface 127.0.0.1 --base-url http://127.0.0.1 --port 1111
```

## Build and check

```sh
zola check --skip-external-links
zola build
python3 scripts/check_site.py
```

The final command uses Python 3.11+ and its standard library. It checks the generated routes, internal links, assets, anchors, metadata, and basic document structure. `mise run check` runs the same checks in `.local/check-public/` so a production build cannot overwrite the running development preview. GitHub Actions runs the same checks using the pinned Zola release and a verified binary checksum.

The generated site is in `public/`. GitHub Actions validates changes and is configured to deploy `main` to Cloudflare Pages through Wrangler, after verifying owner-only Cloudflare Access protection. The deployment requires the account setup and CI secrets described in the [deployment guide](docs/DEPLOYMENT.md). Pull requests run validation without deploying.

## Pages

| Route | Purpose |
| --- | --- |
| `/` | Studio introduction and selected work |
| `/games/` | Mobile game collection |
| `/games/lighthouse/` | Lighthouse art, features, screenshots, and release state |
| `/games/inkube/` | Inkube art, features, screenshots, and release state |
| `/apps/` | Web app collection |
| `/apps/heronis/` | Personal agent product preview |
| `/apps/yanando/` | Productivity product preview |
| `/open-source/` | Public code and developer tools, with license distinctions |
| `/open-source/ktesio/` | Ktesio overview and source link |
| `/about/` | Studio story, disciplines and identity |
| `/studio/` | Redirect to `/about/`, preserving old links |
| `/contact/` | Public email, copy-address feedback and enquiry guidance |
| `/accessibility/` | Motion settings, keyboard controls and reporting help |
| `/brand/` | Visual identity standards |
| `/brand/states/` | Loading, unavailable, empty, confirmation and release specimens |
| `/404.html` | Custom missing-page design |

## This iteration

The site is a **static UI/UX iteration**. The spatial project index, screenshot viewer and pointer/scroll-driven scenes are presentation features. App Store and app-launch actions are visibly unavailable while products are in development. Contact uses the public address in `zola.toml` (`extra.email`) with standard email links and local copy feedback. No store URLs, account flows, submission forms, payments, analytics, API integrations, or product installations are connected.

The homepage opens on a painted night coast, with indigo mountains and a small saffron lighthouse. The beam responds to the pointer, or to touch and scrolling on phones, and settles when input stops. A soft overlap carries the landscape into Lighthouse's game world. Smaller introductory type leaves most of the first screen to the illustration. About combines the painted coast with an editorial introduction to the work. Reduced motion removes the beam and extra scroll distance. The header and footer use only the boxed “a” on mobile.

Lighthouse and Inkube use actual development screenshots. Heronis and Yanando use labeled interface studies. Ktesio is source available under its own non-commercial license; it is not presented as an OSI-licensed open-source project. No download counts, ratings, customer testimonials, or release dates are invented.

## Working on the site

- `content/`: page text, route structure, and front matter.
- `data/projects.toml`: shared product descriptions, artwork, status, and links.
- `templates/`: Tera 2 page templates and the shared components in `components.html`.
- `sass/site.scss`: shared tokens and product components; imports `_spatial.scss` for project compositions, `_night.scss` for the illustrated opening and `_completion.scss` for studio pages and feedback.
- `static/`: optimized delivery assets, self-hosted fonts, brand artwork, and presentation JavaScript.
- `assets/`: Blender scenes/scripts, shared monogram geometry, archived WebGL studies, render masters and product marketing image sources.
- `output/branding/`: the original logo and color explorations, preserved as design history. These are not published by Zola.

Image loading and retry states respond to real requests. The screenshot dialog reserves its image area, supports previous/next buttons and arrow keys, and offers the original image in a new tab. Screenshot links still work without JavaScript. Collections derive their count from the catalog and provide an empty fallback. `/404.html` supplies the missing-page design; a production host must use it for missing routes and return HTTP 404.

Use the existing components and semantic tokens when extending the site. Product facts belong in the catalog, so a status or description stays consistent across the home, collection, and detail pages.

The earlier Blender entrance remains in the repository as an identity study; no current page requests its animation. To edit the letter and its animation, open `assets/blender/astro90-identity.blend` in Blender. The reproducible scene builder is `assets/blender/build_identity.py`; `scripts/encode_identity.py` exports its frames as a transparent WebP that plays once. See the [asset guide](docs/ASSETS.md) for the render and encoding commands. Blender and Pillow are authoring dependencies; the website build remains Zola-only.

The original hero painting and its generation prompt are in `assets/source/studio/`. The browser uses optimized 1643 px and 960 px WebP deliveries. `scripts/prepare_media.py` regenerates the delivery images with Pillow; it does not alter the source composition.

## Identity and design standards

- [Brand guidelines](docs/BRAND.md)
- [Design system](docs/DESIGN-SYSTEM.md)
- [Confirmed creative direction](docs/DESIGN-DIRECTION.md)
- [Artwork sources and regeneration](docs/ASSETS.md)
- [Deployment and private preview access](docs/DEPLOYMENT.md)

Sora and Manrope are distributed under the SIL Open Font License; their license files are included. The public availability of this repository does not grant rights to Astro90 or product trademarks, artwork, or proprietary product code. See [asset notes](docs/ASSETS.md).
