// Builds one small page per artwork in p/<id>/index.html.
// WhatsApp reads these pages to show the artwork's photo and name in the order message,
// then the page sends the visitor to the artwork on the main site, with the chosen frame and size.
// Run after adding, renaming or removing an artwork:  node scripts/build-product-pages.mjs

import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const html = readFileSync(join(root, 'index.html'), 'utf8');

const start = html.indexOf('/* =====================================================\n   MY DUBAI ARTS — SETTINGS AND PRODUCTS');
const end = html.indexOf('/* ===== Site logic (no need to edit below) ===== */');
if (start < 0 || end < 0) throw new Error('Could not find the settings block in index.html');
const { SITE_URL, PRODUCTS, COLLECTIONS, FRAME_PRICES, FRAME_COLOURS, SIZES } = new Function(
  `${html.slice(start, end)}\nreturn { SITE_URL, PRODUCTS, COLLECTIONS, FRAME_PRICES, FRAME_COLOURS, SIZES };`
)();

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fromPrice = (p) => ((COLLECTIONS.find((c) => c.id === p.category) || {}).price
  ?? Math.min(...[...FRAME_COLOURS, ...p.frames].map((f) => FRAME_PRICES[f] ?? Infinity)))
  + Math.min(...SIZES.filter((s) => !p.sizes || p.sizes.includes(s.name)).map((s) => s.extra));

const outDir = join(root, 'p');
const ids = new Set(PRODUCTS.map((p) => p.id));
if (existsSync(outDir)) {
  for (const d of readdirSync(outDir)) if (!ids.has(d)) rmSync(join(outDir, d), { recursive: true });
}

for (const p of PRODUCTS) {
  const title = `${p.name} | My Dubai Arts`;
  const pr = fromPrice(p);
  const desc = `${p.description}${Number.isFinite(pr) ? ` From AED ${pr}.` : ''}`;
  const image = p.photos.length ? `${SITE_URL}/images/${p.photos[0][0]}` : `${SITE_URL}/images/art/${p.id}.jpg`;
  const target = `/?product=${encodeURIComponent(p.id)}`;
  const page = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="My Dubai Arts">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:image" content="${esc(image)}">
<meta property="og:url" content="${esc(`${SITE_URL}/p/${p.id}/`)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${esc(`${SITE_URL}${target}`)}">
<script>location.replace(${JSON.stringify(target)} + location.search.replace(/^\\?/, '&'));</script>
</head>
<body>
<p><a href="${esc(target)}">View ${esc(p.name)} on My Dubai Arts</a></p>
</body>
</html>
`;
  mkdirSync(join(outDir, p.id), { recursive: true });
  writeFileSync(join(outDir, p.id, 'index.html'), page);
}

console.log(`Built ${PRODUCTS.length} product pages in p/`);
