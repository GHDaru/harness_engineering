// Gera o PDF do livro a partir do site já construído (docs/).
// Uso: node build.mjs && node pdf.mjs   -> docs/engenharia-de-harness.pdf
// Concatena as páginas na ordem do sumário (capa + capítulos + aparato),
// aplica CSS de impressão e imprime via Chromium (Playwright).
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const DOCS = resolve(RAIZ, "docs");
const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const slugDe = (a) => basename(a).replace(/\.md$/, "").toLowerCase();

// versão (mesma lógica do build)
const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
const mv = hist.match(/^###\s+Edição\s+(\d+)\.(\d+)/m);
const versao = mv ? `v${mv[1]}.${mv[2]}.0` : "v0.0.0";
const dataStr = new Intl.DateTimeFormat("pt-BR", { dateStyle: "long" }).format(new Date());

const extrair = (slug) => {
  const f = resolve(DOCS, slug + ".html");
  if (!existsSync(f)) return null;
  const html = readFileSync(f, "utf8");
  const m = html.match(/<article class="markdown">([\s\S]*?)<\/article>/);
  return m ? m[1] : null;
};

let corpo = "";
for (const parte of sumario.partes) {
  corpo += `<h1 class="parte">${parte.nome}</h1>`;
  for (const item of parte.itens) {
    const c = extrair(slugDe(item.arquivo));
    if (c) corpo += `<section class="cap">${c}</section>`;
  }
}

const pagina = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
  @page { size: A4; margin: 22mm 18mm; }
  body { font: 11pt/1.55 Georgia, 'Times New Roman', serif; color: #1a1a1a; margin: 0; }
  .capa-pdf { text-align: center; page-break-after: always; padding-top: 30mm; }
  .capa-pdf img { width: 78mm; border-radius: 3mm; box-shadow: 0 4mm 10mm rgba(0,0,0,.25); }
  .capa-pdf h1 { font-size: 26pt; margin: 12mm 0 3mm; }
  .capa-pdf .sub { font-size: 12pt; color: #555; }
  .capa-pdf .meta { margin-top: 14mm; font-size: 10pt; color: #666; }
  h1.parte { page-break-before: always; font-size: 20pt; border-bottom: 2px solid #b06d0f; padding-bottom: 3mm; }
  section.cap { page-break-before: always; }
  section.cap h1 { font-size: 17pt; }
  h2 { font-size: 13.5pt; margin-top: 8mm; }
  h3 { font-size: 11.5pt; }
  a { color: #1a5fb4; text-decoration: none; }
  .header-anchor { display: none; }
  pre { background: #f4f4f2; border: 1px solid #ddd; border-radius: 2mm; padding: 3mm; font-size: 8.5pt; white-space: pre-wrap; word-wrap: break-word; }
  code { background: #f4f4f2; font-size: .92em; padding: 0 .3mm; }
  table { border-collapse: collapse; width: 100%; font-size: 9pt; page-break-inside: avoid; }
  th, td { border: 1px solid #ccc; padding: 1.6mm 2.2mm; text-align: left; }
  th { background: #efefec; }
  img { max-width: 100%; }
  blockquote { border-left: 3px solid #ccc; margin: 4mm 0; padding: 1mm 4mm; color: #555; }
  .selo-data, [data-viz] { display: none; }
  figure { margin: 5mm 0; text-align: center; } figcaption { font-size: 9pt; color: #666; }
  abbr { text-decoration: none; }
</style></head><body>
<div class="capa-pdf">
  <img src="${resolve(DOCS, "assets/capa.png")}" alt="Capa">
  <h1>${sumario.titulo}</h1>
  <div class="sub">${sumario.subtitulo}</div>
  <div class="meta">Gilsiley Henrique Darú · com co-autoria de IA (Claude, Anthropic)<br>
  ${versao} · gerado em ${dataStr}<br>DOI 10.5281/zenodo.21632412 · ghdaru.github.io/harness_engineering</div>
</div>
${corpo}
</body></html>`;

const tmp = resolve(DOCS, "_livro-print.html");
writeFileSync(tmp, pagina);

const playwright = await import(process.env.PLAYWRIGHT_LIB || "playwright");
const browser = await (playwright.default || playwright).chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + tmp, { waitUntil: "networkidle" });
await page.pdf({ path: resolve(DOCS, "engenharia-de-harness.pdf"), format: "A4",
  printBackground: true, displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate: `<div style="width:100%;text-align:center;font-size:8px;color:#888;">Engenharia de Harness · ${versao} — <span class="pageNumber"></span>/<span class="totalPages"></span></div>`,
  margin: { top: "22mm", bottom: "18mm", left: "18mm", right: "18mm" } });
await browser.close();
console.log("✓ PDF gerado: docs/engenharia-de-harness.pdf");
