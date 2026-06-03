# MCP And API Routing

Use this reference after the intake brief is complete.

## Default Choice

Default to MCP rich HTML for Zoom-note deal rooms.

Zoom recaps usually contain nuanced buyer context, objections, next steps, and resource needs. A custom HTML deal room gives better control over section order, mutual action plans, resource modules, analytics, and buyer-safe translation than a fixed template payload.

## Choose MCP Rich HTML When

- The page needs account-specific narrative.
- The buyer needs a curated resource center.
- The deal requires MSA, infosec, proposal, or implementation modules.
- There are absent stakeholders who need role-specific proof.
- The next step is a meeting, proposal review, or internal team review.
- The page needs custom interactions, tabs, modals, drawers, calculators, or timelines.
- You need to update an existing board.

MCP flow:

1. Call the current Folloze landing-page creation guide.
2. Resolve theme mode with the user if not already authorized.
3. Build a single self-contained HTML file in a git-backed workspace.
4. Preview and QA desktop/mobile.
5. Save through MCP only after explicit save/update/publish intent.
6. Return the exact board ID and URL returned by MCP.

## Choose External Board API When

- The user asks for speed over custom experience.
- Fixed template sections are acceptable.
- The output is a simple deal room, resource center, or account board.
- No custom interactions or section additions are needed.
- No existing board update is required.

API flow:

1. Select an approved template.
2. Fetch template sections if needed.
3. Replace only supported text/image fields.
4. Create the board through the configured API workflow.
5. Return the board ID and URL.

Do not place API credentials, tokens, or Basic auth values in this skill package.

## Choose Brief Only When

- Account identity is unresolved.
- Source notes are too thin.
- The user has not decided whether the output is Folloze-owned or vendor-owned.
- Required resources are missing.
- The ask is only to scope, summarize, or plan.

## Board Identity Checklist

Before any save:

- Save intent: new board or existing-board update.
- Board name.
- Account name and audience.
- Source note date.
- Brand owner.
- Theme mode and theme ID.
- Local HTML path if using MCP.
- Existing or returned board ID.
- Public deployment status.

If any item conflicts with the source note or user instruction, stop and resolve it before saving.
