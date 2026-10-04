// Floral palette helper for the add-testimonial skill.
// Usage: node .claude/skills/add-testimonial/palette.js <folder-under-images> <file>:<x0>,<y0>,<x1>,<y1> [...]
// Regions are fractions of the image (0-1) that cover only flowers. Needs the site served at
// http://127.0.0.1:8099 (python3 -m http.server 8099 from the repo root works) and Playwright.
const { execSync } = require("child_process");
const { chromium } = require(execSync("npm root -g").toString().trim() + "/playwright");

const [folder, ...specs] = process.argv.slice(2);
const regions = specs.map((s) => {
  const [file, box] = s.split(":");
  return [file, box.split(",").map(Number)];
});

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("http://127.0.0.1:8099/404");
  const result = await page.evaluate(async ({ folder, regions }) => {
    const px = [];
    for (const [file, [x0, y0, x1, y1]] of regions) {
      const img = new Image();
      img.src = `/images/${folder}/${file}`;
      await img.decode();
      const c = document.createElement("canvas");
      c.width = img.width;
      c.height = img.height;
      const ctx = c.getContext("2d");
      ctx.drawImage(img, 0, 0);
      const d = ctx.getImageData(x0 * img.width, y0 * img.height, (x1 - x0) * img.width, (y1 - y0) * img.height).data;
      for (let i = 0; i < d.length; i += 8) {
        const r = d[i], g = d[i + 1], b = d[i + 2], mx = Math.max(r, g, b), mn = Math.min(r, g, b);
        const v = mx / 255, s = mx ? (mx - mn) / mx : 0;
        if (s > 0.15 && v > 0.18 && v < 0.98) px.push([r, g, b]); // skip whites, greys and shadows
      }
    }
    const K = 9;
    let C = Array.from({ length: K }, (_, k) => px[Math.floor((k * px.length) / K)].slice());
    for (let it = 0; it < 25; it++) {
      const S = C.map(() => [0, 0, 0, 0]);
      for (const q of px) {
        let bi = 0, bd = Infinity;
        C.forEach((c, k) => { const dd = (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2 + (q[2] - c[2]) ** 2; if (dd < bd) { bd = dd; bi = k; } });
        S[bi][0] += q[0]; S[bi][1] += q[1]; S[bi][2] += q[2]; S[bi][3]++;
      }
      C = S.map((s, k) => (s[3] ? [s[0] / s[3], s[1] / s[3], s[2] / s[3], s[3]] : C[k]));
    }
    const hex = (c) => "#" + c.slice(0, 3).map((v) => Math.round(v).toString(16).padStart(2, "0")).join("").toUpperCase();
    return C.sort((a, b) => b[3] - a[3]).map((c) => `${hex(c)}  ${((100 * c[3]) / px.length).toFixed(1)}%`);
  }, { folder, regions });
  console.log(result.join("\n"));
  await browser.close();
})();
