# Brand And Messaging Source Manifest

Use this manifest to choose the current Folloze message, proof, and visual source without copying restricted team material into a public skill repository.

Last source audit: 2026-07-13.

## Source Priority

Use this order:

1. current user-approved direction for the specific asset
2. current approved Folloze team source, when connected and authorized
3. current official Folloze public website or public article
4. bundled `folloze-brand-kit`
5. this skill's one-pager-specific value-prop fallback
6. historical Folloze material as a research lead only

When sources conflict, prefer the newest approved source and record:

- source names
- dates or versions
- the conflicting language or claim
- the winner and why
- whether approval is still needed

Do not silently blend conflicting numbers or product language.

## Bundled Sources

Load these from `folloze-brand-kit`:

| Source | Use |
|---|---|
| `content-system-v3-2.md` | Active bundled messaging alignment |
| `brand-foundation.md` | Positioning, audience, and category guardrails |
| `messaging-library.md` | Value props and account-signal mappings |
| `claims-and-proof.md` | Proof status and claim rules |
| `voice-and-style.md` | Voice, kill list, and copy QA |
| `content-brief-template.md` | Brief structure |
| `campaign-board-design-context.md` | Folloze-owned microsite design |
| `visual-identity.md` | Bundled logos and legacy color guidance |
| `product-capabilities-customer-ready.md` | Buyer-safe capability descriptions |

The bundled content system was captured on 2026-06-01. Treat it as a strong fallback, not proof that no newer team guidance exists.

## Current Official Public Sources

### Folloze Homepage

- URL: https://www.folloze.com/
- Use for: current public positioning, CTA language, section rhythm, logo treatment, surface mix, typography, and component direction
- Current message anchors observed during the source audit:
  - target and convert key accounts
  - Build, Activate, Signal
  - personalized experiences
  - deploy, host, govern, personalize, and capture signal
- Recheck before a material template redesign because the website can change.

### The Open Approach

- URL: https://www.folloze.com/blog/article/bring-your-own-ai-mcp
- Author: Tyler Hart
- Published: 2026-06-15
- Use for: the open execution story, bring-your-own-AI framing, MCP context, and the distinction between content creation and governed deployment
- Keep MCP as evidence of the open approach. Do not turn MCP into the buyer-facing product category.

## Approved Internal Source Roles

When a connected internal source is authorized, search by exact title rather than storing private URLs or raw internal content in this public package:

| Source title | Owns |
|---|---|
| `Brand Voice Guide` | How Folloze sounds |
| `Content Brief Template` | What inputs content creation needs |
| `Messaging Framework` | What Folloze says and how the story is organized |
| `Customer Proof Library` | Which proof is true and where it may be used |
| `Project Instructions` | Operating rules for content generation |
| `Outbound Sequences` | Buyer-first account outreach patterns |
| `Folloze Content System - Live` | Combined live messaging system |
| `Instructure ABM ROI One-Pager - CMO Leave-Behind` | AE active-deal structural reference for an outcome-led executive takeaway, one operating challenge, proof or impact, Folloze relevance, and a clear decision ask |

Internal source rules:

- Require the user's permission before searching private Slack, DMs, Gmail, CRM, call notes, or restricted Drive folders.
- Record a redacted source ID in the intake ledger.
- Do not copy raw private passages, private links, tokens, or access details into this repo.
- Abstract reusable guidance only when it is safe and approved.
- Keep customer-specific proof inside the approved proof system, not the shared value-prop file.
- Use `Instructure ABM ROI One-Pager - CMO Leave-Behind` only as an AE structural reference. Do not store its private URL, raw copy, account details, modeled assumptions, or numbers in this repo, and do not reuse its metrics as proof.

## Tyler Guidance To Operationalize

Use these durable principles when current approved sources support them:

- Lead with the prospect's operating reality, not Folloze.
- Name a real gap, constraint, or decision.
- Put the differentiator early.
- Use one clear ask.
- One researched account-specific line creates more value than broad cosmetic personalization.
- Use `Promise -> Proof -> Path` for microsite copy.
- Hero copy carries the value promise.
- Supporting copy explains the primary benefit.
- Use proof only when its source and permission are known.
- If the copy could belong to any B2B martech vendor, rewrite it.

## Authorized Team-Guidance Refresh

Do not treat this manifest as a frozen substitute for what Tyler or the team shared later. When the rep or skill owner explicitly authorizes private team-source access and the source audit is stale:

1. Search the approved Slack channels and DMs for Tyler Hart as the author, beginning after the last source-audit date.
2. Search for the durable themes this skill depends on: positioning, `Build. Activate. Signal.`, value props, proof permission, outbound language, buyer-experience design, and words to avoid.
3. Use Slack messages as discovery leads. Confirm reusable guidance in a current approved team document, current public Folloze source, or explicit stakeholder approval before making it buyer-facing.
4. Record a redacted source-ledger ID, date range, classification, and buyer-use rule. Do not store raw messages, private channel links, message IDs, or verbatim private passages in this repo or generated HTML.
5. Reconcile conflicts through the source-priority order above and show the seller any material message choice that still needs approval.

Authorization to search account deal context does not automatically authorize a company-wide messaging harvest, and messaging-refresh permission does not authorize buyer-visible use of private account facts.

## Current Visual Direction

The live public site is the shared visual authority when the bundled visual file is visibly stale. The bundled `folloze-brand-kit` remains the reusable fallback. The one-pager must not depend on Figma access.

Observed public-site direction from the 2026-07-13 audit:

- display type: Instrument Sans when available
- deep navy: `#071428`
- slate: `#2C3D59`
- indigo: `#5B5BFF`
- strong indigo: `#3B3BE0`
- muted blue-gray: `#6B7E9D`
- white and pale tinted surfaces
- readable editorial headlines
- restrained cards and dividers
- outlined and filled pill CTAs
- simple white and pale content surfaces
- restrained motion with reduced-motion support

These are configurable template tokens, not a substitute for a current brand source. Keep the one-pager as a short-scroll, white-paper-style experience and update the token layer when the official site or bundled brand kit changes rather than patching individual components.

## Known Conflicts And Cautions

- Bundled `visual-identity.md` reflects an older bright-blue/cyan system with smaller-radius cards; the current public website uses stronger indigo and more rounded editorial modules.
- Historical ServiceNow + Microsoft lead counts conflict with the newer bundled proof row. Do not use a number until the current proof source is approved.
- Historical Qlik Virtual Passport influenced-pipeline numbers conflict. Do not choose the larger or more familiar number.
- Older `Headless` mode language and newer `Stack-driven` language may describe the same operating pattern. Follow the newest approved source for visible copy.
- `activation layer` remains prohibited external lead language. A current public source may use `execution layer`; do not treat those phrases as interchangeable without review.

## Refresh Rule

Refresh this source map when:

- the live content system or messaging framework changes
- Tyler publishes or shares a replacement source
- a proof conflict is resolved
- the official Folloze website changes its message or design system

A refresh updates source precedence and reusable guidance. It does not authorize rewriting a live customer page or publishing through MCP.
