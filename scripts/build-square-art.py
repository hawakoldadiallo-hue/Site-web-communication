# Builds images/art/square/<id>.jpg (100 x 100 cm previews).
# Most artworks: centred square crop. PAD artworks: kept whole, background extended on the short sides.
import os, sys
from PIL import Image, ImageDraw
import numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'art'))
PAD = set()  # every square fills the frame completely (centred crop)
BLUR = set()  # kept whole, sides filled with a soft blurred copy of the artwork
ALIGN = {'discipline-creates-freedom': 0.0, 'better-version-of-me': 0.0, 'pink-champagne-moment': 0.62, 'good-things-take-time': 0.0, 'more-amour-please': 0.0, 'parisian-rouge': 0.0, 'burj-al-arab-shore': 0.0, 'paris-by-night': 0.05, 'boss-lady-mood': 0.0, 'manifest-your-dreams': 0.0, 'never-stop-pushing': 0.0, 'its-you-vs-you': 0.85, 'golden-fairy': 0.2}
# Text that is taller (or wider) than a square crop: take a slightly larger square and fill the short sides with a mirrored copy of the artwork's own edge, so the frame is still completely filled
# Square artworks: the Extra Large square uses this original file instead of a crop of the 5:7 version
SQUARE_SOURCE = {'throw-stones-build-castles': 'images/art/source/throw-stones-build-castles-square.jpg', 'find-your-spark': 'images/art/source/find-your-spark-square.jpg', 'chosen-clearly': 'images/art/source/chosen-clearly-square.jpg', 'todays-dreams': 'images/art/source/todays-dreams-square.jpg'}
MIRROR = {'new-era-of-me': 1.14, 'where-is-my-bag': 1.12, 'one-percent-better': 1.13}  # crop position for centred crops: 0 = keep the top, 0.5 = centre, 1 = keep the bottom
ONE_COLOUR = {'golden-stiletto': 'l'}  # fill both sides with this edge's colour
def edge(a, side, n):
    strip = {'l': a[:, :n], 'r': a[:, -n:], 't': a[:n], 'b': a[-n:]}[side]
    return tuple(int(v) for v in np.median(strip.reshape(-1, 3), axis=0))
fs = sorted(f for f in os.listdir('.') if f.endswith('.jpg'))
for f in fs:
    im = Image.open(f).convert('RGB'); w, h = im.size; pid = f[:-4]
    if pid in SQUARE_SOURCE:
        sq = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', SQUARE_SOURCE[pid])).convert('RGB')
    elif pid in MIRROR:
        import numpy as np
        short, long_ = min(w, h), max(w, h)
        s = min(long_, round(short * MIRROR[pid])); pad = s - short
        a = np.asarray(im)
        if h >= w:
            y0 = (h - s) // 2; a = a[y0:y0 + s]
            l, r = pad // 2, pad - pad // 2
            a = np.concatenate([a[:, :l][:, ::-1], a, a[:, -r:][:, ::-1] if r else a[:, :0]], axis=1)
        else:
            x0 = (w - s) // 2; a = a[:, x0:x0 + s]
            tp, bt = pad // 2, pad - pad // 2
            a = np.concatenate([a[:tp][::-1], a, a[-bt:][::-1] if bt else a[:0]], axis=0)
        sq = Image.fromarray(a)
    elif pid in BLUR:
        from PIL import ImageFilter, ImageEnhance
        s = max(w, h); k = s / min(w, h)
        bg = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
        bg = bg.crop(((bg.width - s) // 2, (bg.height - s) // 2, (bg.width - s) // 2 + s, (bg.height - s) // 2 + s))
        bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(s * 0.04))).enhance(0.92)
        bg.paste(im, ((s - w) // 2, (s - h) // 2)); sq = bg
    elif pid in PAD:
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
