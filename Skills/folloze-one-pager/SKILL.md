---
name: folloze-one-pager
description: Turn real account call notes, Salesforce and Drive context, prior conversations, and account research into an editable Folloze-branded HTML one-pager plus an email-shareable PDF follow-up. Use when Folloze sellers or CSMs ask for a call-notes follow-up, shareable one-pager, PDF leave-behind, recap page, or account-specific Folloze value-prop page after a prospect or customer conversation.
---

# Folloze One-Pager

Use this skill to turn real account context into a polished Folloze follow-up page that a seller or CSM can review, edit, export to PDF, and email.

This is HTML-first. Build the local HTML source before PDF export so the teammate can review and annotate it in the app.

## Operating Rules

- State the working goal before material edits: account, audience, source context, local HTML target, PDF target if requested, research plan, and private-note boundary.
- Keep durable files in the relevant git-backed workspace. If no obvious repo exists, ask where the one-pager should live before writing files.
- Default deliverable is local editable HTML. Create the PDF only when the user asks for a shareable/email version or approves the HTML.
- Use the Folloze-blue one-page structure as the default template: Folloze + account lockup, large outcome hero, 3 value cards, right-side `Build. Activate. Signal.` motion panel, 4 bottom focus cards, and a clean one-page landscape PDF export.
- Keep the visual system primarily Folloze branded. Use Folloze navy, blue, cyan, white, and pale-blue surfaces as the default palette; use account/vendor colors sparingly as accents for one keyword, one signal/proof cue, or a small chip. Do not let pink, purple, orange, or the account palette dominate unless the user explicitly asks for that direction.
- Use real Folloze and account/company logos. Prefer official company website or official brand/media assets; inspect rendered assets instead of trusting filenames. Do not redraw logos.
- Use real call and account context. Check the user's supplied notes first, then available call history, Salesforce notes, Drive docs, Gmail/Calendar context, and public account research as needed.
- Look across multiple calls when possible. The point is to synthesize a specific follow-up, not summarize the latest note in isolation.
- Treat private notes as strategy inputs. It is acceptable to outline goals, objections, concerns, and required proof, but translate them into buyer-safe language about how Folloze can help. Do not quote private notes or expose internal meeting mechanics unless the user explicitly approves.
- Use `folloze-brand-kit` plus this skill's `references/messaging-source-priority.md` and `references/folloze-value-props.md` to choose Folloze value props. Pick only the value props that map to the account's goals and objections.
- Use the current external Folloze register: `Build. Activate. Signal.`
- Keep `activation layer`, `campaign agent`, `activation agent`, and `insight agent` out of visible customer-facing copy unless the user explicitly asks for internal or sales-enablement language.
- Create a message-fit matrix before writing page copy. Each visible Folloze claim should map to an account signal, an approved Folloze message, and a page placement.
- Keep messaging separate from layout. The template defines where content goes; the message-fit matrix decides what belongs there.
- Do not use numeric claims unless they come from an approved source, a user-approved prior one-pager, or current Folloze sales material. If uncertain, use qualitative value language or `[PROOF]` in working notes, not in buyer-facing final copy.
- Do not publish through Folloze MCP or update a tracker unless the user explicitly asks. If they ask for a board/microsite save, hand off to `Folloze-MCP-Demo-Builder`.

## Workflow

### 1. Gather Context

Use `references/context-research.md`.
Use `references/messaging-source-priority.md` for Folloze messaging sources. Load `folloze-brand-kit` references when you need the portable brand, claim, proof, voice, color, or logo source of truth.

Resolve:

- account and audience
- primary meeting or note source
- prior calls or related account notes
- Salesforce account, opportunity, activity, and note context if available
- Drive docs, decks, notes, or account plans if available
- public website, public account facts, and official logo/brand assets
- current goals, objections, buying questions, and follow-up jobs

Keep working notes internal. The final page should not read like a meeting transcript.

### 2. Create A Message-Fit Brief

Before writing the HTML, reduce the research into:

- buyer situation
- top 2-4 goals
- top 2-4 objections or proof needs
- Folloze value props that directly answer those goals or objections
- proof or credibility points that can be safely shown
- recommended follow-up CTA or next conversation path

Then create a compact message-fit matrix:

| Account signal | Source | Folloze value prop | Buyer-facing claim | Page placement |
|---|---|---|---|---|

Rules:

- Account signal must come from call notes, Salesforce, Drive, Gmail/Calendar, or public research.
- Folloze value prop must come from approved messaging sources or `references/folloze-value-props.md`.
- Buyer-facing claim must be safe to send externally.
- Page placement must name the specific template area: hero, value card, motion row, chip, or bottom card.

If the account details are thin, make the page useful with a general Folloze value path, and state the missing evidence in the final response.

### 3. Build Local HTML

Use `assets/one-pager-template.html` as the starting point unless the user asks for a different structure.

Required page qualities:

- first viewport immediately shows Folloze plus the account/company context
- headline names the business outcome, not the internal meeting
- value cards explain why Folloze is useful for this account
- right-side motion panel explains how Folloze builds, activates, and captures signal for the program
- bottom cards map to the account's goals, objections, program route, and enterprise/proof needs
- page composition is built for a one-page 16:9 landscape PDF: no crowded bottom overlays, no clipped cards, no dominant off-brand color blocks, and no desktop horizontal overflow
- no browser comment markers, draft placeholders, dead links, or internal-only language remain

### 4. Review And Iterate

Open the local HTML in the browser or app preview. Check:

- desktop fit and first-viewport readability
- mobile layout if the page may be shared as HTML
- PDF preview rendering, not just `pdfinfo`; visually inspect the generated PDF or a PNG preview of it before sending
- real logos render correctly
- value cards do not overflow
- capability chips line up cleanly
- dominant palette stays Folloze blue/white/navy with only small account-color accents unless the user requested otherwise
- no private-note phrasing leaks into buyer-facing copy
- every visible value prop maps back to the message-fit matrix
- every account-specific claim has a traceable account source
- every Folloze claim aligns to approved messaging source priority
- the page uses the layout as a container, not as the source of messaging truth
- visible copy follows `Build. Activate. Signal.` or plain-language Folloze descriptions, not internal agent names
- all visible buttons or links either work or are removed

When the user gives browser comments, resolve the selected element and make the smallest source edit that satisfies the comment.

### 5. Export PDF

When the user asks for an email/shareable version:

- export a one-page landscape PDF when the content fits
- verify page count, file size, orientation, and preview rendering
- regenerate desktop/mobile screenshots and the PDF after every visual revision that affects the sent artifact
- if browser print introduces visual artifacts, use a screenshot-backed PDF so the email version matches the approved HTML
- save the PDF beside the HTML or in the repo's established output folder

### 6. Close Out

Return the local HTML link, the PDF link when created, and a short note on verification. Mention unresolved source gaps only if they matter to the seller before sending.
