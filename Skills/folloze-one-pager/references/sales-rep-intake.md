# Sales Rep Intake

Use this reference for Stage 1. The objective is not to make the rep complete a long form. It is to turn a short conversation into a complete, source-safe brief that the rep can approve.

The canonical record is `intake.json`, validated against `../schemas/intake.schema.json`.

Target a two-to-five-minute first pass for an AE with authorized deal context. Expect a longer, research-led conversation for an SDR working a net-new account. The structured record can be detailed without making either conversation feel like a form.

## Interview Principles

- Ask only for missing information.
- Ask three to five related questions at a time.
- Reflect back what you heard before moving to research.
- Make assumptions visible.
- Default private systems to denied until authorized.
- Let the rep approve generalized account language when a useful public signal is unavailable.
- Do not turn an early request to publish into standing publish authorization.
- Do not start page generation while material fields are unresolved.
- Derive what can be supported by authorized evidence, then ask the rep to approve the buyer-safe interpretation.
- Require exactly one buyer challenge and one desired outcome in the final brief.

## Choose The Intake Lane

Start with:

1. Is this an AE active-deal follow-up or an SDR net-new leave-behind?
2. Which prospect and exact domain is this for?
3. Who is the primary reader?

Then follow the matching lane.

### AE Active-Deal Lane

Set `seller_inputs.seller.motion` to `ae_active_deal`.

Ask permission before reading private systems. When authorized, synthesize calls, emails, Salesforce, Granola, Drive, Slack channels, Slack DMs, Calendar, and any rep-supplied material rather than asking the AE to repeat known context. Confirm:

- the one buyer challenge the page should address
- the one desired outcome the buyer is trying to create
- the page's job in the active deal
- whether the next action is `Continue to the Deal Room` or `Reply to the Seller`
- which facts may be visible, paraphrased, or used only as strategy

### SDR Net-New Lane

Set `seller_inputs.seller.motion` to `sdr_net_new`.

Assume private deal context is unavailable. Use the official company website and current public research, then ask the SDR to confirm:

- the primary persona and likely initiative
- one evidence-based buyer challenge or a clearly labeled hypothesis
- one desired outcome
- why Folloze is relevant to the prospect now
- the real scheduling destination for `Book a Meeting`

An SDR does not need to supply every account field from memory. The skill may propose researched options, but the SDR must approve the selected hypothesis and buyer-safe wording before intake approval.

Then fill only the gaps below.

## Required Fields

| Group | Field | Requirement |
|---|---|---|
| Metadata | `intake_id` | Generated stable ID |
| Metadata | `brief_version` | Starts at 1 and increments after material change |
| Seller | name | Required |
| Seller | motion | `ae_active_deal` or `sdr_net_new` |
| Prospect | account name | Required |
| Prospect | domain | Required unless entity is explicitly confirmed |
| Audience | primary persona | Required |
| Audience | lifecycle stage | Required; `unknown` is valid |
| Business context | initiative | Required |
| Business context | challenges | Exactly one |
| Business context | desired outcomes | Exactly one |
| Business context | account signal | Required, or approve generalized mode |
| Page goal | page job | Required |
| Page goal | primary CTA | Real role-specific label, type, and destination |
| Research | source permissions | Explicit for every supported source |
| Claims | numeric-claim policy | Default `verified_only` |
| Brief | normalized message spine | Required before approval |
| Brief | message-fit matrix | Required before approval |
| Approval | decision and version | Explicit approval required |

## Optional But High-Leverage Fields

- why now
- objection or proof need
- deadline, event, renewal, launch, or decision window
- current stack or operating approach
- account trigger line
- approved customer proof
- official account logo
- seller photo or contact details
- one or two secondary personas
- proof cards and Build, Activate, or Signal pillars to emphasize or omit within the standard module set
- up to two optional buyer resources, with the exact label and destination the seller approves
- verified account accent, source ID, and exact extracted source fact containing that one hex, or the source-backed Folloze default

## Source Permission Questions

Ask permission by source family:

- Bundled skill references are available by default; classify each visible use in the source ledger.
- May I use public company research and official brand assets?
- May I read Salesforce for strategy context?
- May I read Granola or meeting notes?
- May I read relevant Drive documents?
- May I read Gmail or Calendar context?
- May I read relevant Slack channels or private surfaces?
- May I read relevant Slack DMs?
- For private sources, may I only use the insight internally, or may a specific fact be paraphrased or used exactly?

Supported read values:

- `allow`
- `deny`
- `not_available`

Supported buyer-use values:

- `per_item`: classify each supplied fact in the source ledger
- `public_fact`
- `paraphrase_only`
- `strategy_only`
- `exact_use`
- `blocked`

Rep input may use `per_item`. Private sources default to `strategy_only`. Exact use requires a dedicated ledger ID for exactly one fact plus item-level approver and timestamp; the visible wording must equal that fact exactly.

## Account Specificity Gate

The brief must choose:

- `account_specific`: at least one buyer-safe account signal supports the visible argument
- `account_generalized`: the seller explicitly accepts a Folloze-led value page with only confirmed account identity and audience context

Do not manufacture personalization from a logo, industry label, or private behavior signal.

## CTA Gate

One primary CTA is required.

| Motion | Required CTA |
|---|---|
| `sdr_net_new` | `meeting`, label exactly `Book a Meeting`, valid scheduling URL |
| `ae_active_deal` | `url`, label exactly `Continue to the Deal Room`, valid HTTP(S) deal-room URL |
| `ae_active_deal` | `mailto`, label exactly `Reply to the Seller`, one plain recipient exactly matching the seller email, with no query parameters or additional recipients |

Do not substitute `Learn more`, `Explore`, or a generic in-page jump for the role-specific primary action.

The validator enforces the approved type, label, exact destination, and HTTP(S) shape. The rep must still confirm during preview review that an SDR URL is the intended scheduling page and an AE URL is the intended deal room; URL semantics are a manual QA check.

## Normalized Brief

Before requesting approval, reduce the intake into:

```text
Buyer situation:
Holistic page goal:
Account context:
Buyer priority:
Why change:
Why now:
Folloze promise:
Proof strategy:
Next action:
Selected pillars:
Recommended sections:
Unresolved gaps:
Assumptions:
```

Create the message-fit matrix:

| Account signal | Source ID | Buyer-use rule | Folloze value prop ID | Buyer-safe claim | Placement |
|---|---|---|---|---|---|

Good placement values:

- `hero`
- `buyer_challenge`
- `desired_outcome`
- `proof`
- `folloze_capabilities`
- `path_build`
- `path_activate`
- `path_signal`
- `cta`
- `resource`
- `metadata`

Placement is part of the approval. Stage 2 must bind each sourced text node to its immutable module placement; globally approved wording cannot be moved to a different section or hidden to satisfy matrix coverage.

Before approval, copy every selected Folloze value-prop ID used by the matrix into `claims_policy.approved_claim_ids`. Put externally approved customer or numeric proof IDs in `claims_policy.approved_proof_ids`. These ID lists are necessary but not sufficient.

Create an exact-approved display-content registry:

- `claims_policy.approved_claim_content`: each claim ID, its Build, Activate, or Signal pillar, every exact buyer-facing display string approved for that ID, and its source IDs
- `claims_policy.approved_proof_content`: each proof ID, every exact buyer-facing display string approved for that ID, and its source IDs

Also approve one buyer-safe meta description and its source IDs. The page title is mechanical: `Folloze for <approved account>`. Register each optional resource under `seller_inputs.page_goal.approved_resources` with its opaque ID, exact label, exact HTTP(S) URL, and source IDs; its label also needs an exact message-fit row.

Every visible claim and proof string must match an entry in the corresponding registry. Numeric content is valid only under an approved proof ID; do not pair a new number with an approved qualitative claim ID. If verified numeric proof is unavailable, approve qualitative language and omit the metric.

Treat `claims_policy.blocked_claims` as both an ID denylist and a buyer-readable phrase denylist. Copy every seller `forbidden_topics` value into `stage2_handoff.constraints.prohibited_visible_terms`; neither set may appear in approved copy, metadata, accessible labels, or rendered page copy.

The matrix `source_use` must exactly match the referenced ledger entry's buyer-use rule. Only `public_fact`, `paraphrase_only`, and item-approved `exact_use` rows may drive visible copy. Stage 2 must trace every matrix source used on the page with an opaque `data-source-id` or `data-source-ids` attribute; source locators remain in the sidecar only.

## Approval Card

Show this compact summary:

```text
Prospect:
Seller motion:
Primary reader:
Page job:
Core argument:
Promise:
Proof approach:
Path:
Primary CTA:
Sources allowed:
Private-source boundary:
Assumptions:
Modules:
```

The standard modules are Hero, Desired outcome, Folloze capabilities, Proof, and CTA. Proof may be qualitative when a verified number is unavailable; do not replace the module with invented evidence.

Then ask:

> Approve this brief for a local one-pager build, or tell me what to revise.

Record:

- `decision: approved`
- approved brief version
- approver name
- timestamp
- the approval text
- a digest of the normalized brief and source permissions
- `approved_scope: local_build`

Approval never includes MCP save, publication, tracker changes, commit, or push.

Build `approval_digest` as `sha256:<hex>` from canonical JSON with sorted keys and compact separators. Include the current brief version, seller inputs, research policy and source ledger, claim policy, normalized brief, and Stage 2 constraints. Exclude metadata timestamps and the approval object itself.

Generate it with:

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --digest approval
```

## Invalidating Approval

Set approval to `invalidated`, increment `brief_version`, and request approval again when any of these change:

- primary audience
- account entity
- buyer problem or outcome
- page job
- CTA
- source permissions
- proof permission
- buyer-visible assumption
- selected claim

Layout-only changes do not require new intake approval, but they require preview approval again. Any punctuation, tightening, or other change to buyer-visible claim or proof wording must already exist as an approved display-text variant; otherwise update the registry, invalidate intake approval, and request approval again.

## Edge Cases

### Ambiguous Account

Stop until the entity is resolved through domain, official URL, board identity, or explicit seller confirmation.

### Thin Evidence

For an SDR, offer generalized mode or a rep-approved hypothesis. Keep the page specific to the persona, initiative, and single desired outcome. Do not present a hypothesis as an account fact. For an AE, ask whether another authorized call, email, Slack, DM, CRM, or Drive source can resolve the gap before generalizing.

### Conflicting Sources

Record the conflict. Prefer the most current approved source. Remove the claim when the conflict cannot be resolved.

### Customer Expansion

Capture:

- what the customer already proved
- what Folloze capability supported it
- what next outcome the expansion should enable

If the first win is unknown, say so in the internal brief.

### Multiple Personas

Require one primary persona. Limit secondary personas to two. Do not flatten all roles into generic committee language.

### Missing Logo

Use a text wordmark. Do not use an unverified logo search result, favicon, or recreated mark.

### Oversized Brief

If the argument needs many resources, stakeholders, stages, or separate storylines, recommend a campaign board or digital deal room rather than overloading the one-pager.
