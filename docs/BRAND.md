# Astro90 identity standards

Version 1.4 · September 2026

Astro90 is an independent studio focused on mobile games and entertainment. The selected identity is **04 Studio Wordmark** with **09 Saffron**, used on dark surfaces by default. The signature line is **Built from curiosity.**

## Signature

Use the supplied lowercase wordmark with its original rounded letterforms. The reference is `output/branding/logo-options-v1/04-wordmark.png`. The website uses an exact lossless WebP conversion, cropped through an SVG viewport at `108 289 1320 244` and filled saffron through its alpha channel. It remains a bitmap-backed web treatment; the full wordmark is not yet an outlined print master. Do not use the slightly different lettering in the generated color studies.

The compact **a** is an optical vector reconstruction of the selected first letter. `assets/brand/monogram.json` holds its path and sampled contour. `scripts/trace_monogram.py` regenerates that geometry and the boxed SVG. The SVG, Blender object and its construction filaments share this contour.

| Use | Standard |
| --- | --- |
| Desktop header | Full saffron wordmark, 166 px wide |
| Header and footer at 650 px or below | Boxed a only |
| Short phone landscape, up to 950 × 600 px | Boxed a only |
| Mobile icon | 43 px artwork inside a 44 px minimum link target |
| Clear space | Half the full mark's height; one quarter of the box width for the a |
| Minimum full mark | 120 CSS px, reviewed at the intended output size |
| Prose name | Astro90 |
| Background | An even dark field or a quiet area of a product image |

Do not stretch, retype, outline, recolor individual letters or attach decoration. The metallic treatment is an illustration of the a, separate from the flat navigation signature. Examples in the identity guide may show both marks on mobile for comparison.

## Digital assets

Use the boxed a for favicons, installed browser-app icons and social avatars. Keep the opaque maskable and Apple variants square; the operating system adds its own corners. For circular crops, use the padded avatar or maskable export. The full letter stays within the central safe circle.

Sharing artwork uses the current painted night coast, the original saffron wordmark and Sora/Manrope typography. Page-specific cards identify the section or product. Game cards use genuine development screenshots and retain their development status. Keep the lighthouse clear of type and preserve quiet space around the signature. The wide banner leaves room at the lower left for a profile-photo overlap; platform crops still need a visual check.

Download the kit from `/brand/#downloads`. See `docs/WEB-ASSETS.md` for the sizes, integration, source files and export commands. Transparent wordmark PNGs remain raster masters; the a is available as SVG.

## Meaning of the form

The a identifies the studio directly. Its rounded corners preserve the selected lettering; the saffron face and dark core translate the two brand colors into a physical object. The index connects the two games to that object with paths that turn through 90 degrees. This is a visual use of the name, not a claim about its origin.

The earlier rings were intended to suggest products orbiting one studio. They did not establish a distinctive Astro90 association and are retired from the website. Original explorations remain in the source archive. Do not reintroduce rings or floating spheres as default brand decoration.

## Color

| Name | Hex | Role |
| --- | --- | --- |
| Midnight | `#090E17` | Main canvas |
| Deep surface | `#111925` | Grouped content |
| Raised surface | `#182230` | Interface previews and disabled controls |
| Studio navy | `#1E293B` | Foundational brand color |
| Saffron | `#F4C84C` | Signature, actions, active paths and emphasis |
| Soft saffron | `#FFE197` | Hover emphasis |
| Warm white | `#F0F1EE` | Headlines and primary text |
| Slate | `#A4ADBB` | Supporting text |
| Quiet slate | `#7E8B9D` | Secondary metadata on dark fields |

Let dark surfaces dominate. Reserve yellow for the signature and a few deliberate points of emphasis. The 3D letter can occupy a large part of a composition; ordinary content should not sit inside large gold panels. Metallic reflections naturally vary around saffron.

The homepage uses saffron as a small source of light in a blue night landscape. Keep mountains, water and vegetation in subdued blues and indigo. Use warm windows and the lighthouse lantern as highlights. Preserve dark, quiet space around the signature and introductory text.

Use dark text on saffron, warm white for headings on dark surfaces, and slate for supporting copy. Recheck contrast for new surface combinations. Color alone must not communicate a release state or an action.

## Typography

Sora is the display face, normally weight 450–550. Large headings use tight tracking and compact line height. Manrope carries body text, navigation and actions. System monospace is reserved for code and technical values. Fonts are self-hosted and their SIL Open Font Licenses are included.

Use scale, alignment and spacing for hierarchy. Avoid decorative chips, numbered eyebrows above every section, repetitive subtitles and several slogans in one composition. The wordmark is supplied artwork, not a typeface.

## Product worlds

The studio's opening is a painted coastal panorama with a small lighthouse. It establishes a setting for exploration and leads into the first game. It is editorial studio artwork, not a gameplay screenshot or a nautical theme to apply to every product. Keep the responsive crop focused on the lighthouse and maintain readable sky above it on phones. Source artwork and its generation prompt are preserved in `assets/source/studio/`.

Lighthouse keeps its coastal illustration and nautical interfaces. Inkube keeps its colorful ink and dark puzzle board.

Actual development screens take priority over invented mockups. Label unreleased games and development previews. Do not fabricate stores, dates, reviews, ratings, customers or usage metrics.

## Motion

On the homepage, the lighthouse's soft beam follows pointer input across the inlet. On touch devices it responds to taps and scroll position. Keep the light attached to the painted lantern as crops change; it must settle when input stops. The first scroll carries the night coast into Lighthouse's existing game artwork through a soft overlap. Do not animate the sky or stars on an idle loop.

The archived Blender identity study constructs the letter once: traced filaments, connected depth, then one rounded metal object. The authored Blender animation lasts 3.2 seconds. No current page loads it. Keep its camera and scale fixed; do not zoom it with scroll. Product scenes respond to scrolling through image crops, oversized titles and device positions. Give the outgoing scene a full viewport of overlap with the incoming scene. The index previews respond equally to pointer hover and keyboard focus.

Scenes settle when input stops. There is no autonomous rotation, floating loop, top progress line, scroll hijacking, loading gate, custom cursor or forced scene completion. Normal document scrolling and direct links remain available.

Honor `prefers-reduced-motion`. The manual Reduce motion control in the index and footer uses a session preference. Reduced motion removes the extra pinned scroll distance and the landscape's light overlays. All content and links remain available.

## Voice

Describe how the game plays and where it stands. Let artwork supply atmosphere. Use concrete language such as “coastal logic puzzles,” “merging ink” and “chain reactions.” State supported platforms and development status.

Astro90 is the shared signature, while Lighthouse and Inkube retain distinct names and game identities.

## Feedback

Use the index’s four-square motif for pending previews. Let images load in their reserved space and keep the rest of the page available. Pair unavailable states with plain language and a retry action. A copied address earns an inline confirmation only after the copy succeeds. See `/brand/states/` for specimens.
