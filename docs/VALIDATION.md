# Validation record

September 13, 2026 · Initial static UI/UX iteration

## Build and content

- Zola 0.23.4 template/content check passed.
- Production build passed.
- Static audit passed: 12 HTML pages and 385 references checked, including internal destinations, local assets, fragment targets, unique page titles, descriptions, canonical URLs, IDs, and main/headline structure.
- JavaScript syntax check passed with `node --check static/js/site.js`.
- Original artwork is kept outside the published asset directory. The complete generated static site is approximately 3.3 MB, with images loaded as needed.

## Browser review

Reviewed in the Codex in-app WebKit browser at 1440 × 1000, 768 × 1024, 390 × 844, and 320 × 740.

- The full page set was checked at phone width: no document-level horizontal overflow or broken eagerly loaded images.
- Home, game collection, app collection, product detail layouts, developer workbench, studio, and identity guide were visually reviewed.
- Mobile navigation opens and closes; Escape dismisses it and returns focus to its toggle.
- Screenshot enlargement opens a native dialog, exposes the close control, and returns focus to the selected screenshot when dismissed.
- The ambient-motion preference survives a reload. Paused pages retain visible headlines, artwork, and navigation.
- Active-section navigation, disabled release actions, and content links were checked.
- The final page-set browser pass reported no console errors or warnings.

The stylesheet includes system reduced-motion overrides that remove animations/transitions and preserve all content. The browser tool does not expose system media-preference emulation, so that system setting was reviewed in source; the equivalent user-controlled ambient pause was exercised in the browser.

## Contrast spot checks

| Pairing | Ratio |
| --- | --- |
| Supporting text on midnight | 8.41:1 |
| Quiet metadata on deep surface | 5.10:1 |
| Midnight text on saffron | 11.98:1 |
| Warm white on studio navy | 12.90:1 |

These are checks of the main token pairings, not a complete accessibility certification. Additional browser engines and physical-device testing remain useful before a public deployment.

## Iteration boundary

Store installation and app launch controls are intentionally unavailable. There are no live product integrations, accounts, forms, payment flows, analytics, or deployment automation. The repository's CI checks the static build only.
