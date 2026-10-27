# Live Events Experience Palette

This reference records the extended Folloze color system extracted from `https://engage.folloze.com/for-events` on 2026-07-24. Trey confirmed that these colors belong to the new Folloze palette. Use this alongside the core homepage system in `visual-identity.md`.

## Capture Method

- Retrieved the live Folloze board source for board `248331`.
- Parsed the embedded HTML section and its declared CSS variables and background recipes.
- Separated page-level surfaces, utility states, and deliberate event-card themes.
- Preserved gradients as complete recipes rather than reducing them to isolated swatches.

Raw token file: `research/brand-harvest/folloze-events-2026-07-24/brand-tokens.css`.

## Core Surfaces

| Role | Value |
|---|---|
| Default canvas | `#FAFAFB` |
| Card and panel | `#FFFFFF` |
| Alternating band | `#F4F4FB` |
| Hero origin | `#F4F4FF` |
| Purple label | `#F0F0FF` |
| Muted control | `#F0F1F7` |
| Positive state | `#E8F8EF` |

## Section Background Recipes

Hero:

```css
background:
  radial-gradient(820px 520px at 82% 8%, rgba(91, 91, 255, .14), transparent 62%),
  radial-gradient(640px 480px at 8% 90%, rgba(255, 107, 92, .08), transparent 60%),
  linear-gradient(180deg, #f4f4ff 0%, #fafafb 88%);
```

Dark pipeline band:

```css
background:
  radial-gradient(900px 520px at 80% 8%, rgba(91, 91, 255, .24), transparent 60%),
  radial-gradient(700px 500px at 6% 96%, rgba(255, 107, 92, .12), transparent 62%),
  linear-gradient(160deg, #0c1330, #070b1f);
```

Final CTA foundation:

```css
background:
  radial-gradient(760px 460px at 80% 6%, rgba(91, 91, 255, .34), transparent 60%),
  radial-gradient(620px 460px at 10% 96%, rgba(0, 173, 255, .16), transparent 62%),
  linear-gradient(150deg, #0c1740, #070b22);
```

The source CTA also includes sparse one- and two-pixel star points. Treat those as optional campaign styling, not a required brand motif.

## Event Theme Backgrounds

| Theme | Recipe | Intended character |
|---|---|---|
| Cyber | `#070B1E` | Technical, dark, signal-oriented |
| Orbit | `#FBFBFE` | Light, clean, product-oriented |
| Paper | `#F4EEE1` | Editorial, human, premium |
| Sunset | `linear-gradient(155deg, #FF8A5C 0%, #FF5C7A 55%, #C8398F 100%)` | Energetic, experiential |
| Terminal | `#0A0A12` | Developer and technical workflow |
| Cobalt | `linear-gradient(155deg, #1560FF, #0A2ECC 60%, #061C8F)` | Bold, enterprise, high-energy |

## Usage Rules

- Use the core surfaces for Folloze corporate, product, and general campaign work.
- Use one expressive theme as the visual world for an event, campaign, or bounded module.
- Multiple themes may appear together only when the design is explicitly comparing distinct event or experience concepts.
- Keep dark-section text white or near-white and verify contrast.
- Keep cream-theme foregrounds deep green or near-black.
- Do not use gradients as empty decoration; connect them to a storytelling surface, state, or theme.
- Do not infer that every color in an arbitrary embedded widget is approved. This reference covers the colors explicitly extracted and confirmed on 2026-07-24.

## Source Limitations

- This is a live experience-derived source, not a formal legal brand book.
- The live page may change; re-verify before a high-stakes brand handoff.
- A future approved Folloze brand book supersedes this reference where it conflicts.
