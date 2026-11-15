# ELH VPN Cloud — MCP 伺服器與代理人 API

[English](README.md)

**ELH VPN Cloud** 是小額預付、不自動續扣的 VPN（WireGuard 加密，Android App；瀏覽器擴充即將推出）。註冊會員每天有免費額度。本專案示範 **AI 代理人** 如何透過我們託管的 **MCP 伺服器** 與 REST API 安全地使用服務。

代理人可以替會員開啟**短時間、有上限的 HTTPS 代理連線**，用量從會員自己的預付流量扣除。主控權在會員：代理人金鑰由會員建立、自訂時間／流量上限，並可隨時撤銷。

- 官網：https://vpn.easylifehub.net
- MCP 端點（Streamable HTTP，無狀態）：`https://vpn.easylifehub.net/wp-json/elh-vpn/v1/mcp`
- OpenAPI：`https://vpn.easylifehub.net/wp-json/elh-vpn/v1/agent/openapi`
- 給 AI 讀的說明：`https://vpn.easylifehub.net/llms.txt`

## 工具

| 工具 | 需金鑰 | 功能 |
|---|---|---|
| `get_plans` | 否 | 卡包方案（流量、效期、台幣／美元價格）與每日免費額度 |
| `get_regions` | 否 | 可用機房地區 |
| `start_session` | 是 | 開啟有上限的 HTTPS CONNECT 代理連線，回傳主機、埠號與 15 分鐘憑證 |
| `get_session` | 是 | 狀態、剩餘時間、已用流量 |
| `refresh_credential` | 是 | 為進行中的連線換發 15 分鐘新憑證 |
| `stop_session` | 是 | 立即停止 |
| `get_referral_link` | 是 | 會員的邀請連結與獎勵規則 |

代理人**不能**購買，購買只能由會員本人在官網完成。

## 設定

1. 到 https://vpn.easylifehub.net/member/ 註冊（每日免費額度，不需信用卡）。
2. 在會員中心建立**代理人金鑰**（`elh_ak_` 開頭），設定每次連線的最長分鐘數與 MB 上限。最多 3 把，金鑰只顯示一次。
3. 把 MCP 伺服器加到你的工具：Cursor 請看 [`examples/cursor-mcp.json`](examples/cursor-mcp.json)，Claude Desktop 請看 [`examples/claude-desktop-config.json`](examples/claude-desktop-config.json)，純 HTTP 請看 [`examples/quickstart.sh`](examples/quickstart.sh) 與 [`examples/use_proxy.py`](examples/use_proxy.py)。

## 安全與規範

- 金鑰請放在環境變數或密鑰管理工具，切勿提交到 Git。
- 達到金鑰的時間或流量上限、或帳號流量用完時，連線會自動停止。
- 開啟代理連線會中斷該會員的其他連線。
- 禁止違法、濫發或攻擊第三方網站等用途，詳見[服務條款](https://vpn.easylifehub.net/terms/)。

## 邀請好友（單層）

好友透過會員的邀請連結註冊後，每付款一次，會員獲得 2 GB 卡包（無上限）；好友第一次付款也獲得 2 GB。付款 7 天後未退款才發放。請只在真心推薦時分享，切勿濫發。

## 授權

本專案範例程式採 MIT 授權；ELH VPN Cloud 服務本身為專有服務。
