# Account build and QA

## Intake

Minimum input is the account and the decision the playbook should support. Begin with the available authorized sources. If a missing input changes the recommendation, flag it while continuing the local draft. Keep a private ledger with columns for claim or asset, source and date, verified or proposed status, and whether it is cleared for the visitor page. Never include the ledger in the HTML.

## Build

1. Copy [account.example.json](../assets/account.example.json) into the account's working folder as `account.json`. The example is fictional. Replace its assumptions and copy.
2. Run the skill's builder from the deal repo with Python 3.11 or later. Use the installed skill directory in the command.

   ```bash
   python3 "$ABM_PLAYBOOK_SKILL/scripts/build.py" path/to/account.json --out path/to/review-output
   ```

   Set `ABM_PLAYBOOK_SKILL` to the directory containing the skill's `SKILL.md`. The builder writes `review.html` for local review and `fragment.html` for an authorized Folloze HTML section. Re-run from the same brief to update both. If the deal needs copy or layout changes beyond the brief, copy the build kit into the deal repo and customize the source templates there.

| Brief field | What to supply |
| --- | --- |
| `account`, `hero_summary` | Approved display name and the buyer decision. Optional `account_logo` is a path relative to the brief. Without it, the header uses the account name as text. |
| `math` | `currency` (ISO code, USD by default), `target`, `opportunity_size`, `engagement_rate`, `opportunity_rate`, `illustrative_win_rate`, optional `note`. Enter percentages as 25 for 25%. Omit unknown amounts or rates. The win-rate illustration defaults to 25%. Use the note for source and scope or to label a scenario. |
| `campaign_summary`, `workflow_inputs`, `seller_action` | One campaign, the signals that drive selection, and what the seller does with engagement. Optional `research_tools` and `channels` are short lists of confirmed names or explicitly marked options. |
| `account_builds`, `pilot_summary`, `pilot_steps` | Buyer-owned work, pilot scope and success decision, and an ordered list of steps with `title` and `detail`. Put approved counts and thresholds here when available. |
| `stages` | Optional `acquire`, `educate`, and `convert` overrides. Each takes optional `description`, `model`, and `example`. Without an example the card shows the recommendation only. |

A stage example can use this shape. The domains and paths below are structural examples. Replace them with verified, audience-accessible URLs and assets.

```json
{
  "title": "Operations campaign",
  "url": "https://example.com/operations",
  "label": "Open operations campaign",
  "thumbnail": {"file": "assets/operations.jpg", "alt": "Operations campaign homepage"},
  "caption": "A campaign tailored by industry.",
  "links": [{"label": "Open executive dinner", "url": "https://example.com/dinner"}],
  "copy_links": [{"label": "Example audience", "url": "https://example.com/operations?segment=example"}]
}
```

Only `title` and `url` are required on an example. Use approved thumbnails and logos relative to the brief, preferably compressed JPG, PNG, WebP, or SVG. Match the screenshot to the generic destination. Use `copy_links` only when personalization depends on a clean session. Copy the variant URL and open it manually in a fresh Incognito window. Verify the general URL separately.

## Acceptance checks

- Check the account's name, logo, goals, channels, and examples against the evidence ledger. Search the generated HTML and asset list for the previous account's names, domains, board IDs, figures, and internal notes.
- On desktop, check all six chapters, the Next and Previous controls, keyboard focus, and longer content on a laptop viewport. On mobile, check reading order, the calculator fields, and horizontal overflow. Check reduced motion and print preview with all chapters and the calculator assumptions visible.
- Test the default math, one edited value, and an invalid value. For the fictional sample, $12M at $150K with 25% engagement and 20% conversion requires 1,600 accounts, 400 engaged, and 80 opportunities. The separate 25% win-rate illustration gives 20 wins.
- Check actual link destinations, clickable thumbnails, and new tabs. For copy buttons, verify the clipboard value and a selectable manual URL when clipboard access is denied. Check audience access and the personalized visitor result.
- For a release, read the current Folloze HTML section guide and Analytics Tracking skill before making changes. Verify hosted assets and the rendered board after saving and again after publishing. Verify at least one visitor action end to end through the available analytics evidence. Report transport separately from reporting.
