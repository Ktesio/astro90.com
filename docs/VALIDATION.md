# Validation record

## September 14, 2026 · Mobile games and entertainment

- Narrowed the website to Lighthouse and Inkube. Removed the former app and code collections, their detail pages, navigation entries, interface illustrations, styles and sharing artwork. The homepage, About, Contact, brand guide, metadata, manifest and downloadable kit now describe the games studio.
- Production and Cloudflare preview builds passed: 11 HTML documents and 479 references. The audit now rejects unexpected routes and obsolete social exports. The kit contains 36 artwork exports, its manifest and guide; nine sharing cards map to the remaining content routes.
- Chrome checked ten pages at 1440 × 1000, 768 × 1024, 390 × 844, 320 × 740 and 812 × 450. No horizontal overflow or page/resource errors were reported. Reviewed the two-game index, revised studio pages, opening coast and the Inkube-to-studio overlap on desktop and phone.
- Verified index hover/focus previews and Escape focus restoration, screenshot navigation, disabled store controls, reduced motion, navigation without JavaScript, removed routes returning 404, the manifest shortcuts and the asset-kit download. The shorter footer navigation retains the compact mobile signature; its grid placement and 68 px mark were checked at three phone/landscape sizes.
- Scanned the rendered HTML, styles, scripts, sitemap and manifest for references to the retired products and sections. No matches remained. The game artwork, original identity, loading/error states and Cloudflare Access configuration are preserved.

## September 14, 2026 · Digital assets and discovery metadata

- Created 41 digital exports, including favicon resolutions, Apple and maskable app icons, avatars, transparent wordmarks, fourteen route-specific sharing cards, social post formats and a wide banner. The downloadable archive contains those files, the app manifest and its guide.
- Production and preview builds passed the expanded standard-library audit: 16 HTML documents and 867 references. Checks cover actual image dimensions, metadata consistency, canonical and schema origins, breadcrumb hierarchy, manifest icons and shortcuts, sitemap exclusions and exact archive contents.
- Chrome parsed the app manifest with no errors and reported no installability errors in a fresh, non-incognito test profile. A normal link click downloaded the complete asset archive successfully. No app was installed on the user's computer.
- Reviewed the Brand download section at 1440 × 1000 and 390 × 844. No horizontal overflow, page errors or failed resource requests were reported. The mobile header retains the compact a. Reviewed all fourteen social cards, the portrait and banner crops, and favicon exports on dark and light backgrounds at their real sizes.
- Verified every non-background pixel of the maskable letter remains inside the centered 40%-radius safe circle, with an entirely opaque background. Reviewed circular and Apple-style masks visually.
- A temporary release configuration rendered indexable production metadata and a sitemap directive, while the error page, interface specimens and non-production branches retained noindex. The committed configuration remains private. The bootstrap check still produces only its two closed-setup files.
- The generated-HTML check caught Zola's minifier collapsing the manifest's `crossorigin="use-credentials"` attribute. HTML minification is disabled to preserve authenticated manifest loading. Owner authentication and installation on physical iOS/Android devices were not performed; Cloudflare Access remains in place.

## September 13, 2026 · Studio pages and interface states

- Added About, Contact, Accessibility and a public interface-state gallery under Brand. The existing Studio route redirects to About. Contact uses the owner-confirmed `hello@astro90.com`; no email was sent and no submission service was added.
- Rebuilt the 404 around the approved night landscape. An actual unknown local URL served the custom recovery page, including working root-relative collection and Contact destinations. The static audit verifies the Studio redirect and its no-script fallback link.
- Production validation passed for 16 HTML documents and 736 references. Zola checks, asset and link resolution, unique metadata, document structure and JavaScript syntax passed. `mise run check` now uses an isolated generated directory so it cannot replace the running local preview with production URLs.
- An isolated content build exercised both an empty project collection and a project with no screenshots. Both compiled their intended fallback content, and the collection displayed a zero count. Current collection counts derive from the catalog.
- Reviewed About and Contact at 1440 × 1000 and 390 × 844; reviewed the 404 at 1440 × 1000 and 320 × 740, and Accessibility and state specimens at 320 × 740. Reviewed the game collection at 768 × 1024. The checked pages had no document-level horizontal overflow. The compact a remains the mobile header/footer signature.
- Email copy produced its inline confirmation. The clipboard rejection path retains the public address and explains manual selection; that path was reviewed in source rather than forcing a browser permission denial.
- The screenshot viewer supports previous/next controls, arrow keys, an original-image link and Escape. Closing restored focus to the selected thumbnail. It also fit an 812 × 450 landscape viewport after retry. Its image area remains fixed across pending, unavailable and loaded states; the reviewed phone dialog measured 771.36 px before and after retry.
- A temporary loopback fixture delayed images and returned failed responses. The viewer and an inline phone preview showed their pending/error states and recovered through Try again. Switching to a second screenshot while the first request was pending kept the second selection and preserved the dialog height. These fixtures are local QA only and do not ship.
- Browser review caught a lazy-image decode wait that could strand a loaded preview in its pending state. The final implementation uses native image load events and current-image dimensions. Both game collection previews then reached the ready state, including the lazy Inkube image.
- The new Accessibility motion control updated the shared preference; navigating to the state gallery retained it and removed the loading trace animation. Full motion was restored afterward. The no-JavaScript, operating-system preference and 20-second slow-request recovery paths were reviewed in source; system media emulation and JavaScript disabling are not exposed by the browser tool.
- About now replaces the former Studio page. Blender sources remain as an archived identity study, and no current page requests the construction animation. The approved homepage landscape and game-scene geometry are preserved.

This is still a static presentation iteration. It adds no forms, accounts, store installations, analytics or backend integrations. Deployment remains a separate step; the eventual host must serve `404.html` with HTTP 404 for missing routes.

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
