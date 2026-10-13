# -*- coding: utf-8 -*-
"""
Genereert het PDF-rapport 'AI-modellen bij JACOPS: benchmark, kosten & privacy'
Uitvoer: rapport-ai-modellen-jacops.html + rapport-ai-modellen-jacops.pdf
Vereist: weasyprint (pip install weasyprint)
"""
from pathlib import Path
from datetime import date

BASE = Path(__file__).parent
DATUM = "13 oktober 2026"

# ---------------------------------------------------------------- data ------
S = dict(i=6.5, c=82.7, o=0.61)          # 90M-sessiemix

def sess(i, c, o):
    return S["i"] * i + S["c"] * c + S["o"] * o

def m(x):                                 # NL-notatie $ 1,59
    return "$ " + f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def n(x, dec=1):
    return f"{x:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

# scores: naam, pdf_maken, ocr, excel, vba, coding, lastenboek, assistentie, privacy
MATRIX = [
    ("GPT-6 Astra", "9", "9", "9", "9", "10", "9", "9", "6"),
    ("Claude Opus 5.5", "9", "8,5", "9", "9", "10", "9", "9", "6,5"),
    ("Claude Sonnet 5.5", "9,5", "8", "9,5", "9", "9", "8,5", "9,5", "6,5"),
    ("GPT-6.1 Sol", "8,5", "8,5", "9", "9", "9,5", "9", "9", "6,5"),
    ("Muse Spark 1.3", "8,5", "9", "9", "8,5", "9,5", "9,5", "9", "6"),
    ("Muse Spark 1.3 Contributor", "8,5", "9", "9", "8,5", "9,5", "9,5", "9", "1,5"),
    ("Qwen3.8 Max", "9", "9,5", "9", "8,5", "9", "9", "8,5", "7,5"),
    ("Kimi K3", "8,5", "8", "8,5", "8", "9,5", "9", "8,5", "7,5"),
    ("GLM-5.3", "8,5", "7,5", "8,5", "8,5", "9", "8,5", "8", "7,5"),
    ("DeepSeek V4.1 Flash", "8,5", "8", "8,5", "8,5", "9,5", "8,5", "8,5", "7,5"),
    ("Mistral Large 4", "8", "7,5", "8,5", "8", "8", "9", "8", "10"),
    ("Gemini 3.8 Flash", "8,5", "8,5", "8", "7,5", "8", "8", "8,5", "7,5"),
    ("GLM-5.3-Flash", "8,5", "8", "8,5", "8", "8,5", "8", "8,5", "7,5"),
    ("Qwen3.8 Flash", "8,5", "8", "8,5", "8", "8,5", "8", "9", "7,5"),
    ("Space Bunny", "8", "7,5", "8", "7,5", "8,5", "8", "8,5", "8"),
    ("GPT-6 Luna", "7,5", "8", "8", "7,5", "8", "7,5", "8,5", "6,5"),
    ("Claude Haiku 5.5", "7", "7,5", "7,5", "7,5", "7,5", "7", "8", "6,5"),
    ("MiMo-V2.6-Flash", "7", "7", "7", "7", "7,5", "7", "8", "7,5"),
    ("Grok 4.7", "7,5", "7,5", "7,5", "7", "8", "7,5", "7,5", "6,5"),
    ("MiniMax-M3", "7", "7", "7", "7", "7,5", "7,5", "7,5", "7,5"),
]

def score_class(v):
    f = float(v.replace(",", "."))
    if f >= 9.5: return "s95"
    if f >= 8.5: return "s85"
    if f >= 7.5: return "s75"
    if f >= 6.5: return "s65"
    if f >= 5.0: return "s50"
    return "s0"

# tarieven: naam, in, cache, out
TARIEF = [
    ("Muse Spark 1.3 Contributor", 0.10, 0.002, 0.20),
    ("Claude Haiku 5.5 (Go/Zen, <=100K)", 0.10, 0.01, 0.50),
    ("GPT-6 Luna", 0.10, 0.01, 0.50),
    ("MiMo-V2.6-Flash", 0.14, 0.0028, 0.28),
    ("GLM-5.3-Flash", 0.15, 0.03, 0.50),
    ("Qwen3.8 Flash", 0.15, 0.016, 0.47),
    ("DeepSeek V4.1 Flash (Go off-peak)", 0.15, 0.003, 0.60),
    ("Space Bunny", 0.15, 0.03, 0.60),
    ("DeepSeek V4.1 Flash (Zen/piek)", 0.30, 0.006, 1.20),
    ("MiniMax-M3", 0.30, 0.06, 1.20),
    ("Qwen3.7 Plus", 0.40, 0.04, 1.60),
    ("DeepSeek V4 Pro 0813 (Go off-peak)", 0.66, 0.022, 1.98),
    ("Mistral Large 4 (Zen, -50%)", 0.68, 0.07, 2.09),
    ("Muse Spark 1.3", 1.25, 0.15, 4.25),
    ("GLM-5.3", 1.40, 0.26, 4.40),
    ("Gemini 3.8 Flash (Zen)", 1.50, 0.15, 7.50),
    ("Kimi K3", 3.00, 0.30, 15.00),
    ("Kimi K2.7 Code", 0.95, 0.19, 4.00),
    ("Claude Sonnet 5.5", 2.00, 0.20, 10.00),
    ("GPT-6.1 Sol (Zen)", 2.00, 0.10, 10.00),
    ("Qwen3.8 Max", 2.00, 0.25, 6.00),
    ("Grok 4.7", 2.00, 0.50, 6.00),
    ("Claude Opus 5.5", 4.00, 0.20, 20.00),
    ("GPT-6 Astra", 10.00, 1.00, 50.00),
    ("GPT-5.5 Pro", 30.00, 30.00, 180.00),
]

# kanaalvergelijking: naam, go(in,cache,out,limiet) of None, zen, direct, opmerking
KANAAL = [
    ("DeepSeek V4.1 Flash", (0.15, 0.003, 0.60, 80), (0.30, 0.006, 1.20), (0.15, 0.003, 0.60), "Direct off-peak = Go-tarief; piek = Zen-tarief"),
    ("GLM-5.3-Flash", (0.15, 0.03, 0.50, 60), (0.15, 0.03, 0.50), (0.15, 0.03, 0.50), "Prijs identiek bij Z.ai"),
    ("Qwen3.8 Flash", (0.15, 0.016, 0.47, 30), (0.15, 0.016, 0.47), (0.15, 0.016, 0.47), "Prijs identiek op QwenCloud"),
    ("GPT-6 Luna", (0.10, 0.01, 0.50, 15), (0.10, 0.01, 0.50), (0.10, 0.01, 0.50), "Prijs identiek bij OpenAI"),
    ("Claude Haiku 5.5", (0.10, 0.01, 0.50, 15), (0.10, 0.01, 0.50), (0.10, 0.01, 0.50), "Prijs identiek bij Anthropic (<100K)"),
    ("Qwen3.8 Max", (2.00, 0.25, 6.00, 15), (2.00, 0.25, 6.00), (2.00, 0.25, 6.00), "Go-limiet klein t.o.v. sessiekost"),
    ("Kimi K3", (3.00, 0.30, 15.00, 15), (3.00, 0.30, 15.00), (3.00, 0.30, 15.00), "Zwaarste sessiekost van de workhorses"),
    ("Claude Sonnet 5.5", None, (2.00, 0.20, 10.00), (2.00, 0.20, 10.00), "Niet in Go-abonnement; premium afwerking"),
    ("Claude Opus 5.5", None, (4.00, 0.20, 20.00), (4.00, 0.20, 20.00), "Duur per sessie, topkwaliteit"),
    ("GPT-6.1 Sol", None, (2.00, 0.10, 10.00), (2.00, 0.20, 10.00), "Zen cachelezing $ 0,10 vs direct $ 0,20"),
    ("Mistral Large 4", None, (0.68, 0.07, 2.09), (0.68, 0.07, 2.09), "La Plateforme zelfde tarief; EU-hosting"),
    ("Gemini 3.8 Flash", None, (1.50, 0.15, 7.50), (0.75, 0.075, 3.75), "Directe promo -50% t/m 31/12/2026"),
    ("Grok 4.7", (2.00, 0.50, 6.00, 15), (2.00, 0.50, 6.00), (2.00, 0.50, 6.00), "Zwakke cachekorting (75%)"),
]

def kanaal_rijen():
    rows = []
    for naam, go, zen, direct, opm in KANAAL:
        z = sess(*zen)
        d = sess(*direct)
        if go:
            g = sess(*go[:3])
            limiet = go[3]
            n_sess = limiet / g
            go_cel = m(g)
            lim_cel = f"{m(limiet)} &middot; ~{n(n_sess)} sessies inbegrepen"
        else:
            go_cel = "&ndash;"
            lim_cel = "n.v.t."
        d_cel = m(d) + ("" if d == z else f" <span class='tag'>promo</span>")
        verschil = "gelijk" if abs(d - z) < 0.005 else ("direct goedkoper" if d < z else "direct duurder")
        rows.append([naam, go_cel, lim_cel, m(z), d_cel, verschil, opm])
    return rows

# maandscenario: 20 zware sessies (1,8 miljard tokens)
def scenario_rijen():
    rows = []
    def regel(naam, go_sess, go_limiet, zen_sess):
        if go_sess is not None:
            binnen = min(20, go_limiet / go_sess)
            gemeten = 20 * go_sess
            if gemeten <= go_limiet:
                via_go = "$ 10,00 (abonnement)"
            else:
                extra = (gemeten - go_limiet) / go_sess
                via_go = f"$ 10,00 + {n(extra)} Zen-sessies ({m(extra * go_sess)})"
        else:
            via_go = "n.v.t."
        rows.append([naam, via_go, m(20 * zen_sess)])
    regel("DeepSeek V4.1 Flash (off-peak)", 1.59, 80, 3.18)
    regel("GLM-5.3-Flash", 3.76, 60, 3.76)
    regel("Qwen3.8 Flash", 2.58, 30, 2.58)
    regel("GPT-6 Luna of Claude Haiku 5.5", 1.78, 15, 1.78)
    rows.append(["Claude Sonnet 5.5 (premium)", "n.v.t.", m(20 * 35.64)])
    return rows

# grafiek: kosten per 90M-sessie (lineair, max 12)
BARS = [
    ("DeepSeek V4.1 Flash - Go (off-peak)", 1.59, "go"),
    ("GPT-6 Luna / Claude Haiku 5.5 - Go", 1.78, "go"),
    ("Qwen3.8 Flash - Go/Zen", 2.58, "go"),
    ("DeepSeek V4.1 Flash - Zen/direct piek", 3.18, "zen"),
    ("GLM-5.3-Flash", 3.76, "go"),
    ("DeepSeek V4 Pro 0813 - Go (off-peak)", 7.32, "go"),
    ("Mistral Large 4 - Zen (EU)", 11.48, "eu"),
]
BAR_MAX = 12.0

# EU-hosting kanttekening
EU_ROWS = [
    ("Scaleway - DeepSeek V4 Flash (met cache)", "\u20ac 9,70", "EU-gehost, cache \u20ac 0,08/M"),
    ("Scaleway - Qwen3.6-35B-A3B (geen cache)", "\u20ac 23,22", "89,2M input volledig gefactureerd"),
    ("OVHcloud - Qwen3.8-27B (geen cache)", "$ 43,75", "89,2M input volledig gefactureerd"),
    ("OpenCode Zen - DeepSeek V4.1 Flash (met cache)", "$ 3,18", "referentie: niet-EU-hosting bij OpenCode"),
]

# privacy: kanaal, hosting, training, retentie, ZDR, score
PRIVACY = [
    ("Mistral La Plateforme / Mistral via Zen", "Frankrijk / EU", "Nee, niet voor training", "Volgens ZDR-beleid (0 dagen)", "Ja", "10"),
    ("OVHcloud AI Endpoints", "Frankrijk (Gravelines)", "Nee (verwerkersovereenkomst)", "EU-opslag, GDPR", "Op aanvraag", "9,5"),
    ("Scaleway Generative APIs", "Frankrijk / EU", "Nee", "EU-opslag, GDPR", "Op aanvraag", "9,5"),
    ("OpenCode Go - open modellen (DeepSeek, GLM, Qwen, Kimi, MiMo, MiniMax)", "VS/EU", "Nee", "0 dagen", "Ja (DeepSeek-akkoord maandelijks hernieuwd, geldig t/m 31/10/2026)", "8"),
    ("OpenCode Zen - betaalde modellen", "VS/EU", "Nee", "0 dagen (uitzonderingen zie onder)", "Ja, standaard", "8"),
    ("OpenAI via Go/Zen of direct", "VS (EU-residentie mogelijk bij direct)", "Nee", "Max. 30 dagen (abuse monitoring)", "Mogelijk (enterprise)", "7"),
    ("Anthropic via Zen of direct", "VS", "Nee", "Max. 30 dagen", "Mogelijk (enterprise)", "7"),
    ("Google Gemini (direct)", "VS/EU naar keuze", "Nee (betaalde tier)", "Volgens Google Cloud-beleid", "Mogelijk", "7,5"),
    ("xAI Grok (direct)", "VS", "Nee", "Max. 30 dagen", "Ja (beperkt stateful features)", "6,5"),
    ("DeepSeek / Moonshot / Z.ai / Alibaba (directe API)", "China", "Nee, maar Chinese jurisdictie", "Eigen beleid", "Niet standaard", "3"),
    ("Meta Muse Spark (betaalde tier)", "VS", "Volgens standaardbeleid", "Volgens beleid", "Nee", "6"),
    ("Meta Muse Spark 1.3 Contributor", "VS", "JA - prompts en output trainen Meta-modellen", "Niet-ZDR", "Nee", "1,5"),
    ("Gratis stealth/modellen met feedbackclausule (Big Pickle, Cat Jam, Exo, MiMo-free, Ling-free, Nemotron-free)", "Varieert", "JA/onduidelijk (verbetering product)", "Gelogd", "Nee", "2"),
    ("Gratis met ZDR (Space Bunny Free, LongCat 2.5, Step 5)", "Varieert", "Nee", "0 dagen", "Ja", "8"),
    ("Self-host (Qwen3.8-27B, DeepSeek V4.1 Flash MIT) op eigen/EU-GPU", "Eigen beheer", "Nee", "Eigen beheer", "Ja", "10"),
]

# routing: taaktype, agent, model, prijs per 90M-sessie, opmerking
ROUTING = [
    ("Routeren/classificeren", "router", "GPT-6 Luna (Go)", "~$ 0,02", "goedkoop, laag risico"),
    ("Dagelijks coderen", "build", "DeepSeek V4.1 Flash (Go)", "~$ 1,59", "off-peak; anders $ 3,18"),
    ("PDF maken & styling", "pdf-designer", "Claude Sonnet 5.5", "~$ 35,64", "beste ontwerpresultaat; budget: GLM-5.3-Flash"),
    ("OCR & PDF lezen", "ocr-extractie", "Qwen3.8 Max", "~$ 37,33", "beste OCR-benchmarks; alternatief Qwen3.8 Flash"),
    ("Excel & Word genereren", "office-excel-word", "Claude Sonnet 5.5", "~$ 35,64", "expliciet sterk in spreadsheets"),
    ("VBA & Office-automatisering", "vba-specialist", "Claude Sonnet 5.5", "~$ 35,64", "legacy-stack; altijd testkopie"),
    ("Lastenboeken & bestekken", "lastenboek-analist", "Mistral Large 4 (EU)", "~$ 11,48", "Harvey Legal #6/75, FR/NL"),
    ("Vertrouwelijk werk", "vertrouwelijk-werk", "Mistral Large 4 (EU)", "~$ 11,48", "geen webtools, EU-verwerking"),
    ("Snelle assistentie", "snelle-vraag", "Claude Haiku 5.5 (Go)", "~$ 1,78", "240 t/s, snel en goedkoop"),
]

# ---------------------------------------------------------------- html ------
def table(headers, rows, cls="", foot=None):
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for r in rows:
        tds = ""
        for c in r:
            c = str(c)
            if cls == "matrix" and c.replace(",", ".").replace(".", "", 1).isdigit():
                tds += f'<td class="cell {score_class(c)}">{c}</td>'
            else:
                tds += f"<td>{c}</td>"
        body += f"<tr>{tds}</tr>"
    tfoot = f"<tfoot><tr><td colspan='{len(headers)}'>{foot}</td></tr></tfoot>" if foot else ""
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody>{tfoot}</table>'

def bars():
    html = ""
    for naam, val, soort in BARS:
        w = max(2.0, val / BAR_MAX * 100)
        html += (f'<div class="brow"><div class="blabel">{naam}</div>'
                 f'<div class="btrack"><div class="bar {soort}" style="width:{w:.1f}%"></div></div>'
                 f'<div class="bval">{m(val)}</div></div>')
    return html

matrix_rows = [[r[0]] + list(r[1:]) for r in MATRIX]
tarief_rows = [[t[0], m(t[1]), m(t[2]), m(t[3]), m(sess(t[1], t[2], t[3]))] for t in TARIEF]

CSS = """
@page {
  size: A4; margin: 16mm 13mm 18mm 13mm;
  @bottom-center { content: "AI-modellen bij JACOPS \u2014 benchmark, kosten & privacy \u2014 pagina " counter(page) " van " counter(pages); font-size: 7.5pt; color: #7a8694; }
}
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9.3pt; color: #1c2733; line-height: 1.42; margin: 0; }
h1 { font-size: 23pt; color: #16324f; margin: 0 0 4px 0; line-height: 1.15; }
h2 { font-size: 13.5pt; color: #16324f; border-bottom: 2.5px solid #e08a2e; padding-bottom: 3px; margin: 18px 0 7px 0; }
h3 { font-size: 10.8pt; color: #16324f; margin: 12px 0 4px 0; }
p { margin: 0 0 6px 0; }
ul { margin: 0 0 6px 16px; padding: 0; }
li { margin-bottom: 3px; }
table { width: 100%; border-collapse: collapse; margin: 6px 0 10px 0; }
th { background: #16324f; color: #fff; font-size: 8pt; text-align: left; padding: 4px 5px; vertical-align: top; }
td { font-size: 8.2pt; padding: 3.5px 5px; border-bottom: 0.6px solid #d7dde4; vertical-align: top; }
tbody tr:nth-child(even) { background: #f4f6f9; }
tfoot td { font-size: 7.6pt; color: #566573; font-style: italic; background: #fff; border-top: 1.2px solid #16324f; }
.cell { text-align: center; font-weight: 600; }
.s95 { background: #1c6b3c; color: #fff; } .s85 { background: #8fc7a2; }
.s75 { background: #d8ead9; } .s65 { background: #f3f0e4; }
.s50 { background: #f7ddb8; } .s0 { background: #e8a09a; color: #5c1613; font-weight: 700; }
.cover { border: 2.5px solid #16324f; border-radius: 6px; padding: 14px 16px; margin-bottom: 12px; }
.cover .sub { font-size: 11pt; color: #566573; }
.meta { font-size: 8.2pt; color: #566573; margin-top: 8px; }
.kpis { display: flex; gap: 8px; margin: 10px 0; }
.kpi { flex: 1; border: 1.2px solid #d7dde4; border-top: 4px solid #e08a2e; border-radius: 5px; padding: 8px 9px; }
.kpi .v { font-size: 15pt; font-weight: 700; color: #16324f; }
.kpi .l { font-size: 7.6pt; color: #566573; }
.tag { background: #e08a2e; color: #fff; border-radius: 8px; font-size: 6.6pt; padding: 0.5px 5px; vertical-align: 1px; }
.note { background: #fdf3e4; border-left: 3.5px solid #e08a2e; padding: 6px 9px; font-size: 8.4pt; margin: 7px 0; border-radius: 0 4px 4px 0; }
.brow { display: flex; align-items: center; gap: 7px; margin-bottom: 4px; }
.blabel { width: 44%; font-size: 8pt; }
.btrack { flex: 1; background: #eef1f5; height: 11px; border-radius: 6px; overflow: hidden; }
.bar { height: 11px; border-radius: 6px; }
.go { background: #2e7d4f; } .zen { background: #3f6ea5; } .eu { background: #8a5a2e; }
.bval { width: 12%; font-size: 8pt; text-align: right; font-weight: 600; color: #16324f; }
.small { font-size: 7.8pt; color: #566573; }
.pagebreak { page-break-before: always; }
.two { display: flex; gap: 12px; } .two > div { flex: 1; }
"""

HTML = f"""<!DOCTYPE html>
<html lang="nl"><head><meta charset="utf-8"><title>AI-modellen bij JACOPS</title><style>{CSS}</style></head>
<body>

<div class="cover">
  <h1>AI-modellen bij JACOPS</h1>
  <div class="sub">Benchmark \u00b7 kostenanalyse (OpenCode vs. directe API's) \u00b7 data &amp; privacy</div>
  <div class="meta">Opgesteld op {DATUM} \u00b7 Bronnen: OpenCode modelcatalogus &amp; documentatie (Zen, Go), OpenCode Data, Artificial Analysis, BenchLM, Vals AI, Mistral, OVHcloud, Scaleway \u00b7 Alle prijzen in USD tenzij vermeld (\u20ac = euro)</div>
</div>

<h2>1. Managementsamenvatting</h2>
<div class="kpis">
  <div class="kpi"><div class="v">{m(1.59)}</div><div class="l">kostprijs 90M-sessie DeepSeek V4.1 Flash via Go (off-peak) tegen {m(3.18)} via Zen/direct en {m(35.64)} voor Claude Sonnet 5.5</div></div>
  <div class="kpi"><div class="v">50&times;</div><div class="l">zoveel 90M-sessies binnen het Go-maandlimiet ($ 80) van DeepSeek V4.1 Flash \u2014 voor $ 10/maand abonnement</div></div>
  <div class="kpi"><div class="v">6 van 15</div><div class="l">modellen in ons voorstel zijn volledig EU-verwerkbaar (Mistral, OVHcloud, Scaleway of self-host)</div></div>
</div>
<ul>
  <li><b>Werkpaard:</b> DeepSeek V4.1 Flash is kwalitatief top (DeepSWE 74,2; AutomationBench 54,8; CyberGym 88,1) aan $ 0,15\u2013$ 0,30/M input met 98% cachekorting.</li>
  <li><b>Kanaalkeuze:</b> OpenCode Zen verkoopt vrijwel alle modellen aan exact dezelfde prijs als directe API's (at-cost, enkel betaalkosten 4,4% + $ 0,30 per transactie). Het Go-abonnement ($ 10/\u200b$ 40 p.m.) geeft 2\u00d7 tot 8\u00d7 korting op de open modellen via maandlimieten. Enkel Google (\u221250% promo) en sommige EU-clouds met tegoeden zijn direct voordeliger.</li>
  <li><b>EU/AVG:</b> voor dossiers met persoonsgegevens of klantvertrouwelijkheid: Mistral Large 4 (EU), OVHcloud/Scaleway of self-host. Nooit Contributor- of gratis-feedbackmodellen gebruiken voor klantdata.</li>
  <li><b>Routering in OpenCode:</b> geen enkele tool kent "vraag \u2192 model" out-of-the-box; de meegeleverde <i>router-agent</i> classificeert elke vraag en delegeert naar specialisten met eigen model (zie deel 7 en <i>opencode.json</i>).</li>
</ul>

<h2>2. Modellenlandschap vandaag (wat is nieuw t.o.v. de referentielijst)</h2>
<table>
<thead><tr><th>Eerder genoemd</th><th>Status nu</th><th>Vervanger / relevantie</th></tr></thead>
<tbody>
<tr><td>DeepSeek V3 / Coder</td><td>Uitgefaseerd</td><td>DeepSeek V4.1 Flash (10/09, MIT, 1M ctx); V4 Pro wordt sinds 14/09 naar V4.1 Flash gerouteerd</td></tr>
<tr><td>Claude Sonnet 5</td><td>Vervangen (28/09)</td><td>Claude Sonnet 5.5 \u2014 $ 2/\u200b$ 10, cachelezing gehalveerd naar $ 0,20</td></tr>
<tr><td>Claude Haiku 3.5</td><td>Gepensioneerd 16/02/2026</td><td>Claude Haiku 5.5 \u2014 $ 0,10/\u200b$ 0,50, 240 t/s, sterk op agentic taken</td></tr>
<tr><td>GPT-4o / 4o-mini</td><td>Vervangen</td><td>GPT-6 Luna (goedkoop werkpaard), GPT-6.1 Sol (documentspecialist)</td></tr>
<tr><td>Qwen3-Coder-30B</td><td>Uit catalogus</td><td>Qwen3.8 Flash (catalogus), Qwen3.8 27B (open weights, via OVH/Scaleway)</td></tr>
<tr><td>Codestral, Mistral Small 4, Ministral 3</td><td>Niet in OpenCode</td><td>Via La Plateforme (Codestral $ 0,30/\u200b$ 0,90 \u2014 FIM/aanvulling)</td></tr>
<tr><td>Nieuw, niet genoemd</td><td colspan="2">Claude Opus 5.5 \u00b7 GPT-6.1 Sol/Astra \u00b7 GLM-5.3(-Flash) \u00b7 Kimi K3 \u00b7 Qwen3.8 Max \u00b7 Muse Spark 1.3 (+Contributor) \u00b7 Space Bunny (stealth) \u00b7 MiMo-V2.6 \u00b7 Grok 4.7 \u00b7 Gemini 3.8 Flash \u00b7 Mistral OCR 4.1</td></tr>
</tbody></table>

<h2>3. Vergelijkende matrix (scores 1\u201310)</h2>
{table(["Model", "PDF maken", "PDF/OCR lezen", "Excel &amp; Word", "VBA &amp; Office", "Algemeen coderen", "Lastenboeken", "Assistentie", "Privacy"], matrix_rows, "matrix",
       "Scores zijn expertinschattingen op basis van publieke benchmarks (DeepSWE v1.1, Terminal-Bench 4.0, OCRBench V2, CC-OCR, GDPval-AA v2, Harvey Legal, JobBench) en leverancierspositionering. Voor VBA bestaat geen publieke benchmark; die kolom weegt legacy-stack-kennis, codekwaliteit en instructiegetrouwheid.")}

<div class="pagebreak"></div>
<h2>4. Tarieven, caching en de 90M-sessie</h2>
<p class="small">Sessiemodel: 6,5M unieke input + 82,7M cached input + 0,61M output = 90M tokens (zware agentische sessie, zoals gemeten in de praktijk: 95%+ cache-hits).</p>
{table(["Model", "Input $/1M", "Cached $/1M", "Output $/1M", "90M-sessie"], tarief_rows, "",
       "Tarieven OpenCode-catalogus 13/10/2026. GPT-6.1 Sol: Zen rekent $ 0,10 cachelezing; de directe OpenAI-API $ 0,20 \u2014 verifieer bij facturatie. De Go-tarieven gelden binnen het abonnement (maandlimieten).")}

<h3>Kosten per 90M-sessie \u2014 de workhorses vergeleken</h3>
{bars()}
<p class="small">Groen = Go-abonnement, blauw = Zen/direct, bruin = EU-premium. Volwaardige flagship-sessies kosten $ 27 (GPT-6.1 Sol) tot $ 178 (GPT-6 Astra); de keuze van het basismodel bepaalt dus 90% van de factuur.</p>

<div class="pagebreak"></div>
<h2>5. Kostenanalyse: OpenCode (Go &amp; Zen) vs. directe API's</h2>
<p><b>Hoe de kanalen zich verhouden.</b> OpenCode Zen (pay-as-you-go) rekent de lijstprijzen van de leveranciers door zonder marge (enkel betaalkosten: 4,4% + $ 0,30 per transactie). Voor bijna elk model is <i>Zen = directe API</i> qua prijs: DeepSeek, Mistral, OpenAI, Anthropic, Moonshot, Z.ai en Qwen hanteren overal dezelfde tarieven. Het verschil zit in gemak (één sleutel, één factuur, genormaliseerde ZDR), in provider-specifieke acties (Google-promo, batchkortingen, tegoeden bij EU-clouds) en in het <b>Go-abonnement</b>, dat open modellen met maandlimieten afkoopt tegen $ 10 (\u00b1$ 60\u2013$ 80 tegoed per model) of $ 40 (Go Plus).</p>

<h3>5.1 Per model: kost per 90M-sessie en Go-leverage</h3>
{table(["Model", "Via Go (abonnement)", "Limiet &amp; sessies inbegrepen", "Via Zen", "Via directe API", "Vergelijking", "Opmerking"], kanaal_rijen(), "",
       "Go-leverage = maandlimiet gedeeld door sessiekost. Voorbeeld: DeepSeek V4.1 Flash levert $ 80 / $ 1,59 \u2248 50 sessies voor $ 10 \u2014 87% voordeliger dan betalen per sessie aan het off-peak-tarief en 95% t.o.v. Zen.")}

<h3>5.2 Maandscenario: 20 zware sessies (\u00b11,8 miljard tokens)</h3>
{table(["Model", "Via Go", "Via Zen / direct"], scenario_rijen(), "",
       "Bij een Go-limietoverschrijding kun je 'Use balance' inschakelen: het overschot loopt dan via je Zen-saldo. Zonder fallback: resterend werk doorschuiven naar een ander Go-model of een gratis model.")}

<h3>5.3 Waar directe API's w\u00e9l winnen</h3>
<ul>
  <li><b>Google Gemini 3.8 Flash:</b> direct $ 0,75/\u200b$ 3,75 (promo t/m 31/12/2026) vs. $ 1,50/\u200b$ 7,50 via Zen \u2014 {m(13.37)} vs. {m(26.73)} per sessie. Vanaf 01/01/2027 verdubbelt de directe prijs ook.</li>
  <li><b>Modellen die niet in OpenCode zitten:</b> Codestral (FIM/aanvulling, $ 0,30/\u200b$ 0,90), Devstral 2 ($ 0,40/\u200b$ 2,00), Mistral Small 4, Ministral 3-serie, Mistral OCR 4.1 (per pagina: $ 4/1.000, batch $ 2, annotated $ 5), Qwen3.8 27B via OVH/Scaleway.</li>
  <li><b>Tegoeden en kortingen:</b> OVHcloud \u20ac 200 startkrediet, Scaleway \u20ac 100, Mistral $ 10/maand gratis credits, batch-API \u221250% bij vrijwel elke leverancier.</li>
  <li><b>Fine-tuning en self-hosting:</b> DeepSeek V4.1 Flash (MIT) en Qwen3.8 27B (Apache 2.0) mogen commercieel zelf gehost worden \u2014 interessant zodra volumes of privacy dat rechtvaardigen.</li>
</ul>

<div class="note"><b>Rekenvalkuil zonder prompt-caching.</b> De 90M-sessie is enkel betaalbaar dankzij caching (DeepSeek 98%, OpenAI/Anthropic 90\u201395%). Providers zonder gedocumenteerde caching factureren de volledige 89,2M input opnieuw. Zelfde werklast:</div>
{table(["Route", "Kost per sessie", "Toelichting"], EU_ROWS)}

<h3>5.4 Kostenefficiëntie per categorie (kwaliteit \u00f7 kost)</h3>
<table>
<thead><tr><th>Categorie</th><th>Beste kwaliteit</th><th>Beste waarde</th><th>Advies</th></tr></thead>
<tbody>
<tr><td>VBA &amp; Office</td><td>Sonnet 5.5 / GPT-6.1 Sol / Opus 5.5</td><td>GLM-5.3-Flash, DeepSeek V4.1 Flash, Qwen3.8 Flash</td><td>Premium voor complexe refactors; waarde-modellen voor bulkwerk met testkopie</td></tr>
<tr><td>PDF maken (WeasyPrint)</td><td>Sonnet 5.5 (9,5) \u2014 design-oog</td><td>GLM-5.3-Flash, Qwen3.8 Flash</td><td>Klantdeliverables op Sonnet; interne rapporten op Flash-modellen</td></tr>
<tr><td>PDF lezen &amp; OCR</td><td>Qwen3.8 Max (9,5), Muse Spark 1.3 (9)</td><td>Qwen3.8 Flash + Mistral OCR 4.1-pipeline</td><td>OCR altijd als aparte pipeline ($ 4/1.000 pag.), daarna LLM-analyse</td></tr>
<tr><td>Excel &amp; Word</td><td>Sonnet 5.5 (9,5), GPT-6.1 Sol, Qwen3.8 Max</td><td>Qwen3.8 Flash</td><td>Scripts blijven mensenwerk: altijd openen en valideren</td></tr>
<tr><td>Lastenboeken</td><td>Muse Spark 1.3, Opus 5.5, Mistral Large 4</td><td>DeepSeek V4.1 Flash, Mistral Large 4 (EU)</td><td>Mistral Large 4 combineert EU met Harvey Legal #6/75</td></tr>
<tr><td>Algemeen coderen</td><td>Astra / Opus 5.5 (10)</td><td>DeepSeek V4.1 Flash (Go), GLM-5.3-Flash</td><td>V4.1 Flash is de #1 in OpenCode-gebruik (43 biljoen tokens/week)</td></tr>
<tr><td>Assistentie</td><td>Sonnet 5.5 (9,5)</td><td>Haiku 5.5 / GPT-6 Luna / Qwen3.8 Flash</td><td>Haiku 5.5 met 240 t/s is de snelste</td></tr>
</tbody></table>

<div class="pagebreak"></div>
<h2>6. Data &amp; privacy-analyse</h2>
<p>Zeven op tien AI-lekken in bedrijven ontstaan door verkeerde kanaalkeuze, niet door het model zelf. Daarom per kanaal: waar wordt verwerkt, wordt er getraind op jouw data, hoe lang blijft die bewaard, en is er een zero-data-retention (ZDR)-garantie?</p>
{table(["Kanaal / leverancier", "Hosting", "Training op jouw data", "Retentie", "ZDR", "Score"], PRIVACY, "",
       "OpenCode Go hanteert voor de open modellen: niet gebruikt voor training + 0 dagen retentie. Let op: het DeepSeek-ZDR-akkoord wordt maandelijks hernieuwd (geldig t/m 31/10/2026). OpenCode Zen host in de VS en EU en geldt standaard als ZDR, met uitzondering van de genoemde gratis/Contributor-modellen.")}
<h3>Conclusies &amp; regels</h3>
<ul>
  <li><b>Vertrouwelijke klantdossiers, lastenboeken met prijsinfo, persoonsgegevens:</b> uitsluitend Mistral Large 4 (EU), een EU-gehost model (OVHcloud/Scaleway) of self-host. Dit kan volledig via OpenCode (mistral-large-4 zit in de catalogus).</li>
  <li><b>Interne code en documenten zonder persoonsgegevens:</b> Go/Zen-modellen met ZDR zijn verantwoord \u2014 dat is 80% van het werkvolume.</li>
  <li><b>Nooit:</b> Muse Spark 1.3 Contributor (uitdrukkelijk: prompts en output trainen Meta-modellen), Big Pickle, Cat Jam, Exo, MiMo-free, Ling-free, Nemotron-free (feedback/trial-clausules).</li>
  <li><b>Grijs zone:</b> DeepSeek/Moonshot/Z.ai/Alibaba <i>directe</i> API's = Chinese jurisdictie; via OpenCode Go zijn diezelfde modellen weliswaar ZDR, maar de juridische entiteit blijft Chinees \u2014 vermijd dit voor persoonsgegevens, ook via Go.</li>
  <li><b>ZDR verandert n\u00edet de modelkwaliteit of de prijs</b> \u2014 het is puur contractueel. Vraag bij kritieke dossiers de actuele ZDR-status op in de console.</li>
  <li><b>Prompt-caching en privacy:</b> caching verlaagt de kost drastisch, maar betekent dat de context tijdelijk bij de provider staat. Bij ZDR-providers is die context vluchtig; bij provider-zonder-ZDR Jour werkt de cache-vraag als drukkingsmiddel: kies eerst de privacy-tier, dan pas het model/tarief.</li>
</ul>

<h2>7. Eindadvies &amp; taakroutering in OpenCode</h2>
<p>OpenCode routeert niet automatisch op vraaginhoud. Drie officiële mechanismen lossen dit op \u2014 ze zitten alle drie in bijgeleverde <i>opencode.json</i>:</p>
<table>
<thead><tr><th>Mechanisme</th><th>Werking</th><th>Voorbeeld</th></tr></thead>
<tbody>
<tr><td>Router-agent (default)</td><td>Een goedkoop model (GPT-6 Luna) leest de vraag, klasseert ze en delegeert via de Task-tool naar de specialist met het juiste model</td><td>Gewoon typen: "lees dit bestek uit en maak een risico-tabel" \u2192 lastenboek-analist (Mistral Large 4)</td></tr>
<tr><td>Subagents met @</td><td>Handmatige, geforceerde route</td><td>@ocr-extractie haal tabel 3 uit deze scan</td></tr>
<tr><td>Commando's met /</td><td>Deterministische route met vast model</td><td>/pdf interventierapport werf 12 \u00b7 /vba macro.xlsm \u00b7 /confidentieel dossier-A</td></tr>
</tbody></table>
<h3>Taaktype \u2192 model (zoals geconfigureerd)</h3>
{table(["Taaktype", "Agent", "Model", "Prijs/sessie", "Opmerking"], ROUTING)}
<div class="note"><b>Installatie:</b> kopieer <i>opencode.json</i> naar de projectroot of naar <i>~/.config/opencode/</i>. Verbind OpenCode Go (abonnement) en/of OpenCode Zen (saldo voor Sonnet/Mistral/Qwen Max). De router staat standaard aan; wisselen kan met Tab (router / build / plan).</div>

<h3>Slotadvies in \u00e9\u00e9n alinea</h3>
<p>Zet het dagelijkse werk op <b>DeepSeek V4.1 Flash via Go</b> (50 zware sessies voor $ 10/maand), escaleer klantdeliverables naar <b>Claude Sonnet 5.5</b> en houd <b>Mistral Large 4</b> als EU-werkpaard voor alles met vertrouwelijke of juridisch-technische inhoud. Laat OCR via de <b>Qwen3.8-max of de OCR 4.1-pipeline</b> lopen en gebruik de router-agent zodat dit alles automatisch op de juiste plek terechtkomt \u2014 zonder dat iemand nog handmatig van model hoeft te wisselen.</p>

<p class="small" style="margin-top:14px">Verantwoording: prijzen en catalogusgegevens uit de OpenCode-omgeving (13/10/2026), OpenCode-documentatie (Zen, Go, agents, config, plugins), OpenCode Data (gebruik, sessiekosten, cache-ratio's), Artificial Analysis, BenchLM, Vals AI, llm-stats, leveranciersdocumentatie (Mistral, OVHcloud, Scaleway, DeepSeek, OpenAI, Anthropic, Google, xAI, Moonshot, Z.ai, Alibaba, Meta). Scores en kostenscores zijn inschattingen; tarieven kunnen wijzigen \u2014 controleer v\u00f3\u00f3r facturatie. Dit rapport is gegenereerd met Python + WeasyPrint.</p>

</body></html>
"""

(BASE / "rapport-ai-modellen-jacops.html").write_text(HTML, encoding="utf-8")
print("HTML geschreven:", BASE / "rapport-ai-modellen-jacops.html")

try:
    from weasyprint import HTML as WHTML
    WHTML(string=HTML, base_url=str(BASE)).write_pdf(BASE / "rapport-ai-modellen-jacops.pdf")
    print("PDF geschreven:", BASE / "rapport-ai-modellen-jacops.pdf")
except Exception as e:
    print("WeasyPrint-fout:", type(e).__name__, e)
    # Fallback: Microsoft Edge headless (geen GTK nodig)
    import shutil, subprocess, tempfile
    edge = None
    for p in (
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("msedge"),
    ):
        if p and Path(p).exists():
            edge = p
            break
    if edge:
        pdf = BASE / "rapport-ai-modellen-jacops.pdf"
        uri = "file:///" + str(BASE / "rapport-ai-modellen-jacops.html").replace("\\", "/").replace(" ", "%20")
        subprocess.run([
            edge, "--headless", "--disable-gpu", "--no-first-run", "--no-pdf-header-footer",
            f"--user-data-dir={tempfile.gettempdir()}\\edge-profile",
            f"--print-to-pdf={pdf}", uri,
        ], timeout=120)
        if pdf.exists():
            print("PDF via Edge geschreven:", pdf)
        else:
            print("Edge-fallback mislukt: PDF niet gevonden.")
    else:
        print("Geen Edge gevonden; installeer GTK voor WeasyPrint of open het HTML-bestand handmatig en druk op Ctrl+P > Opslaan als PDF.")
