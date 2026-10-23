import os, math
from reportlab.pdfgen import canvas as rl
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont as RLFont
from reportlab.lib.utils import simpleSplit, ImageReader
from build_logo import *

pdfmetrics.registerFont(RLFont('Plex', os.path.join(HERE, 'fonts', 'IBMPlexSans-Regular.ttf')))
pdfmetrics.registerFont(RLFont('Plex-Med', os.path.join(HERE, 'fonts', 'IBMPlexSans-Medium.ttf')))
pdfmetrics.registerFont(RLFont('Plex-Semi', os.path.join(HERE, 'fonts', 'IBMPlexSans-SemiBold.ttf')))

PW, PH = 841.89, 595.28
M = 42
BLUE, ORANGE, INK, NIGHT = '#0A5CB8', '#D95A0B', '#232A33', '#0F1720'
MUTED = '#5B6572'; RULE = '#D8DDE3'; WASH = '#F4F6F9'

def hexc(c, h): c.setFillColorRGB(*[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)])
def strokec(c, h): c.setStrokeColorRGB(*[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)])

def txt(c, x, y, s, font='Plex', size=9.5, color=INK, tracking=0, align='l'):
    hexc(c, color); t = c.beginText(); t.setFont(font, size); t.setCharSpace(tracking)
    w = pdfmetrics.stringWidth(s, font, size) + tracking * len(s)
    if align == 'c': x -= w / 2
    elif align == 'r': x -= w
    t.setTextOrigin(x, y); t.textOut(s); c.drawText(t)

def para(c, x, y, w, s, font='Plex', size=9.5, lead=13.5, color=INK):
    hexc(c, color); yy = y
    for line in simpleSplit(s, font, size, w):
        t = c.beginText(); t.setFont(font, size); t.setTextOrigin(x, yy); t.textOut(line); c.drawText(t); yy -= lead
    return yy

def draw(c, items, size, x, ytop, width, pal, ax=1.0, ay=1.0, rot=0, shadow=False):
    """Draw logo items (y-down units) with top-left at (x, ytop) in PDF space, scaled to `width` pt."""
    k = width / size[0]
    c.saveState()
    if rot:
        cx_, cy_ = x + size[0] * k / 2, ytop - size[1] * k / 2
        c.translate(cx_, cy_); c.rotate(rot); c.translate(-cx_, -cy_)
    for name, p, role in items:
        pa = c.beginPath()
        for s in p.segs:
            X = lambda v: x + v * k * ax; Y = lambda v: ytop - v * k * ay
            if s[0] == 'M': pa.moveTo(X(s[1]), Y(s[2]))
            elif s[0] == 'L': pa.lineTo(X(s[1]), Y(s[2]))
            elif s[0] == 'C': pa.curveTo(X(s[1]), Y(s[2]), X(s[3]), Y(s[4]), X(s[5]), Y(s[6]))
            else: pa.close()
        hexc(c, pal[role]); c.drawPath(pa, stroke=0, fill=1, fillMode=0)
    c.restoreState()

def PAL(v): V = VARIANTS[v]; return {r: V[r] for r in ('blue', 'orange', 'ink')}

LOG = {n: finish(LAYOUTS[n]()) for n in LAYOUTS}

def header(c, n, label, title):
    txt(c, M, PH - M - 4, f'{n:02d}', 'Plex-Med', 8, BLUE, 1.2)
    txt(c, M + 22, PH - M - 4, label.upper(), 'Plex-Med', 8, MUTED, 1.6)
    txt(c, M, PH - M - 34, title, 'Plex-Semi', 22, INK)
    strokec(c, RULE); c.setLineWidth(0.6); c.line(M, PH - M - 48, PW - M, PH - M - 48)

def footer(c, n):
    strokec(c, RULE); c.setLineWidth(0.6); c.line(M, M - 4, PW - M, M - 4)
    txt(c, M, M - 18, 'QuniPa  ·  Logo guidelines  ·  v1.0  ·  October 2026', 'Plex', 7.5, MUTED)
    txt(c, PW - M, M - 18, str(n), 'Plex-Med', 7.5, MUTED, align='r')

def rect(c, x, y, w, h, fill=None, stroke=None, lw=0.6, r=0, dash=None):
    c.saveState()
    if fill: hexc(c, fill)
    if stroke: strokec(c, stroke); c.setLineWidth(lw)
    if dash: c.setDash(*dash)
    (c.roundRect if r else c.rect)(x, y, w, h, *( (r,) if r else ()), fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()

def cross(c, x, y, s=7):
    c.saveState(); c.setStrokeColorRGB(.78, .16, .16); c.setLineWidth(1.6)
    c.line(x - s, y - s, x + s, y + s); c.line(x - s, y + s, x + s, y - s); c.restoreState()
def tick(c, x, y, s=7):
    c.saveState(); c.setStrokeColorRGB(.1, .55, .3); c.setLineWidth(1.8)
    c.line(x - s, y, x - s * .3, y - s * .7); c.line(x - s * .3, y - s * .7, x + s, y + s * .8); c.restoreState()

# ======================================================================
def build(path):
    c = rl.Canvas(path, pagesize=(PW, PH), pageCompression=1)
    c.setTitle('QuniPa – Logo guidelines'); c.setAuthor('QuniPa research group'); c.setSubject('Logo guidelines v1.0')

    # ---------------- 1 COVER ----------------
    items, size = LOG['horizontal']
    w = 520; draw(c, items, size, (PW - w) / 2, PH / 2 + 62, w, PAL('color'))
    txt(c, PW / 2, PH / 2 - 92, 'LOGO GUIDELINES', 'Plex-Med', 10, INK, 3.2, 'c')
    txt(c, PW / 2, PH / 2 - 112, 'Version 1.0  ·  October 2026', 'Plex', 8.5, MUTED, 0, 'c')
    strokec(c, RULE); c.line(PW / 2 - 24, PH / 2 - 70, PW / 2 + 24, PH / 2 - 70)
    c.showPage()

    # ---------------- 2 ANATOMY ----------------
    header(c, 1, 'The mark', 'One system, two voices')
    items, size = LOG['emblem']; ew = 290; ex, ey = M + 10, PH - 112
    draw(c, items, size, ex, ey, ew, PAL('color'))
    k = ew / size[0]
    def U(xu, yu): return ex + (xu + 119 + 0.005 * 238) * k, ey - (yu + 119 + 0.005 * 238) * k
    marks = [(1, U(-84, -62)), (2, U(119 - 8, 0)), (3, U(60, -70)), (4, U(-37, -23))]
    def badge(n, x, y, col=INK):
        c.saveState(); hexc(c, '#FFFFFF'); strokec(c, col); c.setLineWidth(0.9); c.circle(x, y, 7.2, fill=1, stroke=1); c.restoreState()
        txt(c, x, y - 2.7, str(n), 'Plex-Med', 7.5, col, 0, 'c')
    wm_items, wsize = LOG['wordmark']; ww = 340; wx0, wy0 = 420, PH - 112
    draw(c, wm_items, wsize, wx0, wy0, ww, PAL('color'))
    wk = ww / wsize[0]; mgw = 0.005 * max(wsize) / 1.01
    for n, (x, y) in marks: badge(n, x, y)
    badge(5, wx0 + (40 + mgw) * wk, wy0 - (40 + mgw) * wk)
    badge(6, wx0 + (163 + mgw) * wk, wy0 - (61 + mgw) * wk)
    rows = [
        (1, 'Two-colour ring', 'Orange on the left, blue on the right: two halves of one circle, as in the draft.'),
        (2, 'Four nodes', 'Hollow rings set into the gaps, one at each cardinal point. Their colours alternate (blue top and right, orange bottom and left).'),
        (3, 'Inner arcs', 'A point-symmetric pair that occupies the two quadrants the monogram leaves free.'),
        (4, 'qp monogram', 'The two initials, staggered along the diagonal and separated by a narrow central seam.'),
        (5, 'Initials in colour', 'The wordmark’s q and P are built exactly like the monogram’s: one bowl, one stem.'),
        (6, 'Neutral letters', 'u, n, i, a are set in Audiowide, in Ink, so the two custom-drawn initials lead.'),
    ]
    y = PH - 250
    for n, h, t in rows:
        badge(n, 420 + 7, y + 3)
        txt(c, 440, y, h, 'Plex-Semi', 9.5, INK)
        y = para(c, 440, y - 13, 360, t, 'Plex', 8.8, 12.2, MUTED) - 7
    txt(c, M, M + 6, 'The meaning of the name and the concept itself are unchanged from the draft; this document describes form only.', 'Plex', 8, MUTED)
    footer(c, 2); c.showPage()

    # ---------------- 3 CLEAR SPACE & MIN SIZE ----------------
    header(c, 2, 'Space and size', 'Clear space and minimum size')
    items, size = LOG['horizontal']; lw_ = 420; lx, ly = M + 30, PH - 130
    k = lw_ / size[0]; xu = 39.0 * k
    mgu = 0.005 * max(size) / 1.01; mg = mgu * k
    L_, R_ = lx + mg, lx + size[0] * k - mg
    T_, B_ = ly - mg, ly - size[1] * k + mg
    rect(c, L_ - xu, B_ - xu, R_ - L_ + 2 * xu, T_ - B_ + 2 * xu, fill=WASH, stroke='#9AA5B1', lw=0.6, dash=([3, 3], 0))
    draw(c, items, size, lx, ly, lw_, PAL('color'))
    c.saveState(); hexc(c, BLUE); c.setFillAlpha(0.18)
    c.rect(L_ - xu, T_, xu, xu); c.rect(R_, B_ - xu, xu, xu); c.restoreState()
    txt(c, L_ - xu / 2, T_ + xu / 2 - 3.5, 'x', 'Plex-Med', 10, BLUE, 0, 'c')
    txt(c, R_ + xu / 2, B_ - xu / 2 - 3.5, 'x', 'Plex-Med', 10, BLUE, 0, 'c')
    ncx = lx + (119 + mgu) * k; ncy = ly - (19.5 + mgu) * k
    c.saveState(); strokec(c, BLUE); c.setLineWidth(0.8); c.setDash(2, 2)
    c.circle(ncx, ncy, 19.5 * k, fill=0, stroke=1); c.restoreState()
    txt(c, ncx + 19.5 * k + 6, ncy - 3, '= x', 'Plex-Med', 9, BLUE)
    para(c, M, B_ - xu - 22, 440,
         'Keep a clear margin of x on every side, where x is the outer diameter of one emblem node (about one sixth of the emblem’s height). '
         'For the wordmark on its own, x equals the x-height of the letters u n i a. Nothing other than the background may enter this zone.',
         'Plex', 9, 12.8, INK)
    # table
    tx = 530; ty = PH - 100
    txt(c, tx, ty, 'MINIMUM SIZES', 'Plex-Med', 8, MUTED, 1.4)
    rowsT = [('Version', 'Print', 'Screen'),
             ('Horizontal', '38 mm wide', '170 px wide'),
             ('Horizontal + descriptor', '50 mm wide', '230 px wide'),
             ('Stacked', '22 mm wide', '95 px wide'),
             ('Wordmark only', '22 mm wide', '90 px wide'),
             ('Emblem (full)', '12 mm', '48 px'),
             ('Emblem (compact)', '6 mm', '24 px'),
             ('Monogram qp', '4 mm', '16 px')]
    yy = ty - 18
    for i, (a, b, d) in enumerate(rowsT):
        f = 'Plex-Med' if i == 0 else 'Plex'; col = MUTED if i == 0 else INK
        txt(c, tx, yy, a, f, 8.8, col); txt(c, tx + 128, yy, b, f, 8.8, col); txt(c, tx + 208, yy, d, f, 8.8, col)
        strokec(c, RULE); c.setLineWidth(0.5); c.line(tx, yy - 5.5, PW - M, yy - 5.5); yy -= 19
    para(c, tx, yy - 6, PW - M - tx,
         'Below its minimum, switch to a smaller version rather than shrinking further: horizontal → stacked → full emblem → compact emblem → monogram. '
         'Minimums were set by rendering each version at real pixel sizes and checking that the i-dot, node openings and the thin letters stay distinct.',
         'Plex', 8.4, 11.8, MUTED)
    # small-size ladder
    sx = M + 30; sy = 130
    txt(c, sx, sy + 38, 'VERSIONS FOR SMALL SIZES', 'Plex-Med', 8, MUTED, 1.4)
    xcur = sx
    for lay, wpt, cap in [('emblem', 58, 'Full emblem'), ('emblem-compact', 40, 'Compact'), ('monogram', 30, 'Monogram')]:
        it, sz = LOG[lay]; draw(c, it, sz, xcur, sy + 22 - 0, wpt, PAL('color'))
        txt(c, xcur, sy - 52, cap, 'Plex', 7.8, MUTED)
        xcur += wpt + 46
    para(c, xcur + 10, sy + 18, 300, 'The compact emblem drops the inner arcs and thickens the ring and nodes. The monogram is for favicons and other very small marks.', 'Plex', 8.4, 11.8, MUTED)
    footer(c, 3); c.showPage()

    # ---------------- 4 COLOUR ----------------
    header(c, 3, 'Colour', 'Palette and specifications')
    def lum(h):
        r, g, b = [int(h[i:i+2], 16) / 255 for i in (1, 3, 5)]
        f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
    def cr(a, b):
        la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
    rgbs = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
    cards = [('QuniPa Blue', BLUE, (95, 60, 0, 0), 'K 85', 'On white'),
             ('QuniPa Orange', ORANGE, (0, 75, 100, 10), 'K 65', 'On white'),
             ('QuniPa Ink', INK, (50, 35, 25, 90), 'K 95', 'On white')]
    cw, ch = 244, 150; x0 = M; y0 = PH - 112 - ch
    for i, (nm, hx, cm, gy, ctx) in enumerate(cards):
        x = x0 + i * (cw + 12)
        rect(c, x, y0 + 74, cw, 76, fill=hx)
        txt(c, x + 12, y0 + 128, nm, 'Plex-Semi', 11, '#FFFFFF')
        yy = y0 + 62
        for lab, val in [('HEX', hx), ('RGB', '%d  %d  %d' % rgbs(hx)), ('CMYK', 'C%d  M%d  Y%d  K%d' % cm), ('Grayscale', gy + ' %'), (ctx + ' contrast', '%.1f : 1' % cr(hx, '#FFFFFF'))]:
            txt(c, x, yy, lab, 'Plex', 8.2, MUTED); txt(c, x + 82, yy, val, 'Plex-Med', 8.8, INK); yy -= 13
    # on dark
    y1 = y0 - 138
    txt(c, M, y1 + 118, 'FOR DARK BACKGROUNDS', 'Plex-Med', 8, MUTED, 1.4)
    dcards = [('Night (background)', NIGHT, None), ('Blue on dark', '#4DA3FF', None), ('Orange on dark', '#FF8A3D', None), ('Paper (letters)', '#F3F5F8', None)]
    dw = 178
    for i, (nm, hx, _) in enumerate(dcards):
        x = M + i * (dw + 12)
        rect(c, x, y1 + 40, dw, 60, fill=hx, stroke=RULE if hx == '#F3F5F8' else None)
        txt(c, x + 10, y1 + 78, nm, 'Plex-Semi', 9.5, '#FFFFFF' if hx in (NIGHT,) else NIGHT)
        txt(c, x, y1 + 26, hx + '   ' + '%d %d %d' % rgbs(hx), 'Plex-Med', 8.4, INK)
        if hx != NIGHT: txt(c, x, y1 + 13, 'contrast on Night  %.1f : 1' % cr(hx, NIGHT), 'Plex', 8, MUTED)
    # notes
    ny = y1 - 10
    notes = ('Orange is a graphic colour: at 3.9 : 1 on white it suits the large initials, but should not be used for body text. Use Ink or Blue for text. '
             'Blue and orange are a hue-opposed pair, which is generally robust for common forms of colour-vision deficiency (not formally simulated here); in grayscale the two halves still separate (K 85 vs K 65).  '
             'CMYK builds were derived with the FOGRA39 (coated) profile, relative colorimetric with black-point compensation, then rounded to 5 %. '
             'Blue is slightly less saturated in print because it sits at the edge of the CMYK gamut. Always proof, and match to a physical swatch book if exact brand colour is critical. '
             'No spot-colour (Pantone) equivalents are specified.')
    para(c, M, ny, PW - 2 * M, notes, 'Plex', 8.3, 11.6, MUTED)
    footer(c, 4); c.showPage()

    # ---------------- 5 VERSIONS ----------------
    header(c, 4, 'Versions', 'Layouts and colour variants')
    lays = [('horizontal', 'Horizontal  (primary)', 210), ('stacked', 'Stacked', 120), ('horizontal-descriptor', 'Horizontal + descriptor', 210),
            ('wordmark', 'Wordmark only', 160), ('emblem', 'Emblem', 92), ('emblem-compact', 'Compact emblem', 70), ('monogram', 'Monogram', 60)]
    rowA = [('horizontal', M, 220), ('horizontal-descriptor', M + 262, 220), ('wordmark', M + 524, 170)]
    rowB = [('stacked', M, 112), ('emblem', M + 262, 98), ('emblem-compact', M + 410, 74), ('monogram', M + 524, 62)]
    caps = dict(lays_cap := {n: cap for n, cap, _ in lays})
    for row, ytop, capy in ((rowA, PH - 98, PH - 202), (rowB, PH - 228, PH - 372)):
        for lay, x, wd in row:
            it, sz = LOG[lay]; draw(c, it, sz, x, ytop - 4, wd, PAL('color'))
            txt(c, x, capy, caps[lay], 'Plex-Med', 8, MUTED)
    # variants strip
    vy = 140
    txt(c, M, vy + 46, 'COLOUR VARIANTS', 'Plex-Med', 8, MUTED, 1.4); txt(c, M + 100, vy + 46, 'every version is supplied in each', 'Plex', 8, MUTED)
    vlist = [('color', 'Full colour', '#FFFFFF'), ('color-on-dark', 'Colour, for dark', NIGHT), ('gray', 'Grayscale', '#FFFFFF'),
             ('gray-on-dark', 'Gray, for dark', NIGHT), ('black', 'Black', '#FFFFFF'), ('white', 'White', NIGHT)]
    it, sz = LOG['horizontal']; tw = 122; th = 56; gx = 8
    for i, (v, cap, bg) in enumerate(vlist):
        x = M + i * (tw + gx)
        rect(c, x, vy - 12, tw, th, fill=bg, stroke=RULE)
        draw(c, it, sz, x + 10, vy - 12 + th - 13, tw - 20, PAL(v))
        txt(c, x, vy - 26, cap, 'Plex', 7.8, MUTED)
    para(c, M, 92, PW - 2 * M, 'Use full colour on white or very light backgrounds. On dark backgrounds use the “for dark” variants (recommended background: Night #0F1720, or any dark of similar depth). '
         'On photographs or coloured backgrounds use black or white, whichever contrasts more. Grayscale is for documents printed without colour; black and white are for one-colour jobs, engraving, stamps and embroidery.',
         'Plex', 8.4, 11.8, MUTED)
    footer(c, 5); c.showPage()

    # ---------------- 6 TYPOGRAPHY ----------------
    header(c, 5, 'Typography', 'Lettering and typeface')
    wi, wsz = LOG['wordmark']; draw(c, wi, wsz, M, PH - 118, 330, PAL('color'))
    para(c, M, PH - 118 - 330 * wsz[1] / wsz[0] - 24, 330,
         'The wordmark combines two sources. The initials q and P are custom-drawn (one bowl, one stem, the same construction as the emblem’s monogram). '
         'The letters u, n, i and a are Audiowide Regular (SIL Open Font License), converted to outlines and scaled to a 42-unit x-height. '
         'The wordmark is supplied as outlined artwork, so no font needs to be installed. Reproduce it only from the supplied files and never retype it.',
         'Plex', 9, 12.8, INK)
    tx = 440
    txt(c, tx, PH - 116, 'COMPANION TYPEFACE (descriptor and text)', 'Plex-Med', 8, MUTED, 1.4)
    txt(c, tx, PH - 146, 'IBM Plex Sans', 'Plex-Semi', 24, INK)
    txt(c, tx, PH - 168, 'Regular  ·  Medium  ·  SemiBold', 'Plex', 10, MUTED)
    y = para(c, tx, PH - 192, 360,
             'Used for the optional “Research Group” descriptor (Medium, capitals, letter-spaced to the width of the wordmark) and recommended for headings, slides and posters so that text sits comfortably beside the logo. '
             'Licence: SIL Open Font License 1.1: free for any use, including embedding, with no restrictions on documents or web. Download: github.com/IBM/plex.',
             'Plex', 9, 12.8, INK)
    y -= 6
    para(c, tx, y, 360, 'Where Plex is unavailable (for example, a colleague’s PowerPoint), fall back to Arial or Helvetica. Do not substitute a rounded or decorative face.', 'Plex', 9, 12.8, MUTED)
    # sample
    rect(c, tx, 100, PW - M - tx, 120, fill=WASH)
    txt(c, tx + 16, 192, 'Aa  Bb  Qq  Pp  0123', 'Plex-Semi', 20, INK)
    txt(c, tx + 16, 166, 'The quick brown fox jumps over the lazy dog.', 'Plex', 11, INK)
    txt(c, tx + 16, 148, 'RESEARCH GROUP', 'Plex-Med', 9, INK, 3.2)
    txt(c, tx + 16, 120, 'Descriptor: Plex Medium, capitals, +0.31 em tracking (fitted to the wordmark width).', 'Plex', 8, MUTED)
    para(c, M, 130, 330, 'The descriptor text “RESEARCH GROUP” is a placeholder; edit it in build_logo.py or ask for a custom line.', 'Plex', 8, 11, MUTED)
    footer(c, 6); c.showPage()

    # ---------------- 7 DO / DON'T ----------------
    header(c, 6, 'Usage', 'Use it as supplied')
    it, sz = LOG['horizontal']
    tw, th = 244, 100; gx, gy = 12, 22
    def tile(i, row, bg, caption, ok, fn, cap_ok=True):
        x = M + i * (tw + gx); y = PH - 104 - row * (th + gy + 14)
        rect(c, x, y - th, tw, th, fill=bg, stroke=RULE)
        fn(x, y)
        (tick if ok else cross)(c, x + tw - 14, y - 14, 6)
        txt(c, x, y - th - 13, caption, 'Plex', 8.4, INK)
    lw = 160
    def center(x, y, ax=1, ay=1, rot=0, pal=None, w=lw):
        hgt = w * sz[1] / sz[0] * ay; draw(c, it, sz, x + (tw - w * ax) / 2, y - (th - hgt) / 2, w, pal or PAL('color'), ax, ay, rot)
    tile(0, 0, '#FFFFFF', 'On white or light backgrounds: full colour.', True, lambda x, y: center(x, y))
    tile(1, 0, NIGHT, 'On dark backgrounds: the “for dark” variant.', True, lambda x, y: center(x, y, pal=PAL('color-on-dark')))
    tile(2, 0, BLUE, 'On colour or photographs: white (or black).', True, lambda x, y: center(x, y, pal=PAL('white')))
    tile(0, 1, '#FFFFFF', 'Don’t stretch, squash or skew.', False, lambda x, y: center(x, y, ax=1.3, ay=0.78))
    tile(1, 1, '#FFFFFF', 'Don’t recolour, or swap orange and blue.', False,
         lambda x, y: center(x, y, pal={'blue': ORANGE, 'orange': BLUE, 'ink': '#2E8B57'}))
    tile(2, 1, '#FFFFFF', 'Don’t rotate or tilt.', False, lambda x, y: center(x, y, rot=-10, w=150))
    def shadow(x, y):
        center(x + 3, y - 3, pal={'blue': '#B9BFC7', 'orange': '#B9BFC7', 'ink': '#B9BFC7'}); center(x, y)
    tile(0, 2, '#FFFFFF', 'Don’t add shadows, outlines, glows or gradients.', False, shadow)
    tile(1, 2, '#E9A15E', 'Don’t place full colour on low-contrast backgrounds.', False, lambda x, y: center(x, y))
    def retype(x, y):
        e, esz = LOG['emblem']; ew = 70
        draw(c, e, esz, x + 24, y - (th - ew) / 2, ew, PAL('color')); txt(c, x + 112, y - th / 2 - 8, 'QuniPa', 'Plex-Semi', 30, INK)
    tile(2, 2, '#FFFFFF', 'Don’t retype the name or rebuild the lockup.', False, retype)
    footer(c, 7); c.showPage()

    # ---------------- 8 REFINEMENT NOTES ----------------
    header(c, 7, 'Process', 'From draft to final: what changed and why')
    c.drawImage(ImageReader(os.path.join(HERE, 'draft_for_pdf.png')), M, PH - 104 - 250 * 0.4522, width=250, height=250 * 0.4522, mask='auto')
    txt(c, M, PH - 232, 'DRAFT', 'Plex-Med', 7.5, MUTED, 1.4)
    it, sz = LOG['horizontal']; draw(c, it, sz, M + 290, PH - 112, 250, PAL('color'))
    txt(c, M + 290, PH - 232, 'REFINED', 'Plex-Med', 7.5, MUTED, 1.4)
    notes = [
        ('Weights.', 'Seven different stroke weights (≈6 to 17.7) in the draft were brought into one system for the emblem and the custom initials. Audiowide’s lighter strokes are the exception.'),
        ('Knock-outs.', 'The node centres were filled with white, so the logo failed on dark or coloured backgrounds. They are now true openings.'),
        ('Clearances.', 'The ring gaps around the nodes were tight (≈3 units) and uneven. Every arc end now sits exactly the same distance from its node.'),
        ('Symmetry.', 'The two inner arcs started and ended at different angles. They are now an exact 180° pair, concentric with the ring.'),
        ('Central seam.', 'The q and p stems nearly touched (≈3 units), creating tension. The gap is now a deliberate seam, and the stagger equals one bowl radius.'),
        ('Reading.', 'Very short stems made the emblem’s q easy to misread as “a”. Tails are longer, so q and p are unambiguous.'),
        ('Baseline.', 'The big bowls hung about 11 units below the small letters’ baseline without aligning to anything. They now sit on it, with stems descending evenly.'),
        ('u n i a.', 'Your original “a” had a distinctive slit-and-rounded-end form that none of my own redraws kept. u, n, i and a are now Audiowide, whose “a” is the closest free match.'),
        ('Details.', 'Letter spacing was re-set optically for the new letters, and colours were tuned slightly for contrast.'),
        ('Production.', 'Live strokes and nested scaled groups became clean outlines; added dark, mono, compact and small-size versions.'),
    ]
    colx = [M, M + 395]; y0 = PH - 268; y = [y0, y0]
    for i, (h, t) in enumerate(notes):
        ci = 0 if i < 5 else 1
        txt(c, colx[ci], y[ci], h, 'Plex-Semi', 8.8, INK)
        y[ci] = para(c, colx[ci] + 62, y[ci], 330, t, 'Plex', 8.6, 11.8, MUTED) - 6
    footer(c, 8); c.showPage()
    c.save()

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    build(os.path.join(OUT, 'QuniPa_Logo_Guidelines.pdf')); print('ok')
