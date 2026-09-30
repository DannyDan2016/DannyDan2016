"""Genera los componentes SVG animados del README de perfil.

Uso:
    python scripts/generate_assets.py

Crea en assets/ una variante por tema (dark/light) y, cuando el componente
tiene texto, por idioma (es/en). Solo usa la biblioteca estándar.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg": "#0a0c10", "dot": "#1a202b", "panel": "#0f141b", "chip": "#141a23",
        "border": "#232b38", "text": "#e6edf3", "muted": "#8b949e", "faint": "#2d3645",
        "g1": "#7b8cff", "g2": "#38e1ff", "green": "#3fb950", "orange": "#ff9a5c",
        "purple": "#b392f0", "chrome": "#131922", "pass_fg": "#0a0c10",
    },
    "light": {
        "bg": "#ffffff", "dot": "#e3e8ef", "panel": "#f6f8fa", "chip": "#ffffff",
        "border": "#d0d7de", "text": "#1f2328", "muted": "#59636e", "faint": "#d8dee4",
        "g1": "#4a5cff", "g2": "#0891b2", "green": "#1a7f37", "orange": "#c2410c",
        "purple": "#8250df", "chrome": "#eef1f4", "pass_fg": "#ffffff",
    },
}

MONO = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
MONO_W = 0.6  # ancho aproximado de un carácter monoespaciado, en em
SANS_W = 0.55


def x(text):
    return escape(text, {'"': "&quot;"})


def pct(value):
    return f"{value:.3f}".rstrip("0").rstrip(".")


def svg(w, h, t, body, css="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{x(title)}">
<title>{x(title)}</title>
<defs>
  <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['g1']}"/><stop offset="1" stop-color="{t['g2']}"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.1" fill="{t['dot']}"/>
  </pattern>
  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{t['g2']}" stop-opacity="0.16"/><stop offset="1" stop-color="{t['g2']}" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  .mono {{ font-family: {MONO}; }}
  .sans {{ font-family: {SANS}; }}
  @keyframes fadeUp {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
  @keyframes pulse {{ 0% {{ opacity: .8; transform: scale(1); }} 100% {{ opacity: 0; transform: scale(2.6); }} }}
{css}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
<rect width="{w}" height="{h}" rx="16" fill="{t['bg']}"/>
<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>
{body}
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="15.5" fill="none" stroke="{t['border']}"/>
</svg>
"""


def window_chrome(t, x0, y0, w, title):
    return f"""<rect x="{x0}" y="{y0}" width="{w}" height="36" rx="12" fill="{t['chrome']}"/>
<rect x="{x0}" y="{y0 + 24}" width="{w}" height="12" fill="{t['chrome']}"/>
<line x1="{x0}" y1="{y0 + 36}" x2="{x0 + w}" y2="{y0 + 36}" stroke="{t['border']}"/>
<circle cx="{x0 + 20}" cy="{y0 + 18}" r="6" fill="#ff5f57"/>
<circle cx="{x0 + 40}" cy="{y0 + 18}" r="6" fill="#febc2e"/>
<circle cx="{x0 + 60}" cy="{y0 + 18}" r="6" fill="#28c840"/>
<text x="{x0 + 84}" y="{y0 + 23}" class="mono" font-size="13" fill="{t['muted']}">{x(title)}</text>"""


def pass_badge(t, x0, y0):
    return f"""<rect x="{x0}" y="{y0 - 15}" width="52" height="21" rx="5" fill="{t['green']}"/>
<text x="{x0 + 26}" y="{y0}" class="mono" font-size="13" font-weight="700" text-anchor="middle" fill="{t['pass_fg']}">PASS</text>"""


# --------------------------------------------------------------------------- hero

HERO = {
    "es": {
        "kicker": "Advanced QA Engineer · 8+ años",
        "roles": ["Test Automation Architect", "AI-Driven Testing con Claude",
                  "Playwright · Pytest · Cypress", "Shift-Left & Continuous Testing"],
        "status": [("estado", "disponible"), ("rol", "QA Automation · Sr QA"),
                   ("modo", "remoto | híbrido"), ("sede", "Bogotá, CO")],
    },
    "en": {
        "kicker": "Advanced QA Engineer · 8+ years",
        "roles": ["Test Automation Architect", "AI-Driven Testing with Claude",
                  "Playwright · Pytest · Cypress", "Shift-Left & Continuous Testing"],
        "status": [("status", "open to work"), ("role", "QA Automation · Sr QA"),
                   ("mode", "remote | hybrid"), ("based", "Bogotá, CO")],
    },
}


def hero(t, lang):
    c = HERO[lang]
    w, h = 900, 250
    roles = c["roles"]
    n = len(roles)
    cycle = 4.0 * n
    fs = 18
    x0, y0 = 104, 212
    css, parts = [], []

    for i, role in enumerate(roles):
        tw = len(role) * fs * MONO_W
        a = i * 100 / n
        typed = a + 1.4 / cycle * 100
        erase = a + 3.2 / cycle * 100
        gone = a + 3.8 / cycle * 100
        end = (i + 1) * 100 / n
        steps = len(role)
        vis = f"0% {{ opacity: {1 if i == 0 else 0}; }}"
        if i > 0:
            vis += f" {pct(a)}% {{ opacity: 0; }} {pct(a + 0.01)}% {{ opacity: 1; }}"
        vis += f" {pct(end - 0.01)}% {{ opacity: 1; }} {pct(end)}% {{ opacity: 0; }} 100% {{ opacity: 0; }}"
        reveal = (f"0% {{ transform: translateX(-{tw + 24:.0f}px); }} "
                  f"{pct(a)}% {{ transform: translateX(-{tw + 24:.0f}px); animation-timing-function: steps({steps}, end); }} "
                  f"{pct(typed)}% {{ transform: translateX(0); }} "
                  f"{pct(erase)}% {{ transform: translateX(0); animation-timing-function: steps({steps}, end); }} "
                  f"{pct(gone)}% {{ transform: translateX(-{tw + 24:.0f}px); }} "
                  f"100% {{ transform: translateX(-{tw + 24:.0f}px); }}")
        caret = (f"0% {{ transform: translateX(0); }} "
                 f"{pct(a)}% {{ transform: translateX(0); animation-timing-function: steps({steps}, end); }} "
                 f"{pct(typed)}% {{ transform: translateX({tw:.0f}px); }} "
                 f"{pct(erase)}% {{ transform: translateX({tw:.0f}px); animation-timing-function: steps({steps}, end); }} "
                 f"{pct(gone)}% {{ transform: translateX(0); }} 100% {{ transform: translateX(0); }}")
        css.append(f"  @keyframes vis{i} {{ {vis} }}\n  @keyframes rev{i} {{ {reveal} }}\n  @keyframes car{i} {{ {caret} }}")
        css.append(f"  .role{i} {{ animation: vis{i} {cycle}s linear infinite; }}\n"
                   f"  .clip{i} {{ animation: rev{i} {cycle}s linear infinite; }}\n"
                   f"  .caret{i} {{ transform: translateX({tw:.0f}px); animation: car{i} {cycle}s linear infinite; }}")
        # el primer rol queda visible si no hay animación (prefers-reduced-motion)
        base_opacity = "" if i == 0 else ' opacity="0"'
        parts.append(f"""<clipPath id="c{i}"><rect class="clip{i}" x="{x0}" y="{y0 - 22}" width="{tw + 24:.0f}" height="32"/></clipPath>
<g class="role{i}"{base_opacity}>
  <text x="{x0}" y="{y0}" class="mono" font-size="{fs}" fill="{t['text']}" clip-path="url(#c{i})">{x(role)}</text>
  <g class="caret{i}"><rect class="blinker" x="{x0 + 2}" y="{y0 - 17}" width="10" height="21" rx="1" fill="{t['g2']}"/></g>
</g>""")

    css.append("  .blinker { animation: blink 1s step-end infinite; }")
    css.append("  .pulse { transform-box: fill-box; transform-origin: center; animation: pulse 1.8s ease-out infinite; }")
    css.append("  .in1 { animation: fadeUp .7s ease-out .1s both; } .in2 { animation: fadeUp .7s ease-out .35s both; }"
               " .in3 { animation: fadeUp .7s ease-out .6s both; } .in4 { animation: fadeUp .7s ease-out .9s both; }")

    line_numbers = "\n".join(
        f'<text x="44" y="{62 + 32 * i}" class="mono" font-size="14" fill="{t["faint"]}" text-anchor="end">{i + 1}</text>'
        for i in range(6))

    cx0, cy0, cw = 598, 58, 270
    status_rows = []
    for j, (k, v) in enumerate(c["status"]):
        yy = cy0 + 66 + j * 24
        color = t["green"] if j == 0 else t["text"]
        status_rows.append(
            f'<text x="{cx0 + 18}" y="{yy}" class="mono" font-size="12.5" fill="{t["g2"]}">{x(k)}:</text>'
            f'<text x="{cx0 + 92}" y="{yy}" class="mono" font-size="12.5" fill="{color}">{x(v)}</text>')
    status_block = f"""<g class="in4">
  <rect x="{cx0}" y="{cy0}" width="{cw}" height="150" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  <rect x="{cx0}" y="{cy0}" width="{cw}" height="2.5" rx="1" fill="url(#grad)"/>
  <text x="{cx0 + 18}" y="{cy0 + 30}" class="mono" font-size="12.5" fill="{t['muted']}">profile.yml</text>
  <circle class="pulse" cx="{cx0 + cw - 24}" cy="{cy0 + 26}" r="5" fill="{t['green']}"/>
  <circle cx="{cx0 + cw - 24}" cy="{cy0 + 26}" r="5" fill="{t['green']}"/>
  {''.join(status_rows)}
</g>"""

    body = f"""<circle cx="760" cy="110" r="260" fill="url(#glow)"/>
{line_numbers}
<g class="in1"><text x="80" y="62" class="mono" font-size="17" fill="{t['muted']}"><tspan fill="{t['g1']}">//</tspan> {x(c['kicker'])}</text></g>
<g class="in2"><text x="80" y="112" class="sans" font-size="40" font-weight="800" letter-spacing="6" fill="{t['text']}">DANNY PARRADO</text></g>
<g class="in3"><text x="77" y="172" class="sans" font-size="60" font-weight="800" letter-spacing="-1.5" fill="url(#grad)">AI Agentic QA</text></g>
<text x="80" y="{y0}" class="mono" font-size="{fs}" fill="{t['purple']}">$</text>
{''.join(parts)}
{status_block}"""
    return svg(w, h, t, body, "\n".join(css), "Danny Parrado — AI Agentic QA")


# ----------------------------------------------------------------------- terminal

AGENTS = [
    ("planner", "user story → test plan · ISTQB"),
    ("generator", "Playwright · Pytest · POM"),
    ("api", "Postman · Swagger · REST"),
    ("perf", "K6 · load & stress"),
    ("judge", "LLM-as-a-Judge review"),
    ("ci", "GitHub Actions · Docker"),
]


def terminal(t):
    w = 900
    lh = 30
    top = 36 + 38
    rows = 3 + len(AGENTS)
    h = top + rows * lh + 10
    cycle = 12.0
    css = []

    def appear(i):
        start = (0.5 + i * 0.55) / cycle * 100
        css.append(f"  @keyframes ln{i} {{ 0% {{ opacity: 0; transform: translateY(5px); }} "
                   f"{pct(start)}% {{ opacity: 0; transform: translateY(5px); }} "
                   f"{pct(start + 2.5)}% {{ opacity: 1; transform: translateY(0); }} "
                   f"90% {{ opacity: 1; transform: translateY(0); }} 96% {{ opacity: 0; }} 100% {{ opacity: 0; }} }}\n"
                   f"  .ln{i} {{ animation: ln{i} {cycle}s ease-out infinite; }}")
        return f"ln{i}"

    lines = []
    xl = 28
    y = top
    lines.append(f"""<g class="{appear(0)}"><text x="{xl}" y="{y}" class="mono" font-size="15"><tspan fill="{t['purple']}">$</tspan><tspan fill="{t['text']}"> qa-agents run</tspan><tspan fill="{t['muted']}"> --story</tspan><tspan fill="{t['orange']}"> "checkout-flow"</tspan></text></g>""")
    y += lh
    lines.append(f"""<g class="{appear(1)}"><text x="{xl}" y="{y}" class="mono" font-size="15"><tspan fill="{t['g2']}">›</tspan><tspan fill="{t['g1']}" font-weight="700"> orchestrator</tspan><tspan fill="{t['muted']}"> → spawning {len(AGENTS)} subagents</tspan></text></g>""")
    for i, (name, desc) in enumerate(AGENTS):
        y += lh
        cls = appear(i + 2)
        lines.append(f"""<g class="{cls}"><text x="{xl}" y="{y}" class="mono" font-size="15" fill="{t['green']}">✓</text>
<text x="{xl + 24}" y="{y}" class="mono" font-size="15" fill="{t['g2']}">{x(name)}</text>
<text x="{xl + 138}" y="{y}" class="mono" font-size="15" fill="{t['text']}">{x(desc)}</text></g>""")
    y += lh
    cls = appear(len(AGENTS) + 2)
    lines.append(f"""<g class="{cls}">{pass_badge(t, xl, y)}
<text x="{xl + 64}" y="{y}" class="mono" font-size="15" fill="{t['muted']}">all agents green · <tspan fill="{t['orange']}">-60%</tspan> manual QA tasks</text></g>""")

    # grafo orquestador → subagentes
    ox, oy = 610, top + (rows * lh) / 2 - 16
    nx = 780
    span = (len(AGENTS) - 1) * 40
    graph = [f'<line x1="545" y1="{top - 18}" x2="545" y2="{h - 18}" stroke="{t["border"]}" stroke-dasharray="3 5"/>']
    css.append("  @keyframes flow { to { stroke-dashoffset: -24; } }\n  .edge { animation: flow 1.2s linear infinite; }")
    for i, (name, _) in enumerate(AGENTS):
        ny = oy - span / 2 + i * 40
        graph.append(f'<path class="edge" d="M{ox + 30} {oy} C {ox + 90} {oy}, {nx - 80} {ny}, {nx - 12} {ny}" fill="none" stroke="url(#grad)" stroke-width="1.6" stroke-dasharray="6 6" opacity=".75"/>')
        graph.append(f'<g class="ln{i + 2}"><circle cx="{nx}" cy="{ny}" r="11" fill="{t["panel"]}" stroke="{t["green"]}" stroke-width="2"/>'
                     f'<text x="{nx}" y="{ny + 4}" class="mono" font-size="11" fill="{t["green"]}" text-anchor="middle">✓</text>'
                     f'<text x="{nx + 20}" y="{ny + 4}" class="mono" font-size="12.5" fill="{t["text"]}">{x(name)}</text></g>')
    graph.append(f'<circle class="pulse" cx="{ox}" cy="{oy}" r="26" fill="none" stroke="{t["g2"]}" stroke-width="2"/>'
                 f'<circle cx="{ox}" cy="{oy}" r="28" fill="{t["panel"]}" stroke="url(#grad)" stroke-width="2.5"/>'
                 f'<text x="{ox}" y="{oy + 5}" class="mono" font-size="13" font-weight="700" fill="{t["g1"]}" text-anchor="middle">orch</text>'
                 f'<text x="{ox}" y="{oy + 50}" class="mono" font-size="11.5" fill="{t["muted"]}" text-anchor="middle">Claude</text>')
    css.append("  .pulse { transform-box: fill-box; transform-origin: center; animation: pulse 2s ease-out infinite; }")

    body = f"""{window_chrome(t, 0, 0, w, 'qa-agents — zsh')}
<circle cx="700" cy="{h / 2 + 10}" r="220" fill="url(#glow)"/>
{''.join(graph)}
{''.join(lines)}"""
    return svg(w, h, t, body, "\n".join(css), "qa-agents: multi-agent AI testing pipeline")


# ------------------------------------------------------------------------- impact

IMPACT = {
    "es": {
        "title": "qa-report --impact",
        "items": [("-", 60, "tareas manuales de QA con IA", "Simetrik · fintech"),
                  ("-", 70, "defectos en CRM B2B", "Ingenia · 0 críticos en prod"),
                  ("-", 60, "tiempo de ejecución E2E", "Enmedio · medios digitales"),
                  ("+", 30, "rapidez en despliegues", "Visionamos · banca")],
        "footer": "8+ años en producción · fintech · banca · retail · CRM B2B",
    },
    "en": {
        "title": "qa-report --impact",
        "items": [("-", 60, "manual QA tasks, using AI", "Simetrik · fintech"),
                  ("-", 70, "defects in a B2B CRM", "Ingenia · 0 critical in prod"),
                  ("-", 60, "E2E execution time", "Enmedio · digital media"),
                  ("+", 30, "faster deployments", "Visionamos · banking")],
        "footer": "8+ years in production · fintech · banking · retail · B2B CRM",
    },
}


def impact(t, lang):
    c = IMPACT[lang]
    w, h = 900, 332
    css = ["  @keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }",
           "  @keyframes flash { 0%, 100% { opacity: 1; } }",
           "  @keyframes appear { from { opacity: 0; } to { opacity: 1; } }",
           "  .bar { transform-box: fill-box; transform-origin: left; }"]
    cards = []
    for i, (sign, val, label, sub) in enumerate(c["items"]):
        col, row = i % 2, i // 2
        cx0, cy0 = 24 + col * 432, 58 + row * 112
        delay = 0.3 + i * 0.25
        steps = 6
        slot = 0.11
        counter = []
        for k in range(1, steps):
            v = round(val * k / steps)
            counter.append(f'<text x="{cx0 + 22}" y="{cy0 + 62}" class="sans" font-size="40" font-weight="800" fill="url(#grad)" opacity="0" '
                           f'style="animation: flash {slot}s linear {delay + (k - 1) * slot:.2f}s">{sign}{v}%</text>')
        counter.append(f'<text x="{cx0 + 22}" y="{cy0 + 62}" class="sans" font-size="40" font-weight="800" fill="url(#grad)" '
                       f'style="animation: appear .01s linear {delay + (steps - 1) * slot:.2f}s both">{sign}{val}%</text>')
        bar_w = 244
        cards.append(f"""<g style="animation: fadeUp .6s ease-out {delay - 0.2:.2f}s both">
  <rect x="{cx0}" y="{cy0}" width="420" height="100" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  {''.join(counter)}
  <text x="{cx0 + 152}" y="{cy0 + 40}" class="sans" font-size="16" font-weight="600" fill="{t['text']}">{x(label)}</text>
  <text x="{cx0 + 152}" y="{cy0 + 60}" class="mono" font-size="12" fill="{t['muted']}">{x(sub)}</text>
  <rect x="{cx0 + 152}" y="{cy0 + 74}" width="{bar_w}" height="6" rx="3" fill="{t['faint']}"/>
  <rect class="bar" x="{cx0 + 152}" y="{cy0 + 74}" width="{bar_w * val / 100:.0f}" height="6" rx="3" fill="url(#grad)" style="animation: grow 1s cubic-bezier(.2,.8,.2,1) {delay:.2f}s both"/>
</g>""")
    fy = h - 26
    footer = f"""<g style="animation: fadeUp .6s ease-out 1.6s both">{pass_badge(t, 24, fy)}
<text x="88" y="{fy}" class="mono" font-size="14" fill="{t['muted']}">{x(c['footer'])}</text></g>"""
    body = f"""{window_chrome(t, 0, 0, w, c['title'])}
{''.join(cards)}
{footer}"""
    return svg(w, h, t, body, "\n".join(css), "Impact metrics")


# ----------------------------------------------------------------------- timeline

TIMELINE = {
    "es": [("2018", "Rappipage", "Analista QA", "Postman · SQL Server"),
           ("2019", "Corbeta / Alkosto", "Analista QA", "SoapUI · SQL Server"),
           ("2022", "Visionamos", "Analista QA · banca", "Python · Selenium"),
           ("2023", "Ingenia", "Analista QA · CRM B2B", "Cypress · JMeter"),
           ("2024", "Enmedio", "Analista QA · medios", "Cypress · Playwright"),
           ("2025", "Simetrik", "Advanced QA Engineer", "Playwright · Claude agents")],
    "en": [("2018", "Rappipage", "QA Analyst", "Postman · SQL Server"),
           ("2019", "Corbeta / Alkosto", "QA Analyst", "SoapUI · SQL Server"),
           ("2022", "Visionamos", "QA Analyst · banking", "Python · Selenium"),
           ("2023", "Ingenia", "QA Analyst · B2B CRM", "Cypress · JMeter"),
           ("2024", "Enmedio", "QA Analyst · media", "Cypress · Playwright"),
           ("2025", "Simetrik", "Advanced QA Engineer", "Playwright · Claude agents")],
}


def timeline(t, lang):
    items = TIMELINE[lang]
    w, h = 900, 292
    axis_y = 172
    x_start, x_end = 110, 790
    gap = (x_end - x_start) / (len(items) - 1)
    length = x_end - x_start
    css = [f"  @keyframes draw {{ from {{ stroke-dashoffset: {length}; }} to {{ stroke-dashoffset: 0; }} }}",
           "  @keyframes pop { from { opacity: 0; transform: scale(.2); } to { opacity: 1; transform: scale(1); } }",
           "  .node { transform-box: fill-box; transform-origin: center; }",
           "  .pulse { transform-box: fill-box; transform-origin: center; animation: pulse 1.8s ease-out 2.6s infinite; }"]
    parts = [f'<line x1="{x_start}" y1="{axis_y}" x2="{x_end}" y2="{axis_y}" stroke="{t["faint"]}" stroke-width="3" stroke-linecap="round"/>',
             f'<line x1="{x_start}" y1="{axis_y}" x2="{x_end}" y2="{axis_y}" stroke="url(#grad)" stroke-width="3" stroke-linecap="round" '
             f'stroke-dasharray="{length}" style="animation: draw 2.4s ease-in-out .2s both"/>']
    for i, (year, company, role, tech) in enumerate(items):
        cx = x_start + i * gap
        delay = 0.2 + 2.4 * i / (len(items) - 1)
        last = i == len(items) - 1
        above = i % 2 == 0
        ys = [86, 106, 124, 142] if above else [212, 232, 250, 268]
        tick = (axis_y - 22, axis_y - 12) if above else (axis_y + 12, axis_y + 22)
        name_color = "url(#grad)" if last else t["text"]
        r = 9 if last else 7
        fill = "url(#grad)" if last else t["panel"]
        ring = f'<circle class="pulse" cx="{cx}" cy="{axis_y}" r="9" fill="none" stroke="{t["g2"]}" stroke-width="2"/>' if last else ""
        parts.append(f"""<g style="animation: fadeUp .6s ease-out {delay + 0.1:.2f}s both">
  <line x1="{cx}" y1="{tick[0]}" x2="{cx}" y2="{tick[1]}" stroke="{t['border']}" stroke-width="1.5"/>
  <text x="{cx}" y="{ys[0]}" class="mono" font-size="13" fill="{t['g2']}" text-anchor="middle">{year}</text>
  <text x="{cx}" y="{ys[1]}" class="sans" font-size="15.5" font-weight="700" fill="{name_color}" text-anchor="middle">{x(company)}</text>
  <text x="{cx}" y="{ys[2]}" class="sans" font-size="12.5" fill="{t['muted']}" text-anchor="middle">{x(role)}</text>
  <text x="{cx}" y="{ys[3]}" class="mono" font-size="11" fill="{t['g1']}" text-anchor="middle">{x(tech)}</text>
</g>
{ring}<circle class="node" cx="{cx}" cy="{axis_y}" r="{r}" fill="{fill}" stroke="{t['g1']}" stroke-width="2.5" style="animation: pop .45s cubic-bezier(.3,1.6,.5,1) {delay:.2f}s both"/>""")
    title = "git log --career --since=2018" if lang == "en" else "git log --trayectoria --since=2018"
    body = f"""{window_chrome(t, 0, 0, w, title)}
{''.join(parts)}"""
    return svg(w, h, t, body, "\n".join(css), "Career timeline")


# -------------------------------------------------------------------------- stack

STACK = {
    "es": ["Automatización", "IA aplicada a QA", "API y rendimiento", "CI/CD y nube", "Lenguajes y datos", "Gestión y agilidad"],
    "en": ["Test automation", "AI for QA", "API & performance", "CI/CD & cloud", "Languages & data", "Delivery & agile"],
}
STACK_CHIPS = [
    ("g1", ["Playwright", "Pytest", "Cypress", "Selenium WebDriver", "Page Object Model", "Cucumber · BDD"]),
    ("purple", ["Claude", "AI Agents", "Subagents", "LLM-as-a-Judge", "Prompt Engineering", "n8n"]),
    ("orange", ["Postman", "Swagger", "SoapUI", "REST", "SOAP", "K6", "JMeter"]),
    ("g2", ["GitHub Actions", "Harness", "Jenkins", "Docker", "AWS CloudWatch", "AWS S3", "Git"]),
    ("green", ["Python", "JavaScript", "TypeScript", "SQL", "PostgreSQL", "SQL Server", "MongoDB"]),
    ("muted", ["Jira", "Linear", "Azure DevOps", "Scrum", "Kanban", "ISTQB", "Notion"]),
]


def stack(t, lang):
    w = 900
    fs = 12.5
    chip_h, pad, gap = 26, 12, 8
    x_chips, x_max = 222, w - 24
    y = 36 + 26
    parts, n = [], 0
    for label, (color, chips) in zip(STACK[lang], STACK_CHIPS):
        row_y = y
        parts.append(f'<circle cx="32" cy="{row_y + chip_h / 2}" r="4" fill="{t[color]}"/>'
                     f'<text x="46" y="{row_y + 17.5}" class="sans" font-size="14" font-weight="600" fill="{t["text"]}">{x(label)}</text>')
        cx = x_chips
        for chip in chips:
            cw = len(chip) * fs * MONO_W + pad * 2
            if cx + cw > x_max:
                cx = x_chips
                y += chip_h + 8
            parts.append(f"""<g style="animation: fadeUp .5s ease-out {0.15 + n * 0.035:.2f}s both">
  <rect x="{cx}" y="{y}" width="{cw:.0f}" height="{chip_h}" rx="7" fill="{t['chip']}" stroke="{t['border']}"/>
  <rect x="{cx}" y="{y + 7}" width="2.5" height="12" rx="1" fill="{t[color]}"/>
  <text x="{cx + pad}" y="{y + 17.5}" class="mono" font-size="{fs}" fill="{t['text']}">{x(chip)}</text>
</g>""")
            cx += cw + gap
            n += 1
        y += chip_h + 14
    h = int(y + 10)
    title = "stack.config"
    body = f"""{window_chrome(t, 0, 0, w, title)}
{''.join(parts)}"""
    return svg(w, h, t, body, "", "Tech stack")


# -------------------------------------------------------------------------- cards

PROJECTS = [
    {
        "repo": "cypress-automation-demoqa",
        "lang": ("JavaScript", "#f1e05a"),
        "tags": ["Cypress", "JavaScript", "POM", "Mochawesome"],
        "es": ("E2E web automation · DemoQA",
               "Suite End-to-End con Cypress y Page Object Model: formularios, tablas, botones y reportes Mochawesome."),
        "en": ("E2E web automation · DemoQA",
               "End-to-end suite built with Cypress and the Page Object Model: forms, tables, buttons and Mochawesome reports."),
    },
    {
        "repo": "Test-frontend-QA-Cod",
        "lang": ("Python", "#3572A5"),
        "tags": ["Playwright", "Pytest", "POM", "Allure"],
        "es": ("E2E checkout · Sauce Demo",
               "Flujo completo de compra con Playwright + Pytest bajo POM, con reportes Allure y pipeline CI."),
        "en": ("E2E checkout · Sauce Demo",
               "Full purchase flow automated with Playwright + Pytest using POM, with Allure reports and a CI pipeline."),
    },
    {
        "repo": "Test-Backend-Cod",
        "lang": ("Python", "#3572A5"),
        "tags": ["Pytest", "Requests", "REST API", "Allure"],
        "es": ("API testing · ReqRes",
               "Pruebas de API REST parametrizadas con Pytest + Requests: casos positivos y negativos con reportes Allure."),
        "en": ("API testing · ReqRes",
               "Parametrized REST API tests with Pytest + Requests: positive and negative cases with Allure reports."),
    },
]


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    lines.append(cur)
    return lines


def card(t, project, lang):
    w, h = 440, 190
    subtitle, desc = project[lang]
    lang_name, lang_color = project["lang"]
    css = ["  @keyframes sweep { from { transform: translateX(-160px); } to { transform: translateX(600px); } }",
           "  .sweep { animation: sweep 3.5s ease-in-out infinite; }"]
    desc_lines = "".join(
        f'<text x="24" y="{92 + i * 20}" class="sans" font-size="13.5" fill="{t["text"]}">{x(line)}</text>'
        for i, line in enumerate(wrap(desc, 56)[:3]))
    chips, cx = [], 24
    for tag in project["tags"]:
        cw = len(tag) * 11 * MONO_W + 18
        chips.append(f'<rect x="{cx}" y="{h - 40}" width="{cw:.0f}" height="22" rx="11" fill="{t["chip"]}" stroke="{t["border"]}"/>'
                     f'<text x="{cx + 9}" y="{h - 25}" class="mono" font-size="11" fill="{t["g2"]}">{x(tag)}</text>')
        cx += cw + 6
    body = f"""<clipPath id="top"><rect x="0" y="0" width="{w}" height="{h}" rx="16"/></clipPath>
<g clip-path="url(#top)"><rect x="0" y="0" width="{w}" height="3" fill="{t['faint']}"/>
<rect class="sweep" x="0" y="0" width="160" height="3" fill="url(#grad)"/></g>
<path transform="translate(24 24) scale(1.1)" fill="{t['muted']}" d="M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"/>
<text x="50" y="37" class="mono" font-size="15" font-weight="700" fill="{t['g1']}">{x(project['repo'])}</text>
<text x="24" y="62" class="sans" font-size="12.5" font-weight="600" fill="{t['muted']}">{x(subtitle)}</text>
<circle cx="{w - 24 - len(lang_name) * 12 * SANS_W - 12}" cy="58" r="5" fill="{lang_color}"/>
<text x="{w - 24}" y="62" class="sans" font-size="12" fill="{t['muted']}" text-anchor="end">{lang_name}</text>
{desc_lines}
{''.join(chips)}"""
    return svg(w, h, t, body, "\n".join(css), project["repo"])


# --------------------------------------------------------------------------- main

def main():
    OUT.mkdir(exist_ok=True)
    files = {}
    for theme, t in THEMES.items():
        files[f"terminal-{theme}.svg"] = terminal(t)
        for lang in ("es", "en"):
            files[f"hero-{lang}-{theme}.svg"] = hero(t, lang)
            files[f"impact-{lang}-{theme}.svg"] = impact(t, lang)
            files[f"timeline-{lang}-{theme}.svg"] = timeline(t, lang)
            files[f"stack-{lang}-{theme}.svg"] = stack(t, lang)
            for p in PROJECTS:
                files[f"card-{p['repo'].lower()}-{lang}-{theme}.svg"] = card(t, p, lang)
    for name, content in files.items():
        (OUT / name).write_text(content, encoding="utf-8")
    print(f"{len(files)} SVG generados en {OUT}")


if __name__ == "__main__":
    main()
