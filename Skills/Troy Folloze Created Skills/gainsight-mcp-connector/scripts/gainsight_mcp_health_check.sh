#!/usr/bin/env bash
set -euo pipefail

SERVER_NAME="${GAINSIGHT_MCP_NAME:-gainsight}"
MCP_URL="${GAINSIGHT_MCP_URL:-https://mcp.aptrinsic.com/mcp}"
OAUTH_RESOURCE="${GAINSIGHT_MCP_RESOURCE:-https://mcp.aptrinsic.com}"
CODEX_BIN="${CODEX_BIN:-/Applications/Codex.app/Contents/Resources/codex}"
CODEX_MODEL="${CODEX_MODEL:-gpt-5.5}"
RUN_LOGIN=0
RUN_EXEC=1
CHECK_CWD="${PWD}"

if [[ ! -x "${CODEX_BIN}" ]]; then
  CODEX_BIN="$(command -v codex || true)"
fi

if [[ -z "${CODEX_BIN}" ]]; then
  echo "Codex CLI not found. Set CODEX_BIN to the Codex CLI path." >&2
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --login)
      RUN_LOGIN=1
      shift
      ;;
    --no-exec)
      RUN_EXEC=0
      shift
      ;;
    --cwd)
      CHECK_CWD="${2:?Missing value for --cwd}"
      shift 2
      ;;
    --help|-h)
      cat <<EOF
Usage: $(basename "$0") [--login] [--no-exec] [--cwd PATH]

Ensures the Gainsight MCP server is configured and optionally verifies it from
a fresh Codex process with a read-only px_list_products health check.

Environment overrides:
  CODEX_BIN               Path to the Codex CLI
  CODEX_MODEL             Model for the fresh health-check process
  GAINSIGHT_MCP_NAME      MCP server name, default gainsight
  GAINSIGHT_MCP_URL       MCP endpoint URL
  GAINSIGHT_MCP_RESOURCE  OAuth resource
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

echo "Codex CLI: ${CODEX_BIN}"
echo "MCP server: ${SERVER_NAME}"
echo "MCP URL: ${MCP_URL}"
echo "OAuth resource: ${OAUTH_RESOURCE}"

if ! "${CODEX_BIN}" mcp get "${SERVER_NAME}" >/dev/null 2>&1; then
  echo "MCP server '${SERVER_NAME}' is missing; adding it."
  "${CODEX_BIN}" mcp add "${SERVER_NAME}" \
    --url "${MCP_URL}" \
    --oauth-resource "${OAUTH_RESOURCE}"
else
  echo "MCP server '${SERVER_NAME}' is configured."
fi

if [[ "${RUN_LOGIN}" -eq 1 ]]; then
  echo "Refreshing OAuth for '${SERVER_NAME}'. Complete the browser flow if prompted."
  "${CODEX_BIN}" mcp login "${SERVER_NAME}" --scopes mcp
fi

if [[ "${RUN_EXEC}" -eq 0 ]]; then
  echo "Skipping fresh Codex health check because --no-exec was provided."
  exit 0
fi

echo "Running fresh Codex health check from: ${CHECK_CWD}"
"${CODEX_BIN}" exec \
  -C "${CHECK_CWD}" \
  --dangerously-bypass-approvals-and-sandbox \
  -m "${CODEX_MODEL}" \
  "Minimal Gainsight MCP health check. If Gainsight MCP tools are available, call px_list_products. Return only: connected yes/no, read-only call success/failure, product count, and product names if successful. Do not modify data."
