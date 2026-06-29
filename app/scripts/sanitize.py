"""
Sanitize the HTML dashboard for public deployment.

What this does:
  Reads `../../minorities_project/outputs/dashboards/dashboard.html`
  (the full unredacted version with caller free-text descriptions and
  technical captions),
  applies two passes:
    1. PII redaction: every embedded `"desc":"..."` value is replaced
       with a placeholder string.
    2. Public-presentation polish: removes raw row-count totals,
       technical model-metric captions, and a few labels that are
       useful in docs but noisy in a stakeholder demo.
  Writes the sanitized + polished result to `../dashboard.html`.

When to re-run:
  - After a fresh data refresh in the full project.
  - After someone rebuilds dashboard.html in the full project.

Usage:
    cd minorities_streamlit_deploy/scripts
    python3 sanitize.py
"""
from pathlib import Path
import re

HERE         = Path(__file__).resolve().parent              # app/scripts
APP_ROOT     = HERE.parent                                   # app
HANDOFF_ROOT = APP_ROOT.parent                               # minorities_ews_intern_handoff
SOURCE_HTML  = HANDOFF_ROOT.parent / "minorities_project" / "outputs" / "dashboards" / "dashboard.html"
DST_HTML     = APP_ROOT / "dashboard.html"

PLACEHOLDER = "[redacted for public deployment]"


# ----------------------------------------------------------------------
# Pass 3 — Polished UI replacement for the entire <style> block.
# Modernised typography, card layout, gradient header, refined palette.
# ----------------------------------------------------------------------
POLISHED_CSS = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; height:100%;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    color:#0f172a;
    background:#f8fafc;
    -webkit-font-smoothing: antialiased;
  }
  #app { display:flex; flex-direction:column; height:100vh; }

  /* ---------- Header ---------- */
  header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #312e81 100%);
    color:#fff;
    padding:14px 22px;
    display:flex; align-items:center; gap:18px; flex-wrap:wrap; flex-shrink:0;
    box-shadow: 0 2px 12px rgba(15,23,42,0.18);
    position:relative; z-index:10;
  }
  header h1 {
    font-size:18px; margin:0; font-weight:700; letter-spacing:-0.01em;
    display:flex; align-items:center; gap:8px;
  }
  header h1::before {
    content:"⚡"; font-size:20px;
  }
  header .subtitle {
    font-size:12px; margin-left:4px; opacity:0.78; font-weight:400;
    font-style:normal; color:#cbd5e1; letter-spacing:0.01em;
  }
  header .stats { display:flex; align-items:center; gap:14px; font-size:12.5px; margin-left:auto; }
  header .stats > span {
    background: rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.12);
    padding:6px 12px;
    border-radius:8px;
    backdrop-filter: blur(4px);
  }
  header .stats b { font-weight:700; color:#fff; }

  #main { display:flex; flex:1; min-height:0; }

  /* ---------- Side panels ---------- */
  .panel {
    background:#f8fafc;
    border-right:1px solid #e2e8f0;
    overflow-y:auto;
    flex-shrink:0;
  }
  #left { width:296px; }
  #right { width:360px; border-right:none; border-left:1px solid #e2e8f0; }

  /* ---------- Card-style control blocks ---------- */
  .ctrl-block {
    background:#fff;
    padding:14px 16px;
    margin:10px 10px 0 10px;
    border:1px solid #e2e8f0;
    border-radius:12px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
    transition: box-shadow 0.18s ease;
  }
  .ctrl-block:hover { box-shadow: 0 2px 8px rgba(15,23,42,0.06); }
  .ctrl-block:last-child { margin-bottom:10px; }
  .ctrl-block:first-child { position: static; }

  .ctrl-block h4 {
    margin:0 0 10px;
    font-size:11px; font-weight:600;
    color:#64748b;
    text-transform:uppercase; letter-spacing:0.08em;
  }

  /* ---------- Toggles ---------- */
  label.toggle {
    display:flex; align-items:center;
    padding:6px 0; font-size:13.5px;
    color:#334155;
    cursor:pointer; user-select:none;
    transition: color 0.12s ease;
  }
  label.toggle:hover { color:#0f172a; }
  label.toggle input[type="checkbox"] {
    accent-color: #4f46e5;
    margin-right:8px;
    width:14px; height:14px;
  }
  label.toggle .count { color:#94a3b8; font-size:11px; margin-left:6px; }

  .sub-toggles { padding-left:22px; margin-top:6px; font-size:12.5px; }
  .sub-toggles label {
    display:inline-block; margin:2px 8px 2px 0;
    cursor:pointer; padding:2px 0;
  }
  .sub-toggles label input[type="checkbox"] {
    accent-color: #4f46e5;
    margin-right:5px;
  }

  /* ---------- Map ---------- */
  #map { flex:1; }
  .leaflet-popup-content {
    font-family:'Inter', sans-serif;
    font-size:12.5px; line-height:1.5; max-width:320px;
  }
  .leaflet-popup-content b { color:#0f172a; font-weight:600; }
  .leaflet-popup-content .scores {
    background:#f1f5f9; padding:5px 8px; border-radius:6px;
    margin-top:6px; font-family:'JetBrains Mono', monospace; font-size:11.5px;
  }

  /* ---------- Inputs ---------- */
  input[type=range] {
    width:100%;
    accent-color:#4f46e5;
  }
  #threshold-val {
    font-family:'JetBrains Mono', monospace;
    font-size:12.5px; font-weight:600;
    color:#4f46e5;
  }

  /* ---------- Lists (Top PSes, Top cases, Forward) ---------- */
  #ps-list, #top-cases-list, #forward-list {
    list-style:none; margin:0; padding:0;
  }
  #ps-list li, #top-cases-list li, #forward-list li {
    padding:10px 14px;
    border-bottom:1px solid #f1f5f9;
    transition: background 0.12s ease;
  }
  #ps-list li:last-child, #top-cases-list li:last-child, #forward-list li:last-child {
    border-bottom:none;
  }
  #top-cases-list li, #forward-list li { cursor:pointer; }
  #top-cases-list li:hover { background:#fef2f2; }
  #forward-list li:hover    { background:#fffbeb; }

  #ps-list li .ps-row, #top-cases-list li .tc-row, #forward-list li .fw-row {
    display:flex; justify-content:space-between; align-items:center; gap:8px;
  }
  #ps-list li .name, #top-cases-list li .ps, #forward-list li .fw-ps {
    flex:1; font-size:13px; color:#0f172a; font-weight:500;
  }
  #ps-list li .score, #top-cases-list li .rank, #forward-list li .fw-rank {
    font-family:'JetBrains Mono', monospace; font-weight:700;
  }
  #ps-list li .score { color:#dc2626; font-size:13px; }
  #top-cases-list li .rank { color:#dc2626; font-size:11.5px; }
  #forward-list li .fw-rank {
    color:#64748b; font-size:11.5px; min-width:28px;
    background:#f1f5f9; padding:3px 7px; border-radius:6px; text-align:center;
  }

  .score-pill, #top-cases-list li .score-pill, #forward-list li .fw-score {
    color:white;
    font-family:'JetBrains Mono', monospace;
    font-size:11.5px; font-weight:700;
    padding:3px 9px; border-radius:6px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.12);
  }
  #top-cases-list li .score-pill {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }
  #forward-list li .fw-score {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color:#451a03;
  }

  #ps-list li .sub, #top-cases-list li .sub, #forward-list li .fw-sub {
    color:#64748b; font-size:11px; margin-top:3px;
  }
  #forward-list li .fw-sub { padding-left:36px; }

  /* ---------- Special panels ---------- */
  .warning-panel {
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%) !important;
    border-left:4px solid #f59e0b;
  }
  .warning-panel h4 {
    font-size:14px !important; text-transform:none !important; letter-spacing:0 !important;
    color:#78350f !important; font-weight:700;
  }
  .predictions-panel {
    background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
    border-left:4px solid #dc2626;
  }
  .predictions-panel h4 {
    font-size:14px !important; text-transform:none !important; letter-spacing:0 !important;
    color:#7f1d1d !important; font-weight:700;
  }

  /* ---------- KPI grid in predictions panel ---------- */
  .pred-kpi {
    display:grid; grid-template-columns:1fr 1fr; gap:10px;
    margin-top:4px;
  }
  .pred-kpi .box {
    background:#fff;
    padding:10px 12px;
    border-radius:10px;
    border:1px solid #fecaca;
    box-shadow:0 1px 3px rgba(220,38,38,0.06);
  }
  .pred-kpi .box .v {
    font-size:22px; font-weight:800; color:#dc2626;
    font-family:'JetBrains Mono', monospace;
    line-height:1.1;
  }
  .pred-kpi .box .l {
    color:#64748b; font-size:10px;
    text-transform:uppercase; letter-spacing:0.06em;
    margin-top:4px; font-weight:600;
  }

  /* ---------- Charts (right sidebar) ---------- */
  .chart-wrap {
    padding:14px 16px;
    background:#fff;
    margin:10px;
    border:1px solid #e2e8f0;
    border-radius:12px;
    box-shadow: 0 1px 3px rgba(15,23,42,0.04);
  }
  .chart-wrap h4 {
    margin:0 0 8px;
    font-size:11px; font-weight:600;
    color:#64748b;
    text-transform:uppercase; letter-spacing:0.08em;
  }

  /* ---------- Legend on map ---------- */
  .legend {
    background:rgba(255,255,255,0.96);
    backdrop-filter: blur(6px);
    padding:10px 12px;
    border-radius:10px;
    box-shadow:0 4px 12px rgba(15,23,42,0.12);
    border:1px solid #e2e8f0;
    font-size:11.5px; line-height:1.5;
  }
  .legend .row { display:flex; align-items:center; margin-bottom:3px; }
  .legend .sw {
    display:inline-block;
    width:12px; height:12px; border-radius:50%;
    margin-right:7px; border:1px solid #475569;
  }
  .legend .gradient {
    display:flex; gap:0; height:8px; margin:6px 0;
    border-radius:4px; overflow:hidden;
  }
  .legend .gradient div { flex:1; }

  /* ---------- Scrollbars ---------- */
  .panel::-webkit-scrollbar { width:8px; }
  .panel::-webkit-scrollbar-track { background: transparent; }
  .panel::-webkit-scrollbar-thumb {
    background: #cbd5e1; border-radius:4px;
  }
  .panel::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

  /* ---------- Header threshold/range hover ---------- */
  .ctrl-block input[type=range]::-webkit-slider-thumb {
    cursor: pointer;
  }
</style>"""

# Match the original style block (compact, single block between <style>...</style>)
STYLE_BLOCK_RE = re.compile(r"<style>[\s\S]*?</style>", re.MULTILINE)


# ----------------------------------------------------------------------
# Pass 2 — Public-presentation polish
# ----------------------------------------------------------------------
# Each entry: a regex pattern and the replacement string.
# These intentionally use full lines so multi-pass running stays
# idempotent (running sanitize.py twice gives the same output).
POLISH_REPLACEMENTS = [
    # 1) Strip raw row-count totals from the header — keep only the
    #    "RF flagged ≥0.5" KPI badge. The raw N=4,110 / N Lahore /
    #    N strict-label totals belong in the docs, not on the live page.
    (
        re.compile(
            r"`<span><b>\$\{DATA\.totals\.all[^`]*?cases \(with coords\)</span>`\s*\+\s*"
            r"`<span><b>\$\{DATA\.totals\.lahore[^`]*?Lahore</span>`\s*\+\s*"
            r"`<span><b>\$\{DATA\.totals\.strict[^`]*?strict-label</span>`\s*\+\s*",
            re.DOTALL,
        ),
        "",
    ),
    # 2) Hide the per-community count chips at the right end of the
    #    header (those expose absolute community counts).
    (
        re.compile(
            r"\s*\+\s*Object\.entries\(DATA\.totals\.comm\)[\s\S]*?\.join\(''\);",
        ),
        ";",
    ),
    # 3) "2026 YTD" -> "2026"
    (re.compile(r"2026 YTD"), "2026"),
    # 4) Per-case heading: drop "(retrospective)"
    (re.compile(r"⚡ Per-case triage \(retrospective\)"), "⚡ Per-case triage"),
    # 5) Forecaster technical sub-caption -> friendlier line
    (
        re.compile(r"PS-week LR forecaster[^<]*trained on 2024-2025"),
        "Top police-station areas the model expects may need attention soon",
    ),
    # 6) Per-case technical sub-caption -> friendlier line
    (
        re.compile(r"Random Forest \(trained 2024[–-]2025\)[^<]*Precision@20 0\.35"),
        "Cases the model has flagged as likely minority-targeted",
    ),
    # 7) Chart title: "Cases per month — strict vs all" -> "Trend over time"
    (re.compile(r"Cases per month — strict vs all"), "Trend over time"),
    # 8) "Top-25 PSes by mean RF score" -> "Police-stations by average risk"
    (
        re.compile(r"Top-25 PSes by mean RF score"),
        "Police-stations by average risk",
    ),
    # 9) Drop the technical operational-allocation footnote.
    (
        re.compile(
            r"Where the model flags the most risk on average\. "
            r"Operational input for force allocation\."
        ),
        "Police-station areas the model rates highest on average.",
    ),

    # ----------------------------------------------------------------------
    # PREDICTIONS-FORWARD HERO TREATMENT
    # ----------------------------------------------------------------------
    # 10) CSS — small subtitle next to the H1.
    (
        re.compile(r"header h1 \{ font-size:14px; margin:0; font-weight:600; \}"),
        "header h1 { font-size:15px; margin:0; font-weight:600; }\n"
        "  header .subtitle { font-size:11px; margin-left:8px; opacity:0.78; "
        "font-weight:400; font-style:italic; color:#cfd2d8; }",
    ),

    # 11) Subtitle HTML — anchors the page as forward-looking.
    #     Negative lookahead prevents double-insertion if run twice.
    (
        re.compile(r'<h1>Minorities Early-Warning Dashboard</h1>(?!<span class="subtitle">)'),
        "<h1>Minorities Early-Warning Dashboard</h1>"
        "<span class=\"subtitle\">Forecasts where minority-targeted "
        "incidents are most likely in the next 30 days</span>",
    ),

    # 12) New "Forecast PSes" toggle in the Layers block (default ON).
    #     Negative lookahead prevents duplicate insertion on re-run.
    (
        re.compile(
            r'<label class="toggle"><input type="checkbox" id="lyr-topn" checked> '
            r'Top-100 by model risk \(RF\)</label>(?!\s*<label[^>]*id="lyr-forecast")'
        ),
        '<label class="toggle"><input type="checkbox" id="lyr-topn" checked> '
        'Top-100 by model risk (RF)</label>\n'
        '        <label class="toggle"><input type="checkbox" id="lyr-forecast" checked> '
        '<span style="color:#b9770e;font-weight:600">🔮 Forecast PSes (next 30d)</span></label>',
    ),

    # 13) Forecast-focused header KPI + map overlay layer — injected as a
    #     trailing <script> right before </body>. Runs after the dashboard's
    #     own bootstrap so it overrides the original "RF flagged" stat.
    #     Negative lookbehind on the marker comment guards re-injection.
    (
        re.compile(r"(?<!FORECAST_HERO_INJECTED -->)\s*</body>"),
        """<!-- FORECAST_HERO_INJECTED -->
<script>
(function(){
  if (typeof map === 'undefined' || typeof DATA === 'undefined') return;
  const FWD = Array.isArray(DATA.forward) ? DATA.forward : [];

  // Forecast-focused header KPI — overrides the original after-load.
  const FWD_05  = FWD.filter(f => f.score >= 0.5).length;
  const FWD_TOP = FWD.length ? FWD[0] : null;
  const statsEl = document.getElementById('stats');
  if (statsEl) {
    statsEl.innerHTML =
      '<span style="background:#f39c12;color:#1a1a2e;padding:4px 12px;' +
      'border-radius:4px;font-weight:700">' +
      '🔮 <b>' + FWD_05 + '</b> police-stations flagged for next 30 days</span>' +
      (FWD_TOP
        ? '<span style="margin-left:12px;opacity:0.95">Top: <b>' +
          FWD_TOP.ps + '</b> (' + FWD_TOP.dist + ') &middot; score <b>' +
          FWD_TOP.score.toFixed(2) + '</b></span>'
        : '');
  }

  // Forecast map layer — pulsing orange circles over top-15 forecast PSes.
  const forecastLayer = L.layerGroup();
  FWD.slice(0, 15).forEach((f, i) => {
    if (typeof f.lat !== 'number' || typeof f.lon !== 'number') return;
    const m = L.circleMarker([f.lat, f.lon], {
      radius: 19 - Math.floor(i / 3),
      fillColor: '#f39c12', color: '#ffffff', weight: 2.5,
      opacity: 1, fillOpacity: 0.55,
    });
    m.bindTooltip(
      '<b>Forecast #' + (i + 1) + ' &middot; ' + (f.ps || '(no PS)') + '</b><br>' +
      (f.dist || '') + ' &middot; score ' + f.score.toFixed(2),
      { sticky: true, direction: 'top' }
    );
    forecastLayer.addLayer(m);
  });
  forecastLayer.addTo(map);

  // Wire the toggle (default ON to match the layer state).
  const cb = document.getElementById('lyr-forecast');
  if (cb) {
    cb.addEventListener('change', e => {
      if (e.target.checked) forecastLayer.addTo(map);
      else map.removeLayer(forecastLayer);
    });
  }
})();
</script>
</body>""",
    ),
]


def main():
    if not SOURCE_HTML.exists():
        print(f"ERROR: source dashboard not found at\n  {SOURCE_HTML}")
        print("Make sure the full project is at ../minorities_project relative to this folder.")
        return

    html = SOURCE_HTML.read_text(encoding="utf-8")

    # Pass 1 — PII redaction
    before = html.count('"desc":"')
    html = re.sub(
        r'"desc"\s*:\s*"(?:[^"\\]|\\.)*"',
        f'"desc":"{PLACEHOLDER}"',
        html,
    )
    after_pii = html.count(f'"desc":"{PLACEHOLDER}"')
    print(f"  PII pass:    {before:,} 'desc' fields -> {after_pii:,} placeholders.")

    # Pass 2 — Public-presentation polish
    polish_count = 0
    for pattern, replacement in POLISH_REPLACEMENTS:
        html, n = pattern.subn(replacement, html)
        polish_count += n
    print(f"  Polish pass: {polish_count} substitutions applied.")

    # Pass 3 — Replace the entire <style> block with the polished CSS
    html, k = STYLE_BLOCK_RE.subn(POLISHED_CSS, html, count=1)
    print(f"  UI polish:   {k} style block replaced.")

    DST_HTML.write_text(html, encoding="utf-8")
    print(f"  source:      {SOURCE_HTML}")
    print(f"  output:      {DST_HTML}")
    print("Done.")


if __name__ == "__main__":
    main()
