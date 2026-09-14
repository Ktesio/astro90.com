# Astro90 digital asset kit

The kit extends the approved Studio Wordmark 04 and Saffron 09 identity. All icons use the existing vector a; social compositions use the approved night-coast painting. The artwork does not introduce another logo or return to the retired 3D hero.

## Files and uses

| Asset | Size / format | Use |
| --- | --- | --- |
| `favicon.ico` | 16, 32, 48 px in one file | Desktop and legacy browser fallback |
| `brand/favicon.svg` | SVG | Scalable browser tab mark |
| `brand/favicon-{16,32,48,96}.png` | PNG | Small raster icons; 96 px search favicon |
| `apple-touch-icon.png` | 180 × 180 PNG | Apple home-screen icon, opaque with no baked-in corners |
| `brand/icon-{192,512}.png` | PNG | Standard installed web-app icons |
| `brand/icon-maskable-{192,512}.png` | PNG | Android and other OS icon masks |
| `brand/app-icon-1024.png` | 1024 × 1024 PNG | High-resolution app artwork |
| `brand/avatar-1024.png` | 1024 × 1024 PNG | Social profile photo, safe for a circular crop |
| `brand/safari-pinned-tab.svg` | Monochrome SVG | Safari pinned-tab mask |
| `brand/wordmark-{saffron,white,midnight}.png` | 1320 × 244 transparent PNG | The original signature on dark or light surfaces |
| `brand/social/*.jpg` | 1200 × 630 JPEG | Nine page-specific Open Graph / social cards |
| `brand/social/post-square.jpg` | 1080 × 1080 JPEG | Square social post |
| `brand/social/post-portrait.jpg` | 1080 × 1350 JPEG | Portrait social post |
| `brand/social/profile-banner.jpg` | 1500 × 500 JPEG | Wide profile banner; preview each platform's crop |
| `brand/social/repository-cover.jpg` | 1280 × 640 JPEG | Repository social preview |
| `media/social-cover.png` | 1200 × 630 PNG | Updated artwork at the previous sharing-image URL |

Matching SVG sources accompany the app icons, avatar and pinned-tab mask. The complete kit is available at `/brand/astro90-asset-kit.zip`, with visual previews and download links on `/brand/`.

Keep the maskable artwork on its full saffron square. The entire letter fits inside the centered safe circle with a radius of 40% of the image width. Do not add rounded corners to maskable or Apple artwork: the operating system supplies its mask. The standard `any` icon intentionally preserves the rounded box. Do not combine `any` and `maskable` on one manifest entry.

The full wordmark PNGs preserve the selected raster alpha at its native cropped resolution. They are not outlined print vectors. Do not retype, stretch or upscale them for print. The compact a is a true vector.

## Website integration

`templates/partials/metadata.html` supplies icons, Apple appearance, a credentialed manifest link, complete Open Graph and Twitter image metadata, descriptive titles, descriptions and canonical URLs. `data/social.json` maps each route to its sharing image and alternative text. No social account handle is claimed or invented.

HTML minification is disabled because the current Zola minifier removes the `use-credentials` value from the manifest link. The generated-HTML check explicitly verifies this value so a future minifier change cannot silently break authenticated manifest loading.

`site.webmanifest` defines a stable root app ID, launch URL and scope, a standalone window, midnight launch and theme colors, and shortcuts to Games, Lighthouse and Inkube. Its same-origin paths work on production and branch previews. Installation presentation depends on the browser and operating system. This remains a static website: there is no offline cache, service worker, push permission or custom install prompt.

JSON-LD describes the real organization, website, page and navigation hierarchy. Product availability, pricing, reviews, addresses, dates and social accounts are not fabricated. The generated sitemap excludes the old Studio redirect, the error page and the internal interface-state specimens.

## Private preview and public release

Cloudflare Access continues to protect every route, including icons, the manifest, sharing images and the sitemap. The manifest link uses `crossorigin="use-credentials"` so an authenticated browser can request it. External search and social crawlers cannot retrieve the website while Access is enabled; link unfurling is ready for the public release, not publicly visible during this preview. No crawler bypass is added.

`extra.preview = true` in `zola.toml` produces `noindex, nofollow, noarchive` HTML metadata and `Disallow: /` in robots.txt. Non-production Cloudflare branches keep those directives even after the production configuration is released. The existing `X-Robots-Tag` response header remains in place too.

When the owner authorizes public release, set `extra.preview = false`, remove the preview indexing header from `static/_headers`, and follow `docs/DEPLOYMENT.md` to remove only the intended Access applications. Production robots.txt then advertises the sitemap. Keep the error page and interface-state specimens unindexed. Submit the public sitemap through the owner's search-console accounts after release; no verification tokens or accounts are assumed here.

## Reproduction

Normal Zola and CI builds use the committed assets and need no image tooling. The optional authoring script renders the approved vector contours and HTML layout through Sharp and a fresh headless Chrome process. It does not edit the painting. Layout source: `assets/brand/social-card.html`; route copy: `data/social.json`; icon geometry: `assets/brand/monogram.json`.

With Node.js, Python 3.11+ and Google Chrome installed:

```sh
npm install --prefix .local/brand-tools playwright@1.62.1 sharp@0.35.4
NODE_PATH="$PWD/.local/brand-tools/node_modules" node scripts/generate_brand_assets.cjs
python3 scripts/package_brand_assets.py
bash scripts/build_pages.sh .local/pages-production
```

`assets/brand/exports.json` records the generated files. The package step uses fixed archive timestamps so identical files produce the same kit. Review the small favicons, a circular mask of the avatar, and all social crops after changing any source. Nothing in this workflow publishes a social post or modifies a social profile.

## Platform references

- [Web app icon purposes and sizes](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/icons)
- [Browser installability](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)
- [Open Graph image metadata](https://ogp.me/)
- [Google favicon guidance](https://developers.google.com/search/docs/appearance/favicon-in-search)
- [Organization structured data](https://developers.google.com/search/docs/appearance/structured-data/organization)
- [Website name structured data](https://developers.google.com/search/docs/appearance/site-names)
