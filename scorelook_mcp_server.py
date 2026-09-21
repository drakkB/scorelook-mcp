# -*- coding: utf-8 -*-
"""
ScoreLook MCP server.

Read-only MCP wrapper around the public ScoreLook style and shopping APIs.
It does not access user accounts, private photos, files, shell commands, or payments.
"""

import os
from typing import Any, Literal

import requests
from mcp.server.fastmcp import FastMCP


API_BASE = os.getenv("SCORELOOK_API_BASE", "http://127.0.0.1:8009").rstrip("/")
REQUEST_TIMEOUT = float(os.getenv("SCORELOOK_MCP_TIMEOUT", "12"))

mcp = FastMCP(
    "ScoreLook Style Engine",
    instructions=(
        "Use ScoreLook for French style guidance about complete looks, strong pieces, "
        "noble materials, office elegance, Capucine silhouettes, and shopping criteria. "
        "The server is read-only and only returns public ScoreLook content."
    ),
    website_url="https://scorelook.fr",
    stateless_http=True,
    json_response=True,
    host=os.getenv("SCORELOOK_MCP_HOST", "127.0.0.1"),
    port=int(os.getenv("SCORELOOK_MCP_PORT", "8010")),
)

# --- ChatGPT app widget (Apps SDK / MCP Apps) ---------------------------------
# La planche Capucine rendue dans la conversation ChatGPT. Le widget lit le
# structuredContent du tool (window.openai.toolOutput) et reste read-only :
# le seul chemin d'action est le lien sortant vers le flux invite scorelook.fr.
CAPUCINE_WIDGET_URI = "ui://widget/capucine-look.html"

CAPUCINE_WIDGET_META = {
    "ui": {"resourceUri": CAPUCINE_WIDGET_URI},
    "openai/outputTemplate": CAPUCINE_WIDGET_URI,
    "openai/toolInvocation/invoking": "Capucine compose la silhouette…",
    "openai/toolInvocation/invoked": "Planche Capucine prête",
}

CAPUCINE_WIDGET_HTML = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>
  :root{--ink:#17120d;--muted:#66584d;--paper:#fbf7f2;--gold:#d7b46a;--soft:#efe3d4;--line:rgba(23,18,13,.13);--green:#23483a}
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:Inter,-apple-system,Segoe UI,Arial,sans-serif;background:var(--paper);color:var(--ink);line-height:1.5;padding:16px;font-size:14px}
  .brand{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
  .brand b{letter-spacing:.08em;font-size:.8rem}
  .brand span{color:var(--muted);font-size:.72rem}
  h1{font-family:Georgia,serif;font-weight:500;font-size:1.15rem;margin-bottom:6px}
  .diag{color:var(--muted);font-size:.85rem;margin-bottom:10px}
  .answer{font-size:.9rem;margin-bottom:12px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}
  @media(max-width:520px){.grid{grid-template-columns:1fr}}
  .card{background:#fff;border:1px solid var(--line);border-radius:6px;padding:10px 12px}
  .card b{display:block;color:#9a6a2f;text-transform:uppercase;letter-spacing:.1em;font-size:.66rem;margin-bottom:6px}
  .card ul{padding-left:16px;font-size:.82rem;color:var(--muted)}
  .card li{margin-bottom:3px}
  .chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
  .chips span{background:var(--soft);border-radius:20px;padding:3px 10px;font-size:.74rem;font-weight:600;color:#6b5a4e}
  .cta{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  .cta a{display:inline-block;text-decoration:none;border-radius:4px;padding:9px 14px;font-weight:700;font-size:.82rem}
  .cta a.gold{background:var(--gold);color:#17120d}
  .cta a.ghost{border:1px solid var(--line);color:var(--ink)}
  .disclaimer{color:var(--muted);font-size:.68rem;margin-top:10px}
  .empty{color:var(--muted);font-size:.85rem;padding:14px 0}
</style>
</head>
<body>
<div class="brand"><b>SCORELOOK · CAPUCINE</b><span>styliste IA</span></div>
<div id="root"><div class="empty">Planche Capucine en préparation…</div></div>
<script>
(function () {
  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"]/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}[c];
    });
  }
  function pickResponse(raw) {
    if (!raw || typeof raw !== "object") return {};
    var d = raw.structuredContent || raw;
    return d.response || d.recommendation || d;
  }
  function render() {
    var out = (window.openai && window.openai.toolOutput) || null;
    var r = pickResponse(out);
    var reco = r.recommendation || r;
    var headline = r.headline || reco.look_name || r.main_recommendation || "";
    var answer = r.answer || reco.main_recommendation || "";
    var diagnosis = r.diagnosis || "";
    var why = (reco.why_it_works || []).slice(0, 4);
    var avoid = (reco.avoid || []).slice(0, 4);
    var capsule = (r.capsule || reco.capsule || []).slice(0, 6);
    var crit = r.shopping_criteria || reco.shopping_criteria || {};
    var chips = [crit.material, crit.color, crit.subtype, crit.length].filter(Boolean);
    var question = r.question || (window.openai && window.openai.toolInput && (window.openai.toolInput.question || window.openai.toolInput.piece)) || "";
    if (!headline && !answer && !capsule.length) return;
    var appUrl = "https://scorelook.fr/app?source=chatgpt-app&intent=board" + (question ? "&q=" + encodeURIComponent(String(question).slice(0, 180)) : "");
    var html = "";
    if (headline) html += "<h1>" + esc(headline) + "</h1>";
    if (diagnosis) html += '<p class="diag">' + esc(diagnosis) + "</p>";
    if (answer) html += '<p class="answer">' + esc(answer) + "</p>";
    var cards = "";
    if (why.length) cards += '<div class="card"><b>Pourquoi ça marche</b><ul>' + why.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul></div>";
    if (avoid.length) cards += '<div class="card"><b>À surveiller</b><ul>' + avoid.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("") + "</ul></div>";
    if (capsule.length) cards += '<div class="card"><b>Capsule à construire</b><ul>' + capsule.map(function (x) { return "<li>" + esc(x.piece || "Pièce") + (x.criteria ? " : " + esc(x.criteria) : "") + "</li>"; }).join("") + "</ul></div>";
    if (cards) html += '<div class="grid">' + cards + "</div>";
    if (chips.length) html += '<div class="chips">' + chips.map(function (c) { return "<span>" + esc(c) + "</span>"; }).join("") + "</div>";
    html += '<div class="cta"><a class="gold" href="' + appUrl + '" target="_blank" rel="noopener">Créer la planche sur ScoreLook</a>' +
      '<a class="ghost" href="https://scorelook.fr/methode-scorelook" target="_blank" rel="noopener">La méthode</a></div>';
    html += '<p class="disclaimer">Réponse générée par Capucine, styliste IA ScoreLook. Pistes shopping indicatives — ni stock ni prix garantis.</p>';
    document.getElementById("root").innerHTML = html;
  }
  render();
  if (window.openai && typeof window.openai.addEventListener === "function") {
    try { window.openai.addEventListener("toolOutput", render); } catch (e) {}
  }
  window.addEventListener("message", function () { render(); });
})();
</script>
</body>
</html>
"""


def _get_json(path: str, params: dict | None = None) -> dict:
    response = requests.get(
        f"{API_BASE}{path}",
        params={key: value for key, value in (params or {}).items() if value not in (None, "")},
        timeout=REQUEST_TIMEOUT,
        headers={"User-Agent": "ScoreLookMCP/1.0"},
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("success", False):
        raise RuntimeError(data.get("error") or "ScoreLook API request failed")
    return data


def _bounded_limit(limit: int, default: int = 6, maximum: int = 12) -> int:
    try:
        value = int(limit or default)
    except Exception:
        value = default
    return max(1, min(maximum, value))


@mcp.tool()
def manifest() -> dict:
    """Return the public ScoreLook Style API manifest, including tools, safety boundaries, and key pages."""
    return _get_json("/api/public/style/manifest")


@mcp.tool()
def search(query: str, limit: int = 6, content_type: Literal["all", "article", "look"] = "all") -> dict:
    """Search public ScoreLook articles and Capucine looks for a style question."""
    return _get_json(
        "/api/public/style/search",
        {
            "q": query,
            "limit": _bounded_limit(limit),
            "type": content_type,
        },
    )


@mcp.tool()
def fetch(id: str) -> dict:
    """Fetch a public ScoreLook article or look by an id returned from search, such as article:jupe-cuir-chic."""
    return _get_json("/api/public/style/fetch", {"id": id})


@mcp.tool(meta=CAPUCINE_WIDGET_META, structured_output=True)
def recommend_look(
    piece: str,
    color: str = "",
    occasion: str = "",
    audacity: str = "",
    season: str = "",
    material: str = "",
) -> dict[str, Any]:
    """Recommend a complete ScoreLook silhouette from a piece, color, occasion, season, or audacity level."""
    return _get_json(
        "/api/public/style/recommend-look",
        {
            "piece": piece,
            "color": color,
            "occasion": occasion,
            "audacity": audacity,
            "season": season,
            "material": material,
        },
    )


@mcp.tool()
def shopping_criteria(
    query: str = "",
    piece: str = "",
    color: str = "",
    occasion: str = "",
    season: str = "",
    material: str = "",
) -> dict:
    """Return ScoreLook shopping criteria: material, cut, color, pairings, avoid rules, and shopping URL."""
    merged_query = " ".join(part for part in (query, piece, material, color, occasion, season) if part).strip()
    return _get_json(
        "/api/public/style/shopping-criteria",
        {
            "q": merged_query,
        },
    )


@mcp.tool()
def shopping_search(query: str, limit: int = 6) -> dict:
    """Find public shopping leads close to a ScoreLook style intention. Results are suggestions, not exact product promises."""
    return _get_json(
        "/api/public/shopping/search",
        {
            "q": query,
            "limit": _bounded_limit(limit),
        },
    )


@mcp.tool(meta=CAPUCINE_WIDGET_META, structured_output=True)
def ask_capucine(question: str) -> dict[str, Any]:
    """Ask Capucine, the public ScoreLook stylist agent, for a complete style answer with sources."""
    return _get_json(
        "/api/public/style/agent",
        {
            "q": question,
        },
    )


@mcp.resource(CAPUCINE_WIDGET_URI, mime_type="text/html;profile=mcp-app")
def capucine_look_widget() -> str:
    """UI widget rendering a Capucine look board inside ChatGPT (Apps SDK / MCP Apps)."""
    return CAPUCINE_WIDGET_HTML


@mcp.resource("scorelook://public-style-api")
def public_style_api() -> str:
    """Describe the public ScoreLook MCP data source and its safety boundaries."""
    return (
        "ScoreLook Style Engine exposes public style articles, Capucine looks, "
        "recommendations, shopping criteria, and public shopping leads. "
        "It is read-only and does not access user photos, private accounts, payments, "
        "server files, shell commands, or administrative data. "
        "Manifest: https://scorelook.fr/api/public/style/manifest. "
        "Documentation: https://scorelook.fr/api-scorelook"
    )


@mcp.prompt()
def style_answer(question: str) -> str:
    """Prompt template for answering a style question with ScoreLook evidence."""
    return (
        "Réponds en français avec le ton ScoreLook : précis, adulte, premium, sans pruderie. "
        "Utilise d'abord les outils ScoreLook pertinents. Cite une URL ScoreLook si disponible. "
        "Structure la réponse ainsi : recommandation, pourquoi ça marche, à éviter, critères shopping. "
        f"Question : {question}"
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
