#!/usr/bin/env python3
"""
QuniPa logo – build script.
Rebuilds every deliverable (SVG, PDF, EPS, PNG, CMYK print files, favicons) from qgeom.py.
Run:  python3 build_logo.py            (writes to ./deliverables)
"""
import os, math, json, shutil
import cairosvg
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen
from reportlab.pdfgen import canvas as rl_canvas
from qgeom import *

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'deliverables')
FONT_MED = os.path.join(HERE, 'fonts', 'IBMPlexSans-Medium.ttf')

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------
BRAND = {
    'blue':   dict(name='QuniPa Blue',   hex='#0A5CB8', cmyk=(95, 60, 0, 0)),
    'orange': dict(name='QuniPa Orange', hex='#D95A0B', cmyk=(0, 75, 100, 10)),
    'ink':    dict(name='QuniPa Ink',    hex='#232A33', cmyk=(50, 35, 25, 90)),
    'blue_d':   dict(name='Blue (on dark)',   hex='#4DA3FF'),
    'orange_d': dict(name='Orange (on dark)', hex='#FF8A3D'),
    'paper_d':  dict(name='Paper (on dark)',  hex='#F3F5F8'),
    'night':    dict(name='Night (dark background)', hex='#0F1720'),
}

# variant -> role colours (hex) ; CMYK overrides for print
VARIANTS = {
    'color':          dict(blue='#0A5CB8', orange='#D95A0B', ink='#232A33', bg='#FFFFFF',
                           cmyk=dict(blue=(95, 60, 0, 0), orange=(0, 75, 100, 10), ink=(50, 35, 25, 90))),
    'color-on-dark':  dict(blue='#4DA3FF', orange='#FF8A3D', ink='#F3F5F8', bg='#0F1720', cmyk=None),
    'gray':           dict(blue='#4E4E4E', orange='#777777', ink='#292929', bg='#FFFFFF',
                           cmyk=dict(blue=(0, 0, 0, 85), orange=(0, 0, 0, 65), ink=(0, 0, 0, 95))),
    'gray-on-dark':   dict(blue='#8E8E8E', orange='#C9C9C9', ink='#F2F2F2', bg='#0F1720', cmyk=None),
    'black':          dict(blue='#000000', orange='#000000', ink='#000000', bg='#FFFFFF',
                           cmyk=dict(blue=(0, 0, 0, 100), orange=(0, 0, 0, 100), ink=(0, 0, 0, 100))),
    'white':          dict(blue='#FFFFFF', orange='#FFFFFF', ink='#FFFFFF', bg='#0F1720', cmyk=None),
}

# --------------------------------------------------------------------------
# Typeface outlines (secondary typeface, descriptor only)
# --------------------------------------------------------------------------
class OutlinePen(BasePen):
    def __init__(self, gs, scale, dx, dy):
        super().__init__(gs); self.p = Path(); self.s = scale; self.dx = dx; self.dy = dy
    def _t(self, pt): return (pt[0] * self.s + self.dx, -pt[1] * self.s + self.dy)
    def _moveTo(self, pt): self.p.M(*self._t(pt))
    def _lineTo(self, pt): self.p.L(*self._t(pt))
    def _curveToOne(self, a, b, c): self.p.C(*self._t(a), *self._t(b), *self._t(c))
    def _closePath(self): self.p.Z()


def text_path(text, font_path, cap_height_units, width_units=None, tracking_em=0.16, x0=0.0, baseline=0.0):
    f = TTFont(font_path); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm
    cap = f['OS/2'].sCapHeight
    size = cap_height_units / (cap / upm)       # font size in units
    k = size / upm
    names = [cmap[ord(c)] for c in text]
    adv = [f['hmtx'][n][0] * k for n in names]
    if width_units is not None:
        nat = sum(adv) - 0  # advance sum
        tr = (width_units - nat) / (len(text) - 1)
        # sidebearing compensation so the ink (not the advance box) spans exactly width_units
        lsb0 = f['hmtx'][names[0]][1] * k
        gl = f['glyf'][names[-1]]
        rsb_last = (f['hmtx'][names[-1]][0] - (gl.xMax)) * k
        tr = (width_units - nat + lsb0 + rsb_last) / (len(text) - 1)
        x = x0 - lsb0
    else:
        tr = tracking_em * size; x = x0
    out = Path()
    for n, a in zip(names, adv):
        pen = OutlinePen(gs, k, x, baseline)
        gs[n].draw(pen)
        out.extend(pen.p)
        x += a + tr
    return out, tr / size


# --------------------------------------------------------------------------
# Wordmark with Audiowide letters (u n i a) + custom-drawn q and P
# --------------------------------------------------------------------------
FONT_AW = os.path.join(HERE, 'fonts', 'Audiowide-Regular.ttf')
AW_XH = 42.0     # x-height of the Audiowide letters, in wordmark units
_AW = {}

def aw_glyph(ch, xh=None):
    xh = xh or AW_XH
    if 'f' not in _AW:
        f = TTFont(FONT_AW); _AW.update(f=f, gs=f.getGlyphSet(), cm=f.getBestCmap())
    f, gs, cm = _AW['f'], _AW['gs'], _AW['cm']
    from fontTools.pens.boundsPen import BoundsPen
    name = cm[ord(ch)]; bp = BoundsPen(gs); gs[name].draw(bp)
    k = xh / 1081.0
    pen = OutlinePen(gs, k, -bp.bounds[0] * k, 0.0); gs[name].draw(pen)
    w = (bp.bounds[2] - bp.bounds[0]) * k
    return pen.p, w

def build_wordmark_aw(P=PARAMS, xh=None):
    H, Ro, tail, rt, g = P['H'], P['Ro'], P['tail'], P['rt'], P['gaps']
    Ri = Ro - H
    items = []; x = 0.0
    cxq = x + Ro
    items.append(('letter-q', glyph_q(Ro, Ri, tail, rt).tf(T(cxq, -Ro)), 'orange'))
    x = cxq + Ro + g['q_u']
    for ch, gap in (('u', 10.0), ('n', 10.0), ('i', 10.0)):
        p, w = aw_glyph(ch, xh)
        items.append((f'letter-{ch}', p.tf(T(x, 0)), 'ink')); x += w + gap
    cxP = x + Ro
    items.append(('letter-P', glyph_p(Ro, Ri, tail, rt).tf(T(cxP, -Ro)), 'blue'))
    x = cxP + Ro + g['P_a']
    p, w = aw_glyph('a', xh)
    items.append(('letter-a', p.tf(T(x, 0)), 'ink'))
    return items

build_wordmark = build_wordmark_aw      # the lockups below use this wordmark


# --------------------------------------------------------------------------
# Lockups
# --------------------------------------------------------------------------
def compact_params():
    P = dict(PARAMS)
    P.update(Hr=18.0, rho=21.0, node_m=12.5, clr=8.0, e_Ro=37.0, e_Ri=20.5, e_tail=11.0, e_gap=7.0, e_rt=2.2)
    return P


def build_compact_emblem():
    """Simplified emblem for small sizes: no inner arcs, heavier ring/nodes."""
    P = compact_params()
    R, Hr, rho, nm, c, f = P['R'], P['Hr'], P['rho'], P['node_m'], P['clr'], P['e_rt']
    theta = math.degrees(math.asin((rho + c) / R))
    items = []
    for t0, role, name in [(0, 'blue', 'ring-NE'), (90, 'blue', 'ring-SE'), (180, 'orange', 'ring-SW'), (270, 'orange', 'ring-NW')]:
        items.append((name, annular_sector(0, 0, R - Hr / 2, R + Hr / 2, t0 + theta, t0 + 90 - theta, f), role))
    for t, role, name in [(0, 'blue', 'node-N'), (90, 'blue', 'node-E'), (180, 'orange', 'node-S'), (270, 'orange', 'node-W')]:
        cx, cy = compass(0, 0, R, t)
        items.append((name, ring(cx, cy, rho, rho - nm), role))
    items.extend(build_monogram(P))
    return items


def build_monogram_only():
    P = dict(PARAMS); P.update(e_Ro=34.0, e_Ri=19.0, e_tail=12.0, e_gap=7.0, e_rt=2.0)
    return build_monogram(P)


def place(items, sx, dx, dy):
    return transform_items(items, compose(S(sx), T(dx, dy)))


def lay_horizontal(descriptor=None, wm_scale=1.0, gap=52.0):
    em, theta = build_emblem()
    block = list(build_wordmark())
    wbb = bbox_of(block)
    if descriptor:
        cap = 19.0
        base = wbb[3] + 17.0 + cap
        dp, tr = text_path(descriptor, FONT_MED, cap, width_units=wbb[2] - wbb[0], x0=wbb[0], baseline=base)
        block.append(('descriptor', dp, 'ink'))
        lay_horizontal.tracking = tr
    ebb = bbox_of(em); bb = bbox_of(block)
    wy = -(bb[1] + bb[3]) / 2.0 * wm_scale
    wx = ebb[2] + gap - bb[0] * wm_scale
    return list(em) + place(block, wm_scale, wx, wy)


def lay_stacked(descriptor=None, wm_scale=1.0, gap=34.0):
    em, theta = build_emblem()
    wm = build_wordmark()
    ebb = bbox_of(em); wbb = bbox_of(wm)
    wwid = (wbb[2] - wbb[0]) * wm_scale
    wx = -wwid / 2.0 - wbb[0] * wm_scale
    wy = ebb[3] + gap - wbb[1] * wm_scale
    return list(em) + place(wm, wm_scale, wx, wy)


LAYOUTS = {
    'horizontal':            lambda: lay_horizontal(),
    'horizontal-descriptor': lambda: lay_horizontal('RESEARCH GROUP'),
    'stacked':               lambda: lay_stacked(),
    'emblem':                lambda: build_emblem()[0],
    'emblem-compact':        lambda: build_compact_emblem(),
    'monogram':              lambda: build_monogram_only(),
    'wordmark':              lambda: build_wordmark(),
}
PNG_LONG_SIDE = {'horizontal': 4000, 'horizontal-descriptor': 4000, 'stacked': 3000, 'emblem': 3000,
                 'emblem-compact': 3000, 'monogram': 3000, 'wordmark': 4000}
CMYK_LAYOUTS = list(LAYOUTS)
MARGIN = 0.005   # hairline safety margin (fraction of longest side) – NOT the clear space


def finish(items):
    """Normalise to origin with a hairline margin; returns items, (w,h)."""
    x0, y0, x1, y1 = bbox_of(items)
    mg = MARGIN * max(x1 - x0, y1 - y0)
    items = transform_items(items, T(-x0 + mg, -y0 + mg))
    return items, (x1 - x0 + 2 * mg, y1 - y0 + 2 * mg)


# --------------------------------------------------------------------------
# Writers
# --------------------------------------------------------------------------
def col_hex(v):
    return v if isinstance(v, str) else '#%02X%02X%02X' % v


def svg_string(items, size, palette, title, desc):
    w, h = size
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.3f} {h:.3f}" width="{w:.3f}" height="{h:.3f}" role="img" aria-labelledby="t d">',
           f'<title id="t">{title}</title><desc id="d">{desc}</desc>']
    for name, p, role in items:
        out.append(f'<path id="{name}" fill="{palette[role]}" fill-rule="evenodd" d="{p.d()}"/>')
    out.append('</svg>')
    return '\n'.join(out)


def _rgb(hexs):
    return tuple(int(hexs[i:i + 2], 16) / 255.0 for i in (1, 3, 5))


def pdf_write(path, items, size, palette, cmyk=None, scale=None, title=''):
    w, h = size
    k = scale or (400.0 / max(w, h))
    c = rl_canvas.Canvas(path, pagesize=(w * k, h * k), pageCompression=1)
    c.setTitle(title); c.setAuthor('QuniPa research group'); c.setSubject('Logo')
    for name, p, role in items:
        pa = c.beginPath()
        for s in p.segs:
            if s[0] == 'M': pa.moveTo(s[1] * k, (h - s[2]) * k)
            elif s[0] == 'L': pa.lineTo(s[1] * k, (h - s[2]) * k)
            elif s[0] == 'C': pa.curveTo(s[1] * k, (h - s[2]) * k, s[3] * k, (h - s[4]) * k, s[5] * k, (h - s[6]) * k)
            else: pa.close()
        if cmyk:
            cc = cmyk[role]; c.setFillColorCMYK(*[v / 100.0 for v in cc])
        else:
            c.setFillColorRGB(*_rgb(palette[role]))
        c.drawPath(pa, stroke=0, fill=1, fillMode=0)   # 0 = even-odd
    c.showPage(); c.save()


def eps_write(path, items, size, palette, cmyk=None, title=''):
    w, h = size
    k = 400.0 / max(w, h)
    W, H = w * k, h * k
    o = ['%!PS-Adobe-3.0 EPSF-3.0', f'%%Title: {title}', '%%Creator: QuniPa logo build script',
         f'%%BoundingBox: 0 0 {int(math.ceil(W))} {int(math.ceil(H))}',
         f'%%HiResBoundingBox: 0 0 {W:.4f} {H:.4f}',
         '%%LanguageLevel: 2', '%%Pages: 1', '%%EndComments', '%%Page: 1 1', 'gsave']
    f = lambda v: f'{v:.4f}'.rstrip('0').rstrip('.')
    for name, p, role in items:
        o.append(f'% {name}')
        if cmyk:
            o.append(' '.join(f(v / 100.0) for v in cmyk[role]) + ' setcmykcolor')
        else:
            o.append(' '.join(f(v) for v in _rgb(palette[role])) + ' setrgbcolor')
        o.append('newpath')
        for s in p.segs:
            if s[0] == 'M': o.append(f'{f(s[1]*k)} {f((h-s[2])*k)} moveto')
            elif s[0] == 'L': o.append(f'{f(s[1]*k)} {f((h-s[2])*k)} lineto')
            elif s[0] == 'C': o.append(f'{f(s[1]*k)} {f((h-s[2])*k)} {f(s[3]*k)} {f((h-s[4])*k)} {f(s[5]*k)} {f((h-s[6])*k)} curveto')
            else: o.append('closepath')
        o.append('eofill')
    o += ['grestore', 'showpage', '%%EOF']
    open(path, 'w', newline='\n').write('\n'.join(o) + '\n')


# --------------------------------------------------------------------------
def build_all():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    manifest = []
    for layout, fn in LAYOUTS.items():
        items, size = finish(fn())
        for var, V in VARIANTS.items():
            pal = {r: V[r] for r in ('blue', 'orange', 'ink')}
            base = f'qunipa_{layout}_{var}'
            d_vec = os.path.join(OUT, layout, 'vector'); d_png = os.path.join(OUT, layout, 'png')
            os.makedirs(d_vec, exist_ok=True); os.makedirs(d_png, exist_ok=True)
            title = f'QuniPa logo – {layout} – {var}'
            svg = svg_string(items, size, pal, 'QuniPa', f'QuniPa research group logo ({layout}, {var})')
            sp = os.path.join(d_vec, base + '.svg'); open(sp, 'w').write(svg)
            pdf_write(os.path.join(d_vec, base + '.pdf'), items, size, pal, title=title)
            eps_write(os.path.join(d_vec, base + '.eps'), items, size, pal, title=title)
            long = PNG_LONG_SIDE[layout]
            kw = dict(output_width=long) if size[0] >= size[1] else dict(output_height=long)
            cairosvg.svg2png(url=sp, write_to=os.path.join(d_png, base + '.png'), **kw)
            # CMYK print files
            if V['cmyk']:
                d_cmyk = os.path.join(OUT, layout, 'print-cmyk'); os.makedirs(d_cmyk, exist_ok=True)
                pdf_write(os.path.join(d_cmyk, base + '_CMYK.pdf'), items, size, pal, cmyk=V['cmyk'], title=title + ' (CMYK)')
                eps_write(os.path.join(d_cmyk, base + '_CMYK.eps'), items, size, pal, cmyk=V['cmyk'], title=title + ' (CMYK)')
            manifest.append((layout, var, size))
    return manifest


if __name__ == '__main__':
    mf = build_all()
    print(len(mf), 'layout/variant combinations written to', OUT)
