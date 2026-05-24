---
name: folloze-order-form-builder
description: Build net-new Folloze order forms for prospects and customers from the current pricing guide, prior order-form templates, package targets, add-on creators, modules, AI/Data credits, discounts, and contract terms. Use when a Folloze teammate asks to create, draft, generate, or revise an order form, quote, commercial order document, package pricing form, or multi-year customer order form.
---

# Folloze Order Form Builder

Use this skill to build a net-new Folloze order form as a native Google Doc. The output should be a customer-ready draft that follows the current order-form template, preserves legal appendices, and clearly shows package pricing, add-on line items, discounts, annual totals, and contract details.

## Output Contract

Create a new Google Doc order form. Never overwrite a source template or a previous customer order form unless the user explicitly asks to edit that exact document.

The final order form must include:

- prepared date and expiration date
- customer details table
- Folloze account manager table
- order-form summary table
- line items for package, customer success, onboarding, additional creators, modules, AI/Data credits, and other add-ons as applicable
- discounts that reconcile exactly to the requested annual price points
- contract details table with start date, end date, duration, and payment terms
- applicable agreement language and signature blocks
- MSA, support, DPA, subprocessors, and AI terms appendices from the chosen template when the template includes them

## Source Priority

Use sources in this order:

1. User-provided instructions in the current conversation.
2. User-provided pricing-guide, template, or prior-order-form links.
3. Current Folloze pricing guide in Drive, if the user did not provide one: `https://docs.google.com/presentation/d/1QzO5UjWo-Z62qKeg8QFP6NvSSDqhhfYogJJgYkD1MfY/edit`
4. Current full native Google Doc template, if the user did not provide one: `https://docs.google.com/document/d/1-6kyilfoeIbr_u0i476V2KGHF24r7RVJhLMlJFqKxac/edit`
5. Secondary prior DOCX template for alternate wording or redline examples: `https://docs.google.com/document/d/1DEdpK4aIXeBJ8CRRzoTJFHm54q5zaYww/edit`

Always fetch the live pricing guide and template content before building. Treat static prices in this skill as a cross-check, not as the source of truth.

## Current Pricing Cross-Check

Use these values only after confirming the current pricing guide still matches:

| Item | Price |
|---|---:|
| Starter package | $19,995 |
| Professional package | $39,995 |
| Premium package | $69,995 |
| Enterprise package | $89,995 |
| Bronze Customer Success | $10,000 |
| Silver Customer Success | $20,000 |
| Gold Customer Success | $50,000 |
| Sales Enablement module | $15,000 |
| Website Engagement module | $15,000 |
| Events module | $15,000 |
| Additional Creator | $3,300 |
| Additional Collaborator | $950 |
| 250 AI/Data credits | $1,000 |
| 1,000 AI/Data credits | $3,000 |
| 2,500 AI/Data credits | $6,250 |
| 5,000 AI/Data credits | $10,000 |

Package entitlements from the current pricing guide, if still current:

| Package | Users Included | AI/Data Credits Included | Modules Included |
|---|---:|---:|---|
| Starter | 2 | 250 | ABX |
| Professional | 4 | 1,000 | ABX + Events |
| Premium | 8 | 2,000 | ABX + Events + Website Engagement |
| Enterprise | 12 | 5,000 | ABX + Events + Website Engagement + Sales Enablement |

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

## Build Workflow

### 1. State the working goal

Before material edits, state the goal in plain language:

- customer-visible output
- selected template or source document
- price targets
- term
- add-ons and discount treatment
- verification plan

### 2. Fetch and sample sources

Use Google Drive/Docs/Slides connector tools to fetch:

- the pricing guide text or slide data
- the primary order-form template text and tables
- any secondary template the user provided

For native Google Docs, use connector readback for structure. For Office-format files in Drive, use Drive fetch/export.

### 3. Build the commercial model

Create the math before editing the document.

Use this model:

1. `package_line_price = selected_package_price + selected_customer_success_price`, unless the template separates Customer Success into its own line.
2. `additional_creators = requested_total_creators - included_package_creators`, unless the user directly says the extra creator count.
3. `additional_credit_line_price = selected_credit_tier_price`.
4. Year 1 pre-discount total includes annual package, annual add-ons, and one-time fees.
5. Year 2+ pre-discount total includes annual package and annual add-ons, excluding one-time fees unless the user says otherwise.
6. Zero-discount add-on lines first when the user requests that treatment.
7. Discount the package line by year so each annual total equals the requested target.
8. Total-row discount must equal `pre_discount_total - target_annual_fee`.

Reject or question the math if:

- a requested target cannot be reached with the specified zeroed add-ons and package discount
- the user says "total credits" but it is unclear whether they mean total entitlement or credits in addition to package inclusion
- package/customer-success inclusion is ambiguous enough to materially change the discount

### 4. Draft the order form

Use the existing order-form table shape unless the user asks for a new format.

Recommended order-form summary columns:

| Folloze Package | Price | Quantity | Total | Discount | Discounted Annual Total |

For each add-on the user wants included but free, show:

- list price
- quantity
- total
- discount equal to total
- discounted annual total of `$0`

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
- each requested add-on appears as its own line item
- each zeroed add-on has discount equal to its line total and `$0` discounted annual total
- year-by-year totals equal the user-requested price points
- total contract value is correct
- legal appendices and AI terms remain present when expected
- connector readback can see the key tables and terms
- PDF export visual QA is completed when available; otherwise state that rendered page fit was not verified

## Worked Example: Aprio

User request:

- 2-year deal
- Year 1: `$50,000`
- Year 2: `$70,000`
- Premium package
- 16 total Creators, which means 8 additional Creators beyond Premium's 8 included users
- 1,000 additional AI/Data credits
- show additional Creators and credits as line items and discount them to zero
- discount the package to reach target annual fees

Commercial model:

| Line | List price | Quantity | Year 1 treatment | Year 2 treatment |
|---|---:|---:|---:|---:|
| Premium + Bronze Customer Success | $79,995 | 1 | discount `$29,995`, net `$50,000` | discount `$9,995`, net `$70,000` |
| Additional Creator(s) | $3,300 | 8 | discount `$26,400`, net `$0` | discount `$26,400`, net `$0` |
| Additional AI/Data Credits - 1,000 | $3,000 | 1 | discount `$3,000`, net `$0` | discount `$3,000`, net `$0` |
| Onboarding & Implementation | $10,000 | 1 | discount `$10,000`, net `$0` | excluded unless recurring |

Totals:

| Year | Pre-discount total | Total discount | Net total |
|---|---:|---:|---:|
| Year 1 | $119,395 | $69,395 | $50,000 |
| Year 2 | $109,395 | $39,395 | $70,000 |

## Final Response

Keep the close-out short:

- Google Doc link
- commercial summary
- unresolved blanks or assumptions
- verification completed

Do not include local scratch paths after successful Google Doc import.
