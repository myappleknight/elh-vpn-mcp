# ELH VPN Cloud — MCP server & Agent API

[繁體中文](README.zh-TW.md)

**ELH VPN Cloud** is a prepaid, no-auto-renewal VPN (WireGuard, Android app; browser extension coming). Members get a small free allowance every day. This repo shows how **AI agents** can use it safely through a hosted **MCP server** and a small REST API.

An agent can open a **short-lived, capped HTTPS proxy session** on behalf of a member, charged to that member's own prepaid data. The member stays in control: they create the agent key, set its time/data limits, and can revoke it at any time.

- Website: https://vpn.easylifehub.net
- MCP endpoint (Streamable HTTP, stateless): `https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp`
- OpenAPI: `https://vpn.easylifehub.net/wp-json/elh-vpn/v1/agent/openapi`
- For LLMs: `https://vpn.easylifehub.net/llms.txt`

## Tools

| Tool | Key needed | What it does |
|---|---|---|
| `get_plans` | no | Prepaid packs (data, validity, TWD/USD price) and the daily free allowance |
| `get_regions` | no | Available server regions |
| `start_session` | yes | Start a capped HTTPS CONNECT proxy session; returns host, port and a 15-minute credential |
| `get_session` | yes | Status, remaining time, data used |
| `refresh_credential` | yes | New 15-minute credential for an active session |
| `stop_session` | yes | Stop immediately |
| `get_referral_link` | yes | The member's invite link and reward rules |

Purchases are **never** made by agents — only by the member on the website.

## Setup

1. Sign up at https://vpn.easylifehub.net/member/ (free daily allowance, no credit card).
2. Create an **agent key** (starts with `elh_ak_`), choosing its max minutes and max MB per session. Up to 3 keys; the key is shown only once.
3. Add the MCP server to your client:

**Cursor / clients with native remote MCP** — [`examples/cursor-mcp.json`](examples/cursor-mcp.json)

```json
{
  "mcpServers": {
    "elh-vpn": {
      "url": "https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp",
      "headers": { "Authorization": "Bearer ${env:ELH_AGENT_KEY}" }
    }
  }
}
```

**Claude Desktop** (via `mcp-remote`) — [`examples/claude-desktop-config.json`](examples/claude-desktop-config.json)

**Plain HTTP** — [`examples/quickstart.sh`](examples/quickstart.sh), or the Python example [`examples/use_proxy.py`](examples/use_proxy.py) that starts a session, fetches one page through the proxy and stops.

```bash
curl -s -X POST https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp \
  -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_plans","arguments":{}}}'
```

## Safety & rules

- Keep the agent key secret (env var / secret store). Never commit it.
- Sessions stop automatically at the key's time or data limit, or when the account runs out of data.
- Starting a session ends the member's other active connection.
- Don't use the service for anything illegal, for spam, or for abuse of third-party sites. See the [Terms](https://vpn.easylifehub.net/terms/).

## Referral program (single-level)

A member's invite link gives the member a 2 GB pack for every paid order by an invited friend (no limit), and the friend gets 2 GB on their first paid order. Rewards are released 7 days after payment if not refunded. Share the link only when genuinely recommending the service — never spam.

## License

Examples in this repo: MIT. The ELH VPN Cloud service itself is proprietary.
