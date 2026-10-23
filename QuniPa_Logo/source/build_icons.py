import os, io, struct, cairosvg
from PIL import Image
from build_logo import *

def svg_for(layout, var='color', pad_frac=0.0, bg=None, square=None):
    items, size = finish(LAYOUTS[layout]())
    V = VARIANTS[var]; pal = {r: V[r] for r in ('blue', 'orange', 'ink')}
    if square:
        w, h = size; S_ = square; sc = S_ * (1 - 2 * pad_frac) / max(w, h)
        items = transform_items(items, compose(S(sc), T((S_ - w * sc) / 2, (S_ - h * sc) / 2)))
        size = (S_, S_)
    s = svg_string(items, size, pal, 'QuniPa', 'QuniPa icon')
    if bg:
        s = s.replace('<title', f'<rect width="100%" height="100%" fill="{bg}"/><title', 1)
    return s, size

def png_bytes(svg, px):
    return cairosvg.svg2png(bytestring=svg.encode(), output_width=px, output_height=px)

d = os.path.join(OUT, 'web-icons'); os.makedirs(d, exist_ok=True)

# favicon.svg (compact emblem, colour)
s, _ = svg_for('emblem-compact')
open(os.path.join(d, 'favicon.svg'), 'w').write(s)

# PNG ladder: monogram at 16, compact emblem at 32+  (transparent)
for px in (32, 48, 64, 96, 128, 180, 192, 256, 512):
    s, _ = svg_for('emblem-compact', square=px, pad_frac=0.0)
    open(os.path.join(d, f'icon-{px}.png'), 'wb').write(png_bytes(s, px))
s, _ = svg_for('monogram', square=16, pad_frac=0.0)
open(os.path.join(d, 'icon-16.png'), 'wb').write(png_bytes(s, 16))

# favicon.ico  (16 = monogram, 32 / 48 = compact emblem) – PNG-compressed ICO entries written by hand
entries = []
for px, lay in ((16, 'monogram'), (32, 'emblem-compact'), (48, 'emblem-compact')):
    s, _ = svg_for(lay, square=px, pad_frac=0.0)
    entries.append((px, png_bytes(s, px)))
hdr = struct.pack('<HHH', 0, 1, len(entries)); off = 6 + 16 * len(entries); dirs = b''; blob = b''
for px, data in entries:
    dirs += struct.pack('<BBBBHHII', px, px, 0, 0, 1, 32, len(data), off + len(blob)); blob += data
open(os.path.join(d, 'favicon.ico'), 'wb').write(hdr + dirs + blob)

# apple-touch-icon (opaque, 180) and social avatars (opaque, 1024)
s, _ = svg_for('emblem-compact', var='color', bg='#FFFFFF', square=180, pad_frac=0.14)
open(os.path.join(d, 'apple-touch-icon-180.png'), 'wb').write(png_bytes(s, 180))
s, _ = svg_for('emblem', var='color', bg='#FFFFFF', square=1024, pad_frac=0.17)
open(os.path.join(d, 'social-avatar_light_1024.png'), 'wb').write(png_bytes(s, 1024))
s, _ = svg_for('emblem', var='color-on-dark', bg='#0F1720', square=1024, pad_frac=0.17)
open(os.path.join(d, 'social-avatar_dark_1024.png'), 'wb').write(png_bytes(s, 1024))
print(sorted(os.listdir(d)))
# verify ico
im = Image.open(os.path.join(d, 'favicon.ico')); print('ico sizes', im.info.get('sizes'))
