// renders book.html and cover.html to pdf with chrome, then splits the
// inside pages into odd/even files for manual duplex on a printer that
// doesn't flip paper by itself. needs: chrome, ghostscript (gs), poppler (pdfinfo).
//
// outputs in output/:
//   vol1-inside.pdf        everything, for reading on screen
//   vol1-inside-odd.pdf    pass 1: odd pages (fronts)
//   vol1-inside-even.pdf   pass 2: even pages (backs)
//   vol1-cover-front.pdf   photo paper
//   vol1-cover-back.pdf    photo paper
import { chromium } from "playwright-core";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";
import http from "node:http";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const volume = process.argv[2] ?? "1";   // usage: node make-pdf.mjs <volume> [name-suffix]

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(scriptDir, "..");
const outputDir = path.join(projectDir, "output");
const suffix = process.argv[3] ? `-${process.argv[3]}` : "";
const chromeCandidates = [
  process.env.CHROME_PATH,
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser",
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
].filter(Boolean);
let chromePath;
for (const c of chromeCandidates) { try { await fs.access(c); chromePath = c; break; } catch {} }
if (!chromePath) { console.error("no chrome found. install google chrome or set CHROME_PATH."); process.exit(1); }
await fs.mkdir(outputDir, { recursive: true });

const contentTypes = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8", ".woff2": "font/woff2",
};
const server = http.createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    const requestedPath = path.resolve(projectDir, pathname === "/" ? "book.html" : pathname.slice(1));
    if (!requestedPath.startsWith(`${projectDir}${path.sep}`)) { response.writeHead(403).end(); return; }
    const body = await fs.readFile(requestedPath);
    response.writeHead(200, { "content-type": contentTypes[path.extname(requestedPath)] ?? "application/octet-stream" });
    response.end(body);
  } catch { response.writeHead(404).end("not found"); }
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();

async function pages(pdf) {
  const { stdout } = await execFileAsync("pdfinfo", [pdf]);
  return Number(stdout.match(/^Pages:\s+(\d+)$/m)?.[1]);
}
async function gs(input, output, pageList) {
  await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
    `-sOutputFile=${output}`, `-sPageList=${pageList}`, input]);
}

async function render(browser, file, out) {
  const page = await browser.newPage({ viewport: { width: 1400, height: 1100 } });
  page.on("pageerror", (e) => console.error(`page error: ${e.message}`));
  await page.goto(`http://127.0.0.1:${port}/${file}`, { waitUntil: "load" });
  await page.waitForFunction(() => document.body.dataset.rendered === "true", null, { timeout: 180000 });
  await page.evaluate(() => document.fonts.ready);
  const expected = await page.locator(".pagedjs_page").count();
  const raw = out.replace(/\.pdf$/, ".raw.pdf");
  await page.pdf({ path: raw, format: "A4", printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: false, margin: { top: "0", right: "0", bottom: "0", left: "0" } });
  await page.close();
  // chrome adds a blank sheet after the first named page and one at the end
  // when printing an already-paginated document. drop that known pair.
  const got = await pages(raw);
  if (got === expected + 2) {
    await gs(raw, out, `1,3-${got - 1}`);
    await fs.unlink(raw);
  } else if (got === expected) {
    await fs.rename(raw, out);
  } else {
    await fs.rename(raw, out);
    console.warn(`${file}: expected ${expected} pages, chrome produced ${got}. check the pdf.`);
  }
  return expected;
}

const browser = await chromium.launch({ executablePath: chromePath, headless: true });
try {
  const inside = path.join(outputDir, `vol${volume}${suffix}-inside.pdf`);
  const n = await render(browser, "book.html", inside);
  const total = await pages(inside);
  // pad to an even count so the last sheet has a defined back
  if (total % 2 === 1) {
    await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
      `-sOutputFile=${inside}.tmp`, "-c", "<</PageSize [595.28 841.89]>> setpagedevice", "-f", inside, "-c", "showpage"]);
    await fs.rename(`${inside}.tmp`, inside);
  }
  const finalCount = await pages(inside);
  await gs(inside, path.join(outputDir, `vol${volume}${suffix}-inside-odd.pdf`), "odd");
  await gs(inside, path.join(outputDir, `vol${volume}${suffix}-inside-even.pdf`), "even");
  console.log(`inside: ${finalCount} pages = ${finalCount / 2} sheets of paper`);

  const cover = path.join(outputDir, `vol${volume}${suffix}-cover.pdf`);
  await render(browser, "cover.html", cover);
  await gs(cover, path.join(outputDir, `vol${volume}${suffix}-cover-front.pdf`), "1");
  await gs(cover, path.join(outputDir, `vol${volume}${suffix}-cover-back.pdf`), "2");
  console.log(`cover: front + back, 2 sheets of photo paper`);

  // preview = the physical object: front cover, its blank inside, the pages, the blank inside of the back cover, back cover.
  // view it two-up with "cover page" on and the spreads match the book.
  const blank = path.join(outputDir, ".blank.pdf");
  await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite", `-sOutputFile=${blank}`,
    "-c", "<</PageSize [595.28 841.89]>> setpagedevice showpage"]);
  await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
    `-sOutputFile=${path.join(outputDir, `vol${volume}${suffix}-preview.pdf`)}`,
    path.join(outputDir, `vol${volume}${suffix}-cover-front.pdf`), blank, inside, blank,
    path.join(outputDir, `vol${volume}${suffix}-cover-back.pdf`)]);
  await fs.unlink(blank);
  console.log(`preview: cover + blank + ${finalCount} pages + blank + cover`);
  console.log(`wrote to ${outputDir}`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
