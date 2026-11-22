#!/usr/bin/env python3
"""Gera os SVGs animados e o README.md do perfil (tema Córtex Holográfico).
Uso: python generator/build.py   (rodar na raiz do repositório)"""
import json, math, random, os, textwrap, unicodedata
from xml.sax.saxutils import escape as esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(os.path.join(ROOT, "generator", "config.json"), encoding="utf-8"))
A = os.path.join(ROOT, "assets"); os.makedirs(os.path.join(A, "projects"), exist_ok=True)

CYAN, PINK, BG, PANEL, LINE = "#5ef2ff", "#ff5ec8", "#04060c", "#061120", "#12324a"
MONO = "'JetBrains Mono', Consolas, 'Cascadia Mono', 'Courier New', monospace"
SANS = "'Space Grotesk', 'Segoe UI', Inter, Helvetica, Arial, sans-serif"

def write(path, s):
    open(os.path.join(A, path), "w", encoding="utf-8").write(s)

def corners(W, H, size=22, m=8):
    out = []
    for x, y, dx, dy in [(m, m, 1, 1), (W-m, m, -1, 1), (m, H-m, 1, -1), (W-m, H-m, -1, -1)]:
        out.append(f'<path d="M{x} {y+size*dy} L{x} {y} L{x+size*dx} {y}" fill="none" stroke="{CYAN}" stroke-width="2"/>')
    return "".join(out)

# ---------------- header: cérebro holográfico ----------------
def in_brain(x, y):
    if (x/1.0)**2 + ((y+0.05)/0.68)**2 <= 1 and y < 0.42: return True
    return ((x-0.55)/0.32)**2 + ((y-0.42)/0.18)**2 <= 1

def header():
    random.seed(7)
    W, H, cx, cy, sc = 836, 520, 418, 250, 230
    pts, tries = [], 0
    while len(pts) < 120 and tries < 20000:
        tries += 1
        x, y = random.uniform(-1, 1), random.uniform(-0.8, 0.62)
        if in_brain(x, y) and all((x-a)**2+(y-b)**2 > 0.105**2 for a, b in pts):
            pts.append((x, y))
    P = [(cx+x*sc, cy+y*sc) for x, y in pts]
    E = set()
    for i, (x, y) in enumerate(pts):
        for _, j in sorted(((x-a)**2+(y-b)**2, j) for j, (a, b) in enumerate(pts) if j != i)[:3]:
            E.add(tuple(sorted((i, j))))
    E = sorted(E)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Cérebro neural holográfico emitindo pensamentos">',
         f'''<style>
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@keyframes flow{{to{{stroke-dashoffset:-40}}}}
@keyframes scan{{0%{{transform:translateY(-40px)}}100%{{transform:translateY({H+40}px)}}}}
@keyframes flick{{0%,92%,94%,100%{{opacity:1}}93%{{opacity:.4}}97%{{opacity:.6}}}}
@keyframes rise{{0%{{opacity:0}}20%,80%{{opacity:1}}100%{{opacity:0}}}}
.p0{{animation:pulse 2.6s ease-in-out infinite}}.p1{{animation:pulse 2.6s ease-in-out .9s infinite}}.p2{{animation:pulse 2.6s ease-in-out 1.7s infinite}}
.syn{{stroke-dasharray:2 10;animation:flow 1.6s linear infinite}}
.scan{{animation:scan 5s linear infinite}}.holo{{animation:flick 6s linear infinite}}
''' + "".join(f".t{k}{{animation:rise 6s ease-in-out {k}s infinite;opacity:0}}" for k in range(6)) + '</style>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         '<g stroke="#0e1a2a" stroke-width="1">']
    s += [f'<line x1="{gx}" y1="0" x2="{gx}" y2="{H}"/>' for gx in range(0, W, 38)]
    s += [f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}"/>' for gy in range(0, H, 38)]
    s.append('</g>')
    s.append(f'<ellipse cx="{cx}" cy="{H-28}" rx="150" ry="16" fill="none" stroke="{CYAN}" stroke-opacity=".5"/>')
    s.append(f'<ellipse cx="{cx}" cy="{H-28}" rx="100" ry="10" fill="none" stroke="{CYAN}" stroke-opacity=".8"/>')
    s.append(f'<path d="M{cx-100} {H-28} L{cx-230} {cy-40} M{cx+100} {H-28} L{cx+230} {cy-40}" stroke="{CYAN}" stroke-opacity=".12"/>')
    s.append(f'<g class="holo"><g stroke="{CYAN}" stroke-opacity=".28">')
    s += [f'<line x1="{P[i][0]:.1f}" y1="{P[i][1]:.1f}" x2="{P[j][0]:.1f}" y2="{P[j][1]:.1f}"/>' for i, j in E]
    s.append(f'</g><g stroke="{PINK}" stroke-width="1.6">')
    s += [f'<line class="syn" x1="{P[i][0]:.1f}" y1="{P[i][1]:.1f}" x2="{P[j][0]:.1f}" y2="{P[j][1]:.1f}"/>' for n, (i, j) in enumerate(E) if n % 5 == 0]
    s.append('</g>')
    for n, (x, y) in enumerate(P):
        s.append(f'<circle class="p{n%3}" cx="{x:.1f}" cy="{y:.1f}" r="{3.6 if n%4==0 else 2.2}" fill="{PINK if n%17==0 else CYAN}"/>')
    s.append('</g>')
    anchors = [(-0.7, -0.35), (-0.2, -0.6), (0.45, -0.5), (0.85, -0.05), (-0.85, 0.15), (0.55, 0.42)]
    labels = [(40, 70), (250, 26), (560, 40), (650, 200), (30, 300), (640, 420)]
    for k, ((ax, ay), (lx, ly), t) in enumerate(zip(anchors, labels, CFG["thoughts"][:6])):
        b = min(P, key=lambda p: (p[0]-(cx+ax*sc))**2 + (p[1]-(cy+ay*sc))**2)
        tw = len(t)*7.4 + 24
        ex = lx+tw if lx < cx else lx
        s.append(f'<g class="t{k}"><line x1="{b[0]:.1f}" y1="{b[1]:.1f}" x2="{ex:.0f}" y2="{ly+13}" stroke="{CYAN}" stroke-opacity=".6" stroke-dasharray="3 3"/>'
                 f'<rect x="{lx}" y="{ly}" width="{tw:.0f}" height="26" rx="2" fill="#071423" stroke="{CYAN}" stroke-opacity=".7"/>'
                 f'<text x="{lx+12}" y="{ly+17}" font-family="{MONO}" font-size="12" fill="#b6f9ff">{esc(t)}</text></g>')
    s.append(f'<rect class="scan" width="{W}" height="2" fill="{CYAN}" fill-opacity=".35"/>')
    s.append(corners(W, H))
    s.append(f'<text x="22" y="{H-18}" font-family="{MONO}" font-size="11" fill="#4f6b86">NEURAL_LINK · ATIVO</text>')
    s.append(f'<text x="{W-22}" y="{H-18}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#4f6b86">BR · UTC−3</text>')
    s.append('</svg>')
    write("cortex-header.svg", "\n".join(s))

# ---------------- identidade ----------------
def identity():
    W, H = 836, 190
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(CFG['name'])} — {esc(CFG['tagline'])}">
<style>@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}.c{{animation:blink 1s steps(1) infinite}}</style>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="0" y="24" font-family="{MONO}" font-size="13" letter-spacing="2.6" fill="{CYAN}">// IDENTIDADE</text>
<text x="0" y="96" font-family="{SANS}" font-size="64" font-weight="700" fill="#eaf6ff">{esc(CFG['name'])}</text>
<rect class="c" x="{len(CFG['name'])*36+12}" y="52" width="14" height="46" fill="{PINK}"/>
<text x="0" y="138" font-family="{SANS}" font-size="20" fill="#9fb3c8">{esc(CFG['tagline'])}</text>
<text x="0" y="168" font-family="{SANS}" font-size="20" fill="#9fb3c8">{esc(CFG['tagline2'])}</text>
</svg>'''
    write("identity.svg", s)

def section(slug, title):
    W, H = 836, 44
    write(f"section-{slug}.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">
<style>@keyframes sweep{{from{{transform:translateX(-120px)}}to{{transform:translateX({W}px)}}}}.s{{animation:sweep 4s linear infinite}}</style>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="0" y="26" font-family="{MONO}" font-size="13" letter-spacing="2.6" fill="{CYAN}">// {esc(title.upper())}</text>
<line x1="0" y1="40" x2="{W}" y2="40" stroke="{LINE}"/>
<rect class="s" x="0" y="39" width="120" height="2" fill="{CYAN}" fill-opacity=".7"/>
</svg>''')

# ---------------- cards de projeto ----------------
def card(i, p):
    W, H = 410, 176
    lines = textwrap.wrap(p["desc"], 44)[:3]
    desc = "".join(f'<text x="22" y="{98+k*20}" font-family="{SANS}" font-size="14" fill="#9fb3c8">{esc(l)}</text>' for k, l in enumerate(lines))
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p['name'])}: {esc(p['desc'])}">
<style>@keyframes pulse{{0%,100%{{opacity:.3}}50%{{opacity:1}}}}.d{{animation:pulse 2s ease-in-out {i*0.3:.1f}s infinite}}
@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY({H}px)}}}}.sc{{animation:scan 3.5s linear {i*0.5:.1f}s infinite}}</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{PANEL}" stroke="{LINE}"/>
<rect class="sc" x="1" y="0" width="{W-2}" height="1.5" fill="{CYAN}" fill-opacity=".25"/>
<path d="M1 15 L1 1 L15 1" fill="none" stroke="{CYAN}" stroke-width="2"/><path d="M{W-1} {H-15} L{W-1} {H-1} L{W-15} {H-1}" fill="none" stroke="{CYAN}" stroke-width="2"/>
<circle class="d" cx="26" cy="28" r="4" fill="{PINK}"/>
<text x="38" y="32" font-family="{MONO}" font-size="11" fill="#4f6b86">NODE_{i+1:02d}</text>
<text x="{W-22}" y="32" text-anchor="end" font-family="{MONO}" font-size="11" fill="#ff8fd6">{esc(p.get('status',''))}</text>
<text x="22" y="66" font-family="{SANS}" font-size="21" font-weight="700" fill="#eaf6ff">{esc(p['name'])}</text>
{desc}
<text x="22" y="{H-20}" font-family="{MONO}" font-size="11" fill="{CYAN}">{esc(p['stack'])}</text>
</svg>'''
    n = unicodedata.normalize("NFKD", p["name"].lower()).encode("ascii", "ignore").decode()
    slug = "".join(ch if ch.isalnum() else "-" for ch in n).strip("-")
    write(f"projects/{slug}.svg", s)
    return slug

# ---------------- stack ----------------
def stack():
    W, gap, x, y, rows = 836, 8, 0, 0, []
    chips = []
    for t in CFG["stack"]:
        w = len(t)*7.8 + 26
        if x + w > W: x, y = 0, y + 42
        chips.append((x, y, w, t)); x += w + gap
    H = y + 36
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Stack: {esc(", ".join(CFG["stack"]))}">',
         '<style>@keyframes glow{0%,100%{stroke-opacity:.45}50%{stroke-opacity:1}}' + "".join(f".g{k}{{animation:glow 3s ease-in-out {k*0.25:.2f}s infinite}}" for k in range(len(chips))) + '</style>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    for k, (x, y, w, t) in enumerate(chips):
        s.append(f'<rect class="g{k}" x="{x+0.5:.1f}" y="{y+0.5}" width="{w:.1f}" height="34" fill="{PANEL}" stroke="#1d4d6b"/>'
                 f'<text x="{x+13:.1f}" y="{y+22}" font-family="{MONO}" font-size="13" fill="#b6f9ff">{esc(t)}</text>')
    s.append('</svg>')
    write("stack.svg", "\n".join(s))

def footer():
    W, H = 836, 40
    write("footer.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Sinal transmitido do Brasil">
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="{W/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#4f6b86">sinal transmitido do Brasil · fim da transmissão</text></svg>''')

# ---------------- README ----------------
def readme(slugs):
    u = CFG["username"]
    theme = "bg_color=04060c&title_color=5ef2ff&text_color=9fb3c8&icon_color=ff5ec8&hide_border=true"
    cards = []
    for k in range(0, len(slugs), 2):
        row = []
        for p, slug in slugs[k:k+2]:
            href = f"https://github.com/{u}/{p['repo']}" if p.get("repo") else "#"
            row.append(f'<a href="{href}"><img src="assets/projects/{slug}.svg" width="49%" alt="{esc(p["name"])}"/></a>')
        cards.append("\n".join(row))
    badges = "\n".join(
        f'<a href="{esc(l["url"])}"><img src="https://img.shields.io/badge/{l["label"].replace("-", "--").replace(" ", "_")}-061120?style=for-the-badge'
        + (f'&logo={l["logo"]}&logoColor=5ef2ff' if l.get("logo") else "")
        + f'" alt="{esc(l["label"])}"/></a>'
        for l in CFG["links"])
    md = f'''<!-- Gerado por generator/build.py — edite generator/config.json e rode o script de novo -->
<div align="center">

<img src="assets/cortex-header.svg" width="100%" alt="Cérebro neural holográfico"/>

<img src="assets/identity.svg" width="100%" alt="{esc(CFG['name'])} — {esc(CFG['tagline'])}"/>

<img src="assets/section-projetos.svg" width="100%" alt="Projetos ativos"/>

{(chr(10)*2).join(cards)}

<img src="assets/section-stack.svg" width="100%" alt="Sinapses técnicas"/>

<img src="assets/stack.svg" width="100%" alt="Stack"/>

<img src="assets/section-atividade.svg" width="100%" alt="Atividade neural"/>

<img src="https://github-readme-stats.vercel.app/api?username={u}&show_icons=true&{theme}" width="49%" alt="GitHub stats"/>
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username={u}&layout=compact&{theme}" width="49%" alt="Linguagens"/>

<picture>
  <img src="https://raw.githubusercontent.com/{u}/{u}/output/neural-activity.svg" width="100%" alt="Contribuições como atividade neural"/>
</picture>

{badges}

<img src="assets/footer.svg" width="100%" alt=""/>

</div>
'''
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(md)

if __name__ == "__main__":
    header(); identity(); stack(); footer()
    section("projetos", "Projetos ativos"); section("stack", "Sinapses técnicas"); section("atividade", "Atividade neural")
    live = [p for p in CFG["projects"] if not p.get("draft")]
    for p in CFG["projects"]:
        if p.get("draft"): print(f"[pulado] {p['name']} está como draft — preencha desc/stack e remova \"draft\" no config.json")
    slugs = [(p, card(i, p)) for i, p in enumerate(live)]
    readme(slugs)
    if CFG["username"] == "SEU-USUARIO": print("[atenção] troque \"username\" no config.json")
    print("ok: README.md e assets/ gerados")
