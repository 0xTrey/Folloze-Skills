---
name: folloze-demo-pack-builder
description: Orchestrate repeatable Folloze demo example packs from one company name. Use when the user asks for a company-specific pack of demo examples, campaign landing page, one-to-one account page, event promotion page, subagent-driven demo research, or customer-ready Folloze experiences built separately through Folloze-MCP-Demo-Builder.
---

# Folloze Demo Pack Builder

Use this skill to turn one company name into a repeatable pack of three customer-ready Folloze examples. The pack is an orchestration workflow, not a single board.

## Core Rule

Every pack contains three separate experiences:

- Campaign landing page
- One-to-one account page
- Event promotion page

Kick off each experience separately with `Folloze-MCP-Demo-Builder`. Each one needs its own board identity, source truth, motion, local source path, QA record, save status, and final handoff. Do not collapse the pack into one board, one HTML file, or one shared generic story.

## Skill Routing

- Use `brand-harvester` first when public brand/source DNA is needed and the source is reachable.
- Use `Folloze-MCP-Demo-Builder` for each board's identity, source-design DNA, experience shape, message spine, local HTML build, QA, MCP save, tracker handling, and final status rules.
- Use `folloze-brand-kit` only when the requested pack is Folloze-owned or Folloze-branded. For vendor-owned examples, keep Folloze invisible in buyer-facing copy.
- Read `references/pack-orchestration.md` before planning subagents, source ledgers, or full pack production.
- Read `references/experience-briefs.md` before drafting the campaign, one-to-one, and event briefs.

## Working Order

1. Resolve the company: canonical name, homepage, product/category, aliases, and disambiguation risks.
2. Decide pack mode: local-preview only, Folloze save intended, or existing-board update. If save/publish is intended, follow `Folloze-MCP-Demo-Builder` theme-mode and MCP guide requirements before any live save.
3. Build a source ledger with public, user-approved, internal-planning-only, and blocked evidence labels.
4. Launch bounded subagents when available and useful. Keep source lanes distinct so agents do not duplicate research.
5. Synthesize the research into one pack strategy, then three separate experience briefs.
6. Run `Folloze-MCP-Demo-Builder` separately for the campaign page, one-to-one page, and event page.
7. Run the demo pack quality loop on each board independently, then compare the pack side by side.
8. Save to Folloze only after the user explicitly asks to save, publish, update, or push to Folloze. The main agent owns all MCP saves, tracker writes, git commits, and final status reporting.

## Source Rules

Use current public research for company, product, campaign, proof, customer, and event facts. Do not rely on memory for facts that can drift.

Visible claims may come only from:

- Public vendor pages
- Public target-account sources
- Public proof assets
- User-approved copy or user-provided approved facts

Private notes from Gmail, Granola, Salesforce, Slack, meeting notes, or internal docs may shape strategy only. Translate them into public-market hypotheses and keep them out of buyer-facing copy unless the user explicitly approves the exact claim.

Do not invent metrics, customers, awards, integrations, outcomes, urgency, event dates, speakers, sponsors, or registration details.

## Experience Brief Contract

Before building HTML, create a separate brief for each experience:

- Experience type and motion
- Holistic buyer goal
- Target audience, segment, account, or event audience
- Message spine: context, why change, why now, vendor promise, proof, next action
- Experience shape and section order
- Brand/source DNA inputs
- Public-source claim set and proof assets
- CTA strategy and real destinations/actions
- Local source path plan and QA artifact plan
- Save intent: local-only, net-new Folloze board, or existing-board update

If any brief is generic enough that another company could use it after a logo swap, stop and sharpen it before building.

## Demo Pack Quality Loop

Treat copy quality as a launch gate. The requested Gary Halbert/Gary Halpert flavor means direct-response discipline, not imitation: sharp hook, real buyer tension, concrete promise, proof close to the claim, short active sentences, and a clear CTA. Do not quote, mimic, or rewrite from any copyrighted source.

For each board:

1. Run a public-source proof pass.
2. Run a customer-ready copy pass.
3. Run source-brand fidelity and component-token checks.
4. Run CTA, link, analytics, interaction, asset, mobile, accessibility, and render QA.
5. Fix failures and repeat until the board passes or a real blocker is documented.

Remove visible language about demos, examples, templates, proof-of-concepts, boards, microsites, source paths, build choices, content selection, or why a section exists. Every section must add proof, decision help, role-specific value, urgency, or a useful next action.

The pack is not complete until all three boards pass independently. Then compare the three together and reject any board that feels templated, generic, repetitive, or interchangeable after swapping logos.

## Final Status

Report the pack as three separate operational states:

- Campaign landing page: local source, QA status, board ID, designer/live URL, public deployment status, tracker status, commit status
- One-to-one page: local source, QA status, board ID, designer/live URL, public deployment status, tracker status, commit status
- Event promotion page: local source, QA status, board ID, designer/live URL, public deployment status, tracker status, commit status

Do not imply that local QA, Folloze save, tracker write, git commit, GitHub push, or public deployment happened because another state completed.
