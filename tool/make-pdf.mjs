// renders one volume to pdf with chrome.
// usage: node tool/make-pdf.mjs <author-folder> <volume>
// needs: chrome, ghostscript (gs), poppler (pdfinfo). run tool/build.py first.
//
// writes <author>/pdfs/<n>-<theme>/:
//   read.pdf           cover to cover, for reading on a screen
//   ereader.pdf        a5, no spreads, for a kindle / tablet
//   print-odd.pdf      pass 1 on a printer that doesn't flip paper
//   print-even.pdf     pass 2
//   print-duplex.pdf   the inside pages in one file, for a printer that does
//   cover-front.pdf    one sheet of card or photo paper
//   cover-back.pdf     one sheet
import { chromium } from "playwright-core";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";
import http from "node:http";
import { execFile } from "node:child_process";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);
const [author, volume] = process.argv.slice(2);
if (!author || !volume) { console.error("usage: node tool/make-pdf.mjs <author-folder> <volume>"); process.exit(1); }

const rootDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const authorDir = path.join(rootDir, author);
const buildDir = path.join(authorDir, ".build");
const name = (await fs.readFile(path.join(buildDir, "name.txt"), "utf8")).trim();
const outputDir = path.join(authorDir, "pdfs", name);
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
    const requestedPath = path.resolve(rootDir, pathname.slice(1));
    if (!requestedPath.startsWith(`${rootDir}${path.sep}`)) { response.writeHead(403).end(); return; }
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
  await page.goto(`http://127.0.0.1:${port}/${author}/.build/${file}`, { waitUntil: "load" });
  await page.waitForFunction(() => document.body.dataset.rendered === "true", null, { timeout: 180000 });
  await page.evaluate(() => document.fonts.ready);
  const expected = await page.locator(".pagedjs_page").count();
  const raw = out.replace(/\.pdf$/, ".raw.pdf");
  await page.pdf({ path: raw, printBackground: true, preferCSSPageSize: true,
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
  const inside = path.join(outputDir, `print-duplex.pdf`);
  const n = await render(browser, "book.html", inside);
  const total = await pages(inside);
  // pad to an even count so the last sheet has a defined back
  if (total % 2 === 1) {
    await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
      `-sOutputFile=${inside}.tmp`, "-c", "<</PageSize [595.28 841.89]>> setpagedevice", "-f", inside, "-c", "showpage"]);
    await fs.rename(`${inside}.tmp`, inside);
  }
  const finalCount = await pages(inside);
  await gs(inside, path.join(outputDir, `print-odd.pdf`), "odd");
  await gs(inside, path.join(outputDir, `print-even.pdf`), "even");
  console.log(`inside: ${finalCount} pages = ${finalCount / 2} sheets of paper`);

  const cover = path.join(outputDir, `.cover.pdf`);
  await render(browser, "cover.html", cover);
  await gs(cover, path.join(outputDir, `cover-front.pdf`), "1");
  await gs(cover, path.join(outputDir, `cover-back.pdf`), "2");
  console.log(`cover: front + back, 2 sheets of photo paper`);

  // preview = the physical object: front cover, its blank inside, the pages, the blank inside of the back cover, back cover.
  // view it two-up with "cover page" on and the spreads match the book.
  const blank = path.join(outputDir, ".blank.pdf");
  await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite", `-sOutputFile=${blank}`,
    "-c", "<</PageSize [595.28 841.89]>> setpagedevice showpage"]);
  await execFileAsync("gs", ["-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=pdfwrite",
    `-sOutputFile=${path.join(outputDir, `read.pdf`)}`,
    path.join(outputDir, `cover-front.pdf`), blank, inside, blank,
    path.join(outputDir, `cover-back.pdf`)]);
  await fs.unlink(blank); await fs.unlink(cover);
  console.log(`read.pdf: cover + blank + ${finalCount} pages + blank + cover`);

  const ereader = path.join(outputDir, `ereader.pdf`);
  const n2 = await render(browser, "book-ereader.html", ereader);
  console.log(`ereader.pdf: ${n2} a5 pages`);
  console.log(`→ ${path.relative(rootDir, outputDir)}/`);
} finally {
  await browser.close();
  await new Promise((resolve) => server.close(resolve));
}
