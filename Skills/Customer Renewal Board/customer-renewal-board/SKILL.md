---
name: customer-renewal-board
description: Build Folloze customer renewal conversation boards from the shared Folloze demo template board or reusable single-page HTML template. Use when creating a template board or customer-specific board for renewal, optimization, QBR, customer growth, ABM follow-up, event follow-up, deal room, opportunity room, website personalization, or existing-customer expansion conversations.
---

# Customer Renewal Board

## Overview

Create a Folloze-branded renewal conversation board from the shared demo board or from `assets/renewal-board-template.html`. The template is derived from the Conga board structure but uses customer placeholders instead of Conga-specific copy.

Canonical Folloze demo template:

- Board ID: `244551`
- Designer URL: `https://app.folloze.com/app/board/244551/designer`
- Purpose: show the template structure with placeholder fields before a specific customer is applied.

Use the companion generator script when possible:

```bash
python3 /path/to/customer-renewal-board/scripts/generate_renewal_board.py \
  --customer-name "Acme" \
  --current-use-cases "events and ABM" \
  --customer-segment "enterprise renewal" \
  --customer-value-story "AI revenue transformation" \
  --output /absolute/path/acme-renewal-board.html
```

## Placeholder Model

Fill these placeholders before saving or sharing a generated board:

- `{{CUSTOMER_NAME}}`: Account name.
- `{{CURRENT_USE_CASES}}`: Current Folloze usage, such as `events`, `ABM`, `events and ABM`, or `customer programs`.
- `{{CUSTOMER_SEGMENT}}`: Audience label for the workspace preview, such as `enterprise renewal`, `strategic accounts`, or `customer growth`.
- `{{CUSTOMER_VALUE_STORY}}`: Short business narrative, such as `AI revenue transformation`, `security modernization`, or `customer lifecycle`.

## Workflow

1. Start from the canonical demo board `244551` when the user wants to see, copy, or clone the shared Folloze template experience.
2. Generate a fresh HTML file from the bundled template when creating a customized board locally. Never overwrite the source template, demo board `244551`, or a live customer board unless the user explicitly asks.
3. Update the customer-specific narrative by replacing generic phrases with account context from the user, Salesforce, call notes, a PDF, or approved source material.
4. Keep the core structure unless the user asks otherwise: hero, four renewal plays, operating model, core beliefs, AI execution platform, expected impact, customer proof patterns, Folloze resource center, and recommended next step.
5. Keep Folloze branding and theme intact unless the user explicitly requests another theme.
6. Keep customer proof stories generic unless the user provides approved customer-specific proof. Do not invent customer outcomes.
7. Verify locally at desktop and mobile widths before saving: no unresolved `{{PLACEHOLDER}}` tokens, no broken images, no horizontal overflow, and interactive drawers/tabs still work.
8. If saving to Folloze MCP, first call the Folloze landing-page creation guide, then save as a new board unless the user explicitly gives an existing board ID to update.

## Copy Guidance

Position the board as a renewal and optimization conversation, not a salesy upsell page. Prefer:

- `renewal readiness`
- `optimization`
- `customer growth`
- `adjacent revenue motions`
- `opportunity room`
- `customer journey`

Use `expansion` only when it is factual customer proof language or explicitly requested.

## QA Checklist

Before final delivery or MCP save, confirm:

- The original Conga board file remains untouched.
- The canonical demo board `244551` remains untouched unless the user explicitly asks to update the template itself.
- The generated board has no visible Conga-specific copy.
- All external CTAs have `target="_blank" rel="noopener"` and analytics.
- Buttons and drawers have meaningful actions.
- The page renders cleanly on mobile and desktop.
