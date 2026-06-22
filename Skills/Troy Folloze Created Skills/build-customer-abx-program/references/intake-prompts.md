# Customer ABX Intake Prompts

Use these prompts before customer-specific work. Ask in short batches. If structured user-input tools are available, use them; otherwise ask plainly.

## Batch 1 — customer and destinations

1. What customer name and single program segment should this workbook cover?
2. Where is the customer root folder, and where should the completed workbook and supporting outputs be saved?
3. Should the final workbook be XLSX, native Google Sheets, or both?

## Batch 2 — strategy and account sources

Ask the user to paste links or paths for:

- `[CUSTOMER_STRATEGY_FOLDER]`: business priorities, annual plan, market strategy;
- `[CUSTOMER_SEGMENT_AND_ACCOUNT_FOLDER]`: ICP, account list, segment, territory, acquisition/expansion flags;
- `[CUSTOMER_INTERNAL_ENABLEMENT_FOLDER]`: messaging, playbooks, sales process, stage definitions.

Prompt:

> Please paste the folder or file locations for customer strategy, segment/account data, and internal enablement. If one does not exist, label it `NOT PROVIDED`.

## Batch 3 — content and proof sources

Ask the user to paste links or paths for:

- `[CUSTOMER_EXTERNAL_CONTENT_FOLDER]`;
- `[CUSTOMER_STORIES_FOLDER]`;
- `[CUSTOMER_PRODUCT_TECHNICAL_FOLDER]`;
- `[CUSTOMER_BRAND_FOLDER]`.

Prompt:

> Please paste the approved content, customer-proof, product/technical, and brand folder locations. Note any usage restrictions or assets that must not be used externally.

## Batch 4 — data and campaign sources

Ask the user to paste links or paths for:

- `[CUSTOMER_DATA_EXPORT_FOLDER]`: 6sense, Folloze, Salesforce, Marketo, LinkedIn, Outreach/Salesloft;
- `[CUSTOMER_EXISTING_CAMPAIGNS_FOLDER]`: boards, ads, emails, events, results;
- optional notes/call-transcript location.

Prompt:

> Please paste the platform data/export, existing campaign, and relevant meeting-notes locations. Specify the reporting date and whether the data may contain restricted personal information.

## Batch 5 — commercial assumptions

Confirm:

- target accounts;
- 12-month opportunity target;
- acquisition/expansion percentage;
- average opportunity value;
- opportunity-to-win rate;
- target contacts per account;
- regions, languages, and start date.

Prompt:

> May I use the template defaults of 500 accounts, 100 opportunities, 60% acquisition, 40% expansion, $250,000 average opportunity value, 25% win rate, and six contacts per account? Please replace any value that should differ.

## Batch 6 — systems and operating constraints

Confirm the actual platforms and owners for:

- account intelligence/orchestration;
- experience/first-party engagement;
- CRM;
- marketing automation;
- paid social;
- sales engagement;
- events/community;
- BI/reporting.

Ask for:

- suppression and consent rules;
- BDR and seller capacity;
- 24-hour response coverage;
- geography, density, timing, localization, and delivery constraints.

## Minimum-source rule

Do not infer missing customer facts from another customer. If the user directs work to continue with gaps:

- preserve the generic template guidance;
- label missing facts `[NOT PROVIDED]`;
- label decisions `[DECISION REQUIRED]`;
- separate recommendations from verified customer evidence.
