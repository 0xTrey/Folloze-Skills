# Hitachi Vantara Demo Pack Publication Plan

Updated: 2026-08-05

| Experience | Board name | Board ID | Designer URL | Public URL | Source | Vanity slug | Save | Publish | Public QA | Tracker |
|---|---|---:|---|---|---|---|---|---|---|---|
| Campaign | Hitachi Vantara - AI-Ready Data Foundation | 249545 | https://app.folloze.com/app/board/249545/designer | https://engage.folloze.com/hitachi-ai-ready-data-foundation | `artifacts/hitachi-demo-pack/hitachi-ai-ready-data-foundation.html` | `hitachi-ai-ready-data-foundation` | custom Hitachi theme; no Folloze company theme | republished / Published | HTTP 200, no redirect, anonymous guest, expected H1, custom theme tokens, matching hash `529756b...` | row 156 |
| One-to-one | Hitachi Vantara x BMW Group - Production Data Foundation | 249544 | https://app.folloze.com/app/board/249544/designer | https://engage.folloze.com/hitachi-bmw-production-data-foundation | `artifacts/hitachi-demo-pack/hitachi-bmw-production-data-foundation.html` | `hitachi-bmw-production-data-foundation` | custom Hitachi theme; no Folloze company theme | republished / Published | HTTP 200, no redirect, anonymous guest, expected H1, custom theme tokens, matching hash `dc3c2c9...` | row 157 |
| Event | Hitachi Vantara - AI Success Starts With the Right Data Foundation | 249546 | https://app.folloze.com/app/board/249546/designer | https://engage.folloze.com/hitachi-ai-data-foundation-on-demand | `artifacts/hitachi-demo-pack/hitachi-ai-data-foundation-on-demand.html` | `hitachi-ai-data-foundation-on-demand` | custom Hitachi theme; no Folloze company theme | republished / Published | HTTP 200, no redirect, anonymous guest, expected H1, custom theme tokens, matching hash `6dca206...` | row 158 |

Operational rule: MCP save, designer URL, online state, vanity URL, anonymous HTTP/DOM verification, tracker readback, local commit, and Slack delivery are separate checkpoints.

Theme correction: the three experiences use a custom Hitachi Vantara visual system harvested from Hitachi's current digital properties. The Folloze theme ID `5374` and stylesheet link remain only because the MCP save contract requires them; no Folloze visual variables are used, and custom Hitachi CSS owns the rendered pages.

## DSR tile delivery

All three covers follow the Folloze digital sales room contract: 1672 by 941 PNG, official Hitachi Vantara logo, centered motion label, branded blue field, and restrained geometric texture.

| Experience | Local asset | Shared Drive file ID |
|---|---|---|
| Campaign | `artifacts/hitachi-demo-pack/cards/249545-hitachi-vantara-ai-ready-data-campaign-tile.png` | `1_gvqSf50yRGuACA0r0s-EwGmE4j1qDcs` |
| One-to-one | `artifacts/hitachi-demo-pack/cards/249544-hitachi-vantara-bmw-production-data-abm-tile.png` | `1Fidex0fbcydiDfVuVCLtIhXTnNpaYXgn` |
| Event | `artifacts/hitachi-demo-pack/cards/249546-hitachi-vantara-ai-data-foundation-event-tile.png` | `12oIzIkFIIma52v8bsaS34RsvGH_rs__L` |

## Slack delivery

- Recipient: Troy Smith (`U08FTRBFX1R`), direct-message channel `D08GUFP2CKB`.
- Published URL message: https://folloze.slack.com/archives/D08GUFP2CKB/p1785954662635929
- Asset delivery message: https://folloze.slack.com/archives/D08GUFP2CKB/p1785954678900189
- Custom Hitachi theme correction: https://folloze.slack.com/archives/D08GUFP2CKB/p1785956651592609
- Disclosure: all messages identify themselves as automated Codex delivery.
- Asset delivery: the connected Slack account lacks `files:write:user`, so binary attachment upload was unavailable. The approved fallback was used: all three exact PNGs were linked individually from the shared Drive library, and Troy Smith was granted direct reader access to every file.
