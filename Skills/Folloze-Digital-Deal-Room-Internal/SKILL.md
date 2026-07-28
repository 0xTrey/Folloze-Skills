---
name: Folloze-Digital-Deal-Room-Internal
description: Build and publish Folloze-owned digital deal rooms from internal deal context using the direct Folloze API and an approved native Folloze deal-room template. Use when Trey asks to create, push, update, or iterate a Folloze digital deal room through the API, especially when he says to use a specific Folloze template, not the MCP Save tool, and not raw HTML.
---

# Folloze Digital Deal Room Internal

Use this skill to turn Gmail, Granola, Zoom, Kaia/Outreach, Slack, Drive, and pasted deal notes into a buyer-safe Folloze-owned digital deal room, then push it into Folloze through the direct API and a native template.

This is a direct API/native-template workflow. Do not use an MCP save tool as the publishing path. The approved July 2026 template already contains two embedded HTML widgets; preserve and narrowly edit those existing widgets instead of packaging or rebuilding the room as raw HTML.

## Operating Rules

- State the working goal before material edits: account, target template, source context, repo artifact, board-create/update intent, public status, and private-note boundary.
- Start from the real source context. Use Gmail, Granola or Zoom notes, Kaia/Outreach, Slack, Drive, or pasted notes when available instead of generic account copy.
- Treat internal notes as strategy inputs. Do not expose raw meeting-note language, internal tasks, pricing commentary, budget details, personal notes, or unapproved objections in buyer-facing copy.
- Translate private deal facts into buyer-safe copy: priorities, proof needs, recommended resources, next steps, and value themes.
- Keep durable briefs, scripts, and readback notes in a git-backed repo. Do not store API tokens, cookies, auth headers, or raw sensitive exports in the skill package or repo artifacts.
- Resolve whether this is a net-new board, template duplicate, or existing-board update before writing to Folloze.
- Use Board `248623`, `Folloze Resource Center / Digital Deal Room Template - July 2026 Folloze Resource Center`, as the universal template until Trey names a replacement. Confirm `is_template: true` before copying it, and never personalize or publish the template board itself.
- Audit every copied board for inherited account residue before personalization. Preserve the copied template's structure unless this skill explicitly marks a field as personalized.
- Keep this workflow manual. Ignore Salesforce unless Trey explicitly adds it back to the workflow.
- A deal-room draft can begin as soon as the call ends. The task is not complete until the edited Kaia call recording is uploaded to Folloze as a real media content item.
- Publish to Folloze automatically after validation; seller approval is not required for publish. Never share the room with an end customer until the seller approves it.
- Prefer the direct API or approved content-upload automation for supported updates, but always use browser control for WYSIWYG-only work and final visual validation.
- Use `folloze-brand-kit` for Folloze positioning and approved buyer-facing product language when the deal room is Folloze-owned.
- Use `folloze-zoom-deal-room` for intake if the request starts from Zoom or meeting notes; this skill owns the direct API/native Folloze write path.
- Stop before publish if the account identity, template identity, or source ownership is unclear. Stop before external sharing if seller approval is unclear or missing.

## Source-To-Room Workflow

1. Gather deal context from the narrowest reliable source first.
2. Write a compact internal brief with account state, buyer goals, stakeholders, pain, proof needs, promised follow-ups, resources, decision path, and next step.
3. Separate source evidence into `buyer-safe`, `internal-only`, and `missing`.
4. Map the source context to the July template's fixed surfaces: company logo, company-name headline, call-derived hero subheader, Essentials assets, two narrow value-widget substitutions, demo examples, and the untouched ROI calculator.
5. Keep buyer copy concise and action-oriented. The room should read like a working sales room, not a transcript summary or production note.
6. Push through the direct Folloze API only after the brief and room map are coherent enough for a live board.

## Template Section Rules

Board `248623` currently uses these widget IDs. A duplicated board should retain them, but always confirm the widget type and content marker before editing:

- navigation/header shell: `w_086848fc`
- hero: `w_aa3c2917`
- Essentials: `w_da2f8d2f`
- embedded value section: `w_dacd1645`
- Example Folloze Boards: `w_0dbb4e9a`
- ROI calculator: `w_3fb95f3a`

### Section 1: Navigation And Hero

Preserve the template's navigation structure and spacing. Keep the Folloze logo, plus sign, and these two anchor tabs exactly as they are:

- `ROI Calculator` -> `roi`
- `Example Boards` -> `examples`

Replace only the generic company logo in the secondary-logo slot with the target company's approved logo. Keep the Folloze logo in the primary-logo slot. Use a transparent, high-resolution logo with enough contrast against the white navigation background, set useful alt text such as `[Company] logo`, and visually confirm that it is not clipped, stretched, or invisible. Do not rename, relink, reorder, remove, or restyle the navigation tabs unless Trey explicitly asks.

Set the header headline to this pattern:

```text
[Company Name], Welcome to Your Folloze Resource Center.
```

The company-name callout belongs in this headline, not in the navigation bar. Style the company name with the company's primary brand accent color when contrast is accessible; keep the rest of the headline in the template's existing style.

The hero subheader is the main call-derived personalization surface. Write one concise buyer-safe statement explaining how Folloze will help the company reach the goals surfaced in discovery. Match the value proposition to the company's actual priorities, motion, audience, and desired business outcome. Do not name individual buyers, sellers, or attendees, enumerate the entire call, or leave template guidance/example text visible.

Use this pattern:

```text
Explore how Folloze can help your team [company-specific goal] by [relevant Folloze value proposition and outcome].
```

For example, if call notes show that the buyer wants to scale account-based programs and prove revenue impact, the subheadline can be:

```text
Explore how Folloze can help your team scale personalized buyer engagement, improve conversion, and turn engagement into measurable pipeline impact.
```

Keep the subheader concise enough to remain a clean two- or three-line hero at the target desktop and mobile breakpoints.

### Section 2: Start With The Essentials

Board `248623` currently provides the Essentials section shell but no populated template cards. Preserve the section title exactly:

```text
Start with the Essentials
```

Populate it with the core post-call assets the buyer should open first. Keep the copied section's native layout, spacing, image treatment, and interaction pattern.

The required core set is:

1. The edited Kaia demo call recording uploaded to Folloze as an MP3 or MP4 content item.
2. Luke's account-specific follow-up deck, uploaded to Folloze as its own content item.

Add Folloze Case Studies, the Folloze MCP Launch Film, an order form, or another promised resource only when it is relevant to the call and the native layout has room. Do not treat any of those optional items as a substitute for the recording or deck.

Use accurate, asset-specific cards and previews:

- use `assets/demo-call-recording-cover.png` for the Kaia recording
- use the exported deck's own first slide when it is suitable; otherwise use `assets/presentation-deck-cover.png`
- use `assets/order-form-cover.png` only for an order form
- never reuse one stock cover for an unrelated asset type, demo example, guide, or walkthrough

For the Kaia recording:

1. Open the call in the Outreach Kaia web app and request the recording download.
2. Wait for Outreach's emailed ZIP export, then download it to the local machine.
3. Extract the MP3 or MP4 from the ZIP. Do not use the transcript as a required deliverable.
4. Remove pre-call or front-of-call chatter that is only between Folloze employees and cut other clearly useless internal opening chatter.
5. Name the finished media item using `Account Name + Folloze Demo + Recording Date`.
6. Upload the finished MP3 or MP4 as a Folloze content item. Never embed or link the Outreach/Kaia viewer as the buyer-facing asset.
7. Verify playback, title, cover, and card destination in Folloze, then delete the downloaded ZIP. Keep the edited media only as long as needed by the approved local workflow.

For Luke's deck, use the supplied deck when available. Export or prepare an approved upload format, upload it to Folloze, and attach the Folloze-hosted content item to the card instead of linking directly to Google Slides. If the deck is missing, send Luke an automated Slack request that explicitly states it is an automated message from Codex. A missing deck does not prevent the first draft, but the request must be tracked.

Do not turn this section into a generic content library. Keep only the true essentials supported by the template's native card capacity. The deal-room task remains incomplete until the edited recording is uploaded and verified.

### Section 3: Embedded Value Section

Preserve the existing `flz-13863-html-section` whose unique heading is:

```text
From brief to live campaign. In minutes, not sprints.
```

This is an approved template component, not a prompt to build a new HTML section. On Board `248623` it is widget `w_dacd1645`; on a copied board, locate it by the unique heading and widget type instead of trusting the ID alone. Assert that exactly one widget matches.

Keep the existing wrapper, CSS, responsive behavior, four-card structure, inline SVG artwork, eyebrow, main heading, cards 1, 3, and 4, and all proof lines unchanged. Do not regenerate, paste over, or rebuild the entire widget.

Make only these narrow, source-grounded text substitutions:

1. Replace the section subheader with the account's scale and cohort strategy:

```text
Scale personalized ABM across [account count or defensible range] [industry, segment, region, or cohort] accounts without creating one page for every account.
```

Use the exact account count when it was stated in the call or ABM plan. If the count is unknown, use a grounded non-numeric phrase such as `priority enterprise accounts`; never invent a number.

2. Update the account-count phrase in card 2's heading:

```text
1:1 relevance without [account count] separate pages.
```

When a number would be misleading, use:

```text
1:1 relevance without a separate page for every account.
```

Slightly adjust card 2's body only when the company's operating model requires different 1:1, 1:few, or 1:many language. Preserve its meaning, length, and proof line. Do not personalize the other three cards merely to make the section feel more bespoke.

Before saving, compare the original and edited HTML strings and reject any change outside the approved subheader and card 2 text nodes. If the widget source cannot be read or uniquely identified, stop and ask Trey for the source HTML rather than rebuilding the component.

### Section 4: Example Folloze Boards

Preserve the section title, carousel behavior, card styling, and existing curated items. Board `248623` currently contains these six baseline items in this order:

1. `Website Resource Center - Check Point Security`
2. `White Paper to Experience - Cisco`
3. `Acquisition ABM - Instructure`
4. `Field Event Promotion - Bloomreach`
5. `Expansion ABM - Aprio`
6. `Product Promotion - Lenovo`

The live template and Trey's reference screenshot say `Check Point Security`, not `Checkmarx`. Preserve the live Check Point item unless Trey explicitly requests a replacement. The screenshot shows five cards because of its viewport crop; the live template also contains Lenovo.

Add the real Folloze MCP demo examples created for the account's demo calls after the baseline items. Every added card must point to a real, verified destination and use its own accurate title and preview.

Create each new demo-example tile in the same pattern as the baseline covers:

- `1672 x 941` landscape PNG
- company logo at the top
- short motion or use-case label centered below
- account-appropriate gradient or brand color
- subtle geometric texture consistent with the existing set
- no screenshots, dense body copy, fabricated logos, or generic recording/deck artwork

Keep the source/editable asset and final PNG in the deal's git-backed repo. Use a clear filename such as `[company]-[motion]-example-tile.png`. Upload the final tile to the correct Folloze content item, then verify the carousel crop at desktop and mobile sizes.

### Section 5: ROI Calculator

Leave the ROI calculator exactly as it exists in the universal template. Do not personalize its title, copy, inputs, ranges, formulas, styling, outputs, or default assumptions. Confirm only that the untouched calculator still renders and functions after the rest of the board is edited.

## Direct API Sequence

Use existing authorized Folloze session credentials from the environment or local auth cache, but never print or commit them. Prefer the current Folloze app behavior over stale assumptions if endpoints drift.

### 1. Resolve The Native Template

List templates with:

```http
POST /api/v1/boards
Content-Type: application/json

{
  "type": 12,
  "sort_type": 3,
  "sort_direction": "desc",
  "templates_only": true,
  "per_page": 150
}
```

Select the exact requested template by name and confirm:

- `id`
- `name`
- `is_template: true`
- expected public or preview link, if present

When the user does not name another template, default to Board `248623`, `Folloze Resource Center / Digital Deal Room Template - July 2026 Folloze Resource Center`.

### 2. Create A Board From The Template

Prefer the duplicate endpoint because the native create wizard route can require CAPTCHA in non-browser API calls.

```http
POST /api/v1/boards/:templateId/copy
Content-Type: application/json

{
  "item_ids": [],
  "copy_customizations": true,
  "copy_all_items": true,
  "guid": null
}
```

If the response is `206`, read the returned `guid` and poll the same endpoint with that `guid` until the copy completes. Continue only after the response includes the new board ID.

Stop if:

- the template cannot be found with high confidence
- copy returns permission errors
- the copy job never resolves
- the returned board is still marked as a template

### 3. Update Board Metadata

Use the Prism board metadata endpoint to set the live deal-room identity:

```http
PUT /prism/:boardId
Content-Type: application/json

{
  "board": {
    "name": "...",
    "description": "...",
    "is_public": true
  }
}
```

Set the name to the account-specific deal room, not the template name. Keep descriptions buyer-safe.

### 4. Read And Modify Native Config

Read the board config:

```http
GET /api/v1/boards/:boardId/config
```

Modify `unpublished_config` by updating existing widgets and their existing fields. Preserve the template structure.

Allowed changes:

- text, headings, labels, descriptions, button copy, and links inside existing native widgets
- section ordering when the config already supports it
- image, logo, and resource references when they are approved and reachable
- native content widgets, item references, or content rows when supported by the template schema
- the approved text nodes inside the copied value-section HTML widget, under the narrow rules above

Do not add:

- new `html-section` widgets
- full-page HTML payloads
- raw custom-script widgets as the primary room body
- placeholder CTAs, fake documents, fake meeting links, or dead anchors

Board `248623` intentionally contains two existing `flz-13863-html-section` widgets:

- the value section beginning `From brief to live campaign. In minutes, not sprints.`
- the ROI calculator beginning `Estimate potential pipeline and revenue.`

Preserve both. Edit only the approved value-section text nodes, and do not change any ROI widget content.

### 5. Save The Config With A Real Hash Change

Before saving, remove transient `_widgetScripts` properties from floating widgets, widgets, ribbons, and nested widget objects if present.

Recompute the config hash the same way the Folloze designer does:

1. Create a stable JSON string of the config with object keys sorted recursively.
2. Replace `meta` with `null` before hashing.
3. Compute SHA-1 of that stable string.
4. Set `config.meta.newHash` to the new hash.
5. Set `config.meta.localSaveTime` to the current Unix epoch milliseconds.
6. Set `config.meta.currentPageName` to `default` unless editing another page.
7. Preserve the server's existing `originHash` unless the API requires a fresh value from readback.

Save with:

```http
PUT /api/v1/boards/:boardId/config
Content-Type: application/json

{
  "config": { "...": "modified native config" }
}
```

Treat `200` plus readback as success. Treat `208` as likely not persisted or unchanged hash; re-read the config, recompute the hash from the actual modified object, and retry only after confirming the intended copy is present locally.

### 6. Publish

Publish only after a successful config save:

```http
POST /api/v1/boards/:boardId/publish
```

Then read back metadata and config.

## Verification Gates

A direct API push is not done until these pass:

- Metadata readback shows the expected board name and `is_template: false`.
- Public/activation fields show the intended state, such as `is_public: true`, online activation, and a published version when publishing was requested.
- `published_config` contains the account-specific buyer copy after publish.
- `unpublished_config` and `published_config` hashes match when no unpublished changes remain.
- The config contains the two approved embedded HTML widgets from Board `248623`, with the value widget structurally unchanged outside the approved text nodes and the ROI widget's `data.content` byte-for-byte unchanged.
- No new embedded HTML widget, full-page HTML payload, or custom-script body was added.
- The config does not contain raw full-page HTML as the room body.
- The generic company logo is gone and the approved company logo renders correctly.
- The hero contains no template bracket text, example copy, attendee names, or unsupported claims.
- Essentials includes the real Folloze-hosted edited recording and deck, with correct covers and working destinations.
- The value-section subheader and card 2 account-count language agree with each other and with the sourced ABM strategy.
- The baseline example-board cards remain present in order, and each added demo example has a real destination and correctly cropped tile.
- The untouched ROI calculator still renders and calculates at its original defaults.
- The returned public link or designer link is recorded with its state.

Public Folloze links can show email verification or access gating to anonymous visitors. Do not call that a failed publish when API metadata confirms the board is public, online, and published; instead, report the gating state separately.

## Final Response

For a completed push, return:

- board ID
- template name and template ID
- public link or designer link
- source brief path, if one was created
- verification performed
- any caveats, especially visitor gating or missing resources

For a skill or workflow iteration, return:

- what changed in the skill
- where the skill lives
- validation result
- whether installed Codex skills were synced or still need reload

## Common Failure Modes

- Wrong route: using MCP Save or rebuilding the room as custom HTML when the user asked for the API/native template.
- Wrong object: editing a copied board but publishing the original template.
- Hash no-op: saving config without recomputing the designer-compatible hash, often returning `208`.
- Template drift: following the old `248319` section map or adding legacy integration, customer-story, or team sections that are not in Board `248623`.
- Broad HTML rewrite: replacing the approved value widget instead of changing only its subheader and card 2 text nodes.
- Asset mismatch: using the recording cover for a deck, order form, or demo example, or adding a new example without a matching landscape tile.
- Private leakage: copying raw call notes, internal objections, budget comments, or next-step tasks directly into buyer-facing text.
- False live claim: treating a designer URL, local file, or gated public URL as the same state as a published public board.
- Source drift: relying on old endpoint knowledge after the Folloze app bundle has changed; inspect current app behavior when API calls start failing.
