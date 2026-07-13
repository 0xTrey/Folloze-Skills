---
name: folloze-program-kpi-waterfall-board
description: Build and save interactive Folloze MCP boards for program KPI waterfall planning. Use when a user asks to turn the Program KPI workbook, spreadsheet waterfall model, or customer program planning form into a visually polished Folloze board with add-program controls, standard/custom benchmarks, live waterfall calculations, portfolio totals, and MCP analytics.
---

# Folloze Program KPI Waterfall Board

## Purpose

Build a Folloze MCP board that gives customers the same capabilities as the program KPI workbook:

- add as many program sections as needed
- customize the top of the board with the customer's name
- organize the one-year plan by company/fiscal year, program year, and Q1, Q2, Q3, and Q4
- customize the company year start quarter so sequences such as `Q2 -> Q3 -> Q4 -> Q1` are supported
- enter program year, quarter, program type, program name, primary segment/audience, sub-category segment/audience, multi-select marketing channels, primary and secondary content/messaging category dropdowns, notes, accounts targeted, average deal size, and projected live boards
- delete any added program section
- select the customer success manager from `Meghan Richardson`, `Matthew Brown`, `Steven Nguyen`, or `Flor Estrada`
- choose standard or custom benchmarks per program
- calculate account-to-pipeline waterfall values in real time
- track published boards, actual funnel counts, actual pipeline, and actual bookings against the projected benchmark model for each program
- show quarter-only rollups, fiscal year-to-date totals, full-year totals, board-creation growth by quarter, projected-vs-actual totals, and shareable waterfall sections
- link the hero `View waterfalls` CTA to a generated cumulative pipeline-waterfall image that updates from the live model
- include an `Output to slides` control that exports the live planner state as slide-ready JSON and opens the generated Google Slides deck when a deck URL is available
- include an `Output to sheets` control that posts the live planner state to the sheet-builder web app, copies the JDP template workbook, populates the customer-specific program tabs, and opens the generated customer Google Sheet
- include a `Pull Impact Dashboard` control that filters the configured Salesforce Impact Dashboard by the board customer name and renders the view directly in an Impact Dashboard section

## Required MCP Flow

1. Ask for the customer's name if the user has not already provided it. Do not save a board with the literal `CUSTOMER_NAME_PLACEHOLDER`.
2. Read the active Folloze landing page creation guide with `get_folloze_landing_page_creation_guide`.
3. Ask the user whether to use the Folloze company theme before calling `get_company_theme`.
   - Recommend `yes` for Folloze-owned/customer-planning boards.
   - Do not assume the answer.
4. Call `get_company_theme` with the user-authorized `use_folloze_theme` value.
5. Copy `assets/program-kpi-waterfall-board-template.html` to a durable workspace path.
6. Replace `THEME_URL_PLACEHOLDER` in the copied HTML with the returned `themeUrl`.
7. Replace every `CUSTOMER_NAME_PLACEHOLDER` token with the HTML-escaped customer name.
8. If a Google Slides deck has been generated, replace `SLIDES_DECK_URL_PLACEHOLDER` with the verified Google Slides edit URL. If no deck exists yet, leave the placeholder in the skill template but do not save a board with a broken external link.
9. Deploy `assets/google-sheets-output-webapp.gs` as a Google Apps Script web app with access to the Folloze Google Drive account. Replace `SHEET_BUILDER_ENDPOINT_URL_PLACEHOLDER` with the deployed web app URL. The web app copies the JDP template workbook, titles the copy with the customer name, populates `Customer Program Form` and `Programs and KPIs` from the board payload, and returns the generated customer workbook URL. Do not use `SHEETS_OUTPUT_URL_PLACEHOLDER` as a generic template link for the `Output to sheets` button.
10. Replace `SALESFORCE_IMPACT_DASHBOARD_URL_PLACEHOLDER` with the verified Salesforce Impact Dashboard URL. The current default internal Impact Dashboard is `https://folloze.my.salesforce.com/lightning/r/Dashboard/01Z2I000000ls2WUAQ/view`.
11. Keep the returned `themeId` for save.
12. QA the local HTML before save.
13. Save with `save_folloze_board_from_file`.

## Template

Use:

```text
${CODEX_HOME:-$HOME/.codex}/skills/folloze-program-kpi-waterfall-board/assets/program-kpi-waterfall-board-template.html
```

Resolve the template path from the installed skill directory first. If the skill is running from a checked-out repo instead of `~/.codex/skills`, use the `assets/` folder next to this `SKILL.md`.

The template is a single self-contained HTML file with:

- Folloze-branded header and first-screen planner positioning
- customer-name placeholder in the hero headline and subcopy
- customer CSM dropdown in the top-right header
- interactive program list
- add, duplicate, drag-to-reorder, and delete program controls
- per-program lock toggle that disables detail edits until unlocked
- planning-year and company-year-start controls
- per-program year dropdown with `2026`, `2027`, `2028`, and `2029`
- Q1, Q2, Q3, and Q4 assignment per program
- fiscal quarter sequencing that can wrap Q1 to the end of the company year
- collapsed multi-select channel picker that shows selected channels first, expands with an Edit button, and commits selections with a Submit button
- standard benchmark model: `100% -> 30% -> 10% -> 50% -> 30%`
- custom benchmark inputs
- projected live board and published board tracking
- actuals inputs for engaged accounts, meetings, pipeline opportunities, closed deals, pipeline, and bookings
- live full-year totals for programs, projected boards, published boards, pipeline goal, actual pipeline, bookings, actual bookings, and meetings
- quarterly rollup cards that show each fiscal period independently
- quarter/YTD summary table with fiscal-period rows, year-to-date rows, projected values, and actual values
- generated cumulative pipeline-waterfall image linked from the hero `View waterfalls` CTA
- generated waterfall sections grouped by quarter
- overflow-safe number formatting so large values fit inside cards and tables
- slide-output button that downloads the current planner state as `folloze-program-kpi-slide-output.json` and opens the verified Google Slides deck URL
- sheet-output button that submits the current planner state to the configured sheet-builder web app; the web app copies the JDP template workbook, writes `Customer Program Form` rows and `Programs and KPIs` sections from the live board data, then opens the generated customer-named Google Sheet
- the visible `Output to sheets` button must never download a JSON file as its normal behavior; if the sheet-builder endpoint is missing, show a setup-needed state rather than opening the generic template or downloading JSON
- impact-dashboard button and section that use the customer name in the hero title to filter Salesforce with `fv0=<customer name>` and embed the configured Impact Dashboard
- analytics wiring for CTAs, nav, tab switches, model updates, add/remove actions
- local `flzAnalytic` fallback for browser QA

## Copy And Positioning

Use customer-ready language. Keep the page focused on the planner itself, not on internal production language.

Preferred framing:

- `Plan [Customer]'s one-year program mix from engagement to pipeline.`
- `Build the year by quarter, tune benchmarks, model the waterfall.`
- `Every quarter gets ready-to-share program waterfalls.`

Avoid visible terms such as `demo`, `template`, `internal`, `agent`, or `proof of concept` unless the user explicitly asks.

## QA Checklist

Before saving:

- confirm the theme link in `<head>` is no longer `THEME_URL_PLACEHOLDER`
- confirm the HTML no longer contains `CUSTOMER_NAME_PLACEHOLDER`
- confirm the hero headline includes the customer name
- confirm any saved board no longer contains `SLIDES_DECK_URL_PLACEHOLDER` if the slide-output button is visible
- confirm any saved board no longer contains `SHEET_BUILDER_ENDPOINT_URL_PLACEHOLDER` when the sheet-output button is expected to create Google Sheets directly
- confirm any saved board no longer contains `SALESFORCE_IMPACT_DASHBOARD_URL_PLACEHOLDER` if the impact-dashboard button is visible
- confirm there are no placeholder `href="#"` or `javascript:void(0)` links
- render desktop and mobile widths
- confirm no horizontal overflow at 390px and 320px
- confirm large currency values fit inside stat, quarter, summary, preview, and waterfall boxes
- add a program and verify the program count increments
- drag programs in the list and verify their order changes without changing quarter assignment or calculations
- lock a program and verify detail fields, benchmark controls, and remove controls are disabled until unlocked
- move programs between Q1, Q2, Q3, and Q4 and verify quarterly and cumulative totals update
- change the company year start to Q2 and verify the displayed period order becomes `Q2 -> Q3 -> Q4 -> Q1`
- choose program years `2026`, `2027`, `2028`, and `2029` and verify the year appears in quarter rollups, waterfall sections, and sheet export payloads
- click the channel Edit button, select more than one channel, click Submit, and verify the program stores/exports all selected channels
- enter projected live boards and published boards and verify board growth, attainment, quarter cards, and YTD totals update
- enter actual pipeline and bookings and verify actual-vs-projected attainment updates
- delete a program and verify the count, active editor, quarterly rollups, and waterfall sections update
- choose each customer CSM and verify the waterfall sections show the selected CSM
- switch a program to `Custom`, change a benchmark, and verify totals update
- confirm generated waterfall sections are grouped by quarter and match the program count
- click `View waterfalls` and verify it lands on the cumulative pipeline-waterfall image, not only the detailed waterfall section
- click `Output to slides` and verify it calls analytics, exports JSON, and opens the verified deck URL when present
- click `Output to sheets` and verify it calls analytics, posts the board payload to the sheet-builder endpoint, and opens a newly generated customer workbook populated from the board data
- confirm `Output to sheets` does not download `folloze-program-kpi-sheet-output.json` from the live board
- click `Pull Impact Dashboard` and verify the Impact Dashboard section scrolls into view and the iframe URL includes `fv0=<customer name>`
- confirm CTA buttons and meaningful interactions call `flzAnalytic`

Suggested local Playwright-style check:

```bash
node - <<'NODE'
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file://' + path.resolve(process.argv[1]);
  const browser = await chromium.launch({ headless: true });
  for (const viewport of [{width:1440,height:1000},{width:390,height:900},{width:320,height:840}]) {
    const page = await browser.newPage({ viewport });
    await page.goto(file, { waitUntil: 'load' });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    if (overflow) throw new Error(`Horizontal overflow at ${viewport.width}`);
    await page.close();
  }
  await browser.close();
})();
NODE /absolute/path/to/copied-board.html
```

## Save

Use `save_folloze_board_from_file` with:

- `name`: a clear board name, usually `Program KPI Waterfall Planner`
- `path`: absolute path to the QA'd local HTML file
- `themeId`: returned from `get_company_theme`
- `analyticsAcknowledgements.readGuide`: true only after reading the MCP guide
- `analyticsAcknowledgements.ctaClicksTracked`: true only after confirming CTA analytics
- `analyticsAcknowledgements.customInteractionsTracked`: true only after confirming model/nav/tab/add/remove/export interactions
- `analyticsAcknowledgements.externalLinksHaveTargetBlank`: true; the template does not use external URLs by default, and any added external links must use `target="_blank" rel="noopener"`

If the MCP save returns `needs_fix`, patch the durable local HTML file, rerun targeted QA, then retry saving the same file.

## Final Response

Return:

- board ID
- exact MCP-returned designer/live URL
- local source path
- public deployment status if the MCP did not return a public URL
- any tracker or QA caveat
