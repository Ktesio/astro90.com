# Astro90 design system

This document describes the implemented static website. The executable source of truth is `sass/site.scss`; the shared Tera 2 components are in `templates/components.html`.

## Tokens

| Token | Value | Use |
| --- | --- | --- |
| `--canvas` | `#0B101A` | Page background |
| `--surface` | `#111925` | Section and card backgrounds |
| `--surface-raised` | `#182230` | Raised and disabled controls |
| `--ink` | `#1E293B` | Brand navy |
| `--saffron` | `#F4C84C` | Accent |
| `--saffron-soft` | `#FFE197` | Accent hover |
| `--text` | `#F0F1EE` | Main text |
| `--muted` | `#A4ADBB` | Body/support text |
| `--subtle` | `#7E8B9D` | Secondary metadata |
| `--line` | `rgba(182,197,220,.15)` | Quiet separators |
| `--line-strong` | `rgba(182,197,220,.3)` | Control and card boundaries |
| `--content` | `1280px` | Main content maximum |
| `--gutter` | `clamp(24px,5.55vw,88px)` | Page margins |
| `--radius` | `16px` | Main surfaces |
| `--radius-small` | `8px` | Small controls |
| `--fast` | `180ms` | Color response |
| `--medium` | `320ms` | Interaction transforms |
| `--slow` | `700ms` | One-time content reveal |
| `--ease` | `cubic-bezier(.22,1,.36,1)` | Soft deceleration |

## Type and spacing

Use Sora for headings, Manrope for body text and actions, and the system monospace stack for code/labels. Type sizes use fluid `clamp()` values where appropriate.

| Role | Desktop | Phone |
| --- | --- | --- |
| Home headline | Up to 111 px | About 63–92 px, sized to the screen |
| Collection headline | Fluid oversized display | 47–68 px |
| Section heading | 36–54 px | 32–45 px |
| Product name | Up to 88 px | 53–73 px |
| Main body | 15–17 px | 14–15 px |
| Card descriptions | 13–14 px | 13 px |
| Labels | 9–11 px | 8–10 px |

Labels inside interface illustrations are part of the visual preview, not controls or instructions. All real action labels remain separately readable.

Compose with 4, 8, 12, 16, 24, 32, 48, 64, and 96 px intervals, with optical adjustment for large display layouts. Desktop sections generally use 116 px vertical padding; phone sections use 76 px. Avoid adding a box around content that can be organized by spacing and a divider.

## Layout and responsiveness

The main content maxes out at 1280 px. Large art can extend outside its column but is clipped at the page boundary. The page itself must never scroll horizontally.

- Desktop: two-column project collections; split hero; four-field product metadata row.
- Tablet: condensed navigation and spacing, with art sized to preserve the copy's priority.
- Phone, 650 px and below: single-column cards and hero; disclosure navigation; two-column metadata; screenshot strip with native horizontal scrolling and snap points.
- Very small screens, 370 px and below: tighter headline and action sizing.

Only the screenshot strip intentionally scrolls horizontally. Use native scrolling; do not drag the whole document or replace its scroll behavior.

## Components

| Component | Responsibility |
| --- | --- |
| `ui.wordmark` | Selected lettering and exact saffron treatment |
| `ui.icon` | Consistent 24-unit outline icons, hidden from assistive technology |
| `ui.button` | Real content navigation with primary/secondary treatment |
| `ui.card` | Product artwork, title, description, platform, and status |
| `ui.app_visual` | Explicitly labeled Heronis/Yanando interface study |
| `ui.terminal` | Static Ktesio developer illustration |
| `ui.next_chapter` | Large next-page invitation |
| Gallery dialog | Native modal screenshot enlargement with close control |

Real controls have hover and visible keyboard focus states. Disabled install/launch previews do not react like active controls and have release-status text nearby. Do not add a fake URL to make them look functional.

The mobile menu is a disclosure, not a modal: its expanded state is exposed and Escape closes it. Native dialog behavior traps focus for enlarged screenshots; closing returns focus to the initiating screen button.

## Motion and accessibility

The hero and studio sculptures drift over 12–14 seconds. Small forms use similarly slow loops. The outer decorative orbit rotates over 75 seconds. Content reveals once, with 24 px maximum travel. Cards and arrows use small hover transforms.

The motion control pauses ambient animations and stores its preference in `sessionStorage`. Storage failure is harmless. System reduced motion takes priority, removes all animation/transitions, and keeps content visible. No cookies or remote services are used.

Standards for additions:

- Preserve a logical heading outline, one `h1` per page, and a clear main landmark.
- Supply a unique page title and description.
- Use actual links for navigation and actual buttons for local interaction.
- Keep action targets at least 44 × 44 CSS px where space permits; inline prose links remain textual.
- Keep focus visible against the active background and outside clipped artwork.
- Provide meaningful image alternatives; hide purely decorative forms and icons.
- Keep the content readable without JavaScript. The no-script mobile navigation is exposed.
- Honor reduced motion and keep all content visible when ambient movement is paused.
- Never depend on hover alone, color alone, or motion to convey information.
- Recheck contrast when adding a color/surface pairing. Aim for WCAG AA: 4.5:1 for normal text and 3:1 for large text and meaningful non-text boundaries.

## Content model

`data/projects.toml` is the shared catalog. Each entry has an ID, category, platform, status, summary, accent, route, media, features, release label, source URL, and license. Each detail page identifies its catalog entry through `extra.project` and supplies the editorial headings in Markdown front matter.

Before changing a release state, verify the actual store or product destination. Link to a store only after there is a real listing. Keep source availability and open-source licensing distinct. The website's static iteration does not make an unreleased product available.

## Validation

Run `mise run check` before committing. Visually inspect the home, a collection, each detail layout type, and the brand guide at desktop and phone widths. Check menu, focus, gallery, motion pause, and reduced-motion behavior after changes to those components. Keep screenshots and temporary review artifacts in `.local/`, outside the public build.
