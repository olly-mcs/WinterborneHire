// Makes the web copies of the Bespoke Florals product photos.
// For every photo in images/bespoke-florals/<type>/originals/, writes <type>/<name>-600.webp and <name>-1200.webp
// (never enlarged), skipping copies that already exist. Pages use the copies; the originals are kept as the archive.
// Needs sharp:  npm install --no-save sharp  then  node scripts/resize-bespoke-images.mjs
import fs from "node:fs";
import path from "node:path";
import sharp from "sharp";

const root = path.join(path.dirname(new URL(import.meta.url).pathname), "..", "images", "bespoke-florals");
let made = 0;
for (const type of fs.readdirSync(root)) {
  const originals = path.join(root, type, "originals");
  if (!fs.existsSync(originals)) continue;
  for (const file of fs.readdirSync(originals)) {
    if (!/\.(jpe?g|png|webp)$/i.test(file)) continue;
    const name = file.replace(/\.[^.]+$/, "");
    for (const width of [600, 1200]) {
      const out = path.join(root, type, `${name}-${width}.webp`);
      if (fs.existsSync(out)) continue;
      await sharp(path.join(originals, file)).rotate().resize({ width, withoutEnlargement: true }).webp({ quality: 80 }).toFile(out);
      made++;
    }
  }
}
console.log(`made ${made} web copies`);
