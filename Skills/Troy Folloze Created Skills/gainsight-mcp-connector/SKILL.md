---
name: gainsight-mcp-connector
description: Connect, configure, refresh, and verify the Gainsight PX/Aptrinsic MCP server for Codex. Use when a teammate needs to add the Gainsight MCP endpoint, repair expired OAuth auth, confirm Gainsight MCP tools load in new chats, run a read-only health check, or troubleshoot missing Gainsight tools.
---

# Gainsight MCP Connector

## Overview

Use this skill to make sure Codex can connect to the shared Gainsight PX MCP server at `https://mcp.aptrinsic.com/mcp`.

The standard MCP server name is `gainsight`. The OAuth resource is `https://mcp.aptrinsic.com`.

## Quick Workflow

1. Resolve the Codex CLI:
   - Prefer `/Applications/Codex.app/Contents/Resources/codex`.
   - Fall back to `codex` if the app-bundled binary is unavailable.

2. Check whether the MCP server is configured:

```bash
/Applications/Codex.app/Contents/Resources/codex mcp get gainsight
```

3. If the server is missing, add it:

```bash
/Applications/Codex.app/Contents/Resources/codex mcp add gainsight \
  --url https://mcp.aptrinsic.com/mcp \
  --oauth-resource https://mcp.aptrinsic.com
```

4. If auth is missing or expired, refresh OAuth:

```bash
/Applications/Codex.app/Contents/Resources/codex mcp login gainsight --scopes mcp
```

Approve the browser OAuth flow. Do not ask the user for tokens or paste secrets into chat.

5. Verify from a fresh Codex process, because the current chat may not see newly added or refreshed MCP tools until a new session loads:

```bash
Skills/gainsight-mcp-connector/scripts/gainsight_mcp_health_check.sh --login
```

Use `--no-exec` when you only need to confirm local MCP configuration and do not want to start a fresh Codex health-check subprocess.

## Health Check

The preferred read-only verification is to call `px_list_products` through the Gainsight MCP tools. A successful response should report that the read-only call worked and return a product count with product names.

Known product names observed during setup included `Outreach`, `Try me`, `Sales Account Dashboard`, `Folloze`, and `EU`. Treat this list as a sanity check, not a permanent source of truth.

## Troubleshooting

Load `references/troubleshooting.md` when the connection still fails after the quick workflow.

Common fixes:
- `Expired JWT`, `invalid_token`, or `AuthRequired`: run `codex mcp login gainsight --scopes mcp` again.
- MCP tools missing in the current chat after a successful login: start a new chat or run the bundled health-check script, which uses a fresh Codex process.
- `codex mcp get gainsight` fails: add the server with the endpoint and OAuth resource above.
- Login opens a browser but never completes: rerun the login command and complete the browser approval flow in the same local user session.
