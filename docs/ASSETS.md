# Artwork and asset sources

## Studio identity

The logo concepts and color studies were generated during the Astro90 branding session with the built-in image generation tool. Original images and prompts are preserved under `output/branding/`.

Selected shape: `logo-options-v1/04-wordmark.png`. Selected palette: `wordmark-colors-v2/09-saffron.png`. The original monochrome shape, rather than the slightly different generated color-study lettering, supplies the website mark. `selected/identity.json` records the current dark-default decision.

The website uses the original raster alpha through a cropped SVG viewport and a solid saffron filter. The full wordmark is not a production outline vector. The boxed a is an optically reconstructed vector from the selected first letter, shared by the favicon and mobile signature.

## Original 3D artwork

`scripts/trace_monogram.py` writes the shared a contour and SVG. `assets/blender/make_monogram.py` extrudes it with a saffron face and navy backing, producing the fallback poster and sharing card. Geometry, camera placement, materials and lighting were authored for Astro90 in Blender 5.2.1 LTS. No external model packs or HDRIs are used.

- `assets/brand/monogram.json`: optical path and sampled contour.
- `assets/blender/astro90-monogram.blend`: editable physical letter scene.
- `assets/renders/monogram.png`: transparent 1500 × 1500 master.
- `static/media/monogram.webp`: optimized poster.
- `static/media/social-cover.png`: opaque sharing image, 1200 × 630.

Earlier orbital and interlocking studies remain in `assets/blender/` and `assets/renders/` as design history. They are retired from live page compositions.

To regenerate on macOS:

```sh
python3 scripts/trace_monogram.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets/blender/make_monogram.py
python3 scripts/prepare_media.py
```

On other systems, replace the Blender executable path with `blender`. Image preparation requires Pillow and only converts delivery formats; it does not change the artwork. Blender and Pillow are optional authoring tools, not website build dependencies.

## Real-time scene

`assets/webgl/scene.js` consumes the same contour. Its physical materials and studio lighting respond to pointer and scroll input through `static/js/site.js`. It uses Three.js 0.186.0 with the built-in RoomEnvironment. The pinned authoring package uses esbuild 0.28.2; run `npm ci` then `npm run build` in `assets/webgl/` to update the committed delivery bundle. Three.js's MIT license is included at `static/vendor/THREE-LICENSE.txt`; the generated bundle also carries linked license comments.

## Product artwork

Marketing images are from the studio's existing product projects. Only product-facing art/screens were copied; private implementation code, internal service configuration, secrets, and third-party visual references are excluded.

| Website source | Original project source | Use |
| --- | --- | --- |
| `assets/source/products/lighthouse-coast.png` | Lighthouse `App/Resources/Assets.xcassets/Coast.imageset/coast.png` | Illustrated coastal artwork |
| `assets/source/products/lighthouse-icon.png` | Lighthouse `AppIcon.appiconset/AppIcon.png` | Preserved app icon |
| `assets/source/products/lighthouse-home.png` | Lighthouse `Evidence/NauticalReview/main-phone/74-cabinet-harbor.png` | Home screen preview |
| `assets/source/products/lighthouse-world.png` | Lighthouse `Evidence/NauticalReview/main-phone/76-world-chart.png` | World chart preview |
| `assets/source/products/lighthouse-game.png` | Lighthouse `Evidence/NauticalReview/main-phone/77-tools-ready.png` | Puzzle screen preview |
| `assets/source/products/inkube-home.jpg` | Inkube `docs/img/home.jpg` | Home screen preview |
| `assets/source/products/inkube-game.jpg` | Inkube `docs/img/game.jpg` | Puzzle screen preview |
| `assets/source/products/inkube-gameover.jpg` | Inkube `docs/img/gameover.jpg` | Result screen preview |

All displayed screenshots are development previews. The Heronis and Yanando windows are original HTML/CSS interface studies for this website, explicitly labeled as such. They are not screenshots of a released product. The Ktesio terminal is an editorial illustration, not a live terminal or runtime telemetry.

## Fonts

Sora and Manrope Latin variable WOFF2 files are self-hosted in `static/fonts/`. They were obtained from the Google Fonts distribution. A Manrope TTF from the [official Google Fonts repository](https://github.com/google/fonts/tree/main/ofl/manrope) is retained under `assets/source/fonts/` for Blender text. Each font's SIL Open Font License is included in `static/fonts/` (`Sora-OFL.txt`, `Manrope-OFL.txt`). No third-party font request is made when visiting the website.

## Rights and publication

The Astro90 identity and product artwork belong to their respective studio/product owners. Publishing this website's repository does not relicense proprietary games, grant use of trademarks, or change any linked project's license. Ktesio's license is identified separately on its page. Check a repository's own license before using its code.

The original branding history and source masters live outside `static/` and are not included in a Zola website deployment. Deliveries use optimized WebP images, a PNG sharing card and SVG icons. The selected wordmark WebP preserves the original alpha losslessly.
