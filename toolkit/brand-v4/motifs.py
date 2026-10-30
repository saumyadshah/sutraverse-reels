"""SutraVerse v4 motif library: Mithila-inspired SVG building blocks (original drawings, not copies of any artwork)."""
import math

C = dict(kajal="#100E17", neel="#1A1D47", neel2="#2A2F6B", chandan="#F4EADB", chandan2="#D9CBB4",
         haldi="#F2B33D", sindoor="#D63E2A", palash="#EE7A2E", mor="#137C77", kumkum="#9E2348")


def hatch_band(x, y, w, h, color, gap=14, stroke=3, both=True):
    """Kachni-style band: two outer lines with diagonal hatching between (the Mithila double outline)."""
    out = [f'<g stroke="{color}" stroke-width="{stroke}" fill="none">',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>',
           f'<rect x="{x+h*0}" y="{y}" width="{w}" height="{h}"/>']
    # hatch lines
    clip = f'clip{int(x)}{int(y)}{int(w)}'
    out.append(f'<clipPath id="{clip}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
    out.append(f'<g clip-path="url(#{clip})">')
    i = -h
    while i < w + h:
        out.append(f'<line x1="{x+i}" y1="{y+h}" x2="{x+i+h}" y2="{y}"/>')
        i += gap
    out.append('</g></g>')
    return "\n".join(out)


def mithila_frame(x, y, w, h, color, band=26, gap=13):
    """A full double-outline border with hatched band, plus small dot row inside (Bharni/Kachni mix)."""
    s = [f'<g fill="none" stroke="{color}" stroke-width="3">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>',
         f'<rect x="{x+band}" y="{y+band}" width="{w-2*band}" height="{h-2*band}"/>', '</g>']
    cid = f"mf{int(x)}{int(y)}"
    s.append(f'<clipPath id="{cid}"><path fill-rule="evenodd" d="M{x},{y}h{w}v{h}h{-w}z M{x+band},{y+band}v{h-2*band}h{w-2*band}v{-(h-2*band)}z"/></clipPath>')
    s.append(f'<g clip-path="url(#{cid})" stroke="{color}" stroke-width="2.5">')
    i = -h
    while i < w + h:
        s.append(f'<line x1="{x+i}" y1="{y+h}" x2="{x+i+h}" y2="{y}"/>')
        i += gap
    s.append('</g>')
    # dot row
    d = band + 16
    s.append(f'<g fill="{color}">')
    for k in range(int((w - 2*d) / 22) + 1):
        s.append(f'<circle cx="{x+d+k*22}" cy="{y+d}" r="3.2"/><circle cx="{x+d+k*22}" cy="{y+h-d}" r="3.2"/>')
    for k in range(int((h - 2*d) / 22) + 1):
        s.append(f'<circle cx="{x+d}" cy="{y+d+k*22}" r="3.2"/><circle cx="{x+w-d}" cy="{y+d+k*22}" r="3.2"/>')
    s.append('</g>')
    return "\n".join(s)


def fish(cx, cy, s, body, line, angle=0):
    """Mithila fish: double outline, scales as arcs, big eye."""
    return f'''<g transform="translate({cx},{cy}) rotate({angle}) scale({s})">
<path d="M-120,0 C-60,-70 60,-70 110,0 C60,70 -60,70 -120,0 Z" fill="{body}" stroke="{line}" stroke-width="5"/>
<path d="M-104,0 C-52,-56 52,-56 94,0 C52,56 -52,56 -104,0 Z" fill="none" stroke="{line}" stroke-width="3"/>
<path d="M110,0 L170,-50 L160,0 L170,50 Z" fill="{body}" stroke="{line}" stroke-width="5"/>
{''.join(f'<path d="M{x},-30 q16,30 0,60" fill="none" stroke="{line}" stroke-width="3"/>' for x in range(-40, 80, 22))}
<circle cx="-78" cy="-8" r="16" fill="{C['chandan']}" stroke="{line}" stroke-width="4"/><circle cx="-74" cy="-8" r="7" fill="{line}"/>
</g>'''


def sun(cx, cy, r, color, line):
    rays = "".join(
        f'<path d="M{cx+math.cos(a)*(r+8)},{cy+math.sin(a)*(r+8)} L{cx+math.cos(a+0.12)*(r+46)},{cy+math.sin(a+0.12)*(r+46)} L{cx+math.cos(a+0.24)*(r+8)},{cy+math.sin(a+0.24)*(r+8)}Z" fill="{color}" stroke="{line}" stroke-width="3"/>'
        for a in [i * math.pi / 8 for i in range(16)])
    return f'''{rays}<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" stroke="{line}" stroke-width="5"/>
<circle cx="{cx}" cy="{cy}" r="{r-14}" fill="none" stroke="{line}" stroke-width="3"/>
<path d="M{cx-r*0.45},{cy-r*0.1} q{r*0.2},-{r*0.25} {r*0.4},0" fill="none" stroke="{line}" stroke-width="4"/>
<path d="M{cx+r*0.05},{cy-r*0.1} q{r*0.2},-{r*0.25} {r*0.4},0" fill="none" stroke="{line}" stroke-width="4"/>
<path d="M{cx-r*0.3},{cy+r*0.35} q{r*0.3},{r*0.25} {r*0.6},0" fill="none" stroke="{line}" stroke-width="4"/>'''


def mithila_archer(x, y, s, skin, cloth, line, accent):
    """Original Mithila-style archer in profile (Karna-type warrior): long fish eye, bold double outline, patterned dhoti."""
    return f'''<g transform="translate({x},{y}) scale({s})" stroke-linejoin="round" stroke-linecap="round">
<!-- bow -->
<path d="M260,-420 C420,-200 420,200 260,420" fill="none" stroke="{line}" stroke-width="14"/>
<path d="M260,-420 C410,-200 410,200 260,420" fill="none" stroke="{accent}" stroke-width="6"/>
<line x1="260" y1="-420" x2="260" y2="420" stroke="{line}" stroke-width="3"/>
<!-- body / torso -->
<path d="M-40,-150 C10,-170 80,-160 110,-120 L150,60 C120,110 -20,120 -70,70 Z" fill="{skin}" stroke="{line}" stroke-width="8"/>
<path d="M-30,-130 C10,-148 70,-140 96,-108" fill="none" stroke="{line}" stroke-width="3"/>
<!-- armour collar -->
<path d="M-50,-140 C20,-90 90,-100 120,-130 L125,-100 C80,-60 0,-60 -55,-110 Z" fill="{accent}" stroke="{line}" stroke-width="6"/>
{''.join(f'<circle cx="{-30+i*24}" cy="{-104+abs(i-3)*4}" r="5" fill="{line}"/>' for i in range(7))}
<!-- arm drawing the string -->
<path d="M100,-110 C170,-120 230,-80 262,-60" fill="none" stroke="{line}" stroke-width="40"/>
<path d="M100,-110 C170,-120 230,-80 262,-60" fill="none" stroke="{skin}" stroke-width="28"/>
<!-- head -->
<path d="M-10,-200 C-20,-290 60,-330 120,-300 C160,-280 170,-230 150,-200 C140,-180 150,-170 160,-160 C140,-150 130,-140 110,-140 C60,-130 0,-150 -10,-200 Z" fill="{skin}" stroke="{line}" stroke-width="8"/>
<!-- crown -->
<path d="M-6,-260 C30,-330 110,-345 150,-300 L130,-380 L95,-330 L70,-400 L45,-330 L10,-370 Z" fill="{accent}" stroke="{line}" stroke-width="7"/>
<path d="M0,-270 C40,-310 110,-320 145,-292" fill="none" stroke="{line}" stroke-width="4"/>
<!-- long fish eye (signature Mithila eye) -->
<path d="M70,-232 C92,-252 132,-250 150,-232 C130,-218 94,-214 70,-232 Z" fill="{C['chandan']}" stroke="{line}" stroke-width="5"/>
<circle cx="116" cy="-233" r="9" fill="{line}"/>
<path d="M64,-262 C92,-280 130,-276 152,-258" fill="none" stroke="{line}" stroke-width="5"/>
<!-- earring -->
<circle cx="40" cy="-190" r="16" fill="{accent}" stroke="{line}" stroke-width="5"/>
<!-- dhoti with stripes -->
<path d="M-70,70 C-20,110 120,110 150,60 L200,380 C120,420 -40,420 -110,380 Z" fill="{cloth}" stroke="{line}" stroke-width="8"/>
{''.join(f'<path d="M{-90+i*8},{120+i*40} C{-10},{150+i*40} {120},{140+i*40} {175+i*4},{110+i*40}" fill="none" stroke="{line}" stroke-width="4"/>' for i in range(7))}
{''.join(f'<circle cx="{-40+j*50}" cy="{170+i*80}" r="6" fill="{accent}" stroke="{line}" stroke-width="2"/>' for i in range(3) for j in range(4))}
</g>'''


def modern_woman(x, y, s, skin, top, hair, rim):
    """Modern office character, cinematic flat-shaded with rim light (illustrative composite)."""
    return f'''<g transform="translate({x},{y}) scale({s})">
<defs><linearGradient id="skin{x}" x1="0" x2="1"><stop offset="0" stop-color="{skin}"/><stop offset="1" stop-color="#7a4a35"/></linearGradient></defs>
<!-- shoulders / blazer -->
<path d="M-260,420 C-250,220 -150,150 0,140 C150,150 250,220 260,420 Z" fill="{top}"/>
<path d="M-60,150 L0,300 L60,150" fill="none" stroke="#0b0a12" stroke-width="10" opacity=".6"/>
<path d="M240,420 C232,240 150,170 40,150" fill="none" stroke="{rim}" stroke-width="8" opacity=".85"/>
<!-- lanyard -->
<path d="M-70,150 L-10,330 L50,150" fill="none" stroke="{rim}" stroke-width="7"/>
<rect x="-42" y="320" width="64" height="86" rx="8" fill="{C['chandan']}" stroke="#0b0a12" stroke-width="4"/>
<!-- neck -->
<path d="M-50,40 L-50,150 C-20,175 20,175 50,150 L50,40 Z" fill="url(#skin{x})"/>
<!-- hair back -->
<path d="M-150,-120 C-170,-260 -60,-330 30,-320 C150,-310 190,-200 170,-60 C160,40 150,120 120,160 C60,120 -120,150 -170,120 C-160,40 -150,-40 -150,-120 Z" fill="{hair}"/>
<!-- face -->
<path d="M-110,-130 C-110,-240 -30,-270 30,-262 C110,-252 140,-180 130,-90 C122,-10 80,60 10,70 C-60,70 -110,10 -110,-130 Z" fill="url(#skin{x})"/>
<!-- rim light on face -->
<path d="M118,-170 C138,-110 126,-20 70,40" fill="none" stroke="{rim}" stroke-width="7" opacity=".9"/>
<!-- hair front -->
<path d="M-120,-150 C-100,-270 40,-300 120,-230 C70,-240 0,-220 -40,-170 C-60,-200 -90,-190 -120,-150 Z" fill="{hair}"/>
<!-- eyes looking to the side, worried -->
<path d="M-62,-118 q22,-14 44,0" fill="none" stroke="#1b1010" stroke-width="7" stroke-linecap="round"/>
<path d="M28,-122 q22,-12 44,2" fill="none" stroke="#1b1010" stroke-width="7" stroke-linecap="round"/>
<ellipse cx="-36" cy="-96" rx="11" ry="13" fill="#1b1010"/><ellipse cx="54" cy="-98" rx="11" ry="13" fill="#1b1010"/>
<circle cx="-32" cy="-100" r="3.5" fill="#fff"/><circle cx="58" cy="-102" r="3.5" fill="#fff"/>
<path d="M-70,-140 q30,-22 60,-6" fill="none" stroke="#1b1010" stroke-width="6" stroke-linecap="round"/>
<path d="M24,-150 q30,-14 56,8" fill="none" stroke="#1b1010" stroke-width="6" stroke-linecap="round"/>
<path d="M4,-80 q-10,30 6,40" fill="none" stroke="#6b3b2a" stroke-width="5" stroke-linecap="round"/>
<path d="M-24,8 q30,-12 56,0" fill="none" stroke="#5a2a20" stroke-width="7" stroke-linecap="round"/>
<circle cx="0" cy="-160" r="5" fill="{C['sindoor']}"/>
</g>'''
