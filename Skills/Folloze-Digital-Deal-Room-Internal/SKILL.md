---
name: Folloze-Digital-Deal-Room-Internal
description: Build and publish Folloze-owned digital deal rooms from internal deal context using the direct Folloze API and an approved native Folloze deal-room template. Use when Trey asks to create, push, update, or iterate a Folloze digital deal room through the API, especially when he says to use a specific Folloze template, not the MCP Save tool, and not raw HTML.
---

# Folloze Digital Deal Room Internal

Use this skill to turn Gmail, Granola, Zoom, Salesforce, Slack, Drive, and pasted deal notes into a buyer-safe Folloze-owned digital deal room, then push it into Folloze through the direct API and a native template.

This is a direct API/native-template workflow. Do not use an MCP save tool as the publishing path. Do not package the page as raw HTML, `html-section`, or a full-page custom script unless the user explicitly changes scope.

## Operating Rules

- State the working goal before material edits: account, target template, source context, repo artifact, board-create/update intent, public status, and private-note boundary.
- Start from the real source context. Use Gmail, Granola or Zoom notes, Salesforce, Slack, Drive, or pasted notes when available instead of generic account copy.
- Treat internal notes as strategy inputs. Do not expose raw meeting-note language, internal tasks, pricing commentary, budget details, personal notes, or unapproved objections in buyer-facing copy.
- Translate private deal facts into buyer-safe copy: priorities, proof needs, recommended resources, next steps, and value themes.
- Keep durable briefs, scripts, and readback notes in a git-backed repo. Do not store API tokens, cookies, auth headers, or raw sensitive exports in the skill package or repo artifacts.
- Resolve whether this is a net-new board, template duplicate, or existing-board update before writing to Folloze.
- Use `folloze-brand-kit` for Folloze positioning and approved buyer-facing product language when the deal room is Folloze-owned.
- Use `folloze-zoom-deal-room` for intake if the request starts from Zoom or meeting notes; this skill owns the direct API/native Folloze write path.
- Stop before publish if the account identity, template identity, source ownership, or buyer-facing approval boundary is unclear.

## Source-To-Room Workflow

1. Gather deal context from the narrowest reliable source first.
2. Write a compact internal brief with account state, buyer goals, stakeholders, pain, proof needs, promised follow-ups, resources, decision path, and next step.
3. Separate source evidence into `buyer-safe`, `internal-only`, and `missing`.
4. Draft the native room map: hero, executive message, buyer priorities, resource rows, mutual action plan, stakeholder proof, security or integration proof, and CTA.
5. Keep buyer copy concise and action-oriented. The room should read like a working sales room, not a transcript summary or production note.
6. Push through the direct Folloze API only after the brief and room map are coherent enough for a live board.

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

Default to the approved `Folloze Digital Deal Room Template` only when the user did not name another template.

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

Modify `unpublished_config` by updating native widgets and their existing fields. Preserve the template's native structure where possible.

Allowed changes:

- text, headings, labels, descriptions, button copy, and links inside existing native widgets
- section ordering when the config already supports it
- image, logo, and resource references when they are approved and reachable
- native content widgets, item references, or content rows when supported by the template schema
- navigation labels and anchors that point to real sections
- contact or team modules with approved names and roles

Do not add:

- `html-section`
- full-page HTML payloads
- raw custom-script widgets as the primary room body
- placeholder CTAs, fake documents, fake meeting links, or dead anchors

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
- The config does not contain `html-section` unless the user explicitly changed scope.
- The config does not contain raw full-page HTML as the room body.
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

- Wrong route: using MCP Save or custom HTML when the user asked for API/native template.
- Wrong object: editing a copied board but publishing the original template.
- Hash no-op: saving config without recomputing the designer-compatible hash, often returning `208`.
- Private leakage: copying raw call notes, internal objections, budget comments, or next-step tasks directly into buyer-facing text.
- False live claim: treating a designer URL, local file, or gated public URL as the same state as a published public board.
- Source drift: relying on old endpoint knowledge after the Folloze app bundle has changed; inspect current app behavior when API calls start failing.
