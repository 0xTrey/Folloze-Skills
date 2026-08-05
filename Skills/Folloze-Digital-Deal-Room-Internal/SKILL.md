---
name: folloze-digital-deal-room-internal
description: Manually build and publish Folloze-owned digital deal rooms from Granola or a supplied Kaia/local transcript, a local or Kaia-exported recording, and internal deal context using the direct Folloze API and an approved native Folloze template. Use when Trey or Luke asks to create, push, update, or iterate an internal Folloze deal room; personalize the fixed speed/scale, personalization/enrichment, and analytics/optimization value cards; conditionally include external-AI openness; process a supplied recording; or fall back to Kaia browser export when local media is absent. Do not use MCP Save or raw HTML.
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
- Keep this workflow manual. Do not queue or invoke it from the paused `folloze-post-intro-dsr-automation`, Hermes, or a LaunchAgent. Start only from Trey or Luke's explicit manual request with the account and source context.
- Identify the operator before intake. For Trey-run rooms, use the matching Granola meeting transcript/notes first and materialize a temporary readable local transcript for evidence mapping and clipping. For Luke-run rooms, inspect the explicitly supplied Kaia download/email package first for both the transcript and recording. Prefer valid local media and never open Kaia, email, or browser automation when the local package is complete. Use Kaia/Outreach browser automation only when a required local asset is absent and fallback is authorized. If a supplied local file is corrupt, incomplete, or belongs to the wrong meeting, stop instead of silently falling back. Follow [references/recording-transcript-intake.md](references/recording-transcript-intake.md) completely.
- A deal-room draft can begin as soon as the call ends. The task is not complete until the verified local or Kaia-exported call recording is processed according to the clip decision and uploaded to Folloze as a real media content item.
- Publish to Folloze automatically after validation; seller approval is not required for this internal published state. A published public URL must not be attached to a campaign, sent, or otherwise exposed to a customer until the seller approves it. Never treat URL existence as customer sharing approval.
- For Luke-owned opportunities, invite **Luke Rafferty** as a board **Editor** after the board exists and before declaring it ready for review. Trey has confirmed `luke@folloze.com` as Luke's expected Folloze login, so normalize and use that email for the lookup while still resolving Luke's stable current organization user/invite ID from the authoritative application response. Verify the stable identity, normalized email, and Luke's display name in the board Editors readback; an email match, search result, invite request, or success toast alone is not sufficient evidence.
- Treat publishing, editor verification, seller-review notification, and customer-share approval as separate states. Publishing never implies that Luke approved customer sharing.
- Prefer the direct API or approved content-upload automation for supported updates, but always use browser control for WYSIWYG-only work and final visual validation.
- Use `folloze-brand-kit` for Folloze positioning and approved buyer-facing product language when the deal room is Folloze-owned.
- Use `folloze-zoom-deal-room` for intake if the request starts from Zoom or meeting notes; this skill owns the direct API/native Folloze write path.
- Stop before publish if the account identity, template identity, or source ownership is unclear. Stop before external sharing if seller approval is unclear or missing.

## Production Speed Contract

Treat this as a production workflow, not an integration-debugging session. Read and follow [references/production-fast-path.md](references/production-fast-path.md) completely before starting a board run. Validate package releases against [references/fast-path-acceptance.md](references/fast-path-acceptance.md).

- Classify the preflight result as `fast_ready`, `standard_ready`, or `blocked`. Target `fast_ready` at no more than 300 seconds, `standard_ready` at no more than 480 seconds, and require every `blocked` or exception run to return a truthful result by 600 seconds.
- Target a normal warmed-path runtime of **5–8 minutes** from invocation to `review_notified`. The hard production ceiling is **10 minutes**, including external service waits.
- A sub-five-minute result is a stretch target, not a guarantee. Claim it only when all inputs are locally available or already resolved, the recording cut finishes inside the media budget, the Folloze Experience API is healthy, and the authenticated board-editor invitation path is preflighted.
- Run one preflight before any board copy or mutation. It must validate the input package, transcript and recording, deck, Salesforce Opportunity ID or prototype override, template identity, Experience API token, tracker and tile-library access, account brand inputs, editor-invite readiness, Slack delivery readiness, required local tools, output repo, and time budget. Access-token expiry is normal: first call the selected Folloze MCP profile's refresh-capable `auth_login` with `force=false`, then run the compact template readback using the refreshed cache. A stored refresh token must prevent an expired access token from becoming a manual-login blocker; open interactive authentication only when the refresh grant itself fails.
- If app/editor authentication, source ownership, required assets, or connector access fails preflight, stop within 60 seconds with one actionable blocker. Do not create a board and then investigate authentication.
- Resolve independent inputs concurrently: package/media inspection, transcript evidence mapping, deck lookup, tracker rows, Drive tiles, brand inputs, template/auth readback, and seller identity. Do not perform those lookups serially when they have no dependency.
- Use one account-neutral runner and a structured run specification. Do not write or adapt an account-specific production script during the timed run.
- Use one bounded final verifier after publish. It may perform compact metadata/config/item/editor readbacks, one authenticated desktop visual pass, one mobile value-section pass, media playback/endpoint verification, tracker readback, and Slack readback. Do not repeat successful gates without contrary evidence.
- Cap browser fallback or WYSIWYG exception handling at 60 seconds. Never download app bundles, inspect source maps, discover endpoints, repair OAuth, or debug browser extensions during the production clock. Record the highest verified nonterminal state and move the investigation to a separate task.
- Keep connector and API responses field-scoped. Read only the tracker header plus selected rows, selected Drive files, and the board/config fields required by the receipt. Never print full configs, full organization responses, unbounded sheet ranges, tokens, cookies, or source maps.
- Target no more than **100,000 model tokens** for a normal run and treat **150,000 tokens** as a hard diagnostic ceiling. When the runtime can expose token usage, record input, cached-input, and output tokens. Otherwise record `token_usage_available=false`; never invent usage.
- Record stage timings, total elapsed time, token usage availability, and an estimated cost only when a defensible model/rate basis is available. Otherwise return `cost_estimate_usd=null` with the missing basis.
- At 10 minutes, stop work, emit the highest verified workflow state plus blockers, and do not continue exploring. A timeout is not success, but it must be bounded and diagnosable.
- At 480 seconds, start no new discovery. At 540 seconds, start no new retry. At 600 seconds, emit the machine result immediately.

Use these stage budgets:

| Stage | Target ceiling |
| --- | ---: |
| Preflight | 45 seconds |
| Transcript/evidence and asset resolution | 75 seconds |
| Media edit and upload preparation | 120 seconds |
| Board copy, mutation, asset upload, vanity, and publish | 120 seconds |
| Bounded verification, editor invite, tracker, and Slack | 90 seconds |
| Contingency reserve | 150 seconds |

The stage ceilings are diagnostic budgets, not mandatory waits. Start independent stages together when safe and finish as soon as their gates pass.

## Mandatory Preflight

Complete preflight before copying or mutating a board. It must return one compact record with `runtime_profile`, elapsed time, every gate, and blockers.

Require:

- exact operator, account, meeting, Salesforce Opportunity ID or explicit prototype override
- exactly one authoritative transcript and recording with meeting-match evidence
- required deck and covers, or the explicitly allowed pending behavior
- tracker metadata/header access plus exact candidate account rows
- shared Drive folder access plus exact required tiles and upload permission when needed
- valid Experience API authentication after a non-forced refresh-capable auth warmup, exact template `248623`, config/hash access, and preferred vanity availability
- authenticated designer/preview access and a known invitation-capable app/API path
- Luke Rafferty's exact current organization user/invite identity, using normalized `luke@folloze.com` as the expected login and requiring stable-ID plus display-name readback
- resolvable Slack recipient and usable Slack delivery connector
- brand logo/accent sources, media tools, reusable runner, bounded verifier, output repo, and 600-second deadline

Default `publish_without_editor=false`. If editor invitation capability is missing, stop before board copy. An explicit draft-only override may proceed no farther than `published_internal`, must report `editor_pending`, and must suppress the Slack completion handoff.

Do not broadly scan Gmail, Drive, Downloads, the home directory, or an entire spreadsheet during preflight. Use only the named package/source and bounded source queries.

## Bundled Fast-Path Tools

Use the bundled tools instead of creating an account-specific production script:

- `scripts/fast_path_preflight.js` validates the materialized package, deck, media, local dependencies, auth cache, optional template readback, editor readiness, and tracker/Drive example manifest. It is read-only by default, probes the exact ZIP media entry through a cleaned temporary file, and emits `fast_ready`, `standard_ready`, or `blocked`.
- `scripts/fast_path_orchestrator.js` executes an account-neutral adapter specification with real parallel groups, idempotent resume state, at most one targeted retry, explicit external-write authorization, 480/540/600-second deadlines, compact output hashes, and exactly one final-verifier stage. Dry-run is the default.
- `scripts/verify_deal_room_receipt.js` validates the compact adapter-produced board receipt and emits the required `DSR_VERIFY_JSON_END` marker. It checks publication, hashes, HTML/ROI integrity, Essentials, value framework, examples, brand/visual QA, editor identity, tracker, Slack, and runtime evidence without live writes.
- `scripts/clip_call_recording.py` performs the real transcript-supported media cut using hardware-first `auto` mode with a `libx264 veryfast` fallback and timing evidence.
- `scripts/package_skill.py` creates a deterministic teammate ZIP and excludes caches and machine artifacts.

Typical read-only preflight:

```bash
node scripts/fast_path_preflight.js \
  --account ACCOUNT \
  --operator luke \
  --package CALL.zip \
  --deck DECK.pdf \
  --meeting-match-confirmed \
  --examples-manifest EXAMPLES.json \
  --network-readback \
  --editor-ready
```

Validate an account-neutral run plan before external writes:

```bash
node scripts/fast_path_orchestrator.js --spec RUN.json
```

Apply only after dry-run succeeds, using the exact run ID, persistent resume state, and explicit authorization:

```bash
node scripts/fast_path_orchestrator.js \
  --spec RUN.json \
  --apply \
  --confirm-run-id RUN_ID \
  --state RUN.state.json \
  --allow-external-writes \
  --receipt RUN.receipt.json
```

Never put credentials in the run specification. Adapter commands inherit authorized credentials from the process environment or existing local auth cache. The last non-optional stage must be the single receipt verifier and depend on every preceding required stage.

## Source-To-Room Workflow

1. Resolve the invocation identity and run the Mandatory Preflight.
   - For a real sales opportunity, resolve and record the exact Salesforce Opportunity ID before `source_ready`; stop if the account maps ambiguously. For an explicitly requested prototype with no opportunity, record `prototype_override=true` instead of inventing an ID.
2. Start independent lanes concurrently:
   - evidence lane: transcript match, buyer-safe brief, hero/value copy, AI signal, and cut boundary
   - asset lane: deck, covers, tracker rows, Drive tiles, logo, and upload manifests
   - media lane: `ffprobe`, clip decision, edit, technical verification, and upload preparation
   - Folloze lane: authenticated template/config/vanity/editor-path checks, then copy only after preflight passes
3. Separate source evidence into `buyer-safe`, `internal-only`, and `missing`; parse the transcript once and pass forward only the compact evidence map and prepared copy.
4. Resolve `transcript_source_mode` as `granola`, `kaia_package`, `local_file`, or `kaia_browser_export`, then choose recording `acquisition_mode` as `local_provided` or `kaia_browser_export`. Do not open Kaia when the local package is complete; stop on a supplied-but-invalid file.
5. Map the prepared context to the July template's fixed surfaces: company logo, company-name headline, call-derived hero subheader, Essentials assets, the section subheader plus the fixed value framework, demo examples, and the untouched ROI calculator.
6. Keep buyer copy concise and action-oriented. The room should read like a working sales room, not a transcript summary or production note.
7. Push through the direct Folloze API only after every required lane is ready. Upload independent assets concurrently, save once, publish once, and use one bounded verifier.
8. Finish the internal handoff only after the vanity URL, published state, Luke editor access, Essentials assets, value-card evidence map, tracker update, and seller-review notification have independent evidence in the single compact receipt.

## Board Identity, Brand, And Vanity

- Name the copied board `[Account] | Folloze Resource Center` unless Trey supplies another buyer-safe name.
- Default the vanity slug to `[normalized-account]-resource-center`. Validate uniqueness before setting it, then re-read metadata and record the exact resulting public URL. Do not leave a random generated slug in the final handoff.
- Source the company logo and accent color from an official company website, brand kit, approved logo asset, or other first-party source. Record the source and selected hex value in the deal artifact/readback.
- Use the verified accent only for the company-name callout and other explicitly approved account accents. Check accessible contrast and visually compare the rendered result with the source brand; do not substitute a guessed darker or muted approximation merely because it is legible.
- Treat browser visual QA as its own gate. If the public board is email-gated, validate in the authenticated designer/preview and record anonymous gating separately.

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

1. The processed demo call recording uploaded to Folloze as an MP3 or MP4 content item.
2. Luke's account-specific follow-up deck, uploaded to Folloze as its own content item.

Add Folloze Case Studies, the Folloze MCP Launch Film, an order form, or another promised resource only when it is relevant to the call and the native layout has room. Do not treat any of those optional items as a substitute for the recording or deck.

Use accurate, asset-specific cards and previews. Read [references/asset-usage.md](references/asset-usage.md) before assigning a cover:

- use `assets/demo-call-recording-cover.png` for the processed demo recording
- use the exported deck's own first slide when it is suitable; otherwise use `assets/presentation-deck-cover.png`
- use `assets/order-form-cover.png` only for an order form
- never reuse one stock cover for an unrelated asset type, demo example, guide, or walkthrough

For the recording and transcript, read and follow [references/recording-transcript-intake.md](references/recording-transcript-intake.md) completely. The required decision is:

1. For Trey, use the matching Granola transcript/notes first and create a temporary readable local transcript input. For Luke, inspect his supplied Kaia download package for the transcript and recording before using any browser or email automation.
2. If Luke supplied a valid local MP3, MP4, M4A, MOV, or WAV recording, use it and skip Kaia, browser automation, emailed export retrieval, and another ZIP export.
3. If a required local asset is absent and the invocation authorizes fallback, use the existing Kaia browser export workflow. If a supplied local file fails validation, stop for correction instead.
4. In either path, perform a real audio/video edit when removable opening chatter exists. Prefer `scripts/clip_call_recording.py`; a download, copy, rename, or container change is not clipping.
5. Verify source and output duration, the exact removed interval, output streams, new opening content, playback, and the Folloze-hosted destination before declaring the recording complete.

Name the finished media item using `Account Name + Folloze Demo + Recording Date`. Never embed or link the Outreach/Kaia viewer as the buyer-facing asset. Do not commit the raw transcript or recording; keep only a buyer-safe brief and media-processing receipt in the deal's git-backed repo.

For Luke's deck, use the supplied deck when available. Export or prepare an approved upload format, upload it to Folloze, and attach the Folloze-hosted content item to the card instead of linking directly to Google Slides. If the deck is missing, send Luke an automated Slack request that explicitly states it is an automated message from Codex. A missing deck does not prevent the first draft, but the request must be tracked.

Use buyer-facing display titles that describe the asset instead of exposing raw filenames, duplicate suffixes, or internal production names. Default patterns are:

```text
[Account] + Folloze | Platform Demo
[Account] + Folloze | Presentation
```

The underlying filename may retain a date or export-safe name; the card title must remain buyer-facing. When a copied Content Center item is shared, owned by another teammate, or cannot be edited safely, detach/create a board-specific item before changing its title, cover, media payload, or destination. Never mutate the shared source item merely to personalize one account room.

Do not turn this section into a generic content library. Keep only the true essentials supported by the template's native card capacity. The deal-room task remains incomplete until the processed recording is uploaded and verified. When `clip_required=false`, an unchanged but validated source is acceptable only with the documented no-chatter review; do not perform a pointless transcode or claim it was clipped.

### Section 3: Embedded Value Section

Preserve the existing `flz-13863-html-section` whose unique heading is:

```text
From brief to live campaign. In minutes, not sprints.
```

This is an approved template component, not a prompt to build a new HTML section. On Board `248623` it is widget `w_dacd1645`; on a copied board, locate it by the unique heading and widget type instead of trusting the ID alone. Assert that exactly one widget matches.

Preserve the existing wrapper, CSS, responsive behavior, four-card structure, inline SVG artwork, eyebrow, main heading, ordering, and accessibility markup. Do not regenerate, paste over, or rebuild the widget.

Keep the existing four-card order and align it to the canonical value framework in [references/value-prop-personalization.md](references/value-prop-personalization.md): (1) Build Speed & Scalability, (2) Personalization & Enrichment, (3) Analytics & Optimization, and (4) Openness & AI Connectivity only when the call supports a third-party AI-system use case. Cards 1–3 always remain. If Claude, ChatGPT, Gemini, an agent/LLM, MCP, or another external AI connection did not come up meaningfully, remove AI/openness as a buyer-facing option and repurpose card 4 to call-informed Operational Scale & Reuse while preserving the four-card layout.

Preserve an existing card's category label and heading when it already maps cleanly to the canonical framework. Personalize the section subheader plus each card's subheadline/body and proof line from the transcript; change a label or heading only to restore the canonical category or remove unsupported AI language. Record the supporting transcript timestamp plus any secondary source reference in the private source brief. Never expose evidence citations or private notes in buyer-facing copy.

Before saving, compare the original and edited HTML strings. Allow changes only to the section subheader and the four cards' text nodes: label, heading, body, and proof line. Reject changes to CSS, markup structure, SVGs, scripts, layout, or the main heading. If the widget source cannot be read or uniquely identified, stop and ask Trey for the source HTML rather than rebuilding it.

### Section 4: Example Folloze Boards

Preserve the section title, carousel behavior, card styling, and existing curated items. Board `248623` currently contains these six baseline items in this order:

1. `Website Resource Center - Check Point Security`
2. `White Paper to Experience - Cisco`
3. `Acquisition ABM - Instructure`
4. `Field Event Promotion - Bloomreach`
5. `Expansion ABM - Aprio`
6. `Product Promotion - Lenovo`

The live template and Trey's reference screenshot say `Check Point Security`, not `Checkmarx`. Preserve the live Check Point item unless Trey explicitly requests a replacement. The screenshot shows five cards because of its viewport crop; the live template also contains Lenovo.

Add the real Folloze MCP demo examples created for the account's demo calls after the baseline items. Read and follow [references/demo-example-sourcing.md](references/demo-example-sourcing.md) completely. Resolve Board IDs, buyer-facing titles, public deployment URLs, and verification notes from the canonical `MCP Demo Environments - May 2026` Google Sheet rather than Trey's local repo. Resolve preview artwork from the `Folloze Demo Example Tile Library` folder in the company-wide `Folloze General` shared drive. Every added card must point to a real, verified destination and use its own accurate tile.

Create each new demo-example tile in the same pattern as the baseline covers:

- `1672 x 941` landscape PNG
- company logo at the top
- short motion or use-case label centered below
- account-appropriate gradient or brand color
- subtle geometric texture consistent with the existing set
- no screenshots, dense body copy, fabricated logos, or generic recording/deck artwork

Use `[board-id]-[normalized-company]-[normalized-motion]-tile.png`. If Luke supplies the correct tile locally, upload a copy to the shared Drive tile library before using it so future runs are machine-independent. Upload the final tile to the correct Folloze content item, then verify the carousel crop at desktop and mobile sizes. Do not use a Drive viewing URL as the Folloze image URL.

### Section 5: ROI Calculator

Leave the ROI calculator exactly as it exists in the universal template. Do not personalize its title, copy, inputs, ranges, formulas, styling, outputs, or default assumptions. Confirm only that the untouched calculator still renders and functions after the rest of the board is edited.

## Direct API Sequence

Use existing authorized Folloze session credentials from the environment or local auth cache, but never print or commit them. The production preflight must prove that the expected API and editor-invite paths are usable before board creation. If endpoints drift, stop the timed run and investigate separately; do not inspect application bundles or source maps during production.

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
- the approved text nodes inside the copied value-section HTML widget: section subheader plus all four cards' labels, headings, bodies, and proof lines, with card 4 using the conditional AI/fallback rule

Do not add:

- new `html-section` widgets
- full-page HTML payloads
- raw custom-script widgets as the primary room body
- placeholder CTAs, fake documents, fake meeting links, or dead anchors

Board `248623` intentionally contains two existing `flz-13863-html-section` widgets:

- the value section beginning `From brief to live campaign. In minutes, not sprints.`
- the ROI calculator beginning `Estimate potential pipeline and revenue.`

Preserve both. Edit only the approved value-section text nodes defined above, and do not change any ROI widget content.

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

### 7. Set And Verify The Vanity URL

Validate the intended `[normalized-account]-resource-center` slug using the current Folloze application endpoint or designer behavior, apply it to the copied board, and re-read board metadata. Record both the designer URL and the resulting vanity public URL. If the preferred slug is already used, choose the smallest defensible account-specific suffix and report it rather than silently accepting a random slug.

### 8. Invite And Verify The Seller Editor

For Luke-owned opportunities, invite the preflight-resolved Luke Rafferty organization identity as an Editor using the current supported Folloze application behavior. Prefer a verified direct API call when the endpoint is known from the current app; otherwise use the already authenticated browser session. Re-open/read the Editors list and require the same stable organization user/invite ID plus the Luke Rafferty display name before moving to `editor_verified`.

The actual invite gets one attempt inside a 60-second budget and at most one targeted retry for a transient response. If CAPTCHA or authentication fails despite preflight, stop at `published_internal`, report `editor_pending`, suppress Slack completion, and investigate the transport in a separate task.

Do not infer board-editor access from Folloze channel/content-play membership. The current application exposes channel user and invitation routes under `/api/v1/channels/:channelId`, but a board ID is not a channel ID and those responses are not board-editor evidence unless the current application explicitly resolves and displays that binding. The editor search route may identify Luke as an allowed organization editor, but search eligibility is also not proof of a completed board invitation. Until a board-specific invitation transport and readback are confirmed against the current app version, use the authenticated board Invite dialog and verify the board's actual Editors tab.

After editor verification and publication, send Luke an automated Slack message that:

- explicitly says it is an automated message from Codex
- says the room is ready for Luke's review
- includes both the designer URL and vanity public URL
- states that customer sharing remains pending Luke's approval

Record the Slack message link or stable message/channel identifiers in the readback. Do not send this completion handoff while required assets, editor verification, or publishing are incomplete.

## Verification Gates

A direct API push is not done until these pass. Collect them through one bounded verifier and one compact receipt instead of separate exploratory readbacks:

- Metadata readback shows the expected board name and `is_template: false`.
- Public/activation fields show the intended state, such as `is_public: true`, online activation, and a published version when publishing was requested.
- `published_config` contains the account-specific buyer copy after publish.
- `unpublished_config` and `published_config` hashes match when no unpublished changes remain.
- The config contains the two approved embedded HTML widgets from Board `248623`, with the value widget structurally unchanged outside the section subheader and all four cards' approved text nodes, and the ROI widget's `data.content` byte-for-byte unchanged.
- No new embedded HTML widget, full-page HTML payload, or custom-script body was added.
- The config does not contain raw full-page HTML as the room body.
- The generic company logo is gone and the approved company logo renders correctly.
- The hero contains no template bracket text, example copy, attendee names, or unsupported claims.
- Essentials includes the real Folloze-hosted processed recording and deck, with correct covers and working destinations.
- The transcript source mode is recorded as `granola`, `kaia_package`, `local_file`, or `kaia_browser_export`; recording acquisition mode is recorded as `local_provided` or `kaia_browser_export`; both inputs match the meeting and were used for the buyer-safe brief, value-card evidence map, and clip decision.
- The media receipt proves real editing when clipping was required: source/output duration, removed interval, tool/command, output stream validation, opening-content review, and playback. A renamed or copied source is not accepted as an edit.
- Essentials card titles are buyer-facing, raw duplicate/export filenames are not exposed, and any personalized shared content was detached before mutation.
- The value-section keeps Build Speed & Scalability, Personalization & Enrichment, and Analytics & Optimization in order; each card's subheadline/body is call-influenced and privately evidenced. Card 4 is AI/openness only with an affirmative external-AI signal; otherwise it contains no AI language and is Operational Scale & Reuse.
- The baseline example-board cards remain present in order. Each added demo example has a canonical tracker row, production deployment URL, matching Board ID, company-wide Drive tile, Folloze-hosted image, and correctly cropped preview.
- The untouched ROI calculator still renders and calculates at its original defaults.
- The returned public link or designer link is recorded with its state.
- The vanity slug was intentionally selected, validated, applied, and matches the public link returned by metadata.
- The account accent has a first-party source, recorded hex value, accessible contrast, and authenticated visual validation.
- The preflight-resolved Luke Rafferty stable organization identity appears in the board Editors list for Luke-owned opportunities.
- Luke received the automated Codex review handoff with both URLs only after the preceding gates passed.

Public Folloze links can show email verification or access gating to anonymous visitors. Do not call that a failed publish when API metadata confirms the board is public, online, and published; instead, report the gating state separately.

## Paused Automation Contract

The former `folloze-post-intro-dsr-automation` LaunchAgent workflow is paused as of 2026-08-04. Do not invoke this skill from that runner or emit success solely to satisfy its status feed. Manual runs may still use these monotonic states as an evidence model:

```text
queued -> source_ready -> assets_pending -> board_saved -> published_internal -> editor_verified -> review_notified -> customer_share_approved
```

`customer_share_approved` is set only from explicit seller approval and is never inferred from publish, editor access, or Slack delivery. A normal manual build stops successfully at `review_notified`.

A manual run may create a useful draft after the transcript is validated, but `source_ready` means only that the transcript, account, opportunity, and buyer-safe brief are resolved. If recording acquisition or the deck remains outstanding, the highest allowed state is `assets_pending`: do not publish, invite/notify Luke, or claim completion. Do not mark the run complete from a Codex process exit code alone.

For machine invocation, emit exactly one JSON object between `DSR_RESULT_JSON_BEGIN` and `DSR_RESULT_JSON_END`. It must include:

- run ID, account, operator, Salesforce Opportunity ID, runtime profile, start/finish timestamps, wall-clock seconds, deadline seconds, and deadline-exceeded status
- terminal workflow state and blockers
- board ID, Board `248623` template identity, designer URL, vanity public URL, slug, and published/online fields
- saved and published hash evidence
- transcript source mode, recording acquisition mode, local/temporary transcript path/readability evidence, source/output durations, removed interval, clip verification, recording and deck item IDs, buyer-facing titles, correct-cover checks, and working-destination/playback checks
- value-framework evidence map with the three required core cards, `ai_signal_present`, `card_4_mode`, private timestamp/source references, and buyer-facing text
- brand source, logo source, accent hex, and visual-QA result
- Luke editor verification evidence
- Slack review-notification link or identifiers
- anonymous visitor-gating result
- tracker source/update evidence plus Drive tile file IDs when demo examples are added
- performance receipt with `target_runtime_seconds=480`, `hard_timeout_seconds=600`, total elapsed seconds, stage timings, stage-budget results, external-wait seconds, API/browser call counts, retry count, timeout status, browser-fallback seconds, and whether the warmed fast path was used
- token and cost receipt with input/cached-input/output tokens or `token_usage_available=false`, `cost_estimate_usd`, pricing/model basis, and external-service cost or unavailable reason

If any required evidence is absent, return the highest verified nonterminal state plus blockers. Never fabricate a success-shaped JSON object to satisfy the runner.

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
- Value-framework drift: replacing the canonical speed/scale, personalization/enrichment, and analytics/optimization categories with ad hoc themes, or retaining AI/openness when the call did not support an external-AI use case.
- Broad HTML rewrite: changing value-widget CSS, structure, SVGs, scripts, layout, or main heading instead of only the allowlisted text nodes.
- False media-edit claim: downloading, copying, renaming, or remuxing a recording without proving the intended opening chatter was actually removed.
- Asset mismatch: using the recording cover for a deck, order form, or demo example, or adding a new example without a matching landscape tile.
- Private leakage: copying raw call notes, internal objections, budget comments, or next-step tasks directly into buyer-facing text.
- False live claim: treating a designer URL, local file, or gated public URL as the same state as a published public board.
- Production debugging: discovering endpoints, inspecting app bundles/source maps, repairing OAuth, or troubleshooting browser extensions after the 60-second preflight limit instead of stopping with an actionable blocker.
- Serial intake: resolving the transcript, deck, tracker, tiles, brand, auth, and seller identity one after another when they can be preflighted concurrently.
- Output bloat: printing full config, sheet, organization, DOM, or source-map payloads instead of field-scoped evidence, causing unnecessary latency and token use.
- Source drift: relying on old endpoint knowledge after the Folloze app bundle has changed; stop the production run and inspect current app behavior in a separate diagnostic task.
