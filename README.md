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

Open <http://127.0.0.1:1111>. Zola compiles the Sass and Tera 2 components directly. Normal builds need no Node step or application server. Fonts, artwork and the Blender animation are served locally.

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

The final command uses Python 3.11+ and its standard library. It checks the generated routes, internal links, assets, anchors, metadata, and basic document structure. `mise run check` runs all three commands. GitHub Actions runs the same checks using the pinned Zola release and a verified binary checksum.

The generated site is in `public/`. Upload that directory to a static host when deployment is wanted. The included workflow validates the site; it does not deploy it.

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
| `/studio/` | Studio story and principles |
| `/brand/` | Visual identity standards |
| `/404.html` | Custom missing-page design |

## This iteration

The site is a **static UI/UX iteration**. The spatial project index, screenshot viewer and pointer/scroll-driven scenes are presentation features. App Store and app-launch actions are visibly unavailable while products are in development. No store URLs, account flows, forms, payments, analytics, API integrations, or product installations are connected.

The homepage moves from a physical version of the selected “a” into full-screen game worlds and layered app previews. The letter is constructed once on page load in a 3.2-second Blender animation; its camera and scale stay fixed. Game sections overlap as one recedes and the next enters. System reduced motion and the manual control remove the extra scroll distance and show the finished Blender still. The header and footer use only the boxed “a” on mobile.

Lighthouse and Inkube use actual development screenshots. Heronis and Yanando use labeled interface studies. Ktesio is source available under its own non-commercial license; it is not presented as an OSI-licensed open-source project. No download counts, ratings, customer testimonials, or release dates are invented.

## Working on the site

- `content/`: page text, route structure, and front matter.
- `data/projects.toml`: shared product descriptions, artwork, status, and links.
- `templates/`: Tera 2 page templates and the shared components in `components.html`.
- `sass/site.scss`: shared tokens and product components; imports `sass/_spatial.scss` for the spatial compositions and responsive rules.
- `static/`: optimized delivery assets, self-hosted fonts, brand artwork, and presentation JavaScript.
- `assets/`: Blender scenes/scripts, shared monogram geometry, archived WebGL studies, render masters and product marketing image sources.
- `output/branding/`: the original logo and color explorations, preserved as design history. These are not published by Zola.

Use the existing components and semantic tokens when extending the site. Product facts belong in the catalog, so a status or description stays consistent across the home, collection, and detail pages.

To edit the letter and its animation, open `assets/blender/astro90-identity.blend` in Blender. The reproducible scene builder is `assets/blender/build_identity.py`; `scripts/encode_identity.py` exports its frames as a transparent WebP that plays once. See the [asset guide](docs/ASSETS.md) for the render and encoding commands. Blender and Pillow are authoring dependencies; the website build remains Zola-only.

## Identity and design standards

- [Brand guidelines](docs/BRAND.md)
- [Design system](docs/DESIGN-SYSTEM.md)
- [Confirmed creative direction](docs/DESIGN-DIRECTION.md)
- [Artwork sources and regeneration](docs/ASSETS.md)

Sora and Manrope are distributed under the SIL Open Font License; their license files are included. The public availability of this repository does not grant rights to Astro90 or product trademarks, artwork, or proprietary product code. See [asset notes](docs/ASSETS.md).
