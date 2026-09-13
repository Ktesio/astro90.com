# Astro90 website system

The executable styles are `sass/site.scss` and its imported `sass/_spatial.scss`. Tera 2 components live in `templates/components.html`; `templates/atlas.html` provides the global project index.

## Foundations

| Token | Value |
| --- | --- |
| Canvas | `#090E17` |
| Surface / raised surface | `#111925` / `#182230` |
| Navy / saffron | `#1E293B` / `#F4C84C` |
| Text / supporting / metadata | `#F0F1EE` / `#A4ADBB` / `#7E8B9D` |
| Content width | 1440 px maximum |
| Page gutter | `clamp(22px, 4.4vw, 88px)` |
| Display / body / code | Sora / Manrope / system monospace |
| Short response | 180–320 ms |
| Spatial input damping | 85 ms exponential time constant |

Display typography is fluid and closely spaced. The desktop home headline scales to 160 px, while product names can become much larger as artwork. Phone headlines fit the available width. Supporting copy stays readable and short. Small labels inside illustrated interfaces are not controls.

## Layouts

- The homepage uses native sticky stages. The hero, each game and the app sequence have their own scroll distance; no wheel or touch-scroll events are intercepted.
- Game worlds expand to the viewport. Their titles, backgrounds and device previews use distinct depth values.
- App previews are layered planes. Their captions remain real links and the illustrations are labeled interface studies.
- Collections use staggered columns on desktop and a single column on mobile.
- Detail pages preserve the product's own artwork, release state, features and screenshots.
- The studio page uses the same interactive a as the home, followed by concrete descriptions of the work.
- The only intentional horizontal scroller is the mobile screenshot gallery.

At 650 px and below, the header and footer show only the boxed a. The index becomes a large project list and its utility links wrap. Short landscape viewports use compressed scenes. Reduced motion removes the extra scroll distance entirely.

## Index and controls

The Index button opens a native modal dialog. Five semantic project links are arranged around the central preview on desktop. Both pointer entry and keyboard focus select the preview. Escape or Close dismisses the dialog and restores focus to the opener. Native dialog behavior handles focus containment and background inertness.

The screenshot viewer is a separate native dialog. Closing it restores focus to the selected screenshot. Install and launch previews are disabled, with development status nearby. Do not substitute fake links for unavailable actions.

## Input-led rendering

`static/js/site.js` owns one requestAnimationFrame scheduler. Scroll and pointer events update targets; damping lets them settle. Frames stop when targets settle, and hidden documents cancel the pending frame. There is no elapsed-time animation clock.

The stylesheet consumes `--progress`, `--arrival`, `--depth`, `--pointer-x` and `--pointer-y`. These drive transforms and image crops. The WebGL module is imported only on pages with a visible scene host and when full motion is enabled.

`assets/webgl/scene.js` builds the shared monogram contour with Three.js 0.186.0. It uses a physical saffron material, navy backing and a generated studio environment. Pixel ratio is capped at 1.7. The minified delivery bundle is committed so Zola remains the sole website build dependency. esbuild 0.28.2 and Three.js are pinned in the authoring package lock.

## Fallbacks and accessibility

System reduced motion takes precedence over the session preference. The manual control appears in the index and footer. Reduced mode disposes WebGL, shows the Blender poster, removes spatial transforms and collapses long scene heights. Storage failure is harmless.

Without JavaScript, the poster, all page content and a simple navigation fallback remain available; long scenes become normal sections. WebGL/module failure leaves the poster in place. A lost context restores the poster.

Maintain one h1 and one main landmark per page, unique metadata, descriptive links, visible keyboard focus, image alternatives and 44 px action targets. Never require hover, color or motion to understand a product. Do not add autoplay media or loading gates. Recheck WCAG AA contrast for new combinations.

## Content and validation

`data/projects.toml` holds product facts. Detail Markdown selects a project and supplies editorial headings. Verify any new store destination before activating a release control. Source availability and open-source licensing must remain distinct.

Run `mise run check` and `node --check static/js/site.js`. When scene code changes, rebuild its bundle and inspect desktop, tablet, phone and short landscape sizes. Exercise the index, focus restoration, galleries and motion control. Check actual changing transforms while scrolling, rather than relying solely on still images. Keep a factual record in `docs/VALIDATION.md`.
