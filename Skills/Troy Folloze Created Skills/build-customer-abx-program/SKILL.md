---
name: build-customer-abx-program
description: Build a customer-specific 12-month ABX strategy and implementation workbook from the Folloze Academy ABX Blueprint, a reusable walkthrough, and customer source folders. Use when a user asks to replicate the ABX program for another customer; create or update an ABX blueprint; target a defined account segment; plan acquisition and expansion campaigns; produce personas, content, channels, Folloze boards, ads, BDR/Marketo sequences, prompts, opportunity pacing, routing rules, measurement, or Crawl-Walk-Run guidance; or convert customer files into the reusable ABX workbook format.
---

# Build a Customer ABX Program

Create a governed customer-specific ABX workbook from the bundled guide, workbook template, and user-supplied source locations.

## Required resources

- Use `assets/Reusable_Customer_ABX_Program_Workbook.xlsx` as the output structure and visual template.
- Use `assets/Customer_ABX_Program_Replication_Walkthrough.docx` as the process guide.
- Read `references/intake-prompts.md` before asking for sources or assumptions.
- Read `references/workbook-contract.md` before building or editing the workbook.
- Read `references/operating-model.md` before drafting strategy, routing, campaigns, sequences, or measurement.

Never modify the bundled assets. Copy them to the approved output location first.

## Workflow

### 1. Establish the engagement

Confirm:

- customer name and one program segment;
- whether this is a new program, a revision, or a comparison;
- desired output location and whether the final workbook should be XLSX, native Google Sheets, or both;
- account and opportunity goals, defaulting to 500 accounts and 100 opportunities only when the user approves the template defaults.

### 2. Run mandatory source-location intake

Use the prompts in `references/intake-prompts.md`. Ask in short batches and wait for answers.

Do not start customer-specific synthesis until the user has supplied:

- a customer root or explicit source locations;
- strategy/segment/account sources;
- approved content/proof/product/brand sources, or an explicit statement that one is unavailable;
- platform data/export locations, or an explicit statement that they are unavailable;
- an output location.

Record unavailable sources as `[NOT PROVIDED]`; never invent their contents.

### 3. Audit sources

Create a source register before writing strategy:

- source location and owner;
- freshness;
- approved use;
- reusable methodology versus customer-specific fact;
- conflicts, gaps, and decisions;
- citations or exact file locations for claims and proof.

Exclude other customers' names, metrics, claims, personas, capacity constraints, and content unless the user explicitly authorizes them as examples.

### 4. Run the decision workshop

Resolve the assumptions in the Program Inputs tab:

- customer, segment, regions, languages;
- target accounts and opportunity target;
- acquisition/expansion mix;
- average opportunity value and win-rate assumption;
- personas and target contacts per account;
- delivery capacity by geography, density, and timing;
- systems, ownership, suppression, consent, and service levels.

Mark unresolved decisions with `[DECISION REQUIRED: owner / due date]`.

### 5. Build the customer workbook

Copy the template, preserve its tab names and formulas, and complete all relevant tabs:

1. How to Use
2. Program Inputs
3. ABX Blueprint
4. Alignment
5. Experience
6. Engagement
7. Signals & Routing
8. Campaign Calendar
9. Persona & Content
10. Commercial Model
11. Sequence Library
12. Prompt Library
13. Measurement
14. Source Files

Preserve the stage-by-stage matrix and the visual roles of purple pillar cells, navy headers, pink active-channel cells, yellow inputs, and green calculated outputs.

### 6. Make the program executable

Populate:

- acquisition and expansion campaigns;
- personas, buyer jobs, content, CTAs, and Folloze experiences by stage;
- channel roles and timing;
- exact upgrade/downgrade logic;
- the verified 24-hour surge-response workflow;
- example BDR and Marketo sequences;
- customer-ready prompts for Folloze boards, LinkedIn ads, sequences, campaign briefs, and optimization;
- monthly opportunity pacing and value;
- required outputs from 6sense, Folloze, Salesforce, Marketo, LinkedIn, and Outreach/Salesloft;
- Crawl-Walk-Run goals and exit gates.

### 7. Validate

Before delivery:

- scan formulas for `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, and `#N/A`;
- confirm monthly opportunities equal the annual target;
- confirm acquisition plus expansion equals 100%;
- confirm stage and opportunity values reconcile with inputs;
- confirm no unrelated customer names remain;
- confirm source claims are traceable;
- confirm every tab is legible and unclipped;
- confirm intent-only outreach is prohibited;
- confirm surge routing includes fit, ownership, capacity, suppression, and first-party corroboration.

### 8. Deliver

Prefer a native Google Sheet when the user supplies a Drive destination and the connector is available. Otherwise deliver the verified XLSX.

Return:

- the customer-specific workbook;
- the source register and unresolved decision list;
- a concise summary of assumptions and validation;
- the companion walkthrough only when requested or materially updated.

## Boundaries

- Do not contact buyers, enroll people in live campaigns, alter CRM records, or publish Folloze boards without explicit authorization.
- Do not treat anonymous intent as buyer consent or sufficient outreach evidence.
- Do not expose tracking or surveillance language in buyer-facing copy.
- Do not present value hypotheses as CRM pipeline.
- Do not fabricate customer proof, performance claims, personas, capacity, or system outputs.
