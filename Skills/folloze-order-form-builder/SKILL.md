---
name: folloze-order-form-builder
description: Build net-new Folloze order forms for prospects and customers from the current pricing guide, prior order-form templates, package targets, add-on creators, modules, AI/Data credits, discounts, and contract terms. Use when a Folloze teammate asks to create, draft, generate, or revise an order form, quote, commercial order document, package pricing form, or multi-year customer order form.
---

# Folloze Order Form Builder

Use this skill to build a net-new Folloze order form as a native Google Doc. The output should be a customer-ready draft that follows the current order-form template, preserves legal appendices, and clearly shows package pricing, add-on line items, discounts, annual totals, and contract details.

## Output Contract

Create a new Google Doc order form. Never overwrite a source template or a previous customer order form unless the user explicitly asks to edit that exact document.

Keep this skill reusable and internal. Do not add real customer names, real order-form links, customer-specific target prices, customer-specific discounts, signature details, contact details, or negotiated commercial terms to the skill itself. When a real deal teaches a useful pattern, abstract it into placeholders, formulas, and generic examples.

The final order form must include:

- prepared date and expiration date
- customer details table
- Folloze account manager table
- order-form summary table
- line items for package, customer success, onboarding, additional creators, modules, AI/Data credits, and other add-ons as applicable
- discounts that reconcile exactly to the requested annual price points
- contract details table with start date, end date, duration, and payment terms
- applicable agreement language that matches the contract-details term length, plus signature blocks
- MSA, support, DPA, subprocessors, and AI terms appendices from the chosen template when the template includes them

## Source Priority

Use sources in this order:

1. User-provided instructions in the current conversation.
2. User-provided pricing-guide, template, or prior-order-form links.
3. The local private pricing and terms reference, resolved from `FOLLOZE_ORDER_FORM_PRICING_PATH` when set.
4. The repo-local private fallback at `private/pricing/folloze-order-form-pricing.md` when present.
5. User-provided customer-specific agreement language or customer-specific commercial instructions.

Never store live pricing-guide URLs, order-form template URLs, exact package prices, package entitlements, renewal percentages, customer-specific targets, customer-specific discounts, or negotiated commercial terms in this shared skill file.

Always load the current private pricing reference before building. If no private reference or user-provided pricing source is available, stop and ask for an approved current pricing guide, order-form template, or local private reference path.

For plain-language explanations of package rows, modules, user roles, Global Scalability, Website Engagement, Events, and Folloze AI/Data credits, use `folloze-brand-kit` `references/product-capabilities-internal.md`. The live pricing guide, order form, and user-provided commercial instructions still outrank the capability reference for actual prices, quantities, and contracted terms.

## Private Pricing And Terms Reference

Use the private reference for:

- current pricing-guide and order-form template links
- package list prices
- customer success tiers
- module and add-on prices
- AI/Data credit tiers
- package entitlements and package-row inclusion copy
- standard applicable agreement language
- term-length wording rules
- renewal, overage, and auto-upgrade clauses

## Inputs To Resolve

Infer what is clear from the user. Ask concise questions only for facts that are necessary and cannot be safely inferred.

Required or strongly preferred:

- customer legal name
- customer address
- primary contact name and email
- payer contact name, email, phone, and address if available
- selected package
- customer success tier
- term length
- start date, end date, prepared date, and expiration date
- year-by-year target annual fees
- included and additional creators, collaborators, modules, and AI/Data credits
- onboarding or implementation fee treatment
- payment terms
- whether to use the standard MSA or a customer-specific agreement

If legal name, address, or contacts are missing:

- Use official public sources for legal name/address only when needed and cite them in the final response.
- Leave contact fields blank instead of inventing names, emails, or phone numbers.
- State unresolved blanks in the final response.

## Applicable Agreement Language

Load standard applicable agreement language and term-length rules from the private pricing and terms reference, unless the user provides customer-specific agreement language. Preserve customer-specific language when supplied and still verify that the term length matches the contract details table.

Do not hardcode renewal percentages, overage thresholds, auto-upgrade clauses, or standard legal language in this shared skill. Those belong in the private reference or in the user-provided customer-specific source.

## Build Workflow

### 1. State the working goal

Before material edits, state the goal in plain language:

- customer-visible output
- selected template or source document
- price targets
- term
- add-ons and discount treatment
- applicable agreement term wording
- verification plan

### 2. Fetch and sample sources

Use Google Drive/Docs/Slides connector tools to fetch:

- the pricing guide text or slide data from the private reference or user-provided source
- the primary order-form template text and tables from the private reference or user-provided source
- any secondary template the private reference or user provided

For native Google Docs, use connector readback for structure. For Office-format files in Drive, use Drive fetch/export.

### 3. Build the commercial model

Create the math before editing the document.

Use this model:

1. Decide whether Customer Success is bundled into the package row or shown as a separate line. The current preferred table shape shows Customer Success as its own row, usually discounted to `$0` when included commercially.
2. `additional_creators = requested_total_creators - included_package_creators`, unless the user directly says the extra creator count.
3. `additional_credit_line_price = selected_credit_tier_price`.
4. Year 1 pre-discount total includes annual package, annual add-ons, and one-time fees.
5. Year 2+ pre-discount total includes annual package and annual add-ons, excluding one-time fees unless the user says otherwise.
6. Zero-discount add-on lines first when the user requests that treatment.
7. Discount the package line by year so each annual total equals the requested target.
8. Total-row discount must equal `pre_discount_total - target_annual_fee`.

Do not double-count Customer Success. If the package row price already includes the Customer Success tier, either make the Customer Success row disclosure-only and keep it out of calculated totals, or reduce the package row to the platform/package price and count the Customer Success row normally. The visible total rows must reconcile to the calculation model. If a row is disclosure-only because it is already included in another line, label it clearly as included or disclosure-only.

Reject or question the math if:

- a requested target cannot be reached with the specified zeroed add-ons and package discount
- the user says "total credits" but it is unclear whether they mean total entitlement or credits in addition to package inclusion
- package/customer-success inclusion is ambiguous enough to materially change the discount

### 4. Draft the order form

Use the existing order-form table shape unless the user asks for a new format.

Recommended order-form summary columns:

| Folloze Package | Price | Quantity | Total | Discount | Discounted Annual Total |

The first commercial row should be the selected package row. In the `Folloze Package` cell, use this pattern:

```text
Premium Package
    - ABX, Events, Website Engagement
    - Account & Contact Intelligence
    - Content Engine
    - Integrations
    - Global Scalability (SSO, DWH, DAM & Localization)
    - 8 Creators included;
    - 2,000 AI/Data Credits
```

Adapt the included bullets to the selected package using the package-row inclusion copy above. Do not list separately priced add-ons as included package scope. If a separately priced add-on is included for free, keep it as its own line item and discount that row to `$0`.

For each add-on the user wants included but free, show:

- list price
- quantity
- total
- discount equal to total
- discounted annual total of `$0`

Use this row order unless the user or template requires otherwise:

1. selected package row with included package bullets
2. customer success tier
3. additional creators
4. additional collaborators, if any
5. additional AI/Data credits
6. additional modules, if any
7. onboarding and implementation
8. discounted annual total rows
9. discount and custom packaging note

For multi-year targets, show either:

- package row with year-specific package discounts and year-specific discounted annual totals, plus annual total rows, or
- separate year rows if the template supports them cleanly

Do not hide the add-ons inside package description when the user asked for them as line items.

### 5. Create the Google Doc

Preferred path for a net-new final Google Doc:

1. Export or fetch the chosen template as DOCX when needed.
2. Build a local DOCX in scratch space using the template structure.
3. Sanitize Google Docs title residue before import.
4. Import the DOCX as a native Google Doc with Drive conversion.
5. Re-read the imported Google Doc with the connector.

If a direct Google Doc copy tool is available and preserves the source formatting better, copy the template first and edit the copy. Still never edit the source template.

### 6. Verify

Before final handoff, verify:

- title and Google Doc URL
- customer name is correct in customer details, agreement opening, and signature block
- no old customer name remains in the commercial front matter
- prepared, expiration, start, and end dates are correct
- term duration matches dates
- applicable agreement language is present and uses the same term length as the contract details table
- standard two-year language uses `twenty-four (24)` months unless the user requested a different term
- package row includes the selected package's included modules, platform capabilities, included creators, and included AI/Data credits
- package row does not hide separately priced add-ons that should be their own line items
- each requested add-on appears as its own line item
- each zeroed add-on has discount equal to its line total and `$0` discounted annual total
- year-by-year totals equal the user-requested price points
- total contract value is correct
- visible total rows reconcile to the calculation model, including any separate or disclosure-only Customer Success treatment
- legal appendices and AI terms remain present when expected
- connector readback can see the key tables and terms
- PDF export visual QA is completed when available; otherwise state that rendered page fit was not verified

## Reusable Commercial Pattern

Use this pattern when a user asks for a multi-year package deal with additional creators or AI/Data credits shown as separate line items and discounted to `$0`.

Inputs:

- `PACKAGE_NAME`
- `PACKAGE_LIST_PRICE`
- `PACKAGE_INCLUDED_CREATORS`
- `PACKAGE_INCLUDED_AI_DATA_CREDITS`
- `CUSTOMER_SUCCESS_TIER`
- `CUSTOMER_SUCCESS_LIST_PRICE`
- `TOTAL_CREATORS_REQUESTED`
- `ADDITIONAL_CREATORS_REQUESTED`
- `ADDITIONAL_CREATOR_UNIT_PRICE`
- `ADDITIONAL_AI_DATA_CREDIT_TIER`
- `ADDITIONAL_AI_DATA_CREDIT_PRICE`
- `ONBOARDING_PRICE`
- `YEAR_1_TARGET`
- `YEAR_2_TARGET`
- `TERM_MONTHS`
- `EXECUTION_DEADLINE`

Derived values:

- `ADDITIONAL_CREATORS_REQUESTED = TOTAL_CREATORS_REQUESTED - PACKAGE_INCLUDED_CREATORS`, unless the user directly specifies the additional creator count.
- `ADDITIONAL_CREATORS_TOTAL = ADDITIONAL_CREATORS_REQUESTED * ADDITIONAL_CREATOR_UNIT_PRICE`.
- `YEAR_1_PRE_DISCOUNT_TOTAL = PACKAGE_LIST_PRICE + ADDITIONAL_CREATORS_TOTAL + ADDITIONAL_AI_DATA_CREDIT_PRICE + ONBOARDING_PRICE`, plus Customer Success only if it is additive rather than included/disclosure-only.
- `YEAR_2_PRE_DISCOUNT_TOTAL = PACKAGE_LIST_PRICE + ADDITIONAL_CREATORS_TOTAL + ADDITIONAL_AI_DATA_CREDIT_PRICE`, plus Customer Success only if it is additive rather than included/disclosure-only.
- `YEAR_1_TOTAL_DISCOUNT = YEAR_1_PRE_DISCOUNT_TOTAL - YEAR_1_TARGET`.
- `YEAR_2_TOTAL_DISCOUNT = YEAR_2_PRE_DISCOUNT_TOTAL - YEAR_2_TARGET`.
- `TOTAL_CONTRACT_VALUE = sum of all annual target fees across the term`.

Commercial model:

| Line | List price | Quantity | Year 1 treatment | Year 2 treatment |
|---|---:|---:|---|---|
| `PACKAGE_NAME` | `PACKAGE_LIST_PRICE` | 1 | package discount needed to reach `YEAR_1_TARGET` after zeroed add-ons | package discount needed to reach `YEAR_2_TARGET` after zeroed add-ons |
| `CUSTOMER_SUCCESS_TIER` | `CUSTOMER_SUCCESS_LIST_PRICE` | 1 | discount to `$0` when commercially included, or label as included/disclosure-only when already included in the package row | discount to `$0` when commercially included, or label as included/disclosure-only when already included in the package row |
| Additional Creator(s) | `ADDITIONAL_CREATOR_UNIT_PRICE` | `ADDITIONAL_CREATORS_REQUESTED` | discount `ADDITIONAL_CREATORS_TOTAL` to `$0` | discount `ADDITIONAL_CREATORS_TOTAL` to `$0` |
| Additional AI/Data Credits - `ADDITIONAL_AI_DATA_CREDIT_TIER` | `ADDITIONAL_AI_DATA_CREDIT_PRICE` | 1 | discount to `$0` | discount to `$0` |
| Onboarding & Implementation (One Time) | `ONBOARDING_PRICE` | 1 | discount to `$0` when waived | excluded unless recurring |

Use summary rows named `Discounted Year 1 Total`, `Discounted Year 2 Total`, and additional year rows as needed. In the discount column, include the approximate discount percentage before the discount amount when helpful, such as `~NN% ($DISCOUNT_AMOUNT)`.

Add a note below the table in this form:

```text
Discounts and Custom Packaging are based on a {{TERM_LABEL}} agreement executed by {{EXECUTION_DEADLINE}}. Year 1 annual fee is {{YEAR_1_TARGET}}; Year 2 annual fee is {{YEAR_2_TARGET}}. Total Contract Value: {{TOTAL_CONTRACT_VALUE}}.
```

For one-year or three-year/custom terms, adjust the annual-fee sentence so it lists only the years included in the contract details table.

## Final Response

Keep the close-out short:

- Google Doc link
- commercial summary
- unresolved blanks or assumptions
- verification completed

Do not include local scratch paths after successful Google Doc import.
