# Astro90 website system

The executable styles are `sass/site.scss` and its imported `sass/_spatial.scss`, `sass/_night.scss` and `sass/_completion.scss`. Tera 2 components live in `templates/components.html`; `templates/atlas.html` provides the global project index.

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

Display typography is fluid and closely spaced. The desktop home headline scales to 116 px, leaving most of the first screen to the night landscape. Product names can become much larger as artwork. Phone headlines fit the available width. Supporting copy stays readable and short. Small labels inside illustrated interfaces are not controls.

## Layouts

- The homepage uses native sticky stages. Consecutive scenes overlap by one small viewport while full motion is enabled. The outgoing stage recedes and its title and phone fade before the incoming stage takes over. No wheel or touch-scroll events are intercepted; scene links use native smooth scrolling.
- Game worlds expand to the viewport. Their titles, backgrounds and device previews use distinct depth values.
- App previews are layered planes. Their captions remain real links and the illustrations are labeled interface studies.
- Collections use staggered columns on desktop and a single column on mobile.
- Detail pages preserve the product's own artwork, release state, features and screenshots.
- The homepage uses a full-bleed painting, responsive crops and a light anchored to the painted lantern. About uses a wide crop of the same coast between the introduction and project disciplines. Contact puts the public email in the first view. The 404 reuses the coast with a readable recovery area.
- The only intentional horizontal scroller is the mobile screenshot gallery.

At 650 px and below, the header and footer show only the boxed a. The index becomes a large project list and its utility links wrap. Short landscape viewports use compressed scenes. Reduced motion removes the extra scroll distance entirely.

## Index and controls

The Index button opens a native modal dialog. Five semantic project links are arranged around the central preview on desktop. Both pointer entry and keyboard focus select the preview. Escape or Close dismisses the dialog and restores focus to the opener. Native dialog behavior handles focus containment and background inertness.

The screenshot viewer is a separate native dialog. Closing it restores focus to the selected screenshot. Install and launch previews are disabled, with development status nearby. Do not substitute fake links for unavailable actions.

## Rendering and motion

The homepage uses a static 1643 × 957 painting with a smaller 960 px delivery. CSS object-fit fills the stage; responsive horizontal focus keeps the lighthouse in frame. The image loads at high priority and has intrinsic dimensions. A separate blurred light cone pivots around the painted lantern. The shared scheduler damps its response to pointer input, while touch scrolling guides it toward the water. A tap on the landscape can also aim it. No idle timeline, startup sequence or hidden content is involved.

The earlier Blender construction is retained as an identity study. No current page requests the animated WebP. If it is used again, retain its fixed scale, 3.2-second single play and finished still for reduced motion; it must never gate the page.

For product scenes, `static/js/site.js` owns one requestAnimationFrame scheduler. Scroll and pointer events update targets; 85 ms damping lets depth effects settle. Frames stop when targets settle, and hidden documents cancel the pending frame.

The stylesheet consumes `--progress`, `--arrival`, `--outro`, `--outro-content`, `--depth`, `--pointer-x` and `--pointer-y`. Scene bounds are cached and invalidated on resize and font load. Overlap progress follows the native scroll position so the outgoing image stays aligned with the incoming section. The original game entrances keep their own progress range. Soft leading masks remove a hard cut between the images.

The landscape begins handing off after 25 svh of scrolling on desktop or 20 svh on phones. A soft leading mask lets Lighthouse's existing coast enter over the night scene. The painting does not zoom with scrolling. The application and project scenes retain their own editorial timing.

## Fallbacks and accessibility

System reduced motion takes precedence over the session preference. The manual control appears in the index and footer. Reduced mode removes the landscape's light overlays, retains the full painting, removes spatial transforms and collapses scene heights and overlaps. Storage failure is harmless.

Without JavaScript, the landscape, all page content and a simple navigation fallback remain available; long scenes become normal sections. Screenshot anchors open their image directly.

Maintain one h1 and one main landmark per page, unique metadata, descriptive links, visible keyboard focus, image alternatives and 44 px action targets. Never require hover, color or motion to understand a product. Do not add loading gates, audio or repeating autoplay media. The finite brand entrance never blocks content or navigation. Recheck WCAG AA contrast for new combinations.

## Content and validation

`data/projects.toml` holds product facts. Detail Markdown selects a project and supplies editorial headings. Verify any new store destination before activating a release control. Source availability and open-source licensing must remain distinct.

Run `mise run check`, `node --check static/js/site.js` and `node --check static/js/feedback.js`. When the Blender scene changes, render and encode it again. The encoder checks every frame for a clear margin, the 3.2-second duration and single repeat count. Inspect desktop, tablet, phone and short landscape sizes. Exercise the index, focus restoration, galleries and motion control. Check actual changing transforms while scrolling, rather than relying solely on still images. Keep a factual record in `docs/VALIDATION.md`.


## Image and action states

`static/js/feedback.js` enhances `[data-media]` wrappers through `ui.media_status`. Preserve intrinsic image dimensions or an explicit aspect ratio. The viewer has a fixed image area so pending, error and loaded states do not move its controls.

- **Pending:** four small outlined squares echo the index, with one saffron square. Only real pending requests animate. An image can render as soon as its load event fires; there is no minimum delay or page-wide loading overlay.
- **Ready:** show the loaded image with a 240 ms fade. Cached images do not wait for an artificial entrance.
- **Unavailable:** show “Preview unavailable.” and a 44 px retry control. A visible request that takes 20 seconds offers retry with different wording; a late successful response can still recover. Retry adds a cache-busting query only to the chosen image.
- **Outside the viewport:** lazy images have no timeout until their frame approaches the viewport. Changing gallery selection replaces the pending image request and timeout. Closing the viewer clears its timer, releases its image source and restores focus.
- **Empty:** `ui.empty_state` explains that projects or screenshots have not been shared yet and links to About. Collection totals derive from current catalog entries.
- **Copying / copied / failed:** Contact confirms a successful clipboard write beside its button. A rejected write explains how to select the address or use the email link. The public address remains visible throughout.

All state changes use text, rather than color alone. Loading traces and fades honor both system and manual reduced motion. The public `/brand/states/` page contains labeled static specimens; its retry appearance is an illustration, while its Contact link leads to the actual copy control.

## Routes and recovery

The Index and footer expose About and Contact. Accessibility is in the footer and includes a motion control using the shared session preference. `/studio/` redirects to `/about/` with a no-script fallback; the route audit verifies that target. `/404.html` includes a home action and links to the collections and Contact. Configure the eventual static host to serve it with HTTP 404 for missing paths. Email is a standard `mailto:` link, never a fake form or invented success screen.
