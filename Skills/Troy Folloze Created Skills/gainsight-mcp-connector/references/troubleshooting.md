# Gainsight MCP Troubleshooting

## Expected Configuration

- Server name: `gainsight`
- MCP URL: `https://mcp.aptrinsic.com/mcp`
- OAuth resource: `https://mcp.aptrinsic.com`
- OAuth scope: `mcp`

## Symptoms And Fixes

### `Expired JWT`, `invalid_token`, or `AuthRequired`

Refresh OAuth:

```bash
/Applications/Codex.app/Contents/Resources/codex mcp login gainsight --scopes mcp
```

Complete the browser approval flow. Do not request or paste bearer tokens.

### `codex mcp get gainsight` fails

Add the MCP server:

```bash
/Applications/Codex.app/Contents/Resources/codex mcp add gainsight \
  --url https://mcp.aptrinsic.com/mcp \
  --oauth-resource https://mcp.aptrinsic.com
```

Then run the login command.

### Tools are missing in the current chat

New or refreshed MCP tools may not be visible to an already-running chat. Start a new chat, or run the skill's health-check script so a fresh Codex process loads the current MCP config.

### Browser login does not complete

Rerun the login command from the local desktop session and complete the browser flow when it opens. If a stale browser tab is open, close it and try again.

### Health check succeeds but product names differ

That is acceptable. Product names in Gainsight can change. A successful read-only `px_list_products` call is the real connection proof.
