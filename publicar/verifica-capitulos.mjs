// Verificação por página do template visual (spec 043; ADR 0005) — por idioma.
// Uso: node verifica-capitulos.mjs                (PT, docs/)
//      LIVRO_LANG=en node verifica-capitulos.mjs  (EN, docs/en/ — após o build EN)
// Qualquer falha encerra com exit 1 (portão de qualidade).

import { readFileSync, existsSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const EN = process.env.LIVRO_LANG === "en";
const DOCS = resolve(RAIZ, EN ? "docs/en" : "docs");

const sumario = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.en.json" : "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome }))).filter((i) => i.arquivo);
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();

const RE_CAPTURA = EN ? /State of the art captured in/ : /Estado da arte capturado em/;
const RE_LEITURA = EN ? /^###\s+Executive summary/m : /^###\s+Leitura executiva/m;
const MIN_LEITURA = EN ? "min read" : "min de leitura";
const MD_LIVRO = EN ? "harness-engineering.md" : "engenharia-de-harness.md";
const PDF_LIVRO = EN ? "harness-engineering.pdf" : "engenharia-de-harness.pdf";

const falhas = [];
let capitulos = 0, aparato = 0;

for (const item of itens) {
  const slug = slugDe(item.arquivo);
  const arq = resolve(DOCS, `${slug}.html`);
  const fonte = resolve(RAIZ, item.arquivo);
  if (!existsSync(arq) || !existsSync(fonte)) { falhas.push(`${slug}: página ou fonte ausente`); continue; }
  const html = readFileSync(arq, "utf8");
  const md = readFileSync(fonte, "utf8");
  const num = (item.titulo.match(/^\s*(\d+)\s*—/) || [])[1];
  const erro = (m) => falhas.push(`${slug}: ${m}`);

  if (num) {
    capitulos++;
    if (!html.includes('class="cap-hero"')) erro("sem C01 (.cap-hero)");
    if (!html.includes(`<div class="cap-num" aria-hidden="true">${num}</div>`)) erro(`badge do número ${num} ausente`);
    if (!html.includes('class="cap-kicker"')) erro("kicker ausente");
    if (!html.includes(MIN_LEITURA)) erro("tempo de leitura ausente");
    if (RE_CAPTURA.test(md) && !html.toLowerCase().includes(EN ? "state of the art" : "estado da arte")) erro("datação não absorvida no C01");
    const h1s = (html.match(/<h1[\s>]/g) || []).length;
    if (h1s !== 1) erro(`esperado 1 <h1>, encontrado ${h1s}`);
    if (new RegExp("<blockquote>\\s*<p><strong>" + RE_CAPTURA.source).test(html)) erro("blockquote de datação sobrou no corpo");
    if (RE_LEITURA.test(md) && !html.includes('class="leitura-exec"')) erro("C08 não aplicado");
    if (!html.includes(`href="md/${slug}.md"`)) erro("link de download .md ausente");
    if (!html.includes(`href="pdf/${slug}.pdf"`)) erro("link de download .pdf ausente");
    if (!existsSync(resolve(DOCS, "md", `${slug}.md`))) erro("md/*.md não copiado");
    if (existsSync(resolve(DOCS, "pdf")) && !existsSync(resolve(DOCS, "pdf", `${slug}.pdf`))) erro("pdf/*.pdf ausente");
  } else {
    aparato++;
    if (html.includes('class="cap-hero"')) erro("página do aparato ganhou C01 indevidamente");
    if (new RegExp("^>\\s*\\*\\*" + RE_CAPTURA.source, "m").test(md) && !html.includes('class="selo-data"')) erro("selo de datação (C02) sumiu");
  }
  if (!html.includes('class="pagcards"')) erro("sem N02 (.pagcards)");
  if (!html.includes('class="lang-pill"')) erro("sem seletor de idioma (spec 067)");

  // Selo de sincronia (spec 067): toda página EN precisa do cabeçalho i18n
  // e o selo deve refletir o estado REAL (hash da fonte PT).
  if (EN) {
    const m = md.match(/^<!--\s*i18n\s+fonte:(\S+)\s+edicao:(\S+)\s+hash:([0-9a-f]{8})\s*-->/);
    if (!m) { erro("fonte EN sem cabeçalho i18n"); continue; }
    if (!existsSync(resolve(RAIZ, m[1]))) { erro(`cabeçalho i18n aponta fonte inexistente: ${m[1]}`); continue; }
    const atual = createHash("md5").update(readFileSync(resolve(RAIZ, m[1]))).digest("hex").slice(0, 8);
    const emDia = atual === m[3];
    if (emDia && !html.includes("sinc-ok")) erro("tradução em dia sem selo sinc-ok");
    if (!emDia && !html.includes("sinc-atras")) erro("tradução atrasada sem selo sinc-atras");
  }
}

// Knowledge Graph (spec 057) — só na passada PT (o EN remapeia o mesmo grafo).
if (!EN) {
  const gPath = resolve(DOCS, "assets/grafo.json");
  if (!existsSync(gPath)) falhas.push("assets/grafo.json ausente");
  else {
    const g = JSON.parse(readFileSync(gPath, "utf8"));
    const caps = g.nos.filter((n) => n.tipo === "capitulo").length;
    if (caps !== 18) falhas.push(`grafo: esperados 18 capítulos, há ${caps}`);
    if (g.nos.length < 40) falhas.push(`grafo: só ${g.nos.length} nós (<40)`);
    if (g.arestas.length < 100) falhas.push(`grafo: só ${g.arestas.length} arestas (<100)`);
  }
} else if (!existsSync(resolve(RAIZ, "docs/assets/grafo.en.json"))) {
  falhas.push("assets/grafo.en.json ausente (remapeamento EN)");
}

// News na capa (spec 062): se as fontes do jornal parseiam, a capa noticia.
{
  const indexHtml = readFileSync(resolve(DOCS, "index.html"), "utf8");
  const radar = existsSync(resolve(RAIZ, "radar/RADAR.md")) ? readFileSync(resolve(RAIZ, "radar/RADAR.md"), "utf8") : "";
  const temNoticia = radar.split("\n").some((l) => {
    const c = l.split("|").map((x) => x.trim());
    return c.length >= 7 && /^\d{4}-\d{2}-\d{2}$/.test(c[1]) && !c[2].includes("(inicial)");
  });
  const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
  const temEdicao = /^###\s+Edição\s+\d+\.\d+\s+—\s+\d{4}-\d{2}-\d{2}\s+·\s+.+$/m.test(hist);
  if (temNoticia && !indexHtml.includes('class="splash-news"')) falhas.push("capa: RADAR tem notícia mas index.html não tem .splash-news");
  if (temEdicao && !indexHtml.includes('class="splash-vedicao"')) falhas.push("capa: HISTORICO tem edição mas index.html não tem .splash-vedicao");
}

// Livro completo para download (spec 045), por idioma.
if (!existsSync(resolve(DOCS, "md", MD_LIVRO))) falhas.push(`consolidado md/${MD_LIVRO} ausente`);
const sum = readFileSync(resolve(DOCS, "sumario.html"), "utf8");
if (!sum.includes(`href="pdf/${PDF_LIVRO}"`) || !sum.includes(`href="md/${MD_LIVRO}"`))
  falhas.push("entrada sem os botões de download do livro completo");

if (falhas.length) {
  console.error(`✗ verificação do template [${EN ? "en" : "pt"}]: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ template verificado [${EN ? "en" : "pt"}]: ${capitulos} capítulos com C01/N02 + ${aparato} páginas de aparato OK`);
