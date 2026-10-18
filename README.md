# My Dubai Arts

Website for [mydubaiarts.online](https://mydubaiarts.online): framed wall art delivered across the UAE.

- `index.html` holds the whole site. Products, collections and frame prices are in the settings block at the top of the script.
- `images/` holds the product photos, and `images/thumbs/` their smaller versions.
- `images/art/<id>.jpg` holds a flat, straightened image of each artwork (and `images/art/thumbs/` a small version). The site puts it in a black, gold or white frame for the frame colour previews. Every new artwork needs one.
- `images/art/square/` holds square versions shown for the Extra Large 100 x 100 cm size. Rebuild them after adding artworks: `python3 scripts/build-square-art.py` (needs Pillow and numpy).
- `p/<id>/` holds one small page per artwork, used by the WhatsApp order links so the message shows the artwork's photo and opens it with the chosen frame and size. Rebuild them after adding, renaming or removing an artwork: `node scripts/build-product-pages.mjs`.

Every push to `main` is published automatically by Vercel.

The site is in English and French. French shows automatically for visitors whose phone is in French, or with `?lang=fr` (for example `https://mydubaiarts.online/?lang=fr`). French texts for collections, artwork descriptions, frames and sizes are in the `FR` block of the settings in `index.html`.
