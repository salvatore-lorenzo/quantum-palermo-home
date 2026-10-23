"""
QuniPa logo – parametric geometry.
Everything is constructed from a small set of numbers (see PARAMS) so the
mark can be rebuilt, audited and adjusted without redrawing.
Coordinates: SVG convention (y points down). Compass angles: 0° = 12 o'clock, clockwise.
"""
import math

# --------------------------------------------------------------------------
# Path container
# --------------------------------------------------------------------------
class Path:
    def __init__(self, segs=None):
        self.segs = segs or []
        self.cur = None

    def M(self, x, y):
        self.segs.append(('M', x, y)); self.cur = (x, y); return self

    def L(self, x, y):
        self.segs.append(('L', x, y)); self.cur = (x, y); return self

    def C(self, x1, y1, x2, y2, x, y):
        self.segs.append(('C', x1, y1, x2, y2, x, y)); self.cur = (x, y); return self

    def Z(self):
        self.segs.append(('Z',)); return self

    def arc(self, cx, cy, r, a0, a1):
        """Circular arc about (cx,cy) from math-angle a0 to a1 (radians, y-down,
        increasing = clockwise on screen). Current point is assumed to be the start."""
        d = a1 - a0
        n = max(1, int(math.ceil(abs(d) / (math.pi / 2) - 1e-9)))
        step = d / n
        k = 4.0 / 3.0 * math.tan(step / 4.0)
        a = a0
        for _ in range(n):
            b = a + step
            x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
            x3, y3 = cx + r * math.cos(b), cy + r * math.sin(b)
            x1, y1 = x0 - k * r * math.sin(a), y0 + k * r * math.cos(a)
            x2, y2 = x3 + k * r * math.sin(b), y3 - k * r * math.cos(b)
            self.C(x1, y1, x2, y2, x3, y3)
            a = b
        return self

    def tf(self, m):
        a, b, c, d, e, f = m
        def P(x, y):
            return (a * x + c * y + e, b * x + d * y + f)
        out = Path()
        for s in self.segs:
            if s[0] in ('M', 'L'):
                x, y = P(s[1], s[2]); out.segs.append((s[0], x, y))
            elif s[0] == 'C':
                p1 = P(s[1], s[2]); p2 = P(s[3], s[4]); p3 = P(s[5], s[6])
                out.segs.append(('C', *p1, *p2, *p3))
            else:
                out.segs.append(('Z',))
        return out

    def extend(self, other):
        self.segs.extend(other.segs); return self

    def d(self, prec=3):
        f = lambda v: ('%.*f' % (prec, v)).rstrip('0').rstrip('.') if '.' in ('%.*f' % (prec, v)) else '%.*f' % (prec, v)
        o = []
        for s in self.segs:
            if s[0] == 'Z':
                o.append('Z')
            else:
                o.append(s[0] + ' '.join(f(v) for v in s[1:]))
        return ''.join(o)

    def bbox(self):
        xs, ys = [], []
        cur = None
        for s in self.segs:
            if s[0] in ('M', 'L'):
                cur = (s[1], s[2]); xs.append(cur[0]); ys.append(cur[1])
            elif s[0] == 'C':
                p0 = cur; p1 = (s[1], s[2]); p2 = (s[3], s[4]); p3 = (s[5], s[6])
                for i in range(0, 41):
                    t = i / 40; u = 1 - t
                    xs.append(u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0])
                    ys.append(u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])
                cur = p3
        return min(xs), min(ys), max(xs), max(ys)


def T(dx=0, dy=0): return (1, 0, 0, 1, dx, dy)
def S(sx, sy=None): return (sx, 0, 0, sx if sy is None else sy, 0, 0)
def MIRX(): return (-1, 0, 0, 1, 0, 0)
def compose(*ms):
    """compose(m1, m2, ...) applies m1 first, then m2 ..."""
    def mul(A, B):  # apply A then B
        a1, b1, c1, d1, e1, f1 = A; a2, b2, c2, d2, e2, f2 = B
        return (a2*a1 + c2*b1, b2*a1 + d2*b1, a2*c1 + c2*d1, b2*c1 + d2*d1,
                a2*e1 + c2*f1 + e2, b2*e1 + d2*f1 + f2)
    r = ms[0]
    for m in ms[1:]:
        r = mul(r, m)
    return r


def rad(deg): return deg * math.pi / 180.0


def compass(cx, cy, r, t_deg):
    p = rad(t_deg) - math.pi / 2
    return cx + r * math.cos(p), cy + r * math.sin(p)


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------
def circle(cx, cy, r, cw=True):
    p = Path(); sgn = 1 if cw else -1
    p.M(cx + r, cy); p.arc(cx, cy, r, 0, sgn * 2 * math.pi); p.Z(); return p


def ring(cx, cy, ro, ri):
    return circle(cx, cy, ro, True).extend(circle(cx, cy, ri, False))


def rounded_poly(pts, radii):
    """Closed polygon with a tangent fillet of radius radii[i] at vertex i."""
    n = len(pts); info = []
    for i in range(n):
        v = pts[i]; a = pts[i - 1]; b = pts[(i + 1) % n]; r = radii[i]
        if r <= 0:
            info.append((v, v, None, 0, 0)); continue
        u1 = (a[0]-v[0], a[1]-v[1]); l1 = math.hypot(*u1); u1 = (u1[0]/l1, u1[1]/l1)
        u2 = (b[0]-v[0], b[1]-v[1]); l2 = math.hypot(*u2); u2 = (u2[0]/l2, u2[1]/l2)
        phi = math.acos(max(-1, min(1, u1[0]*u2[0] + u1[1]*u2[1])))
        dist = r / math.tan(phi / 2)
        t1 = (v[0] + u1[0]*dist, v[1] + u1[1]*dist)
        t2 = (v[0] + u2[0]*dist, v[1] + u2[1]*dist)
        bis = (u1[0]+u2[0], u1[1]+u2[1]); lb = math.hypot(*bis); bis = (bis[0]/lb, bis[1]/lb)
        cd = r / math.sin(phi / 2)
        c = (v[0] + bis[0]*cd, v[1] + bis[1]*cd)
        info.append((t1, t2, c, r, 1))
    p = Path()
    p.M(*info[0][1])
    for i in list(range(1, n)) + [0]:
        t1, t2, c, r, rounded = info[i]
        p.L(*t1)
        if rounded:
            a0 = math.atan2(t1[1]-c[1], t1[0]-c[0]); a1 = math.atan2(t2[1]-c[1], t2[0]-c[0])
            dd = (a1 - a0 + math.pi) % (2*math.pi) - math.pi
            p.arc(c[0], c[1], r, a0, a0 + dd)
    p.Z()
    return p


def annular_sector(cx, cy, r1, r2, t0, t1, f):
    """Annular sector (compass degrees t0->t1, clockwise) with fillets f on all four corners."""
    do = math.degrees(math.asin(f / (r2 - f))); so = math.sqrt((r2 - f)**2 - f**2)
    di = math.degrees(math.asin(f / (r1 + f))); si = math.sqrt((r1 + f)**2 - f**2)
    P = lambda r, t: compass(cx, cy, r, t)
    ang = lambda c, p: math.atan2(p[1]-c[1], p[0]-c[0])
    def fil(p, c, q, r):
        a0 = ang(c, p); a1 = ang(c, q)
        dd = (a1 - a0 + math.pi) % (2*math.pi) - math.pi
        p_.arc(c[0], c[1], r, a0, a0 + dd)
    p_ = Path()
    A = P(r2, t0 + do); B = P(r2, t1 - do)
    p_.M(*A)
    # outer arc clockwise
    a0 = rad(t0 + do) - math.pi/2; a1 = rad(t1 - do) - math.pi/2
    p_.arc(cx, cy, r2, a0, a1)
    # outer-end corner
    Co = P(r2 - f, t1 - do); Eo = P(so, t1)
    fil(B, Co, Eo, f)
    # end radial inward
    Ei = P(si, t1); p_.L(*Ei)
    Ci = P(r1 + f, t1 - di); Bi = P(r1, t1 - di)
    fil(Ei, Ci, Bi, f)
    # inner arc counter-clockwise
    a0 = rad(t1 - di) - math.pi/2; a1 = rad(t0 + di) - math.pi/2
    p_.arc(cx, cy, r1, a0, a1)
    # inner-start corner
    Ai = P(r1, t0 + di); Ci0 = P(r1 + f, t0 + di); Si = P(si, t0)
    fil(Ai, Ci0, Si, f)
    So = P(so, t0); p_.L(*So)
    Co0 = P(r2 - f, t0 + do)
    fil(So, Co0, A, f)
    p_.Z()
    return p_


# --------------------------------------------------------------------------
# Parameters (single source of truth)
# --------------------------------------------------------------------------
PARAMS = dict(
    # ---- wordmark (units; baseline y=0) ----
    H=17.0,          # heavy stroke: q and P
    Ro=40.0,         # q/P bowl outer radius
    tail=15.0,       # stem extension below baseline (descender)
    m=12.0,          # light stroke: u n i a  (= 0.70 H)
    xh=38.0,         # x-height of u n i a
    uW=42.0,         # u / n outer width
    uRi=6.0,         # u / n inner bottom radius (outer = uRi + m  -> concentric)
    rt=1.8,          # terminal corner radius, all flat terminals
    gaps=dict(q_u=9.0, u_n=11.0, n_i=11.0, i_P=10.0, P_a=8.0),
    dot_gap=5.5,     # stem top -> i-dot
    # ---- emblem (units; centre 0,0) ----
    R=100.0,         # ring centre-line radius
    Hr=15.0,         # ring stroke
    rho=19.5,        # node outer radius
    node_m=10.5,     # node ring stroke (= 0.70 Hr)
    clr=6.5,         # clearance node <-> arc end
    e_Ro=34.0, e_Ri=19.0, e_tail=12.0,   # emblem monogram q/p
    e_gap=6.0,       # gap between facing q / p stems
    in_r=73.0, in_w=10.5, in_t0=5.0, in_t1=65.0,  # inner arcs
    e_rt=1.8,
)


# --------------------------------------------------------------------------
# Glyphs
# --------------------------------------------------------------------------
def glyph_q(Ro, Ri, tail, rt):
    """Bowl + right-hand stem, centred on the bowl centre (0,0); stem descends `tail` below bowl."""
    yb = Ro + tail
    yj = math.sqrt(Ro**2 - Ri**2)
    p = Path()
    p.M(Ro, 0)
    p.L(Ro, yb - rt)
    p.arc(Ro - rt, yb - rt, rt, 0, math.pi / 2)
    p.L(Ri + rt, yb)
    p.arc(Ri + rt, yb - rt, rt, math.pi / 2, math.pi)
    p.L(Ri, yj)
    p.arc(0, 0, Ro, math.atan2(yj, Ri), 2 * math.pi)
    p.Z()
    p.extend(circle(0, 0, Ri, False))
    return p


def glyph_p(Ro, Ri, tail, rt):
    return glyph_q(Ro, Ri, tail, rt).tf(MIRX())


def glyph_u(W, h, m, Ri_b, rt):
    Ro_b = Ri_b + m
    pts = [(0, 0), (m, 0), (m, h - m), (W - m, h - m), (W - m, 0), (W, 0), (W, h), (0, h)]
    rr = [rt, rt, Ri_b, Ri_b, rt, rt, Ro_b, Ro_b]
    return rounded_poly(pts, rr)


def glyph_n(W, h, m, Ri_b, rt):
    return glyph_u(W, h, m, Ri_b, rt).tf((-1, 0, 0, -1, W, h))


def glyph_i(m, h, rt):
    return rounded_poly([(0, 0), (m, 0), (m, h), (0, h)], [rt] * 4)


def glyph_a(h, m, rt):
    """Single-storey 'a': bowl + full-height right stem, same construction as q (no descender)."""
    Ro = h / 2.0; Ri = Ro - m
    cx, cy = Ro, Ro
    yj = math.sqrt(Ro**2 - Ri**2)
    T_, B_ = 0.0, h
    p = Path()
    p.M(cx + Ro - rt, T_)
    p.L(cx + Ri, T_)
    p.L(cx + Ri, cy - yj)
    # outer arc counter-clockwise over the top, left, bottom
    a_start = math.atan2(-yj, Ri)
    a_end = math.atan2(yj, Ri) - 2 * math.pi
    p.arc(cx, cy, Ro, a_start, a_end)
    p.L(cx + Ri, B_)
    p.L(cx + Ro - rt, B_)
    p.arc(cx + Ro - rt, B_ - rt, rt, math.pi / 2, 0)
    p.L(cx + Ro, T_ + rt)
    p.arc(cx + Ro - rt, T_ + rt, rt, 0, -math.pi / 2)
    p.Z()
    p.extend(circle(cx, cy, Ri, True))
    return p


# --------------------------------------------------------------------------
# Assemblies.  Each returns list of (id, Path, role)
# --------------------------------------------------------------------------
def build_wordmark(P=PARAMS):
    H, Ro, tail, m, xh = P['H'], P['Ro'], P['tail'], P['m'], P['xh']
    Ri = Ro - H; rt = P['rt']; g = P['gaps']
    items = []
    x = 0.0
    # q
    cxq = x + Ro
    items.append(('letter-q', glyph_q(Ro, Ri, tail, rt).tf(T(cxq, -Ro)), 'orange'))
    x = cxq + Ro + g['q_u']
    # u
    items.append(('letter-u', glyph_u(P['uW'], xh, m, P['uRi'], rt).tf(T(x, -xh)), 'ink'))
    x += P['uW'] + g['u_n']
    items.append(('letter-n', glyph_n(P['uW'], xh, m, P['uRi'], rt).tf(T(x, -xh)), 'ink'))
    x += P['uW'] + g['n_i']
    items.append(('letter-i', glyph_i(m, xh, rt).tf(T(x, -xh)), 'ink'))
    dot_r = 7.6
    items.append(('letter-i-dot', circle(x + m / 2, -xh - P['dot_gap'] - dot_r, dot_r), 'ink'))
    x += m + g['i_P']
    cxP = x + Ro
    items.append(('letter-P', glyph_p(Ro, Ri, tail, rt).tf(T(cxP, -Ro)), 'blue'))
    x = cxP + Ro + g['P_a']
    items.append(('letter-a', glyph_a(xh, m, rt).tf(T(x, -xh)), 'ink'))
    return items


def build_emblem(P=PARAMS):
    R, Hr, rho, nm, c = P['R'], P['Hr'], P['rho'], P['node_m'], P['clr']
    f = P['e_rt']
    items = []
    theta = math.degrees(math.asin((rho + c) / R))
    quad = [(0, 'blue', 'ring-NE'), (90, 'blue', 'ring-SE'), (180, 'orange', 'ring-SW'), (270, 'orange', 'ring-NW')]
    for t0, role, name in quad:
        items.append((name, annular_sector(0, 0, R - Hr / 2, R + Hr / 2, t0 + theta, t0 + 90 - theta, f), role))
    # inner arcs (point-symmetric pair, occupying the quadrants the monogram leaves free)
    ir1 = P['in_r'] - P['in_w'] / 2; ir2 = P['in_r'] + P['in_w'] / 2
    items.append(('inner-NE', annular_sector(0, 0, ir1, ir2, P['in_t0'], P['in_t1'], f), 'blue'))
    items.append(('inner-SW', annular_sector(0, 0, ir1, ir2, 180 + P['in_t0'], 180 + P['in_t1'], f), 'orange'))
    # nodes
    for t, role, name in [(0, 'blue', 'node-N'), (90, 'blue', 'node-E'), (180, 'orange', 'node-S'), (270, 'orange', 'node-W')]:
        cx, cy = compass(0, 0, R, t)
        items.append((name, ring(cx, cy, rho, rho - nm), role))
    items.extend(build_monogram(P))
    return items, theta


def build_monogram(P=PARAMS, centre=(0.0, 0.0)):
    Ro, Ri, tl, g = P['e_Ro'], P['e_Ri'], P['e_tail'], P['e_gap']
    rt = P['e_rt']
    a = Ro + g / 2.0           # half-distance between bowl centres (x)
    b = Ro / 4.0               # half stagger: total stagger = Ro / 2 ... see note below
    b = Ro / 2.0               # total vertical stagger between bowl centres = Ro
    top = -b - Ro; bot = b + Ro + tl
    dy = -(top + bot) / 2.0    # centre the pair vertically
    q = glyph_q(Ro, Ri, tl, rt).tf(T(-a + centre[0], -b + dy + centre[1]))
    p = glyph_p(Ro, Ri, tl, rt).tf(T(a + centre[0], b + dy + centre[1]))
    return [('mono-q', q, 'orange'), ('mono-p', p, 'blue')]


def bbox_of(items):
    bs = [pa.bbox() for _, pa, _ in items]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def transform_items(items, m):
    return [(n, p.tf(m), r) for n, p, r in items]
