# Artwork and asset sources

## Studio identity

The logo concepts and color studies were generated during the Astro90 branding session with the built-in image generation tool. Original images and prompts are preserved under `output/branding/`.

Selected shape: `logo-options-v1/04-wordmark.png`. Selected palette: `wordmark-colors-v2/09-saffron.png`. The original monochrome shape, rather than the slightly different generated color-study lettering, supplies the website mark. `selected/identity.json` records the current dark-default decision.

The website uses the original raster alpha through a cropped SVG viewport and a solid saffron filter. It is not a production outline vector. The favicon is a simplified code-native optical `a` for the browser tab.

## Original 3D artwork

`assets/blender/make_sculptures.py` creates the orbital and interlocking studio sculptures. Geometry, camera placement, materials, lighting, and composition were authored for Astro90 in Blender 5.2.1 LTS. No external model packs or HDRIs are used.

- `assets/blender/astro90-orbit.blend`: editable orbital scene.
- `assets/renders/orbit.png`: transparent master, 1680 × 1540.
- `assets/renders/studio-sculpture.png`: transparent master, 1440 × 1000.
- `static/media/social-cover.png`: opaque sharing image, 1200 × 630.
- `static/media/orbit.webp` and `studio-sculpture.webp`: optimized website deliveries.

To regenerate on macOS:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python assets/blender/make_sculptures.py
python3 scripts/prepare_media.py
```

On other systems, replace the Blender executable path with `blender`. Image preparation requires Pillow and only converts delivery formats; it does not change the artwork. Blender and Pillow are optional authoring tools, not website build dependencies.

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

Sora and Manrope Latin variable WOFF2 files are self-hosted in `static/fonts/`. They were obtained from the Google Fonts distribution. Each font's SIL Open Font License is included alongside it (`Sora-OFL.txt`, `Manrope-OFL.txt`). No third-party font request is made when visiting the website.

## Rights and publication

The Astro90 identity and product artwork belong to their respective studio/product owners. Publishing this website's repository does not relicense proprietary games, grant use of trademarks, or change any linked project's license. Ktesio's license is identified separately on its page. Check a repository's own license before using its code.

The original branding history and source masters live outside `static/` and are not included in a Zola website deployment. Deliveries are optimized WebP images, apart from the sharing card and selected logo reference.
