# MCP Build Contract

Use this reference only after the local one-pager has been built and the user explicitly requests save to Folloze, board publication, a board update, repush, or push to Folloze. A generic request to save the work means Git persistence, not an MCP operation.

The one-pager skill owns the brief and local source. `Folloze-MCP-Demo-Builder` owns the live MCP save workflow.

## Ownership

### One-Pager Skill

Owns:

- seller intake
- source permissions
- research and source ledger
- normalized brief
- message-fit matrix
- proof selection
- local HTML
- local structural and browser QA
- local preview approval
- sidecar handoff state

Does not own:

- the current MCP creation guide
- theme lookup
- live board identity resolution
- MCP save acknowledgements
- board creation or update
- returned URL interpretation
- tracker write
- public URL verification

### MCP Builder

Owns:

- current creation guide
- explicit theme-mode question
- theme lookup and required theme link
- net-new versus update identity
- exact save payload and acknowledgements
- `needs_fix` handling
- returned board ID and URL
- first-create tracker behavior when in scope
- post-save result note
- public deployment status

## Handoff State

Maintain this exact `stage2_handoff.mcp_state` object in the intake. A separate result note may mirror it, but the intake remains canonical and is the object the validator reads. Brand owner, target account, and canonical `motion: one_to_one` remain in their existing intake fields rather than being duplicated here.

```yaml
save_intent: local_only          # local_only | net_new | update
save_authorized_by: ""
save_authorized_at: ""
save_authorization_text: ""
authorization_digest: ""
board_name: ""
board_id: null
local_html_path: ""
theme_mode: pending             # pending | yes | no
theme_authorized: false
theme_id: null
theme_url: null
designer_url: null
save_result_status: not_recorded   # not_recorded | saved
save_result_recorded_by: ""
save_result_recorded_at: ""
save_result_account_name: ""
save_result_board_id: null
save_result_designer_url: null
save_result_evidence: ""
save_result_digest: ""
public_url_status: pending      # pending | returned | user_supplied | verified
public_url: null
public_deployment_authorized_by: ""
public_deployment_authorized_at: ""
public_deployment_authorization_text: ""
public_deployment_authorization_digest: ""
public_verification_method: not_run   # not_run | folloze_readback | public_http_readback
public_verified_by: ""
public_verified_at: ""
public_verification_account_name: ""
public_verification_board_id: null
public_verification_evidence: ""
public_verification_digest: ""
manual_share_status: not_shared    # not_shared | seller_reported_shared
manual_share_reported_by: ""
manual_share_reported_at: ""
tracker_status: not_in_scope
qa_status: not_started            # not_started | local_pass | browser_pass | ready | failed
```

Do not infer missing values.

Every non-empty approval, authorization, result, verification, and manual-share timestamp must be RFC3339 with a timezone. Keep the sequence monotonic: intake approval, preview approval, MCP authorization, MCP save result, public authorization, public verification, then manual sharing.

The save `authorization_digest` binds the exact approved preview, board intent, board identity, local source, theme decision, authorizing person, timestamp, and instruction. Generate or verify it with the one-pager validator's MCP digest mode before the live call.

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --digest mcp
```

After a successful save response, record who captured it, when, the approved account, returned board ID, returned designer URL, and concrete MCP response evidence. Bind those values to the authorization and approved HTML before entering `mcp_saved`:

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --digest mcp-result
```

Public deployment has a separate authorization record and digest. It is permitted only when `seller_inputs.seller.motion` is `ae_active_deal`. The authorization binds the account, motion, saved board identity, designer URL, authorizing person, timestamp, and exact deployment instruction. MCP save authorization is never a substitute for public-deployment authorization. `seller_inputs.page_goal.requested_delivery` records the initial plan; a later explicit deployment authorization may expand that plan without rewriting the approved page brief.

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --digest public
```

After deployment, do not set `public_verified` from a returned URL alone. Read the Folloze record or public page, record the method, verifier, timestamp, approved account name, saved board ID, and concrete readback evidence, then bind that record with the verification digest:

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --digest public-verification
```

Before `public_verified`, every verification field remains at its empty or `not_run` value.

The Stage 2 handoff also records `preview_approval`: decision, approved brief version, approver, timestamp, approval text, and the `sha256:` digest of approval-normalized HTML. The digest excludes only the theme-slot comment or inserted `data-folloze-theme` link. Any other HTML change invalidates it.

```yaml
preview_approval:
  decision: pending
  brief_version: 0
  approved_by: ""
  approved_at: ""
  approval_text: ""
  html_digest: ""
```

If the authorized theme materially changes the rendered design, invalidate preview approval and request review again even when the normalized digest still matches.

## Approval Boundaries

| State | What it authorizes |
|---|---|
| `intake_approved` | Build a local page from the approved brief |
| `local_preview_ready` | Show the local result |
| `local_preview_approved` | Preserve the local result as approved |
| `mcp_save_authorized` | Run the MCP guide/theme/save sequence |
| `mcp_saved` | The board save returned success |
| `public_deployment_pending` | An AE explicitly authorized deployment, but no public URL has been verified |
| `public_verified` | A separate Folloze/public readback bound the URL to the approved account and saved board |

None of these states authorizes Git push unless the user asks for remote backup or publication.

## Pre-Save Requirements

Before MCP work:

- intake approval is current
- local preview is approved
- save intent is explicit
- local source path is verified
- target account and board name are correct
- existing board ID is resolved for updates
- current MCP creation guide has been read
- preview approval record matches the exact local HTML
- explicit save authorization includes actor, time, and instruction
- save authorization digest matches the current handoff state
- theme mode is explicitly authorized
- exact MCP theme URL is in `<head>`
- exact MCP theme ID is the value of `data-folloze-theme`
- local source passes the validator in MCP mode
- browser QA covers desktop, mobile, and narrow mobile
- `qa_status` is `ready`

Before public deployment:

- seller motion is `ae_active_deal`
- MCP save is complete and board identity is recorded
- deployment authorization includes actor, time, exact instruction, and matching digest
- deployment remains distinct from the later manual act of sharing the link with the prospect

MCP-mode validation command:

```bash
python3 Skills/folloze-one-pager/scripts/validate_one_pager.py \
  --brief path/to/intake.json \
  --html path/to/one-pager.html \
  --profile microsite \
  --mode mcp
```

## HTML Requirements

- one self-contained document
- exactly one current theme stylesheet link in `<head>` with `rel="stylesheet"`, the returned URL in `href`, and the returned theme ID as `data-folloze-theme`
- custom CSS and JavaScript inline
- no external JavaScript
- every external link has `target="_blank" rel="noopener"`
- every external CTA has a direct inline `flzAnalytic('cta_click', ...)`
- every optional resource link emits `resource_click`
- meaningful scroll or custom interactions emit analytics
- custom events supplement Folloze native visitor, page, engagement, and content analytics
- no raw hash navigation
- no placeholders or dead controls
- no unresolved proof token
- accessible focus and reduced-motion behavior

## Save Sequence

1. Call the MCP landing-page creation guide.
2. Ask and record company-theme mode if not already authorized.
3. Call theme lookup even for authorized no-theme mode.
4. Insert the exact returned theme URL and ID in the sidecar.
5. Revalidate the exact local file in MCP mode.
6. Save from the local file.
7. If MCP returns `needs_fix`, patch the durable local source and retry the same board intent.
8. Preserve the existing board ID on update.
9. Record the exact board ID and MCP-returned URL.
10. Leave public deployment pending unless a separate authorized deployment flow returns or supplies a public URL.

## Public Deployment Sequence

Only for `ae_active_deal`, after separate explicit authorization:

1. Verify the deployment actor, timestamp, exact instruction, and authorization digest against the saved board state.
2. Run the current Folloze deployment operation.
3. Record the returned or supplied public URL without inferring verification.
4. Read back the Folloze record or public page, confirm the approved account and saved board ID, record the verification evidence, and validate the `public-verification` digest before setting `public_verified`.
5. Leave link sharing unperformed unless the seller manually shares it.

Do not send, email, DM, or otherwise share the link automatically; manual seller sharing is a separate state.

## Post-Save State Separation

Report each independently:

- Folloze save
- board ID
- designer URL
- public deployment URL
- public verification
- manual link sharing, only when separately performed by the seller
- tracker write
- local QA
- post-save hosted QA
- Git commit
- Git push

A signed-in designer URL is not proof of a public deployment.

## Tracker And Git

- Tracker logging follows the operator-scoped rules in `Folloze-MCP-Demo-Builder`.
- A first-create tracker write does not authorize later tracker changes.
- Stage only files for this one-pager.
- Commit only when the user asks to save or when the active workflow explicitly requires a scoped commit.
- Push only when the user asks for GitHub/remote backup or publication.
- Never combine unrelated dirty files into the one-pager change.
