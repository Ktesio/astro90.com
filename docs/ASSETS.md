# Artwork and asset sources

## Studio identity

The logo concepts and color studies were generated during the Astro90 branding session with the built-in image generation tool. Original images and prompts are preserved under `output/branding/`.

Selected shape: `logo-options-v1/04-wordmark.png`. Selected palette: `wordmark-colors-v2/09-saffron.png`. The original monochrome shape, rather than the slightly different generated color-study lettering, supplies the website mark. `selected/identity.json` records the current dark-default decision.

The website uses the original raster alpha through a cropped SVG viewport and a solid saffron filter. The full wordmark is not a production outline vector. The boxed a is an optically reconstructed vector from the selected first letter, shared by the favicon and mobile signature.

## Illustrated night coast

The homepage painting was generated with the built-in image generation tool for this revision. Its gouache-and-ink treatment uses layered midnight mountains, pines, a rocky inlet and a small warm lighthouse. It is studio artwork, not a capture from Lighthouse or any other game. No external reference image was supplied to the generator.

- `assets/source/studio/night-coast.png`: unchanged 1643 × 957 generation master.
- `assets/source/studio/night-coast-prompt.md`: complete generation prompt and provenance.
- `static/media/night-coast-1643.webp`: full-resolution web delivery, 186,092 bytes.
- `static/media/night-coast-960.webp`: smaller delivery, 72,220 bytes.
- `sass/_night.scss`: full-bleed composition, responsive image crops and soft CSS light.

`scripts/prepare_media.py` regenerates these WebPs with Pillow using quality 88. The source is not repainted or cropped during encoding. A responsive `srcset` chooses the delivery image; CSS crops the same panorama to keep the lighthouse in view on phones. The JavaScript measures that crop to anchor the light at the lantern, 74.5% across and 45% down in the master. All light movement is a browser presentation effect; it is not baked into an autoplay asset.

## Blender identity animation

`scripts/trace_monogram.py` supplies the selected a contour. `assets/blender/build_identity.py` models a rounded, crowned saffron shell, a recessed titanium core and eight physical contour filaments with depth connections. A locked orthographic camera and four rectangular studio lights produce the reflections. All geometry, materials, lights and animation keyframes are included in the native Blender 5.2.1 LTS scene. No external model packs, textures or HDRIs are required.

The 96-frame timeline is 3.2 seconds at 30 fps: contours are traced, depth connections form, then the cast surfaces become solid and the filaments disappear. Camera position, object position and scale remain fixed. The final 14 frames hold the completed object. Cycles renders 960 × 960 RGBA frames with denoising; the authoring script selects Metal when available and can also render on CPU.

- `assets/brand/monogram.json`: optical path and sampled contour.
- `assets/blender/astro90-identity.blend`: editable current model, lighting and animation.
- `assets/blender/build_identity.py`: reproducible scene builder and renderer.
- `assets/renders/monogram.png`: final transparent 960 × 960 frame.
- `static/media/monogram.webp`: finished still for reduced motion and fallback.
- `static/media/monogram-build.webp`: 720 × 720 transparent animation encoded to play once.
- `scripts/encode_identity.py`: delivery encoding and checks for framing, duration and repeat count.
- `static/media/social-cover.png`: now the 1200 × 630 night-coast sharing card, preserving the previous image URL.

To regenerate on macOS:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets/blender/build_identity.py -- --render
python3 scripts/encode_identity.py
```

Use `--preview` instead of `--render` to inspect four smaller keyframes before rendering the sequence. Frames are written into ignored `.local/identity-frames/`. On other systems, replace the executable path with `blender`; the encoder requires Pillow. These are optional authoring tools, not website build dependencies.

The Blender entrance is retained as an identity study. No current page requests it: `/studio/` now redirects to the editorial About page. Its optional `data-brand-film` enhancement remains in `static/js/site.js`, with one playback, frame release and a reduced-motion still, for a future identity demonstration. The homepage uses the painted coast.

Earlier orbital studies, the first static monogram scene and the WebGL experiment remain outside `static/` as design history. The WebGL authoring package writes only to `.local/`; its Three.js license is preserved beside the archived source. It is not used or delivered by the website.

## Digital exports

`scripts/generate_brand_assets.cjs` renders app icons from `assets/brand/monogram.json` and sharing cards from `assets/brand/social-card.html`. The current coast, wordmark alpha and existing game screens are composed without repainting their sources. `data/social.json` holds the route mapping and copy. The committed exports, dimensions, installation metadata and downloadable kit are documented in `docs/WEB-ASSETS.md`.

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
