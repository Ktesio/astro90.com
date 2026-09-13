# Astro90 brand guidelines

Version 1 · September 2026

## The idea

Astro90 is a development studio building games, agentic AI software, and open-source projects. Its identity is curious, considered, and warm. The signature line is **Built from curiosity.**

The user selected **04 — Studio Wordmark**, followed by **09 — Saffron**, then confirmed a **cinematic studio showcase** with dark surfaces as the default. That latest direction governs the website and supersedes the yellow-background emphasis of the early palette studies.

## Wordmark

The mark is the lowercase **astro90** wordmark, with bold, rounded forms. Keep the original proportions and letter shapes. Do not substitute a font, retype it, change the spacing, add a stroke, apply a gradient, or decorate it with an orbit. Orbital imagery is a separate part of the visual language.

The original geometry reference is `output/branding/logo-options-v1/04-wordmark.png`. The website's `static/brand/wordmark-reference.webp` is the same artwork. Its SVG viewport isolates the wordmark at `108 289 1320 244`; an alpha-preserving SVG filter applies the exact saffron fill. The inline component is `ui.wordmark` in `templates/components.html`.

This is a bitmap-backed web treatment, **not outlined production vector artwork**. The earlier generated color studies contain small letterform differences and must not replace the geometry reference. For large-format print or a master vector release, trace and optically review the selected reference before export.

| Rule | Standard |
| --- | --- |
| Preferred treatment | Saffron wordmark on midnight or studio navy |
| Clear space | At least half the mark's height on all four sides |
| Minimum wordmark width | 120 CSS px on screen; inspect at final size |
| Small icon | Use the supplied simplified `a` favicon at small browser sizes |
| Background | Quiet and even; keep photography and detailed objects away from the mark |
| Studio name in prose | Astro90 |
| Studio name in the mark | astro90 |

The favicon is a simplified optical web icon. It does not replace the full mark or the selected standalone `a` reference in master identity work.

## Color

| Name | Hex | Role |
| --- | --- | --- |
| Midnight | `#0B101A` | Main canvas |
| Deep surface | `#111925` | Sections and grouped content |
| Raised surface | `#182230` | Interactive surfaces and previews |
| Studio navy | `#1E293B` | Foundational brand color and sculptural material |
| Saffron | `#F4C84C` | Wordmark, primary action, meaningful emphasis |
| Soft saffron | `#FFE197` | Hover treatment |
| Warm white | `#F0F1EE` | Headlines and primary text |
| Slate | `#A4ADBB` | Supporting text |
| Quiet slate | `#7E8B9D` | Small secondary metadata on midnight |

Aim for roughly 70% midnight, 25% supporting surfaces and content, and 5% saffron in studio compositions. This is a guide for visual balance, not a quota. Large yellow blocks are not the default. In 3D artwork, light and metallic reflections can produce shades around the core gold hue.

Use dark text on a saffron button. Do not set white body text on yellow. Color supports labels and states; it must not be the only way to communicate status. Recheck contrast when applying muted colors to new surfaces.

## Typography

**Sora** carries display text. Its round geometry complements the selected mark without imitating it. Use weight 550–600 for large headlines, compact tracking, and a deliberate line break only where the layout supports it.

**Manrope** carries body text, navigation, and actions. Use comfortable line height, short paragraphs, and clear differences between primary and supporting copy.

**System monospace** carries code and small orientation labels. Uppercase labels are brief and secondary. Essential instructions must remain readable body copy.

The wordmark is artwork, not either typeface. Fonts are self-hosted, and both font licenses are included with the files.

## Images and forms

The studio's recurring form is the orbit: a dark ceramic core, warm gold rings, and small companion spheres. It expresses exploration and connected ideas. Use a small number of carefully lit forms, with generous negative space.

Lighthouse keeps its coastal greens, sea blues, brass details, and illustrated world. Inkube keeps its playful ink colors. Heronis uses soft violet and Yanando uses cool mint within their interface studies. Product art can be expressive inside the consistent dark studio frame.

Use actual product screens where available. Mark conceptual interfaces as studies, and development screenshots as previews. Avoid stock dashboards or unrelated imagery that imply a product feature or release.

## Motion

Motion is gentle and optional. Sculptures float slowly; a card moves slightly on hover; content enters once as it comes into view. Nothing takes control of the visitor's scrolling.

Respect `prefers-reduced-motion`. Provide a visible pause control for ambient animation and remember the choice for the current browser session. A paused or reduced-motion view must preserve every word, image, link, and layout.

Do not use flashing, custom cursors, loading gates, autoplay video, forced scene changes, or repetitive animation on essential text.

## Voice

Speak plainly and with care. Describe the experience or useful behavior before its implementation. Keep technical detail for the developer workbench, where it helps the reader.

| Context | Example |
| --- | --- |
| Studio introduction | Built from curiosity. |
| Game invitation | Take a closer look. |
| Release state | In development · Release details coming soon |
| Developer product | Run AI agents like services. |
| Error state | This page isn't here. There's plenty more to explore. |

Avoid unearned superlatives, invented testimonials, fictional metrics, and promises about unconfirmed release dates. State license terms accurately: public source code is not automatically open source.

## Brand architecture

Astro90 is the parent studio. Lighthouse, Inkube, Heronis, Yanando, and Ktesio retain distinct product names and personalities. Use “from Astro90” where attribution helps. A product's imagery and tone can vary; the site's navigation, typography hierarchy, spacing, and interaction rules stay consistent.
