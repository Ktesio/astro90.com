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

- The homepage uses native sticky stages. Consecutive scenes overlap by one small viewport while full motion is enabled. The outgoing stage recedes and its title and phone fade before the incoming stage takes over. No wheel or touch-scroll events are intercepted; scene links use native smooth scrolling.
- Game worlds expand to the viewport. Their titles, backgrounds and device previews use distinct depth values.
- App previews are layered planes. Their captions remain real links and the illustrations are labeled interface studies.
- Collections use staggered columns on desktop and a single column on mobile.
- Detail pages preserve the product's own artwork, release state, features and screenshots.
- The studio page uses the same Blender construction as the home, followed by concrete descriptions of the work.
- The only intentional horizontal scroller is the mobile screenshot gallery.

At 650 px and below, the header and footer show only the boxed a. The index becomes a large project list and its utility links wrap. Short landscape viewports use compressed scenes. Reduced motion removes the extra scroll distance entirely.

## Index and controls

The Index button opens a native modal dialog. Five semantic project links are arranged around the central preview on desktop. Both pointer entry and keyboard focus select the preview. Escape or Close dismisses the dialog and restores focus to the opener. Native dialog behavior handles focus containment and background inertness.

The screenshot viewer is a separate native dialog. Closing it restores focus to the selected screenshot. Install and launch previews are disabled, with development status nearby. Do not substitute fake links for unavailable actions.

## Rendering and motion

The brand entrance is an authored Blender render. Its physical filaments trace the logo and join into the solid object over 3.2 seconds. Camera and object scale stay fixed throughout. `static/js/site.js` inserts the transparent animated WebP once when full motion is enabled. The encoded repeat count is one; there is no idle loop and scrolling cannot restart it. The page remains usable during the entrance. After playback, the animation is replaced by the identically framed higher-resolution still and its decoded frames can be released.

For product scenes, `static/js/site.js` owns one requestAnimationFrame scheduler. Scroll and pointer events update targets; 85 ms damping lets depth effects settle. Frames stop when targets settle, and hidden documents cancel the pending frame.

The stylesheet consumes `--progress`, `--arrival`, `--outro`, `--outro-content`, `--depth`, `--pointer-x` and `--pointer-y`. Scene bounds are cached and invalidated on resize and font load. Overlap progress follows the native scroll position so the outgoing image stays aligned with the incoming section. The original game entrances keep their own progress range. Soft leading masks remove a hard cut between the images.

The fixed-size hero begins handing off after a short scroll. Avoid adding scroll distance that exists only for a camera zoom. The application and project scenes retain their own editorial timing.

## Fallbacks and accessibility

System reduced motion takes precedence over the session preference. The manual control appears in the index and footer. Reduced mode removes the animated image, shows the completed Blender still, removes spatial transforms and collapses scene heights and overlaps. Returning to full motion on the same page does not replay an entrance that already started. Storage failure is harmless.

Without JavaScript, the poster, all page content and a simple navigation fallback remain available; long scenes become normal sections. A failed animation image request restores the still.

Maintain one h1 and one main landmark per page, unique metadata, descriptive links, visible keyboard focus, image alternatives and 44 px action targets. Never require hover, color or motion to understand a product. Do not add loading gates, audio or repeating autoplay media. The finite brand entrance never blocks content or navigation. Recheck WCAG AA contrast for new combinations.

## Content and validation

`data/projects.toml` holds product facts. Detail Markdown selects a project and supplies editorial headings. Verify any new store destination before activating a release control. Source availability and open-source licensing must remain distinct.

Run `mise run check` and `node --check static/js/site.js`. When the Blender scene changes, render and encode it again. The encoder checks every frame for a clear margin, the 3.2-second duration and single repeat count. Inspect desktop, tablet, phone and short landscape sizes. Exercise the index, focus restoration, galleries and motion control. Check actual changing transforms while scrolling, rather than relying solely on still images. Keep a factual record in `docs/VALIDATION.md`.
