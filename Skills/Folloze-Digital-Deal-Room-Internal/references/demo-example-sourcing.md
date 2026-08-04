# Demo Example And Tile Sourcing

Use the canonical MCP Demo Environments Google Sheet for board identity and URLs. Use the company-wide Drive tile library for preview artwork. Do not assume Luke can access Trey's local demo repository.

## Canonical tracker

- Spreadsheet: `MCP Demo Environments - May 2026`
- Spreadsheet ID: `1s_NU2O7lO8f_QSVmP2mI5dBNOGgUh7oQo3bfenerMqk`
- Tab: `Demo Environments`
- Current columns:
  - `A` Company name
  - `B` Board Name
  - `C` Deployment URL
  - `D` Designer edit URL
  - `E` Needed By Date
  - `F` Production Date
  - `G` Board Builder
  - `H` Agent Notes
  - `I` Board ID

Read spreadsheet metadata first, then read only `A1:I1` to confirm the tab and headers. Search the bounded company-key column to identify candidate row numbers, then read only each exact candidate range such as `A151:I151`. Do not fetch the full `A:I` table, scan an unbounded grid, or assume column positions when headers have changed.

Treat tracker access as a preflight gate. If Luke's connected Google account or Codex connector cannot read the spreadsheet metadata and header row, stop before adding examples and ask Trey to grant viewer access. Do not replace the tracker with Trey's local repo, guessed URLs, or stale copied rows.

For each candidate row:

1. Confirm the company/use case belongs to the demo pack relevant to the current deal.
2. Require a real Board ID and HTTPS Deployment URL.
3. Prefer production `https://experience.folloze.com/...` URLs with notes showing published/Online and anonymous verification.
4. Reject `Deployment URL pending`, blank URLs, dead URLs, local preview URLs, and QA/staging URLs unless Trey explicitly requests a non-production example.
5. Use column C as the buyer-facing card destination.
6. Keep column D as private internal evidence only; never link a buyer-facing tile to the designer URL.
7. Use the Board Name as the starting title, shortening it only when needed for the template while preserving the motion/use case.

Record spreadsheet ID, tab, row number, Board ID, board name, deployment URL, designer URL, builder, production date, and verification note in the private receipt. Re-read only the selected exact row ranges immediately before modifying the board.

## Company-wide tile library

- Shared drive: `Folloze General`
- Folder: `Folloze Demo Example Tile Library`
- Folder ID: `1dTAsMtmopoSgTVQY4JXnhwRh7S28ZXFb`
- Folder URL: `https://drive.google.com/drive/folders/1dTAsMtmopoSgTVQY4JXnhwRh7S28ZXFb`

The Drive folder is the cross-machine source of truth for example tile artwork. A local tile is only an intake source, not the durable shared source.

Preflight folder access before selecting examples. Read access is sufficient when every required tile already exists and verifies. If a required tile must be uploaded from Luke's machine, require write access to the folder and verify the upload by readback; otherwise stop and ask Trey for the needed folder permission.

Use this filename convention:

```text
[board-id]-[normalized-company]-[normalized-motion]-tile.png
```

Resolve a tile by exact Board ID first, then normalized company and motion. Verify:

- `1672 x 941` landscape PNG
- correct company logo and motion/use-case label
- no unrelated company or account residue
- readable crop at desktop and mobile card sizes
- Drive file ID, filename, SHA-256, and dimensions recorded privately

Build one compact Board-ID-to-file metadata index for the candidate tiles and reuse it for the run. Do not repeatedly list the entire shared drive or download every image. The cache may contain only non-sensitive file IDs, names, hashes, dimensions, and modification timestamps; refresh the exact selected files immediately before use.

If Luke supplies a correct local tile that is missing from Drive:

1. Upload a copy to this folder using the filename convention.
2. Verify the new Drive file and inherited shared-drive access.
3. Download/materialize it through the authenticated Drive connector when needed.
4. Upload it to the correct Folloze content item and verify the rendered crop.

Do not use a private Drive viewing URL as the Folloze image URL. Do not use page screenshots, recording covers, deck covers, or generic artwork as substitutes for a missing demo-example tile. If no correct tile is available locally or in Drive, leave that example blocked and report the missing Board ID/tile instead of fabricating one.

## Selection and completion gate

Add only the examples supported by tracker rows for the relevant company/demo pack. Preserve the six baseline template items, then append the selected tracker-backed examples in the intended campaign/account/event order when the pack contains those motions.

An example card is complete only when all of these agree:

- tracker Board ID and Deployment URL
- buyer-facing card title and destination
- Drive tile Board ID/company/motion
- Folloze-hosted tile image and rendered crop
- anonymous destination verification
