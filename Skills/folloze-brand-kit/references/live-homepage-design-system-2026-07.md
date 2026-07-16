# Live Homepage Design System Evidence

This reference records design facts extracted from `https://www.folloze.com/` on 2026-07-16. It is a source-aware supplement to `visual-identity.md`, not an approved replacement brand book.

## Capture Method

- Browser-computed styles at `1440px` desktop and `390px` mobile widths.
- Full-page desktop and mobile screenshots.
- Direct inspection of the live Webflow stylesheet.
- Cookie controls and embedded product/demo CSS were excluded from the curated conclusions.
- Brandfetch was not used because no token was configured; the browser, stylesheet, and live assets supplied the authoritative evidence.

Raw bundle: `research/brand-harvest/folloze-home-2026-07-16/`.

## Font Sources

The page requests:

- Instrument Sans `400`, `500`, `600`, `700`
- Inter `300`, `400`, `500`, `600`, `700`
- Open Sans / Open Sans Variable for navigation and legacy components

Observed hierarchy:

- `Instrument Sans` is the marketing display face.
- `Inter` is the page body, card, button, metric-support, and text-link face.
- `Open Sans Variable` is limited to the global navigation.

## Computed Type Samples

| Element | Desktop | Mobile |
|---|---|---|
| Homepage H1 | Instrument Sans 500, `80/80`, `-2.4px` | Instrument Sans 500, `48/48`, `-1.44px` |
| Large H2 | Instrument Sans 500, `56/67.2`, `-1.68px` | Instrument Sans 500, `40/48`, `-1.2px` |
| Medium H2 | Instrument Sans 500, `48/57.6`, up to `-1.6px` | Instrument Sans 500, `32/38.4`, up to `-1.6px` |
| Card H3 | Instrument Sans 500, `24/28.8`, `-1.6px` | Instrument Sans 500, `20/24`, `-1.6px` |
| Body | Inter 400, `16/24` | Inter 400, `16/24` |

## Button Recipes

Live stylesheet rules:

```css
.button {
  color: #fff;
  background: #0a1230;
  border: 1px solid #0a1230;
  border-radius: 999px;
  padding: .875rem 1.5rem;
  font-family: Inter, sans-serif;
  transition: all .2s cubic-bezier(.645, .045, .355, 1);
}

.button:hover {
  background: #5b5bff;
  border-color: #5b5bff;
}

.button.is-secondary {
  color: #0a1230;
  background: #fff;
  border-color: #e6e8f0;
  display: inline-flex;
  gap: .5rem;
}

.button.is-secondary:hover {
  color: #5b5bff;
}
```

At the mobile breakpoint, vertical button padding increases from `.875rem` to `1rem`.

## Curvature Recipes

```css
.layout239_item,
.testimonial_item {
  background: #fff;
  border: 1px solid #e6e8f0;
  border-radius: 24px;
  padding: 2.5rem 1.75rem;
}

.customer-stories_component {
  border-radius: 2rem;
}

.customer-stories_grid-item {
  background: rgba(255, 255, 255, .04);
  border: 1px solid rgba(255, 255, 255, .08);
  border-radius: 24px;
  backdrop-filter: blur(5px);
  padding: 2rem;
}
```

Large two-column G2 and integrations panels also use restrained borders and large-radius corners. The repeated pattern is `24px` for ordinary cards and `32px` for major visual containers.

## Dominant Color Evidence

The most frequent computed colors, after filtering embedded content, are:

| Color | Role |
|---|---|
| `#1C293F` | Main display ink |
| `#FFFFFF` | Page and card surface |
| `#6B7E9D` | Muted/supporting copy |
| `#071428` | Deep body/dark foundation |
| `#5B5BFF` | Current action and metric accent |
| `#2C3D59` | Body copy |
| `#3B3BE0` | Dark accent |
| `#0A1230` | Primary controls and footer |
| `#E6E8F0` | Borders |
| `#EEEEFF` | Capability labels |

## Composition Patterns

- The hero is centered and text-led, followed by real product imagery rather than an abstract illustration.
- Light sections use white surfaces, thin borders, and almost no shadow.
- The three-card product story uses a visible connecting line, circular icon medallions, tinted product images, and violet text links.
- Customer proof is grouped into one 32px dark image panel; cards inside it use translucent fill and blur rather than opaque white.
- The final CTA repeats the dark proof surface and uses a white secondary-style pill button.
- Desktop uses wide centered containers. Mobile stacks cards and controls while preserving the same hierarchy and increasing control height.

## Source Limitations

- Website implementation includes legacy Webflow variables and embedded demo/widget CSS. Not every declared variable is part of the current marketing expression.
- Homepage screenshots are evidence of the current public design, not a legal or formal brand approval artifact.
- Re-harvest after material homepage changes or once the formal brand book is published.
