#!/usr/bin/env python3
"""Render zjn281r's GitHub profile as animated, self-contained SVG cards.

SVGs are safe to show through README img tags: inline CSS/SMIL only, embedded
subset WOFF fonts, and no external requests. Use STATIC=1 for final frames.
"""
from __future__ import annotations

import base64
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "cards"
FONT_DIR = ROOT / "fonts"
PORTRAIT = ROOT / "source-photo.jpg"
WIDTH, GAP = 960, 14
BG, PANEL, PANEL_2 = "#080e15", "#101923", "#14212d"
INK, MUTED, FAINT, RULE = "#f3f5f7", "#91a0b2", "#526071", "#99acc129"
BLUE, CYAN, LIME = "#72a9ff", "#67e8f9", "#a8f36b"
SERIF, SANS, MONO = "Georgia, 'Times New Roman', serif", "Arial, Helvetica, sans-serif", "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace"
STATIC = bool(os.environ.get("STATIC"))
FONT_SOURCES = {
    "serif": ("serif-400.woff", "Georgia", "normal", "400"),
    "serif-i": ("serif-italic.woff", "Georgia", "italic", "400"),
    "sans": ("geist-400.woff", "Geist", "normal", "400"),
    "sans-b": ("geist-600.woff", "Geist", "normal", "600"),
    "mono": ("geistmono-400.woff", "Geist Mono", "normal", "400"),
}
CSS = """
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes pulse{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes drift{0%,100%{transform:rotate(-25deg)}50%{transform:rotate(25deg)}}
@keyframes sweep{from{transform:translateX(-180px)}to{transform:translateX(620px)}}
.rise{opacity:0;animation:rise .75s cubic-bezier(.2,.7,.2,1) both;transform-box:fill-box}
.fade{opacity:0;animation:fade .75s ease-out both}.grow{transform-box:fill-box;transform-origin:bottom;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}
.pulse{animation:pulse 2s ease-in-out infinite}.drift{transform-box:fill-box;transform-origin:center;animation:drift 10s ease-in-out infinite}.sweep{animation:sweep 5s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.rise,.fade,.grow,.pulse,.drift,.sweep{animation:none!important;opacity:1!important;transform:none!important}.smil{display:none!important}}
"""


def subset_fonts() -> dict[str, str]:
    """Run pyftsubset when available; committed WOFFs are local-preview fallback."""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,/:+&-—'!?()<>@#%↑·"
    executable = shutil.which("pyftsubset")
    result = {}
    for key, (filename, family, style, weight) in FONT_SOURCES.items():
        source = FONT_DIR / filename
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / filename
            if executable:
                subprocess.run([executable, str(source), f"--output-file={target}", f"--text={chars}", "--flavor=woff"], check=True)
                raw = target.read_bytes()
            else:
                raw = source.read_bytes()
        result[key] = f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};src:url(data:font/woff;base64,{base64.b64encode(raw).decode()}) format('woff')}}"
    return result


FONT_CSS = subset_fonts()


def delay(seconds: float) -> str:
    return f'style="animation-delay:{seconds:.2f}s"'


def svg(name: str, height: int, body: str, fonts: tuple[str, ...], label: str) -> None:
    css = "".join(FONT_CSS[k] for k in fonts) + CSS
    if STATIC:
        css += ".rise,.fade,.grow,.pulse,.drift,.sweep{animation:none!important;opacity:1!important;transform:none!important}"
    content = f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><style>{css}</style>{body}</svg>\n'
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"wrote cards/{name} ({len(content) // 1024} KB)")


def lines(x: int, y: int, values: list[str], step: int, attrs: str) -> str:
    return "".join(f'<text x="{x}" y="{y + i * step}" {attrs}>{escape(value)}</text>' for i, value in enumerate(values))


def wrap(text: str, limit: int) -> list[str]:
    result, current = [], ""
    for word in text.split():
        if current and len(current) + len(word) + 1 > limit:
            result.append(current); current = word
        else:
            current = f"{current} {word}".strip()
    return result + ([current] if current else [])


def hero() -> None:
    h = 420
    smil = "" if STATIC else '<animateTransform attributeName="transform" type="rotate" values="-3 790 190;3 790 190;-3 790 190" dur="9s" repeatCount="indefinite"/>'
    portrait = ""
    if PORTRAIT.exists():
        encoded = base64.b64encode(PORTRAIT.read_bytes()).decode()
        portrait = f'<clipPath id="portrait"><circle cx="790" cy="190" r="112"/></clipPath><image href="data:image/jpeg;base64,{encoded}" x="678" y="78" width="224" height="224" preserveAspectRatio="xMidYMid slice" clip-path="url(#portrait)" opacity=".92"/>'
    body = f'''<rect width="{WIDTH}" height="{h}" rx="16" fill="{BG}"/><path class="drift smil" d="M610 190c80-126 244-126 324 0s-80 126-160 0-244-126-324 0" fill="none" stroke="{BLUE}" stroke-opacity=".22">{smil}</path>
<circle class="pulse" cx="80" cy="68" r="5" fill="{LIME}"/><text class="fade" {delay(.1)} x="98" y="73" font-family="{MONO}" font-size="12" letter-spacing="1.2" fill="{MUTED}">NASSER HUSSAIN / ZJN281R</text>
<text class="rise" {delay(.25)} x="72" y="175" font-family="{SERIF}" font-size="76" fill="{INK}">Designing systems</text><text class="rise" {delay(.4)} x="72" y="248" font-family="{SERIF}" font-style="italic" font-size="76" fill="{BLUE}">for real momentum.</text>
<g class="rise" {delay(.62)}>{lines(76, 300, ['Brand, digital product, and growth—made clear,', 'useful, and built to move people forward.'], 24, f'font-family="{SANS}" font-size="17" fill="{MUTED}"')}</g>
<text class="fade" {delay(.82)} x="76" y="378" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{FAINT}">HARGEISA, SOMALILAND</text><text class="fade" {delay(.9)} x="300" y="378" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{BLUE}">zjn281r.tech ↗</text>
<g>{portrait}<circle cx="790" cy="190" r="114" fill="none" stroke="{BLUE}" stroke-opacity=".5"/><text x="650" y="348" font-family="{MONO}" font-size="10" fill="{FAINT}">INDEPENDENT DESIGNER &amp; BUILDER</text><text x="650" y="372" font-family="{SERIF}" font-style="italic" font-size="22" fill="{INK}">Good work should work beautifully.</text></g>'''
    svg("hero.svg", h, body, ("serif", "serif-i", "sans", "mono"), "Nasser Hussain (@zjn281r), designer, media manager, and developer in Somaliland.")


def tiles() -> None:
    h = 210
    pad_x = 40
    items = [
        ("01", "WORK", "Selected systems and products", "#173047", BLUE, "zjn281r.tech/#vault"),
        ("02", "CAPABILITIES", "Growth, creative, digital, spatial", "#12302e", CYAN, "zjn281r.tech/#capabilities"),
        ("03", "CONTACT", "Start a conversation", "#283021", LIME, "mailto:zjn281r@gmail.com"),
    ]
    for i, (number, title, desc, fill, accent, href) in enumerate(items):
        wrapped = wrap(desc, 42)
        desc_y = 104 if len(wrapped) == 1 else 94
        desc_svg = lines(pad_x, desc_y, wrapped, 34, f'font-family="{SERIF}" font-size="30" fill="{INK}"')
        body = (
            f'<rect width="{WIDTH}" height="{h}" rx="16" fill="{fill}" stroke="{accent}" stroke-opacity=".35"/>'
            f'<g class="rise" {delay(1.15 + i * .18)}>'
            f'<text x="{pad_x}" y="44" font-family="{MONO}" font-size="12" letter-spacing="1.4" fill="{accent}">{number} / {title}</text>'
            f'<text x="{WIDTH - pad_x}" y="44" text-anchor="end" font-family="{MONO}" font-size="18" fill="{accent}">↗</text>'
            f'{desc_svg}'
            f'<line x1="{pad_x}" y1="156" x2="{WIDTH - pad_x}" y2="156" stroke="{accent}" stroke-opacity=".3"/>'
            f'<text x="{pad_x}" y="182" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">OPEN LINK</text>'
            f'<text x="{WIDTH - pad_x}" y="182" text-anchor="end" font-family="{MONO}" font-size="11" fill="{accent}">{escape(href)}</text>'
            f'</g>'
        )
        svg(f"tile-{i+1}.svg", h, body, ("serif", "mono"), f"{title}: {desc}")


def activity(data: dict) -> None:
    h, monthly = 350, data["monthly"][-12:]
    maximum = max((item["total"] for item in monthly), default=1)
    bars, x0, base, bw, gap = [], 68, 282, 48, 13
    for i, item in enumerate(monthly):
        bh, x = max(8, item["total"] / maximum * 150), x0 + i * (bw + gap)
        month = dt.date.fromisoformat(item["month"] + "-01").strftime("%b")
        color = BLUE if item["total"] == maximum else PANEL_2
        bars.append(f'<rect class="grow" {delay(2+i*.08)} x="{x}" y="{base-bh:.1f}" width="{bw}" height="{bh:.1f}" rx="5" fill="{color}"><title>{month}: {item["total"]:,}</title></rect><text x="{x+bw/2}" y="{base+22}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{FAINT}">{month}</text>')
    cs, active, busiest = data["current_streak"]["length"], data["active_days"], data["best_day"]["count"]
    body = f'''<rect width="{WIDTH}" height="{h}" rx="16" fill="{PANEL}" stroke="{RULE}"/><text class="fade" {delay(1.85)} x="40" y="48" font-family="{MONO}" font-size="11" letter-spacing="1.1" fill="{MUTED}">CONTRIBUTIONS / LAST 12 MONTHS</text><text class="rise" {delay(1.95)} x="40" y="104" font-family="{SERIF}" font-size="50" fill="{INK}">{data["total_contributions"]:,} <tspan font-style="italic" fill="{BLUE}">contributions</tspan></text>{''.join(bars)}<line x1="650" y1="68" x2="650" y2="296" stroke="{RULE}"/><g class="rise" {delay(2.45)}><text x="690" y="104" font-family="{SERIF}" font-size="36" fill="{BLUE}">{cs}</text><text x="690" y="128" font-family="{MONO}" font-size="11" fill="{MUTED}">DAY STREAK</text><text x="690" y="185" font-family="{SERIF}" font-size="36" fill="{CYAN}">{active}</text><text x="690" y="209" font-family="{MONO}" font-size="11" fill="{MUTED}">ACTIVE DAYS</text><text x="690" y="266" font-family="{SERIF}" font-size="36" fill="{LIME}">{busiest}</text><text x="690" y="290" font-family="{MONO}" font-size="11" fill="{MUTED}">BUSIEST DAY</text></g>'''
    svg("activity.svg", h, body, ("serif", "serif-i", "mono"), f'{data["total_contributions"]:,} contributions, {cs}-day streak, {active} active days, busiest day {busiest}.')


def repos(data: dict) -> None:
    featured = data.get("featured_repos") or [{"name": "zjn281r", "description": "Design systems, profile art, and experiments by Nasser Hussain.", "language": "SVG / Python", "url": "https://github.com/zjn281r/zjn281r"}]
    for i, repo in enumerate(featured):
        name, desc = repo["name"].split("/")[-1], repo.get("description") or "A featured project by zjn281r."
        body = f'''<rect width="{WIDTH}" height="170" rx="16" fill="{PANEL}" stroke="{RULE}"/><g class="rise" {delay(3+i*.18)}><circle cx="42" cy="42" r="5" fill="{BLUE}"/><text x="60" y="48" font-family="{SANS}" font-weight="600" font-size="22" fill="{INK}">{escape(name)}</text><text x="42" y="88" font-family="{SANS}" font-size="15" fill="{MUTED}">{escape(desc[:105])}</text><text x="42" y="132" font-family="{MONO}" font-size="11" fill="{FAINT}">{escape(repo.get("language", "PROJECT"))}</text><text x="900" y="132" text-anchor="end" font-family="{MONO}" font-size="11" fill="{BLUE}">VIEW ON GITHUB ↗</text></g>'''
        svg(f"repo-{name}.svg", 170, body, ("sans", "mono"), f"Featured repository {name}: {desc}")


def heatmap(data: dict) -> None:
    days, first = data["days"], dt.date.fromisoformat(data["days"][0]["date"])
    lead, cell, step, x0, y0 = (first.weekday() + 1) % 7, 12, 15, 44, 92
    levels, cells, months, seen = ["#14212d", "#213a56", "#355e8d", "#4c7fbe", BLUE, "#a6c7ff"], [], [], set()
    for i, day in enumerate(days):
        col, row, date = divmod(i + lead, 7)[0], divmod(i + lead, 7)[1], dt.date.fromisoformat(day["date"])
        if date.day <= 7 and (date.year, date.month) not in seen and row == 0:
            seen.add((date.year, date.month)); months.append((col, date.strftime("%b")))
        level = 0 if day["count"] == 0 else min(5, 1 + day["count"] // 15)
        cells.append(f'<rect class="rise" {delay(3.2+col*.018+row*.01)} x="{x0+col*step}" y="{y0+row*step}" width="{cell}" height="{cell}" rx="3" fill="{levels[level]}"><title>{day["date"]}: {day["count"]} contributions</title></rect>')
    cols = (len(days) + lead + 6) // 7
    labels = "".join(f'<text x="{x0+col*step}" y="204" font-family="{MONO}" font-size="10" fill="{FAINT}">{month}</text>' for col, month in months if col < cols-2)
    body = f'''<rect width="{WIDTH}" height="250" rx="16" fill="{BG}" stroke="{RULE}"/><text class="rise" {delay(3)} x="40" y="48" font-family="{SERIF}" font-size="30" fill="{INK}">Every day, <tspan font-style="italic" fill="{BLUE}">in blue.</tspan></text><text x="920" y="48" text-anchor="end" font-family="{MONO}" font-size="10" fill="{FAINT}">REFRESHED DAILY</text>{''.join(cells)}{labels}<text x="40" y="226" font-family="{MONO}" font-size="10" fill="{FAINT}">zjn281r.tech / github.com/zjn281r</text>'''
    svg("heatmap.svg", 250, body, ("serif", "serif-i", "mono"), "zjn281r contribution graph in the zjn281r.tech brand blue.")


if __name__ == "__main__":
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    hero(); tiles(); activity(payload); repos(payload); heatmap(payload)