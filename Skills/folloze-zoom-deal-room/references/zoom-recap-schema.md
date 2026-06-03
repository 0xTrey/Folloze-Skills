# Zoom Recap Intake Schema

Use this schema to normalize Zoom AI summaries, pasted call notes, and meeting-assets emails.

## Intake Object

```yaml
source:
  type: gmail_zoom_assets | pasted_notes | transcript | calendar_notes | other
  subject:
  sent_at:
  meeting_date:
  source_link_internal_only:
  confidence: confirmed | likely | unclear | missing

account_resolution:
  account_name:
  website_or_domain:
  salesforce_account_id:
  salesforce_opportunity_id:
  owner:
  confidence: confirmed | likely | unclear | missing
  conflicts:

meeting_context:
  meeting_name:
  attendees:
  absent_stakeholders:
  next_meeting:
    date:
    time:
    timezone:
    attendees_needed:
  summary:

buyer_context:
  business_goal:
  current_workflow:
  incumbent_tools:
  event_or_campaign_context:
  success_criteria:
  proof_needed:

deal_context:
  pains:
  objections:
  commercial_notes_internal_only:
  package_direction_internal_only:
  decision_process:
  timeline:
  risks:

follow_ups:
  seller_tasks:
  buyer_tasks:
  shared_tasks:
  required_resources:
  security_or_legal_items:
  proposal_items:

deal_room_plan:
  recommended_route: mcp_rich_html | api_template_board | brief_only
  brand_owner: folloze_owned | vendor_owned | account_owned | unclear
  audience:
  sections:
  ctas:
  save_readiness: ready | blocked | needs_review
  blockers:
```

## Confidence Rules

- `confirmed`: explicitly present in the source or verified in Salesforce/public source.
- `likely`: strongly inferred from source wording, but not directly named.
- `unclear`: possible, but ambiguous enough to avoid visible claims.
- `missing`: required for save/build but absent from current evidence.

## Minimum Fields Before Live Save

Do not save a live Folloze board until these are resolved:

- account name or intended audience
- brand owner: Folloze-owned sales room versus vendor-owned page
- next external CTA
- at least three real resource items or in-page content modules
- owner of the next meeting or follow-up motion
- whether MCP theme mode is authorized

## Common Zoom Recap Signals

| Signal in recap | Deal-room implication |
| --- | --- |
| `share with internal team` | Add a team-review section and role-specific proof paths. |
| `review budget` | Add a focused launch path and value-proof section. |
| `send proposal` | Add a proposal-summary module and commercial next step. |
| `MSA` or `infosec` | Add security/legal readiness resources. |
| `current tool` or `integration` | Add workflow-fit and integration section. |
| `meet in two weeks` | Add a mutual action plan with the next meeting date. |
| `examples` | Add curated example cards with real links or modal summaries. |
| `event` | Add pre-event, live-event, and post-event follow-up journey. |
