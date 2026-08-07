// Gera os PDFs do livro a partir do site já construído (docs/):
//   docs/pdf/engenharia-de-harness.pdf  — livro completo (capa + tudo)
//   docs/pdf/<slug>.pdf                 — um por capítulo numerado (spec 045)
// Uso: node build.mjs && node pdf.mjs
// Nota (spec 043): o <article> das páginas de capítulo não tem mais <h1> nem
// blockquote de datação (foram para o cabeçalho C01) — aqui o título volta a
// ser injetado a partir do sumário, com a linha de datação extraída do herói.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const EN = process.env.LIVRO_LANG === "en";
const DOCS = resolve(RAIZ, EN ? "docs/en" : "docs");
const ASSETS = resolve(RAIZ, "docs/assets");
const PDFS = resolve(DOCS, "pdf");
mkdirSync(PDFS, { recursive: true });
const sumario = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.en.json" : "sumario.json"), "utf8"));
const slugDe = (a) => basename(a).replace(/\.md$/, "").toLowerCase();

// versão (mesma lógica do build)
const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
const mv = hist.match(/^###\s+Edição\s+(\d+)\.(\d+)/m);
const versao = mv ? `v${mv[1]}.${mv[2]}.0` : "v0.0.0";
const dataStr = new Intl.DateTimeFormat(EN ? "en-US" : "pt-BR", { dateStyle: "long" }).format(new Date());
const DOI = "10.5281/zenodo.21632412";

// Extrai o conteúdo e, quando houver, a linha de meta do cabeçalho C01.
function extrair(slug) {
  const f = resolve(DOCS, slug + ".html");
  if (!existsSync(f)) return null;
  const html = readFileSync(f, "utf8");
  const m = html.match(/<article class="markdown">([\s\S]*?)<\/article>/);
  if (!m) return null;
  const meta = (html.match(/<div class="cap-meta">([\s\S]*?)<\/div>/) || [])[1] || "";
  const chips = [...meta.matchAll(/<span[^>]*>([\s\S]*?)<\/span>/g)].map((x) => x[1].trim());
  return { corpo: m[1], meta: chips.join(" · ") };
}

const CSS = `
  @page { size: A4; margin: 22mm 18mm; }
  body { font: 11pt/1.55 Georgia, 'Times New Roman', serif; color: #1a1a1a; margin: 0; }
  .capa-pdf { text-align: center; page-break-after: always; padding-top: 30mm; }
  .capa-pdf img { width: 78mm; border-radius: 3mm; box-shadow: 0 4mm 10mm rgba(0,0,0,.25); }
  .capa-pdf h1 { font-size: 26pt; margin: 12mm 0 3mm; }
  .capa-pdf .sub { font-size: 12pt; color: #555; }
  .capa-pdf .meta { margin-top: 14mm; font-size: 10pt; color: #666; }
  h1.parte { page-break-before: always; font-size: 20pt; border-bottom: 2px solid #b06d0f; padding-bottom: 3mm; }
  section.cap { page-break-before: always; }
  section.cap:first-child, section.cap.solo { page-break-before: auto; }
  section.cap h1, h1.cap-t { font-size: 17pt; }
  .cap-meta-pdf { font-size: 9pt; color: #777; margin: 0 0 6mm; }
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
  .leitura-exec { background: #faf6ee; border: 1px solid #e3d9c4; border-left: 3px solid #b06d0f; border-radius: 2mm; padding: 3mm 4mm; }
  .leitura-exec h3 { font-size: 8.5pt; letter-spacing: .08em; text-transform: uppercase; color: #b06d0f; margin: 0 0 2mm; }
  figure { margin: 5mm 0; text-align: center; } figcaption { font-size: 9pt; color: #666; }
  abbr { text-decoration: none; }
`;

// Um capítulo -> seção com título (do sumário) + linha de datação do herói.
// (Páginas do aparato ainda trazem o próprio <h1> no corpo — não duplicar.)
function secao(item, solo = false) {
  const ext = extrair(slugDe(item.arquivo));
  if (!ext) return "";
  const temH1 = /^\s*<h1[\s>]/.test(ext.corpo);
  const cabeca = temH1 ? "" : `<h1 class="cap-t">${item.titulo}</h1>${ext.meta ? `<div class="cap-meta-pdf">${ext.meta}</div>` : ""}`;
  return `<section class="cap${solo ? " solo" : ""}">${cabeca}${ext.corpo}</section>`;
}

const docHtml = (corpo, capa) => `<!doctype html><html lang="${EN ? "en" : "pt-BR"}"><head><meta charset="utf-8">
<style>${CSS}</style></head><body>${capa}${corpo}</body></html>`;

// spec 089: o mesmo endereço do build, sem protocolo nem barra — é rodapé impresso.
const SITE_CURTO = (process.env.SITE_URL || "https://ghdaru.github.io/harness_engineering/")
  .replace(/^https?:\/\//, "").replace(/\/*$/, "");

const capaLivro = `<div class="capa-pdf">
  <img src="${resolve(ASSETS, "capa.png")}" alt="Capa">
  <h1>${sumario.titulo}</h1>
  <div class="sub">${sumario.subtitulo}</div>
  <div class="meta">Gilsiley Henrique Darú · ${EN ? "with AI co-authorship (Claude, Anthropic)" : "com co-autoria de IA (Claude, Anthropic)"}<br>
  ${versao} · ${EN ? "generated on" : "gerado em"} ${dataStr}<br>DOI ${DOI} · ${SITE_CURTO}</div>
</div>`;

const rodape = (rotulo) =>
  `<div style="width:100%;text-align:center;font-size:8px;color:#888;">${rotulo} · ${versao} — <span class="pageNumber"></span>/<span class="totalPages"></span></div>`;

const playwright = await import(process.env.PLAYWRIGHT_LIB || "playwright");
const browser = await (playwright.default || playwright).chromium.launch(process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {});
const page = await browser.newPage();

async function imprimir(html, saida, rotulo) {
  const tmp = resolve(DOCS, "_print.html");
  writeFileSync(tmp, html);
  await page.goto("file://" + tmp, { waitUntil: "networkidle" });
  await page.pdf({ path: saida, format: "A4", printBackground: true, displayHeaderFooter: true,
    headerTemplate: "<span></span>", footerTemplate: rodape(rotulo),
    margin: { top: "22mm", bottom: "18mm", left: "18mm", right: "18mm" } });
}

// 1) Livro completo
let corpo = "";
for (const parte of sumario.partes) {
  corpo += `<h1 class="parte">${parte.nome}</h1>`;
  for (const item of parte.itens) { if (item.arquivo) corpo += secao(item); }
}
await imprimir(docHtml(corpo, capaLivro), resolve(PDFS, EN ? "harness-engineering.pdf" : "engenharia-de-harness.pdf"), sumario.titulo);
console.log(`✓ PDF do livro [${EN ? "en" : "pt"}]: ${EN ? "docs/en" : "docs"}/pdf/`);

// 2) Um PDF por capítulo numerado
let avulsos = 0;
for (const parte of sumario.partes) {
  for (const item of parte.itens) {
    if (!item.arquivo || !/^\s*\d+\s*—/.test(item.titulo)) continue;
    const s = secao(item, true);
    if (!s) continue;
    await imprimir(docHtml(s, ""), resolve(PDFS, `${slugDe(item.arquivo)}.pdf`), `${sumario.titulo} · ${item.titulo}`);
    avulsos++;
  }
}
await browser.close();
console.log(`✓ PDFs por capítulo [${EN ? "en" : "pt"}]: ${avulsos}`);
