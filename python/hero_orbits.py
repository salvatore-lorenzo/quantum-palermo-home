"""Orbits behind the title of the home page, drawn like the qunipa logo mark: concentric arcs
cut into a few long segments; a segment ends in a small hollow ring, in a short radial step to
the next arc, or plainly. Colours are set by the CSS (currentColor and --orbit-accent).

usage: python3 python/hero_orbits.py OUT.svg SEED RADII NODE

The three images in assets/images/hero/ were made with
    python3 python/hero_orbits.py assets/images/hero/orbit-large.svg 14 70,135,200,265 18
    python3 python/hero_orbits.py assets/images/hero/orbit-medium.svg 13 70,135,200,265 18
    python3 python/hero_orbits.py assets/images/hero/orbit-small.svg 22 45,90,135 13
Another SEED gives another drawing with the same style.
"""
import math, random, sys

out, seed = sys.argv[1], int(sys.argv[2])
radii = [float(r) for r in sys.argv[3].split(",")]
rings = len(radii)
NODE = float(sys.argv[4])   # ring radius (viewBox units)
random.seed(seed)
SW = 2.5              # stroke width (px, not scaled)
R = radii[-1] + NODE + 6

def pt(r, a):
    t = math.radians(a)
    return r * math.cos(t), r * math.sin(t)

# 1. arcs: each ring is cut into segments separated by gaps
arcs = []             # dict(k, a0, a1, col, ends={0: kind, 1: kind})
for k, r in enumerate(radii):
    n = random.choice((1, 2, 2, 2, 3)) if k else 1
    gaps = [random.uniform(22, 48) for _ in range(n)]
    cuts = sorted(random.uniform(0.25, 0.75) for _ in range(n - 1))
    total = 360 - sum(gaps)
    bounds = [0] + [c * total for c in cuts] + [total]
    start, used = random.uniform(0, 360), 0.0
    for i in range(n):
        seg = bounds[i + 1] - bounds[i]
        a0 = start + used
        col = "b" if random.random() < 0.4 else "a"
        arcs.append(dict(k=k, a0=a0, a1=a0 + seg, col=col, ends={0: None, 1: None}))
        used += seg + gaps[i]

def covering(k, a, margin):
    for arc in arcs:
        if arc["k"] != k:
            continue
        lo, hi = arc["a0"] + margin, arc["a1"] - margin
        x = (a - lo) % 360
        if x <= (hi - lo) and hi > lo:
            return arc
    return None

# 2. steps: an arc end joins the arc on the next ring, which takes its colour
steps = []
for arc in arcs:
    for e, a in ((0, arc["a0"]), (1, arc["a1"])):
        if random.random() < 0.22:
            for dk in random.sample((-1, 1), 2):
                tgt = covering(arc["k"] + dk, a, 8) if 0 <= arc["k"] + dk < rings else None
                if tgt:
                    tgt["col"] = arc["col"]
                    arc["ends"][e] = "step"
                    steps.append((radii[arc["k"]], radii[tgt["k"]], a, arc["col"]))
                    break

# 3. rings on some of the free ends
for arc in arcs:
    for e in (0, 1):
        if arc["ends"][e] is None and random.random() < 0.62:
            arc["ends"][e] = "node"

paths = {"a": [], "b": []}
nodes = {"a": [], "b": []}
for arc in arcs:
    r = radii[arc["k"]]
    trim = math.degrees(NODE / r)
    a0 = arc["a0"] + (trim if arc["ends"][0] == "node" else 0)
    a1 = arc["a1"] - (trim if arc["ends"][1] == "node" else 0)
    (x0, y0), (x1, y1) = pt(r, a0), pt(r, a1)
    paths[arc["col"]].append(f'<path d="M{x0:.1f} {y0:.1f}A{r:.0f} {r:.0f} 0 {int(a1 - a0 > 180)} 1 {x1:.1f} {y1:.1f}"/>')
    for e, a in ((0, arc["a0"]), (1, arc["a1"])):
        if arc["ends"][e] == "node":
            x, y = pt(r, a)
            nodes[arc["col"]].append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE}"/>')
for ra, rb, a, col in steps:
    (x0, y0), (x1, y1) = pt(ra, a), pt(rb, a)
    paths[col].append(f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}"/>')

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-R:.0f} {-R:.0f} {2 * R:.0f} {2 * R:.0f}" aria-hidden="true" focusable="false">',
       f'<g fill="none" stroke-width="{SW}" stroke-linecap="round" vector-effect="non-scaling-stroke">']
for col, stroke in (("a", "currentColor"), ("b", "var(--orbit-accent, #ff8a3d)")):
    svg.append(f'<g stroke="{stroke}" class="orbit-{col}">' + "".join(paths[col]) + "".join(nodes[col]) + "</g>")
svg.append("</g></svg>")
open(out, "w").write("\n".join(svg) + "\n")
print(out.rsplit("/", 1)[-1], len(arcs), "arcs", len(steps), "steps", sum(len(v) for v in nodes.values()), "rings")
