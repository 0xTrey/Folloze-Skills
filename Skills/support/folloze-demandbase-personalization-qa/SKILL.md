---
name: folloze-demandbase-personalization-qa
description: QA Demandbase-driven personalization rules on live Folloze board URLs using a discovery-first four-phase workflow. Use when a user asks to validate Folloze personalization rules that depend on the Demandbase data service, One Tag, enrichment, field mappings, merge tag behavior, rule matches, rule null results, semicolon-delimited values, or domain-based enrichment. Execute live board checks with Folloze Experience MCP plus browser DevTools evaluate. Do not use Zo, ChatGPT-local shell, or mcporter. Do not treat first-party URL params as Demandbase proof.
---

# Folloze Demandbase personalization QA

QA-test Demandbase-driven personalization rules on Folloze boards. Use a discovery-first framework: discover runtime schema and rule definitions, propose a test matrix, execute only approved tests, then classify bugs and ownership.

Use this when rules depend on Demandbase, not when the ask is generic URL-param testing.

Demandbase, like 6sense, is configured under `FollozeState.initialState.data_service_configuration`, not `board.integrations`.

## Execution model

This skill runs on the operator's agent with Folloze MCP and a live browser. Do not call Zo Computer tools, ChatGPT-local shell, or `npx mcporter`.

Preferred tool order:

1. **Folloze Experience MCP** for board/org context when it can return personalization config. Never print Demandbase API keys from MCP or page state.
2. **Browser MCP / Chrome DevTools MCP** to open the public board URL and evaluate JavaScript against `FollozeState.initialState`. Use the session's navigate and evaluate tools (names vary: `navigate_page` / `navigate`, `evaluate_script` / `evaluate`). View-source of the liveboard HTML (`var state`) is an acceptable fallback.
3. **In-page Demandbase fetch** for `domain.json` so the API key never leaves the browser. Fall back to shell `curl` only if CORS blocks the in-page call. If you must curl, hold the key in a local env var and never echo it.

QA hygiene:

- Use the public board link in a clean / incognito session. A logged-in Folloze session can keep Strong Lead Identity as the operator and hide visitor-path results.
- Tokenized links already have `?`. Append attributes with `&`. Only one `?` in the URL.
- `?dom=`, `?ind=`, `?em=`, `?fn=`, `?var=` inject first-party URL attributes. They prove first-party identity injection. They do not prove a Demandbase-backed rule fired.
- Test visits land in Pulse. Remove them before a customer send if that matters.

Read intended rules in Designer when you need the authored rule set and human merge-tag names. The public payload often has only numeric `mergeTagId`. This skill QAs whether those rules fire on the live URL.

Do not invent account, industry, intent, or pipeline values. Ignore rotating hero images when eyeballing. Diff headline, CTA, section copy, and `personalization_rules_results`, not pixels.

## State machine

Follow this order:

1. Phase 0: DISCOVER.
2. Phase 1: PROPOSE.
3. Wait for user approval before live test execution when tests may be numerous, customer-visible, or require domain assumptions.
4. Phase 2: EXECUTE.
5. Phase 3: REPORT.

Do not skip discovery. Do not assume customer-specific Demandbase field names, watchlist structure, or rule mapping.

## Universal invariants

1. `personalization_rules_results` returns `{ruleId: true|false|null}`.
   - `true` means the rule matched.
   - `false` means the rule evaluated but the resolved value did not match the configured rule value. Investigate formatting and exact values. `false` plus `landing_page: default` means no rule matched.
   - `null` means the rule did not evaluate because the merge tag could not resolve enrichment. Fix mapping first.
2. Folloze rule matching is exact string matching. Do not assume fuzzy matching, substring matching, or automatic splitting of semicolon-delimited Demandbase values.
3. Closed-list merge tags can silently reject values that are not in the allowed list.
4. Demandbase enrichment varies by test domain. Check each domain independently.
5. The Demandbase domain endpoint pattern is `https://api.company-target.com/api/v3/domain.json?key={KEY}&query={DOMAIN}`.

## What has to work

Folloze + Demandbase: Identify, Enrich, Personalize.

1. Demandbase One Tag actually runs on the live board (Network: Demandbase tag/API, not only Folloze liveboard.js).
2. Demandbase returns an account for that visit (IP/cookie identification). If that payload is empty, Personalization Studio has no Demandbase fields to match and the visitor gets the default board.
3. Personalization Studio rules are bound to Demandbase fields (industry, revenue, employee size, journey/intent, custom connector fields), not only to first-party URL attributes.
4. Company Admin has the Demandbase connector and API key. The Folloze Personalization module is required. Custom Demandbase attributes need the custom-fields connector.

## Phase 0: discovery

Navigate to the public board URL. Wait until `FollozeState` is present (retry once before falling back to view-source / static analysis).

### Step 0a: extract board rules

Evaluate this in the live page. Mask any API key. Never return the raw key.

```javascript
() => {
  const board = FollozeState.initialState.board;
  const dsc = FollozeState.initialState.data_service_configuration;
  const rules = board.config.personalization?.rules || {};
  const key = dsc?.api_key || "";
  return {
    board: { id: board.id, name: board.name, org_id: board.organization_id },
    data_service: dsc
      ? {
          type: dsc.type,
          api_key_masked: key ? key.substring(0, 4) + "..." : "none"
        }
      : null,
    rules: Object.fromEntries(
      Object.entries(rules).map(([rid, r]) => [
        rid,
        {
          mergeTagId: r.mergeTagId,
          mergeTagValues: r.mergeTagValues,
          compareOperator: r.compareOperator,
          appliedOn: r._appliedOn
        }
      ])
    ),
    rules_count: Object.keys(rules).length
  };
}
```

Gate check: `data_service_configuration.type` must be `"demandbase"`. If it is `folloze_data_service` with no third-party key, Demandbase rules cannot fire. Stop and report that the Folloze board does not have the Demandbase data service connector active.

Also confirm in Network that a Demandbase One Tag / identify call actually ran. No Demandbase call means those rules cannot fire even if Designer shows Demandbase fields.

Application cookies: Demandbase cookies vs only Folloze lead cookies (`folloze_lead`, `privacywarning`).

### Step 0b: fetch Demandbase schema

Prefer an in-page fetch so the key stays in the browser:

```javascript
async (domain) => {
  const dsc = FollozeState.initialState.data_service_configuration;
  if (!dsc?.api_key) return { error: "no_key" };
  const url =
    "https://api.company-target.com/api/v3/domain.json?key=" +
    encodeURIComponent(dsc.api_key) +
    "&query=" +
    encodeURIComponent(domain);
  const res = await fetch(url);
  if (!res.ok) return { error: "http_" + res.status, cors_or_http: true };
  return await res.json();
}
```

If CORS or network policy blocks that call, curl from the agent shell with the key in an env var. Never print the key, the full URL, or the raw response in Slack if it contains customer enrichment you were not asked to share.

Catalog all returned fields, including top-level fields and `watch_list` fields. Treat the returned JSON as the source of truth for the selected domain only.

### Step 0c: auto-map merge tags to Demandbase fields

Classify mappings as:

| Confidence | Meaning |
| --- | --- |
| HIGH | There is direct evidence that a merge tag maps to a Demandbase field and returned value. |
| MEDIUM | Best inference based on naming and returned schema, but not proven. |
| UNMAPPED_BLOCKER | Mapping cannot be determined or enrichment does not return the required field. |

Keep unmapped fields separate from failed matches. A rule cannot be fairly tested until its merge tag resolves. Designer is where you read the human name of a merge tag.

## Phase 1: propose test plan

Draft a compact test matrix before execution. Include:

- Positive tests: domains expected to match each rule.
- Negative tests: domains expected not to match.
- Null enrichment tests: domains missing a required field.
- Edge cases: multi-value fields, semicolon-delimited values, capitalization, whitespace, closed-list values.

Ask for approval before executing the matrix when the user did not already authorize live testing. If the user already asked to run the test, proceed with a reasonable minimum matrix.

Use URL params only to isolate first-party rules. Use a clean visit that Demandbase can identify (or Demandbase's own test/identify tools) for Demandbase-dependent rules.

## Phase 2: execute tests

For each approved domain:

1. Construct a test URL: `{boardURL}?dom={domain}` (or `&dom={domain}` when the link is already tokenized). Treat this as a domain-attribute test, not as proof of IP identification.
2. Navigate in a clean session and wait for `FollozeState`.
3. Extract `personalization_rules_results`:

```javascript
() => FollozeState.initialState.personalization_rules_results
```

4. If a result is unexpected, verify enrichment through the Demandbase API using the in-page fetch (or curl fallback). Confirm Network One Tag / enrich payload still has account fields.
5. Run a semicolon diagnostic on multi-value fields; do not assume `A;B;C` matches `B` unless evidence proves splitting occurs.
6. Capture screenshots only when visual personalization is part of the assertion. Save them to the agent's workspace or Drive drop. Do not hardcode machine home paths.

Pass/fail for Demandbase: One Tag request present, enrich payload has account fields, liveboard JSON shows those fields, and `personalization_rules_results` is `true` for the expected variant.

## Phase 3: report

Classify issues using these bug classes:

| Class | Symptom | Likely root cause | Fix owner |
| --- | --- | --- | --- |
| Class 1 | Rules return `null` despite API data existing. | Field mapping mismatch, such as spaces versus underscores. | Company Admin / mapping configuration |
| Class 2 | `;`-separated values fail when testing individual values. | Exact string matching; engine does not split delimiters. | R&D or rule design workaround |
| Class 3 | Rules return `false` despite visual similarity. | Leading/trailing spaces, capitalization, picklist mismatch, or exact value mismatch. | Rule editor / support |

Use this report format:

```markdown
## Demandbase Personalization QA — {Customer} Board

| Area | Result | Evidence |
| --- | --- | --- |
| Data service connector | ✅/❌ | data_service_configuration.type = demandbase |
| One Tag / enrich | ✅/❌ | Demandbase network call and account payload |
| Rules discovered | ✅/❌ | {count} rules |
| Merge tag mappings | ✅/⚠️/❌ | {high}/{medium}/{unmapped} |
| API enrichment | ✅/⚠️/❌ | {domain-specific result} |
| Runtime rule results | ✅/⚠️/❌ | personalization_rules_results summary |

### Test Matrix Results
| Domain | Expected | Actual | Rule IDs | Classification | Notes |
| --- | --- | --- | --- | --- |

### Findings
- What is working.
- What is blocked by mapping or enrichment.
- What appears to be rule configuration versus platform behavior.

### Ownership
| Folloze-fixable / support-actionable | Customer / Demandbase / R&D recommendation |
| --- | --- |
| {items} | {items} |
```

Keep conclusions evidence-bound. A `false` result is not automatically a bug; it often means the field resolved but did not equal the rule value exactly. A `null` result is usually a mapping or enrichment-resolution blocker.

## Product sources

- Folloze Demandbase integration: https://help.folloze.com/s/article/Folloze-Demandbase-Integration
- Folloze Demandbase custom fields connector: https://help.folloze.com/s/article/Folloze-Demandbase-Custom-Fields-Connector-Setup
- Test personalization rules: https://help.folloze.com/s/article/Test-Personalization-Rules
- Demandbase Account Connector / One Tag: support.demandbase.com Account Connector FAQs

Connector setup: Demandbase API key from Demandbase Settings, Account Connector, Folloze, plus the Folloze Personalization module.

## Boundaries

- Do not dump JWTs, CSRF tokens, API keys, or cookies into Slack or git.
- Do not treat a dirty browser profile as pass/fail.
- Do not freehand product behavior. If the help corpus is silent, say so.
