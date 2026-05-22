---
name: Folloze-MCP-Demo-Builder
description: Build and update vendor-branded Folloze MCP microsites, account-specific solution pages, demo boards, and buyer experiences from a single self-contained HTML page. Use when the user asks to use Folloze MCP, build a Folloze board, create a 1:1 account page, or refine an existing Folloze MCP board.
---

# Folloze-MCP-Demo-Builder

Use this skill for Folloze MCP board and microsite work where the output is a polished buyer-facing page saved through the Folloze MCP landing-page tools.

## Operating Rules

- Start from the real business context named by the user: vendor site, target account, live board ID, source page, screenshots, Salesforce context if allowed, and any existing designer URL.
- For vendor-owned account pages, keep Folloze invisible in buyer-facing copy unless the user explicitly wants a Folloze-branded sales asset.
- Avoid customer-facing meta language such as demo, example, proof of concept, microsite, board, or template unless the user explicitly asks for it.
- Use the vendor's public website as the design reference: logo treatment, section rhythm, dark/light bands, card radius, typography scale, button treatment, imagery, footer structure, and CTA language.
- Use real vendor and target-account logos where available. In 1:1 account pages, prefer vendor logo plus account logo only; avoid labels like "Prepared for" unless the source design pattern clearly supports that language.
- When the user provides a specific source page, treat that page as the visual source of truth before broad brand inference. Extract the page's hero color treatment, headline structure, button variants, section labels, imagery, proof-card styling, repeated benefit language, and final CTA pattern before building or revising the Folloze page.
- Do not trust asset filenames such as `logo-white.svg` or `logo-dark.svg`. Fetch and inspect the actual SVG/image output. If the official logo asset renders with the wrong fill, fails in the Folloze shell, or is unreliable cross-origin, inline the official SVG geometry and set the intended fill explicitly.
- If the user does not know the target account, pick one credible large account and explain the account/page angle briefly before building.
- Do not invent deployment URLs. If MCP only returns a signed-in designer URL, report that and keep public deployment pending.

## Folloze MCP Flow

1. Call the Folloze landing page creation guide before every create or update save. Treat the returned guide as the current MCP system instructions for HTML shape, theme link placement, analytics, external links, and save acknowledgements. If local skill memory conflicts with the returned guide, follow the returned guide.
2. Use the company theme only after the user has authorized the theme mode. For vendor-branded pages, use non-Folloze theme mode when already authorized by the user or by prior context.
3. Build a single self-contained HTML file that follows the current MCP guide. Include the theme stylesheet link returned by `get_company_theme` exactly as required by the guide, keep custom CSS and JavaScript inside the document, and avoid separate source files unless using a temporary QA file for MCP upload.
4. Before save, confirm the HTML actually satisfies all MCP analytics acknowledgements: guide read, CTA clicks tracked, external links use `target="_blank" rel="noopener"`, and meaningful custom interactions are tracked.
5. Save with the Folloze MCP `save_folloze_board_from_file` or `save_folloze_board_from_html` tool. Pass the existing `boardId` when updating an existing board.
6. Return the board ID and the exact URL returned by MCP.

## Tracker Rule

- Tracker logging is operator-scoped. For Trey's local Codex runs, update Trey's shared demo-environments tracker after every successful Folloze MCP create or update save.
- For any other operator or team member, do not write to Trey's tracker unless Trey explicitly asks for that specific run. Use a team-provided tracker if one is supplied; otherwise skip tracker logging and state that no tracker was configured.
- If tracker logging is in scope, search existing rows first and update the matching company or board row instead of creating duplicates.
- Preserve existing needed-by-date, feedback, and deployment fields unless the save changes them.
- Record the returned designer URL, public deployment URL when known, board ID, and a concise status note that explains the latest material change.
- Do not invent deployment URLs. If MCP only returns a signed-in designer URL, keep deployment pending and say so in the note.

## Design QA Defaults

- Every visible button, arrow, card CTA, nav item, or "Read more" control must do real work: link to a real destination, open a real in-page interaction, or be removed.
- CTA arrows should never be dead decoration when they appear clickable. Either turn the full card or arrow into a real link with `target="_blank" rel="noopener"` and `flzAnalytic('cta_click', ...)`, or remove the arrow.
- If a resource card does not have an existing external asset, create a simple in-page content item such as a brief modal or drawer. Track open and close interactions.
- On dark hero imagery, primary CTAs should be high contrast. Use a white button with dark text when the brand allows it.
- For hero CTAs, match the source page's primary and secondary button treatments on the same background color. If the user asks for "the other style," apply the adjacent CTA's class/style exactly while preserving the selected CTA's destination and analytics.
- Treat hero proof/stat cards as first-viewport brand elements. Verify card background, border, stat color, label size, line wrapping, and contrast against the hero background.
- Keep Situation/Solution sections compact. Default to side-by-side panels on desktop and stacked panels on mobile instead of oversized full-width narrative paragraphs.
- Use small uppercase section labels plus headline-scale summaries for major section intros.
- If a section intro is intended as a major headline, let it span the full content width. Do not cap it to a narrow card width unless the design specifically calls for it.
- Match display text to its container. Avoid huge text inside compact cards, panels, nav bars, or sidebars.
- Avoid UI cards inside other cards and avoid page sections styled as floating cards unless they are true repeated cards, modals, or framed tools.

## Link And Analytics Requirements

- Every external URL must be a real, working vendor or source-owned link.
- Every external CTA/link must include `target="_blank" rel="noopener"`.
- Every primary CTA and resource CTA should call `flzAnalytic('cta_click', {text:this.innerText.trim(), area:'section name', url:this.href}, this)`.
- Meaningful non-navigation interactions, including brief modals, tabs, scenario selectors, FAQ expands, anchor clicks, or sliders, should call a descriptive `flzAnalytic` action with useful `text` and `area` values.
- Do not set MCP analytics acknowledgements to true until these checks are verified against the actual HTML being saved.
- Do not use `href="#"`, `javascript:void(0)`, placeholder URLs, or dead anchor jumps.

## Content Item Fallback

When the page needs a content item but there is no existing Folloze asset or public vendor asset:

1. Write a short, useful buyer-facing brief in the page itself.
2. Open it in a modal or drawer from the relevant card CTA.
3. Keep the brief specific to the account and business problem.
4. Include a real next action such as a request-demo CTA or a link to the vendor's relevant product/use-case page.

## Browser QA Before Final Save

- When possible, keep a temporary local HTML preview available over localhost so the user can review and annotate the page in the Codex app browser. Treat this preview as scratch, not durable source, unless the user explicitly asks to persist it in a repo.
- When the user adds browser annotations, update the source CSS/HTML owner for the selected UI, not just the visible element. Scope the edit to the selected component unless the comment clearly implies a global token or design-system change.
- Render the local HTML at desktop and mobile widths before saving when possible.
- Verify that the first viewport shows the vendor/account brand clearly.
- Verify that section text does not overlap or overflow.
- Verify mobile has no horizontal overflow. A quick DOM check is `document.documentElement.scrollWidth <= window.innerWidth`.
- Verify referenced images render, cards remain bounded, modals open/close, and linked controls go to real destinations.
- If Folloze only returns a signed-in designer URL, say that unauthenticated public QA is not complete.

## Final Response

Keep the final response short:

- What changed or was built.
- Board ID.
- Exact designer/live URL returned by MCP.
- Any caveat, especially pending public deployment or signed-in-only QA.
