# Validation record

## September 13, 2026 · Illustrated night opening

- Replaced the homepage Blender object with a full-bleed 1643 × 957 painted coast. The original PNG and full built-in image-generation prompt are committed under `assets/source/studio/`.
- The optimized landscape is 186,092 bytes at full resolution and 72,220 bytes at 960 px. The homepage has no brand-film host and does not request the 5.74 MiB construction animation; the studio page still uses it.
- Zola's content/template check, production build and static audit passed: 12 pages, 517 references. The audit now includes responsive `srcset` destinations. JavaScript and Python syntax checks passed.
- Reviewed the first fold at 1440 × 1000, 768 × 1024, 390 × 844, 320 × 740 and 812 × 450. The lighthouse remains visible, all hero copy and the work link fit, and the document has no horizontal overflow at these sizes.
- Pointer input changed the light direction while its source remained attached to the lantern. Resize checks confirmed its position followed the same crop as the painting. The shared animation scheduler stops after input settles; no autonomous timeline was added.
- Inspected the night-to-Lighthouse overlap on desktop and phone. Checked reverse scrolling after entering the game. A composited sticky stage fixes a WebKit alignment issue in which its absolute children could shift during reversal; the stage and painting both measured at viewport top zero in the reviewed midpoint.
- The work link reaches `#lighthouse`. The index opens and closes, and Escape restores focus to its trigger.
- The manual reduced-motion control hides the beam and glow, keeps the painting visible, makes the hero a single 844 px stage on the reviewed phone and removes scene overlap. The preference survived reload. Full motion was restored afterward.
- The browser reported no console errors or warnings during review. System preference emulation and touch-device emulation are not exposed by the browser tool; their shared behavior was reviewed in source. Physical touch hardware and other browser engines were not tested.

This update changes presentation and design documentation only. Product data, installation states, galleries and integrations remain as described below.

## Previous revision

September 13, 2026 · Blender construction and scene transitions

## Build and assets

- Zola 0.23.4 content/template check and production build passed.
- Static audit passed: 12 HTML pages and 516 references, including the dynamically loaded brand animation, internal destinations, assets, anchors, metadata and document structure.
- JavaScript and Python syntax checks passed. The published WebGL bundle was removed; normal website builds still need only Zola and Python's standard library for validation.
- Blender 5.2.1 LTS generated the native scene and rendered the construction with Cycles. The editable scene contains geometry, procedural materials, four studio lights, a locked orthographic camera and animation keyframes. The output path is relative to the project.
- All 96 source frames passed the encoder's framing check: 960 × 960 RGBA with at least 40 px clear space around visible geometry.
- The 720 px delivery animation contains 72 encoded frames after duplicate-frame consolidation, lasts exactly 3200 ms, and has a repeat count of one. The final still is 960 px. The animation is approximately 5.74 MiB and is requested only for the brand entrance with full motion enabled.
- The standard-library site audit checks the animation's RIFF structure, frame count, duration and repeat count in CI. The browser releases the animated image after playback and returns to the identically framed, sharper still.

## Browser review

Reviewed in the Codex in-app browser at 1440 × 1000, 768 × 1024, 390 × 844, 320 × 740 and 812 × 450.

- The home and studio letter stays framed on desktop, tablet, narrow phone and short landscape layouts. No document-level horizontal overflow was found at the reviewed sizes.
- Actual page-load playback was observed: traced physical filaments form the letter, followed by the solid metal object. Playback settles on the 960 px still, with no animation element left in the document.
- Index opens during construction; Escape closes it and restores focus. Navigation remains available throughout the entrance.
- Lighthouse-to-Inkube and Inkube-to-software handoffs were inspected at intermediate scroll positions on desktop and phone. The outgoing scene remains visible while the next enters, including during reverse scrolling. Soft leading masks replace the abrupt edge.
- Game entrance composition and phone depth motion remain active. Scene links use native smooth scrolling. The short hero hold and the studio page's normal document flow remove empty scroll travel.
- The header and footer retain the boxed a at mobile widths. There is no top reading-progress indicator.
- Reduced motion was enabled during playback: the animation disappeared, the still remained, the hero collapsed to one viewport and scene overlap became zero. Returning to full motion on the same page did not replay the animation. The reduced preference survived reload.
- The final playback review reported no console errors or warnings.

System media-preference emulation and JavaScript disabling are not exposed by the browser tool. The system-preference, no-JavaScript and failed-image paths were reviewed in source; the shared reduced-motion path was exercised through its manual control. Other browser engines and physical devices were not tested in this revision.

## Content and scope

The preceding full page-set review covered project details, galleries, disabled release actions, navigation and token contrast. Those product facts and controls are unchanged. This revision adds no accounts, forms, product integrations, analytics, payment flows or deployment. The GitHub workflow checks the static site and the animation export.
