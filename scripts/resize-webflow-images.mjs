// Makes web-sized WebP copies of the saved Webflow images (images/webflow/) in images/webflow-sized/:
// <name>-600.webp for grids and cards, <name>-1200.webp for product pages. Originals are left untouched.
// Never enlarges an image; skips copies that already exist.
// Needs sharp:  npm install --no-save sharp  then  node scripts/resize-webflow-images.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import sharp from "sharp";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const src = path.join(root, "images/webflow");
const out = path.join(root, "images/webflow-sized");
const WIDTHS = [600, 1200];

let made = 0, before = 0, after = 0;
for (const dir of fs.readdirSync(src)) {
  for (const file of fs.readdirSync(path.join(src, dir))) {
    const input = path.join(src, dir, file);
    const stem = file.replace(/\.[^.]+$/, "");
    for (const w of WIDTHS) {
      const dest = path.join(out, dir, `${stem}-${w}.webp`);
      if (fs.existsSync(dest)) continue;
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      await sharp(input).rotate().resize({ width: w, withoutEnlargement: true }).webp({ quality: 80 }).toFile(dest);
      made++;
      after += fs.statSync(dest).size;
    }
    before += fs.statSync(input).size;
  }
}
console.log(`${made} copies made. Originals ${Math.round(before / 1048576)} MB; new copies ${Math.round(after / 1048576)} MB`);
