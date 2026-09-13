# Validation record

September 13, 2026 · Spatial identity revision

## Build and content

- Zola 0.23.4 template/content check passed.
- Production build passed.
- Static audit passed: 12 HTML pages and 514 references checked, including internal destinations, local assets, fragment targets, unique page titles, descriptions, canonical URLs, IDs, and main/headline structure.
- JavaScript syntax checks passed for the presentation controller and WebGL source. The Three.js bundle rebuilt successfully with the pinned authoring dependencies.
- Original artwork is kept outside the published asset directory. The generated static site is approximately 3.5 MB. The 568 KB uncompressed scene module is loaded only for visible brand scenes with full motion enabled.

## Browser review

Reviewed in the Codex in-app WebKit browser at 1440 × 1000, 768 × 1024, 390 × 844, 320 × 740 and 812 × 450.

- The full page set was checked at phone width: no document-level horizontal overflow or broken eagerly loaded images.
- Home, game collection, app collection, product detail layouts, developer workbench, studio, and identity guide were visually reviewed.
- The spatial index opens and closes. Keyboard focus changes its central product preview; Escape dismisses it and restores focus to Index.
- Screenshot enlargement opens a native dialog, exposes the close control, and returns focus to the selected screenshot when dismissed.
- The header and footer use only the boxed a on phones, including short landscape layouts. No top reading-progress element remains.
- Pointer input changes the rendered monogram's perspective and lighting. The live WebGL host and changing pointer state were verified.
- Scrolling changes actual scene values: Lighthouse progressed from 0 to 0.9408 during review, changing its phone transform and background framing. The studio scene remains pinned while its scroll progress changes.
- The reduced-motion preference survives reload. The WebGL canvas is removed, the poster remains, and the hero collapses to a single viewport while all headings and links remain in the document.
- Disabled release actions and content links were checked. Mobile screenshot enlargement returns focus to its triggering screen.
- The final page-set browser pass reported no console errors or warnings.

The browser tool does not expose system media-preference or WebGL-loss emulation. Those fallback paths and the no-JavaScript layout were reviewed in source; the shared reduced-motion path was exercised through the manual control. No claim of system-preference emulation or a forced GPU failure is made.

## Contrast spot checks

| Pairing | Ratio |
| --- | --- |
| Supporting text on midnight | 8.53:1 |
| Quiet metadata on deep surface | 5.10:1 |
| Midnight text on saffron | 12.16:1 |
| Warm white on studio navy | 12.90:1 |

These are checks of the main token pairings, not a complete accessibility certification. Additional browser engines and physical-device testing remain useful before a public deployment.

## Iteration boundary

Store installation and app launch controls are intentionally unavailable. There are no live product integrations, accounts, forms, payment flows, analytics, or deployment automation. The repository's CI checks the static build only.
