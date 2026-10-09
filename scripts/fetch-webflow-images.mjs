// Saves every image listed in data/webflow-content.json from Webflow's CDN into images/webflow/,
// so nothing is lost when the Webflow site is switched off. Skips images already saved.
// Usage: node scripts/fetch-webflow-images.mjs   (then: python3 scripts/build-webflow-content.py)
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const data = JSON.parse(fs.readFileSync(path.join(root, "data/webflow-content.json"), "utf8"));

const images = [];
for (const list of Object.values(data)) {
  for (const item of list) {
    for (const key of ["image", "hover"]) if (item[key]) images.push(item[key]);
  }
}

let saved = 0, skipped = 0;
const failed = [];
for (const img of images) {
  const dest = path.join(root, img.file);
  if (fs.existsSync(dest)) { skipped++; continue; }
  try {
    const res = await fetch(img.src);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.writeFileSync(dest, buf);
    saved++;
    console.log(`saved ${img.file} (${Math.round(buf.length / 1024)} KB)`);
  } catch (err) {
    failed.push(`${img.src} -> ${err.message}`);
  }
}
console.log(`\n${saved} saved, ${skipped} already saved, ${failed.length} failed`);
if (failed.length) console.log("Failed:\n" + failed.join("\n"));
process.exitCode = failed.length && !saved && !skipped ? 1 : 0;
