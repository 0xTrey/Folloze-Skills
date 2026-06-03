# Folloze + Marketo Embedded Form Integration Flow

Status: internal draft for team review
Date: 2026-06-02
Purpose: Example technical flow for explaining how a Marketo form integrates with a Folloze board/site and how lead, attribution, and engagement data moves through the project.

## Deliverables

- `marketo-folloze-form-flow.svg` - shareable visual diagram.
- `marketo-folloze-form-flow.png` - PNG export for Slack, docs, or slides.
- `marketo-folloze-form-flow.mmd` - editable Mermaid source for the flow.
- `README.md` - brief, assumptions, source notes, and open questions.

## Executive Summary

The embedded Marketo form path is primarily a browser-to-Marketo form submission flow. Folloze stores the Marketo form configuration, lets a board creator place that form on a board as a CTA, gated form, registration form, or form section, and renders the Marketo form on the live board.

When a visitor submits the form, Marketo receives the standard form submission and owns normal Marketo lead processing, smart campaigns, scoring, routing, and CRM sync. Folloze also receives the submitted lead identity and engagement context so the visitor can become known in Folloze reporting, Pulse, Impact Dashboard, follow-up campaigns, and optional downstream integrations.

Folloze custom attributes can enrich Marketo form submissions through the embedded form custom script. Typical examples are board-level values such as `business_unit`, `campaign_id`, or `product_line` being written into Marketo hidden fields for attribution and downstream routing.

## Recommended Diagram Stance

Use a two-layer diagram:

1. Required embedded-form runtime
2. Optional connector/API sync

This keeps the customer-facing explanation accurate. The Marketo form submit itself does not need the Folloze-Marketo API connector. The optional connector is useful when the customer also wants Folloze engagement activities, program member status, Marketo identity matching, or other configured sync behavior to flow through Marketo.

## Example Data Flow

1. Marketo Admin creates and publishes a Marketo form.
2. Marketo Admin retrieves the form embed values from Marketo: Base URL, Munchkin ID, and Form ID.
3. Folloze Company Admin adds the form under `Company Admin > Forms > Marketo` and can add an optional custom script.
4. Board creator places the Marketo form on a Folloze board as a CTA, gated form, registration form, or form section.
5. Visitor lands on the Folloze board through email, ad, direct link, or another channel.
6. The Folloze board loads the Marketo Forms 2.0 script and renders the selected Marketo form on the board.
7. Optional custom script sets hidden Marketo fields using Folloze board custom attributes or context from the URL/referrer/cookies.
8. Visitor submits the form.
9. Marketo receives the form submission and handles lead create/update, form activity, smart campaign logic, scoring, routing, and CRM sync according to the customer's Marketo configuration.
10. Folloze captures submitted identity and engagement context for reporting and follow-up.
11. Optional Folloze-Marketo Connector sends Folloze activities and/or program member statuses to Marketo when configured.
12. CRM, sales alerts, BI, and campaign attribution receive signals from Marketo, Folloze, or both depending on the implementation.

## Custom Folloze Data Examples

| Folloze source | Example Marketo target | Usage |
| --- | --- | --- |
| Board custom attribute `business_unit` | Hidden field `businessUnit` | Route leads to the correct business unit. |
| Board custom attribute `campaign_id` | Hidden field `campaignIdSFDC` | Attribute the form fill to a campaign or Salesforce campaign. |
| Board custom attribute `product_line` | Hidden field `productLine` | Segment downstream nurture or sales follow-up. |
| UTM/query/referrer context | Marketo hidden fields or Munchkin context | Preserve acquisition source and campaign attribution. |
| Submitted identity fields | Folloze lead identity | Convert unknown visitor to known lead in Folloze analytics. |
| Folloze engagement activity | Marketo custom activity or program status | Trigger nurture, scoring, or sales action based on behavior. |

## Important Technical Notes

- The visible form fields remain managed in Marketo. Changes published in Marketo are reflected when the embedded form renders in Folloze.
- Folloze stores the Marketo form embed configuration and exposes it to board creators; it is not a second form builder for those fields.
- Public help material says Folloze can auto-fill common identity fields such as first name, last name, email, company, phone, country, and state where data is available.
- Internal Marketo form enrichment material shows the custom script pattern for using Folloze board custom attributes to populate Marketo hidden fields.
- When using Marketo forms, confirm connector settings with Product/Support. The connector setup guidance notes that Folloze-to-Marketo create/update toggles may be set to `No` so the Marketo form controls net-new and existing lead processing.
- Marketo Program mapping is separate from the embedded-form submit path. If configured, a board can report visitor status to a Marketo engagement program or webinar program.
- Marketo identity matching, when enabled, is a separate enrichment process. Internal guidance describes it as a batched API-based lookup, not real-time personalization on first landing.

## Suggested Team Review Questions

- Is the customer asking only about embedded Marketo forms, or do they also need Folloze-Marketo Connector activity sync in the diagram?
- Which CRM should be shown downstream, Salesforce or another system?
- Which exact hidden fields and Folloze custom attributes are in scope for this project?
- Are they using Marketo Munchkin tracking on boards, Marketo Program mapping, or both?
- What consent/cookie manager is in the customer's environment, and does it affect lead tracking or Munchkin behavior?
- Should the external customer version include Folloze internal component names, or should it simplify to platform-level boxes?

## Sources Consulted

- Folloze Help Center: [Embedding Marketo Forms in Folloze](https://help.folloze.com/hc/en-us/articles/4402637490067-Embedding-Marketo-Forms-in-Folloze-)
- Folloze Help Center: [Folloze-Marketo Integration Overview](https://help.folloze.com/hc/en-us/articles/4402395375507-Folloze-Marketo-Integration-Overview)
- Folloze Help Center: [Folloze Forms and Marketo Integration](https://help.folloze.com/hc/en-us/articles/4402947590291-Folloze-Forms-and-Marketo-Integration)
- Google Drive: [Folloze + Marketo - Enriching Marketo Form Submissions - Technical Implementation](https://docs.google.com/document/d/1-XEcKZsbTIT78VWydAUSJIZr3yNWKaNksmIHCH8Xwfk)
- Google Drive: [Marketo Forms](https://docs.google.com/document/d/1zzW-HriptG4D9REmAbAbqxFx59TvMKaEUVakKGDzlhw)
- Google Drive/local help snapshot: [Folloze-llms-Feb2026.txt](https://drive.google.com/file/d/19lJMf5pc_i80UnhRSkFYJ4miR5p4SYtp)
