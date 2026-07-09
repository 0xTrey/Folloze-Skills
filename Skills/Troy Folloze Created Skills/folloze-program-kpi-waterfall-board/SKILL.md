---
name: folloze-program-kpi-waterfall-board
description: Build and save interactive Folloze MCP boards for program KPI waterfall planning. Use when a user asks to turn the Program KPI workbook, spreadsheet waterfall model, or customer program planning form into a visually polished Folloze board with add-program controls, standard/custom benchmarks, live waterfall calculations, portfolio totals, and MCP analytics.
---

# Folloze Program KPI Waterfall Board

## Purpose

Build a Folloze MCP board that gives customers the same capabilities as the program KPI workbook:

- add as many program sections as needed
- customize the top of the board with the customer's name
- organize the one-year plan by Q1, Q2, Q3, and Q4
- enter quarter, program type, program name, segment, channels, content, notes, accounts targeted, and average deal size
- delete any added program section
- select the customer success manager from `Meghan Richardson`, `Matthew Brown`, `Steven Nguyen`, or `Flor Estrada`
- choose standard or custom benchmarks per program
- calculate account-to-pipeline waterfall values in real time
- show quarterly rollups, cumulative quarter-to-date totals, full-year totals, and shareable waterfall sections
- link the hero `View waterfalls` CTA to a generated cumulative pipeline-waterfall image that updates from the live model
- include an `Output to slides` control that exports the live planner state as slide-ready JSON and opens the generated Google Slides deck when a deck URL is available
- include an `Output to sheets` control that exports the live planner state as sheet-ready JSON and opens the generated Google Sheet when a sheet URL is available

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
9. If a Google Sheet output has been generated, copy the JDP template sheet, add or populate board-output tabs, and replace `SHEETS_OUTPUT_URL_PLACEHOLDER` with the verified Google Sheets edit URL. If no sheet exists yet, leave the placeholder in the skill template but do not save a board with a broken external link.
10. Keep the returned `themeId` for save.
11. QA the local HTML before save.
12. Save with `save_folloze_board_from_file`.

## Template

Use:

```text
/Users/troysmith/.codex/skills/folloze-program-kpi-waterfall-board/assets/program-kpi-waterfall-board-template.html
```

The template is a single self-contained HTML file with:

- Folloze-branded header and first-screen planner positioning
- customer-name placeholder in the hero headline and subcopy
- customer CSM dropdown in the top-right header
- interactive program list
- add, duplicate, and delete program controls
- Q1, Q2, Q3, and Q4 assignment per program
- standard benchmark model: `100% -> 30% -> 10% -> 50% -> 30%`
- custom benchmark inputs
- live full-year totals for programs, pipeline goal, bookings, and meetings
- quarterly rollup cards
- cumulative Q1, Q2, Q3, Q4, and full-year summary table
- generated cumulative pipeline-waterfall image linked from the hero `View waterfalls` CTA
- generated waterfall sections grouped by quarter
- overflow-safe number formatting so large values fit inside cards and tables
- slide-output button that downloads the current planner state as `folloze-program-kpi-slide-output.json` and opens the verified Google Slides deck URL
- sheet-output button that downloads the current planner state as `folloze-program-kpi-sheet-output.json` and opens the verified JDP-template Google Sheet URL
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
- confirm any saved board no longer contains `SHEETS_OUTPUT_URL_PLACEHOLDER` if the sheet-output button is visible
- confirm there are no placeholder `href="#"` or `javascript:void(0)` links
- render desktop and mobile widths
- confirm no horizontal overflow at 390px and 320px
- confirm large currency values fit inside stat, quarter, summary, preview, and waterfall boxes
- add a program and verify the program count increments
- move programs between Q1, Q2, Q3, and Q4 and verify quarterly and cumulative totals update
- delete a program and verify the count, active editor, quarterly rollups, and waterfall sections update
- choose each customer CSM and verify the waterfall sections show the selected CSM
- switch a program to `Custom`, change a benchmark, and verify totals update
- confirm generated waterfall sections are grouped by quarter and match the program count
- click `View waterfalls` and verify it lands on the cumulative pipeline-waterfall image, not only the detailed waterfall section
- click `Output to slides` and verify it calls analytics, exports JSON, and opens the verified deck URL when present
- click `Output to sheets` and verify it calls analytics, exports JSON, and opens the verified JDP-template sheet URL when present
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
