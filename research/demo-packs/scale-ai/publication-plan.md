# Scale AI Demo Pack Publication Plan

Updated: 2026-07-20

## Live-Save Authorization

- Save intent: create three net-new Folloze boards from the verified local HTML files.
- User authorization to publish: confirmed on 2026-07-20.
- Folloze company-theme choice: no, explicitly authorized by Trey on 2026-07-20.
- Theme mode: no Folloze company theme, preserving Scale AI's source-brand system.
- Theme ID: `4`.
- Required theme stylesheet: `https://cdn.folloze.com/theme/135433/4.css?v=1764160175`.
- Folloze landing-page creation guide: read on 2026-07-20.
- Guide preflight: custom CSS and JavaScript moved from `<head>` to `<body>` in all three source files; canonical doctype and ARIA grouping fixes applied.
- Post-restructure QA: HTML validation passed with the guide-mandated body-style exception; scripts parsed; Customer Operations, Data Scientist, and Protect tab changes worked; 320px overflow and broken-image checks returned zero; browser console errors returned zero.
- All three boards were saved, published, assigned the planned vanity slugs, verified from an anonymous HTTP client, and logged in the canonical tracker on 2026-07-20.

## Board Identities

| Experience | Folloze board name | Local source | Planned vanity slug | Board ID | Designer URL | Public URL |
| --- | --- | --- | --- | --- | --- | --- |
| Campaign landing page | Scale AI \| Production Systems Campaign | `artifacts/scale-ai-demo-pack/scale-ai-production-systems-campaign.html` | `scale-ai-production-systems` | `248053` | `https://app.folloze.com/app/board/248053/designer` | `https://experience.folloze.com/scale-ai-production-systems` |
| One-to-one account page | Scale AI + Mayo Clinic \| Reliable Care Workflow | `artifacts/scale-ai-demo-pack/scale-ai-mayo-clinic-reliable-care.html` | `scale-ai-mayo-reliable-care` | `248055` | `https://app.folloze.com/app/board/248055/designer` | `https://experience.folloze.com/scale-ai-mayo-reliable-care` |
| Event promotion page | Scale AI \| Churn Prevention Through Experimentation | `artifacts/scale-ai-demo-pack/scale-ai-churn-prevention-webinar.html` | `scale-ai-churn-prevention` | `248056` | `https://app.folloze.com/app/board/248056/designer` | `https://experience.folloze.com/scale-ai-churn-prevention` |

## Vanity Preflight

- `https://experience.folloze.com/scale-ai-production-systems` returned the Folloze `Page not found` title before publication.
- `https://experience.folloze.com/scale-ai-mayo-reliable-care` returned the Folloze `Page not found` title before publication.
- `https://experience.folloze.com/scale-ai-churn-prevention` returned the Folloze `Page not found` title before publication.
- The three slugs were applied through each board's Folloze General settings on 2026-07-20.
- Post-change anonymous checks returned HTTP 200 for all three URLs. Each response identified an anonymous guest session, the expected board ID and vanity slug, and the expected page headline.

## Tracker Plan

- Spreadsheet: `MCP Demo Environments - May 2026`
- Spreadsheet ID: `1s_NU2O7lO8f_QSVmP2mI5dBNOGgUh7oQo3bfenerMqk`
- Tab: `Demo Environments`
- Sheet ID: `2052206331`
- Live headers: `Company name`, `Board Name`, `Deployment URL`, `Designer edit URL`, `Needed By Date`, `Production Date`, `Board Builder`, `Agent Notes`.
- No existing `Scale AI` row was found in the bounded `A1:I140` search.
- Rows `107:109` were confirmed blank immediately before the write.
- All eight mapped columns were written in one bounded `updateCells` request:
  - `Demo Environments!A107:H107`: Production Systems Campaign
  - `Demo Environments!A108:H108`: Mayo Clinic Reliable Care Workflow
  - `Demo Environments!A109:H109`: Churn Prevention Through Experimentation
- API readback and a native Google Sheets visual check confirmed the three rows, clickable public/designer links, production date, builder, and status notes.

## Completion Gates

For each board, require separate evidence for:

1. Final guide-compliant local source with the authorized Folloze theme stylesheet.
2. Successful Folloze save returning a board ID and exact designer URL.
3. Vanity slug applied in the Folloze designer.
4. Board published through the Folloze designer.
5. Anonymous public URL returning the intended page, not merely HTTP 200.
6. Tracker row written with the public and designer URLs.
7. Local publication record updated with board, theme, publish, tracker, QA, and git states.

## Completion Record

| Gate | Campaign | Mayo Clinic | Churn webinar |
| --- | --- | --- | --- |
| Local source | complete | complete | complete |
| Folloze save | board `248053` | board `248055` | board `248056` |
| Designer publish | `Published`; Publish disabled | `Published`; Publish disabled | `Published`; Publish disabled |
| Vanity slug | `scale-ai-production-systems` | `scale-ai-mayo-reliable-care` | `scale-ai-churn-prevention` |
| Anonymous public verification | HTTP 200; board, slug, headline, and anonymous guest verified | HTTP 200; board, slug, headline, and anonymous guest verified | HTTP 200; board, slug, headline, and anonymous guest verified |
| Tracker | row `107` | row `108` | row `109` |

- Folloze theme: no Folloze company theme; theme ID `4`.
- Tracker: `MCP Demo Environments - May 2026`, tab `Demo Environments`.
- GitHub remote push: not requested.
