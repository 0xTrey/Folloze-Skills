# Controlled Test Plan

Do not run this plan until the skill owner has answered the discovery questions and approved the test scenario.

The first run uses only the named, approved scenario. Do not invent a synthetic account or silently substitute another deal. Over time, test both intake lanes:

- `sdr_net_new`: public-research-led intake with a rep-approved buyer hypothesis
- `ae_active_deal`: authorized deal-context synthesis from calls, email, Slack or DMs, Drive, CRM, and other approved sources

## Required Test Inputs

- named prospect and exact domain
- seller name and motion
- primary buyer persona
- real or approved synthetic business context
- exactly one buyer challenge and one desired outcome
- one real role-specific CTA destination
- source permissions
- proof policy
- `visual_authority: live_folloze_site`, with the bundled brand kit represented by an approved `skill_reference` ledger entry
- a Folloze-default or verified-prospect accent whose exact hex is bound to an exact extracted fact in that approved source entry
- explicit confirmation that the scenario may be used for the test

For `sdr_net_new`, the CTA must be a scheduling URL labeled exactly `Book a Meeting`. For `ae_active_deal`, it must be either a deal-room URL labeled exactly `Continue to the Deal Room` or the seller's email labeled exactly `Reply to the Seller`.

## Test Artifacts

Keep all artifacts in a scoped repo folder:

```text
artifacts/folloze-one-pagers/<account-slug>/
  intake.json
  source-summary.md
  render-values.json
  one-pager.html
  qa/
    validator.json
    browser-checks.json
    desktop.png
    mobile.png
    narrow-mobile.png
```

Do not create or save a Folloze board during the first test unless the user separately authorizes the MCP step.

## Test A: Intake Gate

1. Start from `references/intake-template.json`.
2. Run the adaptive rep interview.
3. Confirm the correct AE or SDR lane is selected.
4. Confirm private sources remain denied until authorized. For an SDR test, confirm public research and rep-approved hypotheses do not become asserted account facts. For an AE test, confirm only explicitly authorized private sources are read.
5. Produce the normalized brief, source ledger, message-fit matrix, and exact-approved display-content registries.
6. Attempt Stage 2 before approval by invoking the renderer with `--brief` and otherwise complete render values.

Expected:

- Stage 2 refuses to build.
- The missing approval is stated clearly.
- No HTML, MCP save, tracker write, commit, or push is implied.

## Test B: Approved Local Build

Before rendering a prospect page, run the bundled validator regressions:

```bash
python3 -m unittest discover -s Skills/folloze-one-pager/tests -v
```

1. Approve the normalized brief.
2. Record the version, approver, timestamp, text, and digest.
3. Copy `references/render-values-template.json` to the account folder and fill it only from the approved intake.
4. Render `assets/one-pager-microsite-template.html` with `scripts/render_one_pager.py --brief <approved-intake.json>`.
5. Confirm omitted modules and linked controls were removed and every selected path pillar was renumbered.
6. Run the validator in final microsite mode.
7. After visual review, record separate preview approval with the approved brief version and exact HTML digest.
8. Rerun final validation against the approved digest.

Expected:

- The page makes one account-specific argument.
- The page contains exactly one buyer challenge and one desired outcome.
- Hero, Desired outcome, Folloze capabilities, Proof, and CTA are present.
- Promise, Proof, and Path match the approved brief.
- All account claims map to source IDs.
- All Folloze claims and proof strings match both an approved ID and the exact approved display-content registry.
- Page title, meta description, seller identity, prospect identity, logos, and any resource labels or URLs match their approved bindings exactly.
- No private note wording appears.
- No unsupported numeric claim appears; qualitative proof is used when no verified number is approved.
- Template-owned `01`, `02`, and `03` path labels are treated as structural sequence labels, not proof.
- Ordinary wording such as `one workflow` is not treated as numeric proof.
- The CTA label, type, and destination match the selected seller motion.

## Test C: Browser QA

Check:

- 1440 x 900
- 1024 x 768
- 768 x 1024
- 414 x 896
- 390 x 844
- 320 x 568

Expected:

- no horizontal overflow
- Folloze and prospect context visible in the first viewport
- no logo, header, CTA, or card collision
- images render
- scroll controls move correctly without a hash route
- analytics spy receives `cta_click` and any applicable `resource_click` events
- the page remains compatible with Folloze native visitor, page, engagement, and content analytics
- keyboard focus is visible
- reduced-motion mode preserves all actions
- no console errors

## Test D: Safety Mutations

Make one controlled invalid copy at a time:

- add an unapproved numeric claim
- add a written multiplier such as `double` or `fourfold` under a qualitative claim ID
- add an unsupported single-digit comparison such as `from 9 to 4`
- use a pure-number-word account identity in a numeric sentence to confirm identity masking cannot hide the claim
- change the CTA destination
- add query parameters or another recipient to a `mailto` CTA
- remove seller approval
- insert a raw `href="#path"`
- remove direct CTA analytics
- add an unknown proof ID
- reuse an approved ID with unapproved display copy
- pair a numeric claim with an approved qualitative claim ID
- trace a visible claim to a `strategy_only` source
- remove a required buyer-copy source trace
- attach an extra source ID that is not approved for that exact display string
- add `data-non-claim-number` to buyer copy
- change a path index to any value outside `01`, `02`, or `03`
- change a proof card from `proof` to `claim` without changing its allowlist
- combine `data-evidence-*` with a second proof or claim identity on the same buyer copy
- relabel an authorized private source as `classification: public` and attempt exact buyer use without item approval
- enable private-source refresh without allowing any private source family
- change the approved prospect logo URL in rendered HTML
- change the rendered account accent without changing the approved intake hex
- cite an account-accent source fact containing a different hex
- cite an eight-digit hex whose first six characters match the approved accent
- add an untracked external anchor
- modify the trusted inline interaction script
- add an unexpected inline event handler
- leave one template token unresolved

Expected:

- the validator fails with the matching rule
- the durable approved HTML remains unchanged

## Test E: MCP Boundary

Ask for local preview only.

Expected:

- no MCP guide, theme lookup, board save, tracker write, or public URL claim occurs

Only after separate explicit save authorization:

1. hand off to `Folloze-MCP-Demo-Builder`
2. resolve board identity
3. record theme authorization
4. add the returned theme link
5. validate in MCP mode
6. after a successful save, bind the recorder, RFC3339 time, approved account, returned board ID, returned designer URL, response evidence, and save-result digest before entering `mcp_saved`

Expected:

- local preview approval and MCP save authorization remain distinct
- returned designer URL and public deployment status remain distinct
- no public deployment is inferred

For an `ae_active_deal` only, test public deployment after an additional explicit authorization that records actor, timestamp, exact instruction, and authorization digest. A returned URL remains unverified until a Folloze/public readback records the verifier, time, method, approved account, saved board ID, evidence, and matching verification digest. Confirm that verified deployment and manual link sharing remain separate states; a manual-share reporter must match the approved seller name or email. Do not run a public-deployment test for `sdr_net_new`.

## Acceptance Criteria

The skill passes only when:

- Stage 1 produces a complete approved intake
- Stage 2 is impossible without current approval
- the generated page is account-specific and buyer-safe
- proof and CTA traceability pass
- AE and SDR role policies pass for the tested lane
- desktop, tablet, mobile, and narrow-mobile QA pass
- no private-source leakage is found
- no MCP side effect occurs without explicit authorization
- no public deployment occurs outside an explicitly authorized AE active-deal flow
- no page is reported as shared merely because it was deployed
- all completed states are reported separately
