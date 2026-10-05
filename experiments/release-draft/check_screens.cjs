// Screenshots of every finding of check_display.py, from the running map viewer (http://localhost:5199), for review.
// Needs Playwright with a Chromium build: PLAYWRIGHT=/path/to/node_modules/playwright (default: Track Your Regions').
// Run from the repository root:  node experiments/release-draft/check_screens.cjs [max]
const path = require("path");
const fs = require("fs");
const { chromium } = require(process.env.PLAYWRIGHT || path.resolve(__dirname, "../../../track-your-regions/frontend/node_modules/playwright"));

(async () => {
  const out = path.join(__dirname, "cache", "map", "screens");
  fs.mkdirSync(out, { recursive: true });
  const check = JSON.parse(fs.readFileSync(path.join(__dirname, "cache", "map", "display_check.json"), "utf8"));
  const todo = check.findings.filter((f) => f.visible && !f.explained)
    .sort((a, b) => (b.km2 ?? 1) - (a.km2 ?? 1)).slice(0, Number(process.argv[2] || 60));
  const browser = await chromium.launch({ args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
  const page = await browser.newPage({ viewport: { width: 900, height: 700 } });
  await page.goto("http://localhost:5199/");
  await page.waitForFunction(() => /Click a region/.test(document.getElementById("summary")?.textContent ?? ""), null, { timeout: 300000 });
  for (const [i, f] of todo.entries()) {
    const [x0, y0, x1, y1] = f.box;
    await page.evaluate(([x0, y0, x1, y1]) => window.map.fitBounds([[x0, y0], [x1, y1]], { duration: 0, padding: 20 }), [x0, y0, x1, y1]);
    await page.evaluate(() => new Promise((r) => window.map.once("idle", r)));
    const name = `${String(i).padStart(3, "0")}-${f.check}-${(f.region || f.between?.join("+") || "").replace(/[^a-z0-9]+/gi, "_")}.png`;
    await page.screenshot({ path: path.join(out, name) });
    console.log(name);
  }
  await browser.close();
})().catch((e) => { console.error(e.message); process.exit(1); });
