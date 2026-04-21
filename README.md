# Folloze Skills

Central source of truth for Folloze Codex skills and the team rollout pattern behind them.

This repo is the managed distribution point for the GTM team's shared AI skills. Skills live here, updates are reviewed here, and each teammate syncs this repo into `~/.codex/skills` from one clean local clone.

## Why The Repo Clone Matters

Cloning the repo locally is the correct model for this rollout.

You are centralizing skill ownership and updates for the wider GTM team. A stable local clone gives each teammate:

- one source of truth to pull from
- a clean git worktree the updater can verify before syncing
- a disposable local install under `~/.codex/skills` that can be refreshed from the repo instead of hand-edited

This is more reliable than treating the GitHub installer as the update channel. GitHub install is useful for initial access, but the repo clone is what makes ongoing managed updates predictable.

## Recommended Team Setup

Use this repo as the only place where skill code and instructions are edited. Do not hand-edit skills separately in each person's `~/.codex/skills` directory.

The recommended rollout model is:

1. Each teammate clones this repo to a stable local path such as `~/Projects/Folloze-Skills`
2. They run `python3 scripts/sync_codex_skills.py --overwrite`
3. The sync script links or copies each repo skill into `~/.codex/skills`
4. They create the recurring Codex automation defined in `AutomationTemplates/folloze-skills-weekly-update/template.json`
5. Teammates restart Codex after skill updates so the app reloads the changed skill files

This repo is the source of truth. The recommended automatic update path is a Codex automation, not `launchd`.

If someone wants the setup to be callable from inside Codex instead of shell-first, use the `skills-update-folloze` skill in this repo. That skill is the conversational entrypoint for both one-off refreshes and creating the weekly updater automation.

## What "Automatic Update" Means Here

GitHub push alone will not update a teammate's installed skills.

To make updates propagate automatically, you need two layers:

- this repo as the source of truth
- a local scheduled sync mechanism on each machine that pulls the repo and refreshes `~/.codex/skills`

The repo now includes:

- `skills-manifest.json`
- `scripts/sync_codex_skills.py`
- `scripts/validate_skills.py`
- `AutomationTemplates/folloze-skills-weekly-update/template.json`
- `ops/launchd/com.folloze.codex-skills-sync.plist.template`

The Codex automation template is the recommended default. The `launchd` plist remains here as a machine-level fallback for teammates who specifically want OS-managed scheduling instead of a Codex automation.

## Initial Rollout

From a teammate machine:

```bash
git clone https://github.com/0xTrey/Folloze-Skills.git ~/Projects/Folloze-Skills
cd ~/Projects/Folloze-Skills
python3 scripts/sync_codex_skills.py --overwrite
```

Then create the recurring Codex automation described in `AutomationTemplates/folloze-skills-weekly-update/template.json`.

The standard automation is:

- name: `Folloze Skills Weekly Update`
- schedule: every Wednesday at 12:00 PM in the teammate's local time zone
- scope: only the shared Folloze skills repo and the local Codex skills install

For teammates who prefer a lower-level machine scheduler instead of Codex automation:

1. Copy the `launchd` template in `ops/launchd/`
2. Replace `__REPO_ROOT__` with that teammate's local clone path
3. Load it with `launchctl`

## Governance

Use normal software delivery rules here:

- Protect `main`
- Require PR review for skill changes
- Run validation on every PR
- Avoid machine-specific absolute paths in skills
- Keep secrets and personal tokens out of the repo

If these skills include internal sales process, GTM workflow, or customer-specific implementation details, this repo should be private before full team rollout.

## Structure

- `Skills/`
- `AutomationTemplates/`
- `scripts/`
- `ops/`
- `.github/workflows/`

Each skill lives in its own subdirectory so it can carry its own `SKILL.md`, scripts, references, and agent config.

## Included Skills

### `account-org-chart`
Builds a company org chart workbook across Marketing, Sales, IT, Digital, AI, Strategy, and Product Marketing, then uploads the result into the correct company folder in Google Drive as a native Google Sheet.

### `folloze-sales-doc`
Builds branded Folloze sales and customer lifecycle documents such as discovery prep docs, stakeholder maps, onboarding plans, QBRs, renewal prep docs, and account summaries using the shared Folloze design system.

### `sales-to-cs-internal-handoff-folloze`
Runs the Folloze closed-won Sales to Customer Success internal handoff workflow, creating the internal handoff doc, instance request, onboarding kickoff deck, Drive artifacts, and Slack handoff links.

### `Salesforce-Update`
Manually reconciles Salesforce open opportunities from Gmail, Google Calendar, and Granola evidence, then writes validated updates through the local Salesforce helper flow.

### `skills-update-folloze`
Bootstraps or updates the shared Folloze skills repo on a teammate machine, then runs or helps create the standard weekly Codex updater automation for the team.

### `weekly-customer-action-items`
Builds a weekly by-account summary of unresolved or unanswered customer action items across Granola, Gmail, and Slack for customer follow-up review.

## Conventions

- Put each skill in `Skills/<skill-name>/`
- Keep the runnable instructions in `SKILL.md`
- Put helper scripts in `scripts/` when the skill needs automation
- Put reference docs and examples in `references/`
- Keep skills machine-independent and avoid user-specific absolute paths
- Avoid generated artifacts and local caches in git
