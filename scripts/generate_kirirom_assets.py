#!/usr/bin/env python3
"""Generate premium SVG product renderings and a nature poster for KIRIROM Water."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_DIR = ROOT / "assets" / "products"
POSTER_DIR = ROOT / "assets" / "posters"
PRODUCT_DIR.mkdir(parents=True, exist_ok=True)
POSTER_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#0f77bd"
DEEP = "#082f4f"
MIST = "#dff4f7"
FOREST = "#0f5138"
GOLD = "#d7b76a"


def write(path: Path, body: str) -> None:
    path.write_text(body.strip() + "\n", encoding="utf-8")


def gradients() -> str:
    return f"""
    <defs>
      <linearGradient id="waterGlass" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0" stop-color="#f9ffff" stop-opacity=".90"/>
        <stop offset=".36" stop-color="#b8eff8" stop-opacity=".40"/>
        <stop offset=".72" stop-color="#ffffff" stop-opacity=".62"/>
        <stop offset="1" stop-color="#6ec0d6" stop-opacity=".34"/>
      </linearGradient>
      <linearGradient id="waterBlue" x1="0" x2="0" y1="0" y2="1">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".50"/>
        <stop offset=".45" stop-color="#b8e9f2" stop-opacity=".36"/>
        <stop offset="1" stop-color="#61b9d5" stop-opacity=".50"/>
      </linearGradient>
      <linearGradient id="capBlue" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0" stop-color="#56b6e8"/>
        <stop offset=".48" stop-color="{BLUE}"/>
        <stop offset="1" stop-color="#064a8c"/>
      </linearGradient>
      <radialGradient id="shine" cx="30%" cy="18%" r="70%">
        <stop offset="0" stop-color="#ffffff" stop-opacity=".96"/>
        <stop offset=".35" stop-color="#ffffff" stop-opacity=".20"/>
        <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
      </radialGradient>
      <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
        <feDropShadow dx="0" dy="22" stdDeviation="18" flood-color="#07324f" flood-opacity=".24"/>
      </filter>
      <filter id="mistBlur"><feGaussianBlur stdDeviation="18"/></filter>
      <pattern id="capRidges" width="8" height="8" patternUnits="userSpaceOnUse">
        <path d="M1 0v8" stroke="#e4f7ff" stroke-width="1.2" opacity=".65"/>
      </pattern>
    </defs>"""


def mountain_mark(x, y, scale=1):
    return f"""
    <g transform="translate({x} {y}) scale({scale})">
      <path d="M0 46 C25 20 52 2 88 0 C114 1 134 12 158 35 C128 27 111 28 82 42 C55 55 29 57 0 46Z" fill="{BLUE}"/>
      <path d="M13 39 C37 28 56 14 80 10 C102 7 120 16 142 30" fill="none" stroke="#eaf8ff" stroke-width="5" stroke-linecap="round"/>
      <path d="M96 7 L108 34 L130 19 L114 45" fill="none" stroke="#eaf8ff" stroke-width="3" stroke-linecap="round"/>
      <circle cx="42" cy="19" r="2" fill="#eaf8ff"/><circle cx="57" cy="14" r="1.7" fill="#eaf8ff"/><circle cx="72" cy="11" r="1.4" fill="#eaf8ff"/>
    </g>"""


def label_art(x, y, w, h, theme):
    bg = "#172039" if theme == "dark" else "#d990aa" if theme == "pink" else "#eaf9ff"
    fg = "#ffffff" if theme in {"dark", "pink"} else BLUE
    return f"""
    <g transform="translate({x} {y})">
      <rect width="{w}" height="{h}" rx="{w*.11:.1f}" fill="{bg}" opacity=".97"/>
      <path d="M0 {h*.50:.1f} C{w*.18:.1f} {h*.30:.1f},{w*.34:.1f} {h*.70:.1f},{w*.52:.1f} {h*.46:.1f} C{w*.71:.1f} {h*.22:.1f},{w*.84:.1f} {h*.37:.1f},{w} {h*.25:.1f} L{w} {h} L0 {h} Z" fill="#50a878" opacity=".72"/>
      <path d="M0 {h*.60:.1f} C{w*.20:.1f} {h*.45:.1f},{w*.35:.1f} {h*.72:.1f},{w*.56:.1f} {h*.58:.1f} C{w*.78:.1f} {h*.43:.1f},{w*.91:.1f} {h*.53:.1f},{w} {h*.45:.1f}" fill="none" stroke="#f2c76a" stroke-width="{max(2,w*.035):.1f}" opacity=".85"/>
      <path d="M{w*.10:.1f} {h*.82:.1f} C{w*.28:.1f} {h*.68:.1f},{w*.38:.1f} {h*.86:.1f},{w*.54:.1f} {h*.73:.1f}" fill="none" stroke="#80d7f2" stroke-width="{max(2,w*.03):.1f}" opacity=".82"/>
      <ellipse cx="{w*.65:.1f}" cy="{h*.59:.1f}" rx="{w*.12:.1f}" ry="{h*.24:.1f}" fill="#f7fbff" transform="rotate(-18 {w*.65:.1f} {h*.59:.1f})"/>
      <path d="M{w*.68:.1f} {h*.43:.1f} C{w*.83:.1f} {h*.39:.1f},{w*.89:.1f} {h*.48:.1f},{w*.79:.1f} {h*.56:.1f}" fill="none" stroke="#182533" stroke-width="{max(2,w*.035):.1f}" stroke-linecap="round"/>
      <text x="{w*.50:.1f}" y="{h*.20:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="{w*.155:.1f}" fill="{fg}" letter-spacing="1">KIRIROM</text>
      <text x="{w*.50:.1f}" y="{h*.32:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="{w*.062:.1f}" fill="{fg}" opacity=".88">NATURAL MINERAL WATER</text>
    </g>"""


def bottle_svg(name, volume, kind, label_theme="dark", width=760, height=1000):
    # kind: small, slim, jug5, jug15
    if kind == "slim":
        body = '<path d="M330 150 C305 190 292 255 292 365 L292 790 C292 865 340 904 380 904 C420 904 468 865 468 790 L468 365 C468 255 455 190 430 150 Z"/>'
        neck = '<rect x="345" y="94" width="70" height="82" rx="18"/><rect x="334" y="76" width="92" height="34" rx="11"/>'
        cap = '<rect x="331" y="50" width="98" height="42" rx="10" fill="url(#capBlue)"/><rect x="331" y="50" width="98" height="42" rx="10" fill="url(#capRidges)" opacity=".45"/>'
        lab = label_art(302, 414, 156, 246, "light")
        waves = '<path d="M300 320 C330 300 360 340 392 317 C420 298 445 320 462 306"/><path d="M300 696 C330 676 360 716 392 693 C420 674 445 696 462 682"/>'
    elif kind == "jug5":
        body = '<path d="M238 210 C220 252 205 310 204 390 L204 790 C204 862 254 904 380 904 C506 904 556 862 556 790 L556 390 C555 310 540 252 522 210 C490 180 270 180 238 210 Z"/>'
        neck = '<rect x="326" y="106" width="108" height="102" rx="28"/><rect x="306" y="82" width="148" height="45" rx="16"/>'
        cap = '<rect x="296" y="45" width="168" height="58" rx="13" fill="url(#capBlue)"/><rect x="296" y="45" width="168" height="58" rx="13" fill="url(#capRidges)" opacity=".45"/><path d="M460 54 C543 76 593 113 610 148 C573 151 515 133 456 103" fill="none" stroke="#58a9e9" stroke-width="18" stroke-linecap="round"/><path d="M474 65 C530 83 559 105 574 124" fill="none" stroke="#e8f7ff" stroke-width="5" opacity=".75"/>'
        lab = label_art(292, 452, 176, 218, "pink")
        waves = ''.join(f'<path d="M222 {y} C280 {y-42} 334 {y+40} 398 {y-5} C460 {y-48} 510 {y+22} 540 {y-14}"/>' for y in [342,462,586,720])
    elif kind == "jug15":
        body = '<path d="M158 185 C120 262 98 354 98 508 L98 786 C98 882 174 940 380 940 C586 940 662 882 662 786 L662 508 C662 354 640 262 602 185 C528 126 232 126 158 185 Z"/>'
        neck = '<rect x="303" y="82" width="154" height="120" rx="36"/><rect x="278" y="52" width="204" height="52" rx="18"/>'
        cap = '<rect x="270" y="17" width="220" height="62" rx="14" fill="url(#capBlue)"/><rect x="270" y="17" width="220" height="62" rx="14" fill="url(#capRidges)" opacity=".45"/><path d="M490 27 C585 50 644 91 668 132 C625 138 561 119 489 78" fill="none" stroke="#58a9e9" stroke-width="22" stroke-linecap="round"/><path d="M508 38 C570 59 605 83 625 108" fill="none" stroke="#e8f7ff" stroke-width="6" opacity=".75"/>'
        lab = label_art(272, 392, 208, 272, "dark")
        waves = ''.join(f'<path d="M128 {y} C222 {y-70} 296 {y+62} 392 {y-12} C488 {y-82} 588 {y+55} 640 {y-8}"/>' for y in [306,450,596,744])
    else:
        body = '<path d="M286 220 C262 275 254 350 256 448 L262 792 C264 870 316 905 380 905 C444 905 496 870 498 792 L504 448 C506 350 498 275 474 220 C430 195 330 195 286 220 Z"/>'
        neck = '<rect x="340" y="122" width="80" height="106" rx="22"/><rect x="326" y="98" width="108" height="38" rx="12"/>'
        cap = '<rect x="320" y="64" width="120" height="46" rx="10" fill="url(#capBlue)"/><rect x="320" y="64" width="120" height="46" rx="10" fill="url(#capRidges)" opacity=".45"/>'
        lab = label_art(310, 474, 140, 226, label_theme)
        waves = ''.join(f'<path d="M272 {y} C318 {y-34} 354 {y+30} 404 {y-6} C450 {y-38} 480 {y+16} 492 {y-8}"/>' for y in [350,477,612,744])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 760 1000" role="img" aria-label="KIRIROM {volume} bottle rendering">
  {gradients()}
  <rect width="760" height="1000" fill="none"/>
  <ellipse cx="380" cy="935" rx="250" ry="42" fill="#07324f" opacity=".16"/>
  <g filter="url(#softShadow)">
    <g fill="url(#waterGlass)" stroke="#c7f4ff" stroke-width="4" opacity=".94">{body}{neck}</g>
    <g opacity=".65" fill="none" stroke="#ffffff" stroke-width="10" stroke-linecap="round">{waves}</g>
    <g opacity=".38" fill="url(#waterBlue)">{body}</g>
    <path d="M240 250 C205 335 203 485 210 720" fill="none" stroke="#ffffff" stroke-width="23" opacity=".46" stroke-linecap="round"/>
    <path d="M488 240 C538 360 546 520 528 760" fill="none" stroke="#7dc4da" stroke-width="9" opacity=".26" stroke-linecap="round"/>
    <ellipse cx="310" cy="300" rx="70" ry="145" fill="url(#shine)" opacity=".75"/>
    {cap}
    {lab}
  </g>
  <text x="380" y="986" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="42" fill="{DEEP}">{volume}</text>
</svg>"""


def poster_svg():
    # poster intentionally leaves detailed multilingual copy to HTML overlays for precise, selectable text.
    products = "".join([
        '<image href="../products/kirirom-15l.svg" x="50" y="330" width="420" height="552"/>',
        '<image href="../products/kirirom-330ml.svg" x="430" y="585" width="190" height="250"/>',
        '<image href="../products/kirirom-500ml.svg" x="575" y="530" width="220" height="290"/>',
        '<image href="../products/kirirom-1l.svg" x="760" y="438" width="260" height="342"/>',
        '<image href="../products/kirirom-5l.svg" x="960" y="420" width="340" height="446"/>',
    ])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="960" viewBox="0 0 1600 960" role="img" aria-label="KIRIROM Cambodian mountain spring water poster">
  <defs>
    <linearGradient id="sky" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#dff6ff"/><stop offset=".40" stop-color="#b7e5f2"/><stop offset="1" stop-color="#f8fcfb"/></linearGradient>
    <linearGradient id="forestGrad" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2c7652"/><stop offset="1" stop-color="#0b352b"/></linearGradient>
    <radialGradient id="sun" cx="74%" cy="16%" r="42%"><stop offset="0" stop-color="#fff7c8" stop-opacity=".95"/><stop offset=".36" stop-color="#fff2b0" stop-opacity=".35"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="22"/></filter>
    <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="8"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 .055"/></feComponentTransfer></filter>
  </defs>
  <rect width="1600" height="960" fill="url(#sky)"/>
  <rect width="1600" height="960" fill="url(#sun)"/>
  <path d="M0 498 C190 320 302 310 455 456 C610 247 820 210 1048 468 C1235 336 1420 340 1600 500 L1600 960 L0 960 Z" fill="#8fc4b1" opacity=".84"/>
  <path d="M0 545 C210 392 360 428 505 560 C720 315 916 372 1106 556 C1278 448 1432 456 1600 558 L1600 960 L0 960 Z" fill="url(#forestGrad)" opacity=".92"/>
  <g opacity=".30" fill="#ffffff" filter="url(#blur)">
    <ellipse cx="382" cy="398" rx="300" ry="70"/><ellipse cx="935" cy="452" rx="370" ry="86"/><ellipse cx="1270" cy="388" rx="280" ry="65"/>
  </g>
  <g opacity=".30" stroke="#ffffff" stroke-width="3" stroke-linecap="round">
    <path d="M220 50 L190 230"/><path d="M350 30 L320 210"/><path d="M1160 28 L1120 220"/><path d="M1288 70 L1240 265"/><path d="M1430 40 L1398 220"/>
  </g>
  <path d="M0 804 C260 732 440 806 710 742 C966 680 1180 704 1600 620 L1600 960 L0 960 Z" fill="#eefbf9" opacity=".88"/>
  <g transform="translate(92 86)">{mountain_mark(0,0,1.18)}<text x="204" y="49" font-family="Arial, sans-serif" font-size="54" font-weight="900" fill="{DEEP}" letter-spacing="3">KIRIROM</text><text x="205" y="88" font-family="Arial, sans-serif" font-size="24" fill="{DEEP}" letter-spacing="2">NATURAL MINERAL WATER</text></g>
  <text x="92" y="250" font-family="Georgia, 'Times New Roman', serif" font-size="72" font-weight="700" fill="{DEEP}">Mountain spring purity</text>
  <text x="96" y="304" font-family="Arial, sans-serif" font-size="27" fill="#24586b" letter-spacing="1.5">Morning mist • forest stone • Cambodian highland rain</text>
  <path d="M96 342 L458 342" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>
  {products}
  <rect width="1600" height="960" fill="#fff" filter="url(#grain)" opacity=".25"/>
</svg>"""


def family_svg():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-label="Five KIRIROM water sizes product family rendering">
  <defs><linearGradient id="bg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#f8fdff"/><stop offset="1" stop-color="#edf8f6"/></linearGradient></defs>
  <rect width="1600" height="1000" fill="url(#bg)"/>
  <ellipse cx="770" cy="885" rx="610" ry="72" fill="#0b3550" opacity=".10"/>
  <image href="kirirom-15l.svg" x="80" y="75" width="475" height="625"/>
  <image href="kirirom-330ml.svg" x="490" y="470" width="215" height="283"/>
  <image href="kirirom-500ml.svg" x="662" y="392" width="250" height="329"/>
  <image href="kirirom-1l.svg" x="882" y="272" width="300" height="395"/>
  <image href="kirirom-5l.svg" x="1110" y="232" width="390" height="513"/>
  <text x="800" y="858" text-anchor="middle" font-family="Arial, sans-serif" font-size="46" font-weight="800" fill="{DEEP}" letter-spacing="2">15L · 330ml · 500ml · 1L · 5L</text>
</svg>"""

products = [
    ("kirirom-330ml.svg", "330ml", "small", "dark"),
    ("kirirom-500ml.svg", "500ml", "small", "dark"),
    ("kirirom-1l.svg", "1L", "slim", "light"),
    ("kirirom-5l.svg", "5L", "jug5", "pink"),
    ("kirirom-15l.svg", "15L", "jug15", "dark"),
]
for filename, volume, kind, theme in products:
    write(PRODUCT_DIR / filename, bottle_svg(filename, volume, kind, theme))
write(POSTER_DIR / "kirirom-nature-hero.svg", poster_svg())
write(PRODUCT_DIR / "kirirom-family.svg", family_svg())
print("Generated KIRIROM SVG assets")
