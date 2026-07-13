# Context Research

Use this reference when building a Folloze one-pager from either active-deal evidence or net-new public research.

## Permission Gate

Read only the sources authorized in `intake.json`.

Safe defaults:

- rep input: allowed
- bundled skill references: allowed, with per-item buyer-use classification
- public web and official brand assets: allowed
- Salesforce, Granola, Drive, Gmail, Calendar, Slack channels, and Slack DMs: denied until explicitly authorized
- private-source buyer use: `strategy_only`

Permission to read a source is not permission to quote it. Record buyer-use separately as `per_item`, `public_fact`, `paraphrase_only`, `strategy_only`, `exact_use`, or `blocked`. Use `per_item` only when each supplied fact will be classified in the source ledger.

Do not broaden a public research request into private-system research. Private Slack channels and DMs require explicit permission.

## Motion-Specific Research

### AE Active Deal

For `ae_active_deal`, ask the AE to authorize each source family before access. When allowed, synthesize the history across calls, Granola, Gmail, Salesforce, Drive, Slack channels, Slack DMs, Calendar, and rep-supplied artifacts. Recover the buyer's durable operating challenge and desired outcome without making the AE restate known context.

Private evidence remains strategy-only unless the ledger grants buyer-visible use for a specific fact. Never expose note phrasing, internal intent scores, CRM stage commentary, or private objections verbatim without exact-use approval. Represent each exact-use fact with its own ledger ID, exactly one extracted fact, and its own approver and timestamp.

### SDR Net New

For `sdr_net_new`, begin with the official company website, current public initiatives, public leadership statements, and official brand assets. The SDR may not know every intake field. Propose evidence-based options, then ask the SDR to select and approve exactly one buyer challenge and one desired outcome.

Label inferred needs as hypotheses in the brief. A rep-approved hypothesis may shape generalized copy, but it must not be represented as a confirmed account fact. Keep private systems denied. If meaningful private deal context exists, switch to the AE active-deal lane and record its permissions instead of blending the two source models.

## Source Priority

1. Current user instructions and rep-supplied notes.
2. Current bundled skill references for approved Folloze messaging, capabilities, brand, and proof rules.
3. For an AE, authorized call notes from Granola, meeting exports, or other note sources the user names.
4. For an AE, authorized Salesforce account, opportunity, activity, task, event, and note context.
5. For an AE, authorized Google Drive docs, decks, sheets, account plans, prior proposals, and meeting notes.
6. For an AE, authorized Gmail, Calendar, Slack channels, and Slack DMs when history or follow-up context matters.
7. Public account research, including the official account website, official brand assets, current initiatives, and recent public news. This is the primary research path for an SDR.

Do not invent account facts, contacts, security requirements, or business outcomes. Use a softer framing when the evidence is directional.

## Source Ledger

Give every source a stable, non-sensitive ID:

| Field | Purpose |
|---|---|
| `source_id` | Opaque ID used by the message-fit matrix |
| `source_type` | One of `rep_input`, `skill_reference`, `public_web`, `salesforce`, `granola`, `google_drive`, `gmail`, `calendar`, `slack_channels`, or `slack_dms` |
| `locator` | Public URL or redacted internal locator |
| `classification` | Public, internal, confidential, or restricted customer |
| `buyer_use` | Public fact, paraphrase only, strategy only, exact use, or blocked |
| `confidence` | High, medium, or low |
| `approved_by` | Required for private exact use |
| `approved_at` | Required with `approved_by` for private exact use |
| `extracted_facts` | Compact fact list used during synthesis |
| `conflicts_with` | IDs of conflicting sources |

Keep private URLs, raw notes, tokens, and sensitive excerpts out of buyer-facing HTML. Use source IDs in the page and retain provenance in the sidecar.

For every buyer-visible source-backed string, record the exact approved display text in the message-fit matrix. For every Folloze claim or proof string, also bind the exact text to `claims_policy.approved_claim_content` or `claims_policy.approved_proof_content`. Source permission, an approved ID, and approved display wording are three separate checks.

## Multiple-Call Synthesis

When more than one call or note set exists, synthesize across the account history:

- latest stated goal
- recurring pain or objection
- open question that has not been answered
- stakeholder or team mentioned across calls
- next deadline, meeting, review, or approval path
- proof the account seems to need before moving forward

Prefer durable themes over one-off phrasing from a single call.

## Salesforce Check

When Salesforce is available, look for:

- account summary and current ownership
- open opportunities and stage context
- recent activities, notes, and next steps
- known business initiative or product interest
- procurement, security, legal, regional, or integration concerns
- existing customer or prospect status

Use Salesforce as internal evidence. Translate it into buyer-safe page copy rather than exposing internal CRM wording.

## Drive Check

When Drive is available, search for:

- account name
- domain name
- opportunity name
- key stakeholder names
- prior one-pagers, decks, handoff docs, QBRs, renewal notes, or proposal docs
- meeting notes from the same company or buying committee

Use Drive artifacts to avoid rebuilding context from scratch. Do not quote private docs directly into the one-pager unless the user approves.

## Research Notes Shape

Keep a compact internal evidence matrix while working:

| Fact | Source type | Confidence | Buyer-visible use |
|---|---|---|---|
| Goal or objection | Call note / Salesforce / Drive / public | High / medium / low | Visible / paraphrase / internal only |

Only buyer-visible facts should become page copy.

Before approving the brief, verify that every buyer-visible account claim has:

- a source ID
- a buyer-use rule that permits the wording
- enough confidence for the claim's strength
- no unresolved conflict

Also verify that the final brief contains exactly one buyer challenge and one desired outcome. If evidence supports several, choose the pair most relevant to the primary reader and page job rather than expanding the page.
