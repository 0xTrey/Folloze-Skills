# Messaging Source Priority

Use this reference to keep Folloze one-pagers aligned with approved messaging while still adapting to the account conversation.

## Source Priority

Use Folloze messaging sources in this order:

1. User-provided current messaging, sales deck, campaign direction, or review comments for this specific one-pager.
2. Bundled `folloze-brand-kit` references, especially `content-system-v3-2.md`, `brand-foundation.md`, `messaging-library.md`, `claims-and-proof.md`, `voice-and-style.md`, and `visual-identity.md`.
3. Current Folloze website or active public messaging if the Brand Kit appears stale.
4. Approved prior one-pagers or sales assets that the user explicitly wants to reuse.
5. This skill's `folloze-value-props.md` reference as the lightweight fallback menu.

Do not use restricted customer-specific materials by default. Use them only when the current account, seller, or user explicitly authorizes them.

## Current Messaging Guardrails

These should be verified against `folloze-brand-kit` and any newer user-provided source when possible:

- External frame: Folloze helps teams target and convert key accounts.
- External display register: `Build. Activate. Signal.`
- External prose pattern: `[Your AI does X]. [Folloze does Y].`
- Lead with what happens: deploy, host, govern, personalize, capture signal.
- Avoid external `activation layer` language.
- Avoid external customer-facing agent-name-led messaging.
- Use concrete, buyer-safe claims and proof.
- Avoid hype, full-autonomy claims, retired category language, and future roadmap claims.

## Message-Fit Matrix

Before writing page copy, build this matrix in working notes:

| Account signal | Source | Folloze value prop | Buyer-facing claim | Page placement |
|---|---|---|---|---|

Definitions:

- `Account signal`: something the account said, did, needs, fears, or must prove.
- `Source`: call notes, Salesforce, Drive, Gmail/Calendar, or public research.
- `Folloze value prop`: approved Folloze message, product capability, proof point, or pillar.
- `Buyer-facing claim`: the sentence or phrase safe to show on the one-pager.
- `Page placement`: hero, value card, motion row, chip, bottom card, CTA, or proof area.

The matrix prevents two common failures:

- dumping generic Folloze messaging into every page
- creating a beautiful page that does not answer the account's real goals or objections

## Example Mapping

| Account signal | Folloze value prop | Buyer-facing claim | Page placement |
|---|---|---|---|
| Team needs to launch a campaign quickly with limited resources | Build | Build personalized account experiences without rebuilding each destination | Value card |
| The account is using AI but lacks a governed route to market | Bring your own AI, Govern | Your AI creates the content. Folloze deploys it with brand and governance applied | Motion row |
| Leadership needs evidence that engagement matters | Signal, deep engagement intelligence | Show which accounts engaged, what they consumed, and what should move to sales | Motion row |
| Security and governance review may slow momentum | Enterprise-grade governance | Package security, governance, and proof details early for review | Bottom card |

Only include the rows that matter for the account. A strong one-pager usually uses 5-8 rows, not every possible Folloze value prop.

## Keeping The Library Current

When a one-pager creates a useful reusable phrase, objection pattern, or proof pairing:

- keep the account-specific version in the account artifact
- add the generic pattern to `folloze-value-props.md` only after it works in more than one account context
- add broader reusable brand language to `folloze-brand-kit` when it should guide other skills too
- avoid adding customer names, private notes, pricing, or deal-specific terms to the shared skill
