"""Start a capped session via MCP, fetch one page through the proxy, then stop.

Usage: ELH_AGENT_KEY=elh_ak_... python use_proxy.py
Only the Python standard library is used.
"""
import json, os, subprocess, urllib.request

MCP = "https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp"
KEY = os.environ["ELH_AGENT_KEY"]


def tool(name, args, _id=[0]):
    _id[0] += 1
    body = json.dumps({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
                       "params": {"name": name, "arguments": args}}).encode()
    req = urllib.request.Request(MCP, body, {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "Authorization": f"Bearer {KEY}"})
    res = json.load(urllib.request.urlopen(req, timeout=30))
    if "error" in res:
        raise RuntimeError(res["error"])
    result = res["result"]
    if result.get("isError"):
        raise RuntimeError(result["content"][0]["text"])
    return result.get("structuredContent") or json.loads(result["content"][0]["text"])


s = tool("start_session", {"max_minutes": 5, "max_mb": 20})
sid = s["session_id"]
print("session", sid, "region", s.get("region"), "limits", s["limits"])
try:
    # The proxy is HTTPS (TLS to the proxy) with CONNECT; curl supports it directly.
    # s["proxy"]["url"] already contains the 15-minute credential — never log or commit it.
    out = subprocess.run(["curl", "-sS", "--proxy", s["proxy"]["url"], "https://api.ipify.org"],
                         capture_output=True, text=True, timeout=60)
    print("exit IP:", out.stdout.strip() or out.stderr.strip())
finally:
    print("stopped:", tool("stop_session", {"session_id": sid})["state"])
