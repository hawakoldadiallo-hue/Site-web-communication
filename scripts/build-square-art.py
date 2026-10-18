# Builds images/art/square/<id>.jpg (100 x 100 cm previews).
# Most artworks: centred square crop. PAD artworks: kept whole, background extended on the short sides.
import os, sys
from PIL import Image, ImageDraw
import numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'art'))
PAD = {'boss-lady-mood','manifest-your-dreams','never-stop-pushing','new-era-of-me','golden-stiletto','gloss-lips-duo',
       'crimson-wave','pink-night-drive','rose-on-heels','sage-peach-drip'}
ALIGN = {'burj-al-arab-shore': 0.0}  # crop position for centred crops: 0 = keep the top, 0.5 = centre, 1 = keep the bottom
ONE_COLOUR = {'golden-stiletto': 'l'}  # fill both sides with this edge's colour
def edge(a, side, n):
    strip = {'l': a[:, :n], 'r': a[:, -n:], 't': a[:n], 'b': a[-n:]}[side]
    return tuple(int(v) for v in np.median(strip.reshape(-1, 3), axis=0))
fs = sorted(f for f in os.listdir('.') if f.endswith('.jpg'))
for f in fs:
    im = Image.open(f).convert('RGB'); w, h = im.size; pid = f[:-4]
    if pid in PAD:
        s = max(w, h); a = np.asarray(im); n = max(2, int(min(w, h) * 0.02))
        sq = Image.new('RGB', (s, s))
        if h >= w:
            off = (s - w) // 2
            cl = edge(a, ONE_COLOUR.get(pid, 'l'), n); cr = edge(a, ONE_COLOUR.get(pid, 'r'), n)
            sq.paste(cl, (0, 0, off, s)); sq.paste(cr, (off + w, 0, s, s)); sq.paste(im, (off, 0))
        else:
            off = (s - h) // 2
            sq.paste(edge(a, 't', n), (0, 0, s, off)); sq.paste(edge(a, 'b', n), (0, off + h, s, s)); sq.paste(im, (0, off))
    else:
        s = min(w, h); k = ALIGN.get(pid, 0.5)
        x0 = int((w - s) * (k if w > h else 0.5)); y0 = int((h - s) * (k if h > w else 0.5))
        sq = im.crop((x0, y0, x0 + s, y0 + s))
    sq.thumbnail((1100, 1100)); sq.save('square/' + f, quality=88, optimize=True, progressive=True)
    t = sq.copy(); t.thumbnail((420, 420)); t.save('square/thumbs/' + f, quality=80, optimize=True, progressive=True)
print(len(fs))
