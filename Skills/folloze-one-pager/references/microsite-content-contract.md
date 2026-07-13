# Microsite Content Contract

Use this reference after the intake is approved. It maps the approved brief into a concise buyer-facing page without letting the template dictate the story.

## Page Thesis

Write one sentence before editing HTML:

> For [primary reader at account], this page should make [decision or next action] easier by showing [specific Folloze promise] with [proof approach].

Every visible section must strengthen that thesis. Remove sections that only explain the page, repeat another claim, or tour product modules.

## Narrative Shape

Use `Promise -> Proof -> Path`.

### Promise

The first viewport answers:

- Why is this relevant to this account?
- What business outcome or decision is at stake?
- Why is Folloze relevant now?
- What should the buyer do next?

Required content:

- one short account-context eyebrow
- one H1 with a business outcome or strategic turn
- one supporting paragraph, usually 25 to 45 words
- one primary CTA
- exactly one buyer challenge
- exactly one desired outcome

Avoid:

- `Built for [account]`
- `Your personalized microsite`
- `Meeting recap`
- generic `Transform your ABM` language
- a headline that only inserts the account name into generic Folloze copy

### Proof

Proof can be:

- an approved customer outcome
- an approved platform benchmark
- a verified public product capability
- a buyer-safe account fact and its implication
- a qualitative reason to believe

Rules:

- choose relevance over the largest number
- state the implication, not only the fact
- give every proof card one explicit `data-evidence-kind="proof|claim"` and opaque `data-evidence-id`
- keep source URLs and private provenance in the intake
- use qualitative language when numeric proof is unavailable
- if neither numeric nor qualitative proof is approved, return to Stage 1 rather than shipping an empty or invented proof module

### Path

Translate only the relevant Folloze pillars:

- Build: how the team creates the governed account experience
- Activate: how the team deploys and personalizes it across the relevant motion
- Signal: how the team captures engagement and guides follow-up

Weave governance into Build or Activate when enterprise control matters. Do not create a separate Govern pillar.

Do not force three equal generic feature cards. The template uses a connected progression so each step can answer the approved buyer problem.

## Standard Module Set

Every page uses these five buyer-facing modules, rendered in `Promise -> Proof -> Path` order:

1. Hero: the promise and primary action in `#promise`
2. Desired outcome: the one buyer challenge and one desired outcome, presented with the hero
3. Proof: verified numeric evidence when approved, otherwise an approved qualitative reason to believe in `#proof`
4. Folloze capabilities: the relevant Build, Activate, and Signal path in `#path`
5. CTA: the role-specific next action in `#next-step`

Keep the narrative logic `Promise -> Proof -> Path`, even when the compact Desired outcome treatment sits inside the hero. The capability path should show how Folloze turns the promise into an operating approach, not become a product tour.

The default should remain a short scroll. Route deeper libraries, calculators, multi-stakeholder plans, or many resources to a broader board or deal room.

## Template Field Map

Copy `render-values-template.json`, choose every module explicitly, and fill only values supported by the approved intake. Render with `scripts/render_one_pager.py --brief path/to/intake.json`; do not perform raw string replacement. The renderer first refuses any intake that lacks a current, digest-bound local-build approval. It then HTML-escapes text, validates URL/color/identifier contexts, selects the CTA variant, removes omitted modules, and renumbers selected pillars. A failed approval gate writes no HTML; the separate final validator still verifies the exact rendered output against the approved brief.

| Token | Intake source |
|---|---|
| `ACCOUNT_NAME` | prospect account name |
| `ACCOUNT_LOGO_URL` | verified official logo; remove image for text fallback |
| `ACCOUNT_CONTEXT` | approved buyer-safe initiative or context eyebrow; the co-brand lockup already carries the account name, so do not repeat a numeric-bearing account name where it could be mistaken for a metric |
| `HERO_SOURCE_IDS` | source IDs supporting visible hero claims |
| `BUYER_CHALLENGE` | the single approved buyer challenge or rep-approved hypothesis |
| `BUYER_CHALLENGE_SOURCE_IDS` | source IDs supporting the challenge; use an approved `rep_input` or `skill_reference` source for generalized language |
| `DESIRED_OUTCOME` | the single approved buyer outcome |
| `DESIRED_OUTCOME_SOURCE_IDS` | source IDs supporting the desired outcome; use an approved `rep_input` or `skill_reference` source for generalized language |
| `PAGE_TITLE` | renderer-computed mechanical `Folloze for <approved account>` title; do not supply a custom value |
| `META_DESCRIPTION` | exact `page_goal.meta_description`, approved in the message-fit matrix for every `meta_description_source_ids` entry; omit a numeric-bearing account name because the mechanical title and co-brand lockup already carry it |
| `HERO_HEADLINE` | promise |
| `HERO_SUPPORT` | buyer situation and Folloze relevance |
| CTA object | approved role-specific type, label, and destination; renderer selects URL, mailto, or meeting markup |
| `PROOF_HEADLINE` | proof section's buyer-facing argument |
| `PROOF_INTRO` | why the selected proof matters |
| `PROOF_*_KIND` | `proof` for approved proof IDs or `claim` for approved qualitative claim IDs |
| `PROOF_*_ID` | approved opaque ID from the matching proof or claim allowlist |
| `PROOF_*_VALUE` | approved evidence or qualitative anchor |
| `PROOF_*_COPY` | implication for the buyer |
| `PROOF_*_SOURCE_IDS` | exact source IDs bound to that proof or qualitative evidence record |
| `PROOF_SOURCE_IDS` | source IDs supporting the proof-section framing |
| `RESOURCE_*_ID` | opaque ID from `seller_inputs.page_goal.approved_resources` |
| `RESOURCE_*_LABEL` | exact approved buyer-visible resource label |
| `RESOURCE_*_URL` | exact approved HTTP(S) resource destination |
| `RESOURCE_*_SOURCE_IDS` | exact source IDs bound to the approved resource |
| `PATH_HEADLINE` | how the operating model changes |
| `PATH_INTRO` | concise setup for the selected pillars |
| `PATH_SOURCE_IDS` | source IDs supporting account-specific path framing |
| `BUILD_CLAIM_ID` | selected approved Build value-prop ID |
| `BUILD_HEADLINE` | account-specific Build outcome |
| `BUILD_COPY` | approved Build path |
| `BUILD_SOURCE_IDS` | exact source IDs bound to the approved Build claim |
| `ACTIVATE_CLAIM_ID` | selected approved Activate value-prop ID |
| `ACTIVATE_HEADLINE` | account-specific Activate outcome |
| `ACTIVATE_COPY` | approved Activate path |
| `ACTIVATE_SOURCE_IDS` | exact source IDs bound to the approved Activate claim |
| `SIGNAL_CLAIM_ID` | selected approved Signal value-prop ID |
| `SIGNAL_HEADLINE` | account-specific Signal outcome |
| `SIGNAL_COPY` | approved Signal path |
| `SIGNAL_SOURCE_IDS` | exact source IDs bound to the approved Signal claim |
| `NEXT_STEP_HEADLINE` | decision or action |
| `NEXT_STEP_COPY` | what happens next |
| `NEXT_STEP_SOURCE_IDS` | source IDs supporting the approved next-step copy |
| `SELLER_NAME` | approved seller identity |
| `SELLER_ROLE` | optional seller role |
| `ACCOUNT_ACCENT` | exact `visual_preferences.account_accent.hex`, backed by a source ID and exact extracted fact containing that one hex |

Set unused proof cards, resource links, and path pillars to `false`; the renderer removes their markup and linked controls. Proof requires at least one enabled evidence card. At least one approved Build, Activate, or Signal pillar is required. Enable at most the first two registry-bound resources, in order. If no verified account logo exists, set `account_logo` to `false`. The renderer exposes the text fallback and removes an empty seller-role separator.

Every included buyer-copy source token must contain at least one approved source ID. Generalized copy is still an approved choice, so bind it to the relevant `rep_input` or `skill_reference` ledger entry rather than leaving the trace empty.

The renderer's fixed `data-placement` values bind each sourced string to its approved message-fit location. Do not move globally approved copy between hero, challenge, outcome, proof, capability, CTA, resource, or metadata placements; update and reapprove the matrix instead.

Render command:

```bash
python3 Skills/folloze-one-pager/scripts/render_one_pager.py \
  --brief path/to/intake.json \
  --template Skills/folloze-one-pager/assets/one-pager-microsite-template.html \
  --values path/to/render-values.json \
  --output path/to/one-pager.html
```

## Safe Token Replacement

- Use the renderer for every token substitution; it applies context-aware HTML escaping and URL, identifier, and CSS-color allowlists.
- Accept only verified HTTP(S), meeting, or seller-matching mailto destinations.
- Use the exact approved six-digit `visual_preferences.account_accent.hex` value for `ACCOUNT_ACCENT`; do not choose a color only in the render-values file.
- Do not place rep input, source text, account names, or URLs inside JavaScript literals.
- Do not insert remote HTML, scripts, event handlers, or CSS from researched pages.
- Do not edit renderer-generated event handlers or script blocks. Rerender from the durable values file when content changes.
- Keep CTA analytics labels based on `this.dataset.ctaLabel`, resource labels based on `this.innerText`, destinations based on `this.href`, and areas fixed by the template.

## Copy Limits

Use these as pressure, not mechanical truncation:

| Element | Target |
|---|---|
| Eyebrow | 2 to 7 words |
| H1 | 7 to 16 words |
| Hero support | 25 to 45 words |
| CTA | 2 to 6 words |
| Buyer challenge | 8 to 24 words |
| Desired outcome | 8 to 24 words |
| Proof value | 1 to 8 words |
| Proof implication | 12 to 28 words |
| Path headline | 3 to 8 words |
| Path copy | 20 to 45 words |
| Final CTA copy | 20 to 45 words |

One strong sentence is better than three explanatory sentences.

## Folloze Messaging Rules

Preferred:

- target and convert key accounts
- Build. Activate. Signal.
- deploy, host, govern, personalize, capture signal
- personalized account experience
- first-party engagement signal
- campaign destination
- sales-ready follow-up

Avoid visible:

- activation layer
- campaign agent
- activation agent
- insight agent
- Buyer Experience Platform
- ABX platform
- fully autonomous campaign execution
- generic AI-powered claims
- `this page`, `this microsite`, or explanations of how the asset was built

Use no em dashes.

## CTA Rules

- Use one primary action consistently.
- The destination must match the approved intake.
- For `sdr_net_new`, use a meeting link labeled exactly `Book a Meeting`.
- For `ae_active_deal`, use either a deal-room URL labeled exactly `Continue to the Deal Room` or a mailto link labeled exactly `Reply to the Seller` with one plain recipient matching the seller email and no parameters.
- External links use `target="_blank" rel="noopener"`.
- External CTAs use a direct inline `flzAnalytic('cta_click', ...)` call.
- Remove decorative arrows that imply a dead action.
- Any optional resource link declares its registry ID in `data-resource`, carries the registry source IDs, exactly matches the approved label and URL, and uses exactly `onclick="flzAnalytic('resource_click', {text:this.innerText.trim(), area:'resources', url:this.href}, this)"`. These custom events supplement Folloze's native visitor, page, engagement, and content analytics.

## Brand And Layout Rules

- Folloze is the required primary brand owner. Prospect identity is a restrained co-branding cue, not an account-owned visual system.
- Use the current official Folloze site and bundled `folloze-brand-kit` as the shared visual authority. Do not require Figma access.
- Keep prospect color to one restrained accent. Record its exact hex, buyer-visible source ID, and exact extracted source fact in the intake; the fact must contain that one hex. Otherwise use the source-backed Folloze default.
- Use real Folloze and prospect marks.
- Prefer a simple white-paper composition, readable outcome typography, white and pale surfaces, restrained dividers, and a short scroll.
- Avoid generic purple gradients, glassmorphism, stock illustrations, icon grids, and cards inside cards.
- Preserve visible focus, contrast, reduced-motion handling, and narrow-mobile layout.

## Source And Claim QA

For every buyer-visible account statement:

1. find its source ID in the intake
2. confirm the buyer-use rule permits the wording
3. confirm the statement matches the approved brief

For every buyer-visible Folloze claim:

1. map it to the brand kit, customer-ready capability reference, approved proof, or current official source
2. confirm its value-prop or claim ID is in `claims_policy.approved_claim_ids`
3. confirm the exact visible string is in the matching `claims_policy.approved_claim_content` entry
4. confirm the registry entry carries the supporting source IDs
5. confirm the language is externally safe and answers the approved buyer problem
6. confirm every capability card's claim record is bound to that card's Build, Activate, or Signal pillar

For every number or customer outcome:

1. confirm an approved proof ID
2. confirm every exact visible string is in the matching `claims_policy.approved_proof_content` entry
3. add the ID to the HTML
4. state the buyer implication
5. remove the number if status or permission is uncertain; use an approved qualitative reason to believe instead

## Final Buyer Read

Read the rendered page top to bottom as the prospect:

- Is the argument clear in ten seconds?
- Does the page recognize the buyer without sounding like surveillance?
- Does each section add a new reason to believe?
- Does every proof answer `so what?`
- Does the path explain how Folloze helps, not merely list features?
- Is the next step concrete?
- Could any private-note phrasing embarrass the seller?
- Could this be sent to another account by swapping the logo? If yes, sharpen it.
