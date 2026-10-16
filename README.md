# My Dubai Arts

Website for [mydubaiarts.online](https://mydubaiarts.online): framed wall art delivered across the UAE.

- `index.html` holds the whole site. Products, collections and frame prices are in the settings block at the top of the script.
- `images/` holds the product photos, and `images/thumbs/` their smaller versions.
- `p/<id>/` holds one small page per artwork, used by the WhatsApp order links so the message shows the artwork's photo and opens it with the chosen frame and size. Rebuild them after adding, renaming or removing an artwork: `node scripts/build-product-pages.mjs`.

Every push to `main` is published automatically by Vercel.
