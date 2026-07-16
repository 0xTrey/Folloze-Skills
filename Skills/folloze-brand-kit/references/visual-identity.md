# Visual Identity

Use this file for Folloze logo, color, typography, curvature, button, and layout guidance in generated assets.

## Current Visual Source

The current visual system is derived from the live Folloze homepage at `https://www.folloze.com/`, captured with browser-computed styles and desktop/mobile screenshots on 2026-07-16. Treat it as the interim visual source of truth until an approved replacement brand book is available.

Evidence bundle:

- `research/brand-harvest/folloze-home-2026-07-16/brand.json`
- `research/brand-harvest/folloze-home-2026-07-16/brand-tokens.css`
- `research/brand-harvest/folloze-home-2026-07-16/screenshots/`
- `references/live-homepage-design-system-2026-07.md`

Do not copy the homepage layout pixel for pixel. Reuse its design language: typography, color relationships, curvature, controls, spacing, and surface treatments.

## Logo Assets

Bundled logo files:

| File | Use |
|---|---|
| `assets/logos/folloze-logo-primary.svg` | Preferred vector logo for light backgrounds |
| `assets/logos/folloze-logo-primary.png` | High-resolution logo for light backgrounds when SVG is unsuitable |
| `assets/logos/folloze-logo-secondary.png` | Alternate logo treatment from the approved kit |
| `assets/logos/folloze-logo-white.png` | White logo for dark backgrounds |
| `assets/logos/folloze-symbol-primary.png` | Symbol-only mark for light backgrounds |
| `assets/logos/folloze-symbol-secondary.png` | Alternate symbol-only mark |
| `assets/logos/folloze-symbol-white.png` | White symbol-only mark for dark backgrounds |

Default choice:

- Use `folloze-logo-primary.svg` on white or pale backgrounds.
- Use `folloze-logo-white.png` on deep navy or image backgrounds.
- Use symbol-only marks only when space is constrained or the Folloze wordmark already appears nearby.

## Logo Rules

- Use the real logo asset. Do not redraw it in HTML or CSS.
- Do not stretch, skew, crop, rotate, outline, shadow, recolor, or filter the logo.
- Keep clear space around the logo and verify readability at the rendered size.
- For co-branded assets, use a restrained separator such as `+` or `x` when the layout supports it.

## Current Homepage Palette

Use these colors as a relationship, not as an invitation to fill every surface with blue or violet.

| Role | Token | Hex | Typical use |
|---|---|---|---|
| Primary ink | `--folloze-ink` | `#1C293F` | Display headings, card headings |
| Deep ink | `--folloze-deep-ink` | `#071428` | Strong body copy, dark foundation |
| Action navy | `--folloze-action` | `#0A1230` | Primary buttons, footer, dark UI |
| Body copy | `--folloze-body` | `#2C3D59` | Paragraphs on light surfaces |
| Muted copy | `--folloze-muted` | `#6B7E9D` | Supporting text and footer copy |
| Primary accent | `--folloze-accent` | `#5B5BFF` | Links, metrics, icon accents, hover state |
| Accent dark | `--folloze-accent-dark` | `#3B3BE0` | Deeper violet contrast |
| Accent tint | `--folloze-accent-tint` | `#EEEEFF` | Eyebrow and capability pills |
| Border | `--folloze-border` | `#E6E8F0` | Card and secondary-button borders |
| Soft surface | `--folloze-soft` | `#FAFAFB` | Subtle section and placeholder surfaces |
| White | `--folloze-white` | `#FFFFFF` | Main background and card surfaces |

The website still exposes legacy product variables such as `#00CCFF`, `#00A0FF`, `#0077FF`, `#004BDE`, pink, purple, green, orange, and yellow. Those remain available for product diagrams or established assets, but the live homepage's dominant marketing system is navy, white, and violet. Do not use the legacy rainbow as the default page palette.

## Typography

- Display: `Instrument Sans`, weight `500`.
- Body and buttons: `Inter`, normally weights `400` and `500`.
- Navigation only: `Open Sans Variable`, weights `500` and `600`.
- Use system sans-serif fallbacks when web fonts cannot be loaded.
- Do not apply negative tracking to body text or controls. The homepage uses negative tracking only for large display type.

Desktop reference scale:

| Role | Size / line height | Weight | Tracking |
|---|---|---|---|
| Hero H1 | `80px / 80px` | `500` | `-2.4px` |
| Large section H2 | `56px / 67.2px` | `500` | `-1.68px` |
| Medium section H2 | `48px / 57.6px` | `500` | up to `-1.6px` |
| Card H3 | `24px / 28.8px` | `500` | `-1.6px` |
| Body | `16px / 24px` | `400` | `0` to `0.25px` |
| Eyebrow | `12px` | `500` | about `1.68px`, uppercase |

Mobile reference scale:

- Hero H1: `48px / 48px`.
- Large section H2: `40px / 48px`.
- Medium section H2: `32px / 38.4px`.
- Card H3: `20px / 24px`.
- Body: `16px / 24px`.

## Curvature And Surfaces

The current visual language is rounded but controlled:

- Buttons: fully pill-shaped with `999px` radius.
- Standard content and testimonial cards: `24px` radius.
- Large proof and CTA panels: `32px` radius.
- Icon medallions: circular with a thin `#E6E8F0` border.
- Card borders: `1px solid #E6E8F0` on white.
- Dark proof cards: translucent white fill and border over a deep navy image surface, with subtle backdrop blur.
- Shadows are minimal. Prefer border and contrast over floating-card shadows.

Do not round every container. Full-width page sections remain unframed; curvature belongs to cards, media, large proof panels, and controls.

## Buttons And Links

Primary button:

- background and border: `#0A1230`
- text: white
- radius: `999px`
- type: Inter `16px / 24px`, weight `400`
- desktop padding: `14px 24px` (`54px` total height)
- mobile padding: `16px 24px` (`58px` total height)
- hover: background and border become `#5B5BFF`
- transition: `200ms` using `cubic-bezier(.645,.045,.355,1)`

Secondary button:

- white background, `#0A1230` text
- `1px solid #E6E8F0`
- radius: `999px`
- same type and padding as primary
- optional trailing arrow with `8px` gap
- hover text: `#5B5BFF`

Text link:

- `#5B5BFF`, or white on dark surfaces
- Inter `14px / 21px`, weight `500`
- trailing arrow with `8px` gap
- no decorative container

Navigation controls use Open Sans Variable at about `15.2px`; the dark navigation CTA is `40px` tall with `12px 16px` padding.

## Layout And Visual Direction

Folloze-branded assets should feel modern, precise, enterprise-ready, motion-oriented, and easy to scan.

Recommended patterns:

- centered, outcome-led headlines with generous white space
- mostly white page surfaces with navy text and violet actions
- a restrained `Build / Activate / Signal` card sequence
- soft pastel product imagery inside white cards
- deep navy proof bands with violet metrics and white copy
- compact uppercase eyebrows to orient sections
- logos, screenshots, and actual product states instead of generic decoration
- clear responsive stacking; mobile keeps the typography strong and increases button vertical padding

Avoid:

- defaulting to the older cyan-to-blue palette for every marketing asset
- decorative blobs, generic gradient orbs, or empty atmospheric backgrounds
- strong shadows where a thin border is sufficient
- cards inside cards
- excessively rounded page sections
- unreadable small logos or invented logo marks
- treating embedded demo/widget CSS as the homepage brand system

## PDF And HTML Checks

Before sending an HTML or PDF asset:

- verify the real logo renders from the bundled asset path
- verify Instrument Sans and Inter load, with usable fallbacks
- verify primary, secondary, hover, and dark-surface contrast
- verify 24px cards and pill controls remain consistent at mobile sizes
- verify print/PDF export does not introduce bands or missing backgrounds
- verify all text remains readable at email-attachment scale
