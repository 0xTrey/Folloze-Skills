---
name: Folloze-MCP-Demo-Builder
description: Build and update vendor-branded Folloze MCP microsites, account-specific solution pages, demo boards, and buyer experiences from a single self-contained HTML page. Use when the user asks to use Folloze MCP, build a Folloze board, create a 1:1 account page, or refine an existing Folloze MCP board.
---

# Folloze-MCP-Demo-Builder

Use this skill for Folloze MCP board and microsite work where the output is a polished buyer-facing page saved through the Folloze MCP landing-page tools.

## Operating Rules

- Start from the real business context named by the user: vendor site, target account, live board ID, source page, screenshots, Salesforce context if allowed, and any existing designer URL.
- The deliverable is a repo-backed, vendor-faithful sales experience with measurable interaction QA. It is not a Folloze-specific experience unless the user explicitly asks for Folloze branding or Folloze-owned positioning.
- For vendor-owned account pages, keep Folloze invisible in buyer-facing copy unless the user explicitly wants a Folloze-branded sales asset.
- Avoid customer-facing meta language such as demo, example, proof of concept, microsite, board, or template unless the user explicitly asks for it.
- Use the vendor's public website as the design reference: logo treatment, section rhythm, dark/light bands, card radius, typography scale, button treatment, imagery, footer structure, and CTA language.
- Use real vendor and target-account logos where available. In 1:1 account pages, prefer vendor logo plus account logo only; avoid labels like "Prepared for" unless the source design pattern clearly supports that language.
- When the user provides a specific source page, treat that page as the visual source of truth before broad brand inference. Extract the page's hero color treatment, headline structure, button variants, section labels, imagery, proof-card styling, repeated benefit language, and final CTA pattern before building or revising the Folloze page.
- Treat each experience as its own source-brand component system. Do not carry button colors, nav labels, calculator assumptions, card density, or CTA hierarchy from a prior board unless the current source page or user request supports it.
- Do not trust asset filenames such as `logo-white.svg` or `logo-dark.svg`. Fetch and inspect the actual SVG/image output. If the official logo asset renders with the wrong fill, fails in the Folloze shell, or is unreliable cross-origin, inline the official SVG geometry and set the intended fill explicitly.
- If the user does not know the target account, pick one credible large account and explain the account/page angle briefly before building.
- Do not invent deployment URLs. If MCP only returns a signed-in designer URL, report that and keep public deployment pending.

## Source Boundaries And Motion Fit

- Private notes from Granola, Salesforce, Gmail, Slack, or internal docs are strategy inputs, not page copy. Use them to understand the conversation, priority, audience, and likely motion; do not quote them, paraphrase them into buyer-facing claims, or let the page read like a meeting recap.
- Use private notes only to choose and ground the GTM shape:
  - `one-to-one`: one named target account with account-specific business signals.
  - `one-to-few`: a small named segment or cluster of similar accounts.
  - `one-to-many`: broadly reusable campaign page with no single account posture.
  - `industry or vertical play`: an industry-specific page where account examples support the pattern but do not dominate.
  - `specific account called out`: the named account becomes the page's buyer context when public research supports it.
- Once the motion is selected, make visible claims from public vendor messaging, public target-account evidence, or user-approved copy. If private notes reveal a pain point, translate it into a public-market problem unless the user explicitly authorizes using the private detail.
- If notes and public evidence conflict, follow public evidence for buyer-facing copy and call out the assumption in your working notes or final caveat.
- For 1:1 boards, the page should feel like the vendor is pitching the target account, not like Folloze or the agent is explaining why the page exists.

## Repo-Backed Local Source

- Durable board HTML should live in an obvious Git repo before MCP save whenever the user asks to build, edit in Codex, save, or continue iterating.
- Use the local HTML file as the source of truth for edits, browser QA, and MCP upload. Do not treat the local file as scratch once the user is editing or reviewing it in-app.
- Prefer saving through MCP from the verified local file path. Only use inline HTML save when the page truly exists only in the conversation.
- After meaningful source edits, inspect git status. Commit only the relevant board or skill files when the repo state is ready; leave unrelated dirty files untouched.

## Folloze MCP Flow

1. Call the Folloze landing page creation guide before every create or update save. Treat the returned guide as the current MCP system instructions for HTML shape, theme link placement, analytics, external links, and save acknowledgements. If local skill memory conflicts with the returned guide, follow the returned guide.
2. Use the company theme only after the user has authorized the theme mode. For vendor-branded pages, use non-Folloze theme mode when already authorized by the user or by prior context.
3. Build a single self-contained HTML file that follows the current MCP guide. Include the theme stylesheet link returned by `get_company_theme` exactly as required by the guide, keep custom CSS and JavaScript inside the document, and avoid separate source files unless using a temporary QA file for MCP upload.
4. Before save, confirm the HTML actually satisfies all MCP analytics acknowledgements: guide read, CTA clicks tracked, external links use `target="_blank" rel="noopener"`, and meaningful custom interactions are tracked.
5. Save with the Folloze MCP `save_folloze_board_from_file` or `save_folloze_board_from_html` tool. Pass the existing `boardId` when updating an existing board.
6. Return the board ID and the exact URL returned by MCP.

## Existing Board Update Path

- When the user asks to push, update, resave, or change an existing board, preserve the existing board ID unless they explicitly ask for a new board.
- If a verified local source file exists, update that file, QA it, and save from file with the existing `boardId`.
- If no verified local source exists and MCP cannot read the current board HTML, obtain current HTML first through export, public-render capture, or a user-provided source file before changing live sections or buttons.
- Preserve the existing board name unless the user asks to rename it or the prior name is clearly stale for the new motion.
- Do not re-ask theme mode for a same-board update when the current source and prior context already establish the theme mode. Reconfirm only when the user asks to change theme behavior or the source file lacks the required theme link/theme ID.
- After save, report the exact MCP-returned URL. Do not infer public deployment from a prior tracker URL.

## Tracker Rule

- Tracker logging is operator-scoped. For Trey's local Codex runs, update Trey's shared demo-environments tracker after every successful Folloze MCP create or update save.
- Tracker: `MCP Demo Environments - May 2026`, tab `Demo Environments`, spreadsheet `1s_NU2O7lO8f_QSVmP2mI5dBNOGgUh7oQo3bfenerMqk`.
- Current Row A schema is authoritative:
  - Column A: `Company name`
  - Column B: `Board Name`
  - Column C: `Deployment URL`
  - Column D: `Designer edit URL`
  - Column E: `Needed By Date`
  - Column F: `Luke Feedback`
  - Column G: `Agent Notes`
- Before writing, read row 1 and align writes by header name rather than older column positions. If row 1 differs, stop and adapt to the live headers before writing.
- For any other operator or team member, do not write to Trey's tracker unless Trey explicitly asks for that specific run. Use a team-provided tracker if one is supplied; otherwise skip tracker logging and state that no tracker was configured.
- If tracker logging is in scope, search existing rows first by board ID from the designer URL or notes, exact designer URL, exact board name, and company name; update the matching row instead of creating duplicates.
- Always write the saved board title/name returned or passed to MCP into Column B (`Board Name`). For updates, preserve an existing Column B value only when it is already the same board title; otherwise correct it to the current saved board title.
- Preserve Column E (`Needed By Date`) and Column F (`Luke Feedback`) unless Trey explicitly asks to change them.
- Preserve Column C (`Deployment URL`) unless MCP returns a real public/live deployment URL; if MCP only returns a signed-in designer URL, keep or write `deployment URL pending from MCP`.
- Record Column D (`Designer edit URL`) from the exact MCP returned designer URL.
- Record Column G (`Agent Notes`) as a concise status note with board ID, date, source boundary, theme mode, QA/publish caveat, and latest material change.
- Do not invent deployment URLs. If MCP only returns a signed-in designer URL, keep deployment pending and say so in the note.
- The tracker write is a one-time post-save logging/update step; do not repeatedly update the sheet while polishing unless a later successful MCP save materially changes the row.
- If Google Sheets returns a quota or transient read error after MCP save, do not loop aggressively. Use the last successful search/write result if available; otherwise report tracker logging as skipped or pending while still returning the saved board details.

## Design QA Defaults

- Every visible button, arrow, card CTA, nav item, or "Read more" control must do real work: link to a real destination, open a real in-page interaction, or be removed.
- CTA arrows should never be dead decoration when they appear clickable. Either turn the full card or arrow into a real link with `target="_blank" rel="noopener"` and `flzAnalytic('cta_click', ...)`, or remove the arrow.
- If a resource card does not have an existing external asset, create a simple in-page content item such as a brief modal or drawer. Track open and close interactions.
- On dark hero imagery, primary CTAs should be high contrast. Use a white button with dark text when the brand allows it.
- For hero CTAs, match the source page's primary and secondary button treatments on the same background color. If the user asks for "the other style," apply the adjacent CTA's class/style exactly while preserving the selected CTA's destination and analytics.
- Before building or revising CTA styles, define the page's button variant map from the source brand: primary, secondary/outline, light-on-dark, and utility/header. Apply those variants consistently instead of relying on generic class names such as `secondary` when they no longer describe the visual treatment.
- For every visible CTA, verify label, destination/action, class or variant, computed background color, text color, border color, hover/focus state, text wrapping, external-link safety, and `flzAnalytic` tracking.
- Treat hero proof/stat cards as first-viewport brand elements. Verify card background, border, stat color, label size, line wrapping, and contrast against the hero background.
- Keep Situation/Solution sections compact. Default to side-by-side panels on desktop and stacked panels on mobile instead of oversized full-width narrative paragraphs.
- Use small uppercase section labels plus headline-scale summaries for major section intros.
- If a section intro is intended as a major headline, let it span the full content width. Do not cap it to a narrow card width unless the design specifically calls for it.
- Match display text to its container. Avoid huge text inside compact cards, panels, nav bars, or sidebars.
- Avoid UI cards inside other cards and avoid page sections styled as floating cards unless they are true repeated cards, modals, or framed tools.

## Brand Fidelity Checklist

- Before writing or revising the page, inspect the vendor site or provided screenshot for the actual brand system: header treatment, logo usage, hero composition, section rhythm, typography scale, card radius, imagery, button hierarchy, footer structure, and repeated CTA language.
- Match the vendor's public messaging closely. Prefer real source-page language for product categories, benefit framing, and CTA labels; adapt only enough to fit the selected GTM motion and target account.
- For buttons, capture the concrete visual tokens: fill type, gradient direction, color stops, border, text color, border radius, height, padding, width/min-width, shadow, hover/focus state, and icon usage. Apply the same family of treatments across header, hero, resource, modal, calculator, and final CTA buttons.
- Treat screenshots from the user as visual source-of-truth corrections. If screenshot guidance conflicts with a prior implementation, update the source component/token and verify the computed styles.
- Do not borrow visual patterns from another vendor board unless the current vendor source supports them.

## Annotation-Driven Revision Flow

When the user provides browser annotations or screenshot comments:

1. Resolve the selected element by text, selector, and surrounding section context.
2. Identify the owning source CSS/HTML pattern, not only the visible DOM node.
3. Decide whether the comment implies a one-off instance edit or a reusable component/token change.
4. Make the smallest source edit that satisfies the annotation while preserving links, analytics, accessibility, and responsive behavior.
5. Reload the local preview with a cache-busting query string or a fresh localhost URL before evaluating the result.
6. Verify the selected element again through DOM/computed-style checks or browser screenshots before saving through MCP.
7. If the user's visible browser still shows the old state after the source verifies, tell them the tab may be stale and should be refreshed.

## Navigation QA

- Before save, create a nav map in your working notes: nav label, `href`, target element, target eyebrow/section label, target headline, and expected user job.
- Nav labels should match the content they jump to. Prefer action- or section-specific labels such as "ROI Calculator", "Platform Overview", "Briefs", "Use Cases", or "Proof" over generic taxonomy that is not visible on the page.
- For each nav item, verify that the target exists, scrolls below any sticky header using `scroll-margin-top`, updates the URL hash when appropriate, and fires an anchor analytics event.
- If desktop nav is hidden or simplified on mobile, provide an equivalent mobile path to the same key sections or intentionally keep the primary CTA-only mobile header when the source brand does that.
- Remove or deprioritize stale section IDs that are not linked, or keep them only when they support deep links from external follow-up.

## Calculator And Interactive Model QA

- Add an ROI calculator, value estimator, savings model, or planning model when the product has a measurable economic outcome and the page would benefit from a buyer-specific value frame.
- Match the calculator dimensions to the vendor's product and target account motion. For example, use invoice volume, locations, exception rate, cycle time, recovery opportunity, or labor cost for AP automation rather than a generic revenue-growth model.
- Use public account data or clearly labeled planning assumptions for defaults. Do not expose private-note numbers as buyer-facing assumptions unless the user explicitly authorizes that use.
- Every slider, input, tab, scenario selector, or toggle must update its own displayed value and all dependent visible outputs.
- For ROI or value models, verify at least the default state, one mid-range change, and one edge or high-value change before save. The primary dollar amount, supporting metrics, and label text should all stay consistent.
- Make model assumptions visible in buyer-friendly language. If a lift, multiplier, payback period, or conversion delta is fixed in code, disclose it in the UI or make it adjustable when the buyer is likely to challenge it.
- Prefer showing current state, projected state, and incremental lift separately when space allows. For conversion models, show the before/after rate, current conversions or revenue, incremental conversions or revenue, and projected total.
- Track meaningful model changes with `flzAnalytic("model_update", {text, area, value})` or equivalent useful payload. Do not track only that "something changed" when the selected value is available.
- Guard against misleading precision. Use rounded numbers, clear time periods, and labels such as "modeled", "estimated", or "planning frame" when the numbers are not sourced from the customer's actual data.

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
- Prefer localhost previews with a cache-busting query string over long-lived `file://` tabs during annotation work. Stale local tabs can show old CSS after the source file has changed.
- Render the local HTML at desktop and mobile widths before saving when possible.
- Verify that the first viewport shows the vendor/account brand clearly.
- Verify that section text does not overlap or overflow.
- Verify mobile has no horizontal overflow. A quick DOM check is `document.documentElement.scrollWidth <= window.innerWidth`.
- Verify referenced images render, cards remain bounded, modals open/close, and linked controls go to real destinations.
- For annotation-driven revisions, repeat the specific component QA that matches the edit: button computed styles, nav map and target checks, calculator/input output checks, modal open/close checks, or image rendering checks.
- If Folloze only returns a signed-in designer URL, say that unauthenticated public QA is not complete.

## Final Response

Keep the final response short:

- What changed or was built.
- Local source file path when one exists.
- Board ID.
- Exact designer/live URL returned by MCP.
- Tracker status when tracker logging is in scope.
- Commit hash when repo-backed source changes were committed.
- Any caveat, especially pending public deployment or signed-in-only QA.
