# Source Index

This reference explains what is in the portable Folloze Brand Kit and when to load each file.

## Provenance

This package is curated from public-facing or generally reusable Folloze brand and product materials maintained in the local Folloze Brand Kit.

Active messaging source:

- `Folloze Content System - Live`
- Google Doc ID: `1gwztgTSaWCJ7tgkFjuSPPiDq0hxw6AM8G97WrJbvn2I`
- Captured into this kit: 2026-06-01

This kit intentionally excludes restricted customer-specific folders and deal-specific artifacts.

Last reviewed: 2026-06-01

## References

| File | Use when |
|---|---|
| `content-system-v3-2.md` | Need the active messaging alignment, source priority, external/internal language boundary, current proof pillars, proof-library rules, content brief fields, or content-system rules |
| `content-system-v3-1.md` | Historical v3.1 context only when comparing old work or diagnosing stale outputs |
| `product-capabilities-internal.md` | Need internal Folloze capability, module, license, package-row, integration, Website Engagement, Events, Global Scalability, or AI/Data credit context and Drive/internal access is available |
| `product-capabilities-customer-ready.md` | Need customer-facing capability descriptions without internal source notes, private provenance, pricing-guide details, or local paths |
| `product-capabilities-public-safe.md` | Need generic public-safe product capability definitions for public repos, public prompts, or no-Drive fallback |
| `brand-foundation.md` | Need category, positioning, audience, narrative hierarchy, or messaging guardrails |
| `messaging-library.md` | Need value props, pillars, page copy, campaign claims, one-pager messaging blocks, or account-signal mapping |
| `claims-and-proof.md` | Need numeric claims, customer proof, case-study snippets, proof-selection rules, or verification status |
| `voice-and-style.md` | Need tone, style, words to use, words to avoid, or copy-quality checks |
| `content-brief-template.md` | Need a reusable brief shape for campaign, page, sales, thought-leadership, or one-pager content |
| `campaign-board-design-context.md` | Need Folloze-specific campaign board design context, campaign registers, anti-references, or board design gates |
| `visual-identity.md` | Need colors, logo selection, logo file names, or visual usage guidance |

## Assets

| Asset | Use when |
|---|---|
| `assets/logos/folloze-logo-primary.svg` | Preferred vector logo for light backgrounds |
| `assets/logos/folloze-logo-primary.png` | High-resolution logo for light backgrounds when SVG is unsuitable |
| `assets/logos/folloze-logo-secondary.png` | Alternate logo treatment from the approved kit |
| `assets/logos/folloze-logo-white.png` | White logo for dark backgrounds |
| `assets/logos/folloze-symbol-primary.png` | Symbol-only mark for light backgrounds |
| `assets/logos/folloze-symbol-secondary.png` | Alternate symbol-only mark |
| `assets/logos/folloze-symbol-white.png` | White symbol-only mark for dark backgrounds |

## Default Load Pattern

For a customer-facing Folloze asset:

1. Load `content-system-v3-2.md`.
2. Load `product-capabilities-customer-ready.md` if the asset mentions product features, modules, user roles, integrations, Website Engagement, Events, Global Scalability, or AI/Data credits.
3. Load `brand-foundation.md`.
4. Load `messaging-library.md`.
5. Load `claims-and-proof.md` only if you will use proof, numbers, customer names, or benchmark claims.
6. Load `campaign-board-design-context.md` when Folloze is the brand owner for a board, microsite, landing page, or buyer experience.
7. Load `visual-identity.md` if you are creating HTML, slides, images, PDFs, or other visual output.
8. Load `voice-and-style.md` before final copy QA.

For content creation from a loose request:

1. Load `content-system-v3-2.md`.
2. Load `content-brief-template.md`.
3. Ask only for missing brief fields that materially change the output.
4. Draft in the current external register, then run `voice-and-style.md` QA.

For internal planning or skill-building:

1. Load this source index.
2. Load `product-capabilities-internal.md` when the task needs the internal product capability Google Doc or package-row context.
3. Load only the other files needed by the target skill.
4. Keep downstream skill instructions concise and point back to this kit.

For public repo, public prompt, or no-Drive work:

1. Load `content-system-v3-2.md`.
2. Load `product-capabilities-public-safe.md` if product capability context is needed.
3. Do not rely on internal Google Docs, pricing guides, order forms, or private source material.

## What Not To Add

Do not add:

- pricing guides
- order forms
- contracts
- security questionnaires
- private customer notes
- account-specific decks or strategy docs
- unreleased roadmap claims
- raw Salesforce, Gmail, Granola, or Drive snippets

If a private artifact teaches a useful reusable pattern, abstract the pattern and remove all account-specific details before adding it here.

Internal access-controlled Google Doc links may be referenced from this kit when they are explicitly marked as internal pointers and no private content is copied into the repo.
