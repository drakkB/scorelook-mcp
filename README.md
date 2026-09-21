# ScoreLook MCP — Capucine Style Engine

Remote [MCP](https://modelcontextprotocol.io) server for [ScoreLook](https://scorelook.fr), the French AI styling atelier. It lets any MCP-compatible AI assistant (Claude, ChatGPT, Cursor, VS Code, Perplexity…) ask **Capucine**, ScoreLook's AI stylist, for complete outfit answers: silhouette, why it works, what to avoid, capsule wardrobe, weather-aware looks and shopping criteria — grounded in ScoreLook's public style content and a hand-verified product catalog.

**Hosted endpoint (no install, no API key):**

```
https://scorelook.fr/mcp
```

Transport: streamable HTTP · Auth: none · Read-only.

Published on the official MCP Registry as **`fr.scorelook/capucine`**.

## Try it

Cursor — `~/.cursor/mcp.json`:

```json
{ "mcpServers": { "scorelook": { "url": "https://scorelook.fr/mcp" } } }
```

VS Code — `.vscode/mcp.json`:

```json
{ "servers": { "scorelook": { "type": "http", "url": "https://scorelook.fr/mcp" } } }
```

Claude Desktop (remote via `mcp-remote`):

```json
{ "mcpServers": { "scorelook": { "command": "npx", "args": ["-y", "mcp-remote", "https://scorelook.fr/mcp"] } } }
```

ChatGPT / Claude.ai: *Settings → Connectors → Add* → server URL `https://scorelook.fr/mcp`, no authentication. The `ask_capucine` and `recommend_look` tools ship an inline widget (Apps SDK / MCP Apps) that renders the look board directly in the conversation.

## Tools (17)

| Tool | What it does |
|---|---|
| `ask_capucine` | Full style answer from a free-form question (FR): silhouette, diagnosis, capsule, vigilance points, shopping criteria. Widget-enabled. |
| `recommend_look` | Complete silhouette from structured input: piece, color, occasion, season, audacity. Widget-enabled. |
| `shopping_criteria` | Material, cut, color, pairing and avoid rules for buying a piece. |
| `shopping_search` | Public shopping leads close to a style intention, from a hand-verified premium catalog. Suggestions, not availability promises. |
| `shop_the_look` | Ties a signature piece to its Capucine look and to verified merchant leads. Widget-enabled. |
| `get_piece_hub` | Public hub for one piece family (definition, excerpts, sources, products). |
| `list_piece_hubs` | Mid-tail `/pieces/*` hubs (leather skirt, leather trousers…). |
| `search` | Search public ScoreLook articles and Capucine looks. |
| `fetch` | Fetch one article or look by id (e.g. `article:jupe-cuir-chic`). |
| `cite_sources` | Citable ScoreLook sources for a topic. |
| `classify_circumstance` | Circumstance (dinner, office, wedding…) + city, transport, piece, time slot. |
| `weather_looks` | Morning / noon / evening plan from local weather. No silent fallback to Paris. |
| `get_weather_context` | Weather facts: feels-like, rain %, mm, wind/gusts, UV, timezone, resolved city. |
| `recommend_weather_look` | Crosses circumstance × weather, or checks whether a piece holds for that dinner/city. |
| `public_status` | Minimal public status: beta, payment closed, blockers, shopping read-only. |
| `llms_guide` | Guide for assistants (enriched equivalent of `/llms.txt`). |
| `manifest` | Public Style API manifest: tools, safety boundaries, key pages. |

Plus **7 resources** (3 MCP Apps widgets + `scorelook://public-style-api`, `scorelook://citation-rules`, `scorelook://piece-hubs`, `scorelook://llms-txt`) and **7 prompt templates**.

## Example

> *"Utilise ScoreLook : comment porter une jupe en cuir violet foncé au bureau ?"*

Capucine answers with a named look, why it works, what to watch, a capsule and concrete shopping criteria — and, in MCP Apps clients, a rendered look board linking back to scorelook.fr.

## Discovery

- Server card: https://scorelook.fr/.well-known/mcp/server-card.json
- Discovery file: https://scorelook.fr/.well-known/mcp.json
- Health: https://scorelook.fr/mcp/healthz
- Registry manifest: https://scorelook.fr/mcp/server.json
- AI policy: https://scorelook.fr/ai.txt · https://scorelook.fr/llms.txt

## Safety & scope

- **Read-only.** No tool writes anything. No user accounts, no private photos, no payments, no files, no shell.
- Only public ScoreLook content is exposed.
- Answers are generated style directions in French, not personalized advice; shopping results are indicative (no stock/price guarantee).
- Requests carrying a browser `Origin` header are rejected; call from a backend MCP client.

## Self-hosting

The server is a thin FastMCP wrapper over ScoreLook's public HTTP API — see [`scorelook_mcp_server.py`](./scorelook_mcp_server.py). Point `SCORELOOK_API_BASE` at `https://scorelook.fr` and run:

```bash
pip install "mcp>=1.28" requests
SCORELOOK_API_BASE=https://scorelook.fr python scorelook_mcp_server.py
```

The hosted endpoint above is the recommended way to use it.

## Links

- Site: https://scorelook.fr
- MCP guide: https://scorelook.fr/scorelook-mcp
- API docs: https://scorelook.fr/api-scorelook
- Official registry: `fr.scorelook/capucine`

## License

MIT — see [LICENSE](./LICENSE).
