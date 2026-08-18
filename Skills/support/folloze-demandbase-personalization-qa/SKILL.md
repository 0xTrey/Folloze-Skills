---
name: folloze-demandbase-personalization-qa
description: Troubleshoot Folloze personalization rules that depend on the Demandbase data-service integration. Use when a live board should personalize from Demandbase account fields and the operator needs to prove whether Demandbase One Tag, enrichment, and Personalization Studio actually fired. Do not use first-party URL params as proof of Demandbase.
---

# Folloze Demandbase personalization QA

Use this when a Folloze board's personalization rules depend on Demandbase, not when the ask is generic URL-param testing.

## Do not treat as proof

`?dom=`, `?ind=`, `?em=`, `?fn=`, `?var=` only inject first-party URL attributes. They prove first-party identity injection. They do not prove a Demandbase-backed rule fired.

## What has to work

Folloze + Demandbase: Identify, Enrich, Personalize.

1. Demandbase One Tag actually runs on the live board (Network: Demandbase tag/API, not only Folloze liveboard.js).
2. Demandbase returns an account for that visit (IP/cookie identification). If that payload is empty, Personalization Studio has no Demandbase fields to match and the visitor gets the default board.
3. Personalization Studio rules are bound to Demandbase fields (industry, revenue, employee size, journey/intent, custom connector fields), not only to first-party URL attributes.
4. Company Admin has the Demandbase connector and API key. The Folloze Personalization module is required. Custom Demandbase attributes need the custom-fields connector.

## Live checks

Use local Chrome DevTools on the public board URL. Incognito if cookie state is dirty. Do not test logged into Folloze when Strong Lead Identity is in play.

1. View source the liveboard HTML. Find the bootstrap JSON (`var state`). Read `data_service_configuration.type`. If it is `folloze_data_service` with no third-party key, Demandbase rules cannot fire. Stop.
2. Network filter `demandbase`. Confirm One Tag and an identify/enrich response with account fields. No Demandbase call means the integration is not on this board/org.
3. Application: Demandbase cookies vs only Folloze lead cookies (`folloze_lead`, `privacywarning`).
4. Read `personalization.rules` (mergeTagId, compareOperator, values, `_appliedOn`) and `personalization_rules_results`. `false` plus `landing_page: default` means no rule matched.
5. Designer is where you read the human name of a merge tag. The public payload often has only the numeric `mergeTagId`.
6. Ignore rotating hero images when eyeballing. Diff headline, CTA, section copy, and `personalization_rules_results`, not pixels.
7. Do not invent account, industry, intent, or pipeline values.

## First-party vs Demandbase

Use URL params only to isolate first-party rules. Use a clean visit that Demandbase can identify (or Demandbase's own test/identify tools) for DB-dependent rules.

Pass/fail for Demandbase: One Tag request present, enrich payload has account fields, liveboard JSON shows those fields, and `personalization_rules_results` is true for the expected variant.

## Product sources

- Folloze + Demandbase Integration: https://help.folloze.com/s/article/Folloze-Demandbase-Integration
- Custom fields connector: https://help.folloze.com/s/article/Folloze-Demandbase-Custom-Fields-Connector-Setup
- Test personalization rules: https://help.folloze.com/s/article/Test-Personalization-Rules
- Demandbase Account Connector / One Tag: support.demandbase.com Account Connector FAQs

Connector setup: Demandbase API key from Demandbase Settings, Account Connector, Folloze, plus the Folloze Personalization module.

## Boundaries

- Do not dump JWTs, CSRF tokens, API keys, or cookies into Slack or git.
- Do not treat a dirty browser profile as pass/fail.
- Do not freehand product behavior. If the help corpus is silent, say so.
