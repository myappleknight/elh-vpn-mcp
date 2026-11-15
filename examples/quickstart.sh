#!/usr/bin/env bash
# ELH VPN Cloud MCP quick start (plain JSON-RPC over HTTPS).
# get_plans / get_regions need no key. Session tools need ELH_AGENT_KEY (elh_ak_...).
set -euo pipefail
MCP=https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp
call() {
  curl -sS -X POST "$MCP" \
    -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
    ${ELH_AGENT_KEY:+-H "Authorization: Bearer $ELH_AGENT_KEY"} \
    -d "$1"; echo
}
call '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
call '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_plans","arguments":{}}}'
call '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_regions","arguments":{}}}'
if [ -n "${ELH_AGENT_KEY:-}" ]; then
  # Start a 10-minute, 50 MB capped session (charged to the member's own data).
  call '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"start_session","arguments":{"region":"US","max_minutes":10,"max_mb":50}}}'
  echo "Remember to call stop_session with the returned session_id when done."
fi
