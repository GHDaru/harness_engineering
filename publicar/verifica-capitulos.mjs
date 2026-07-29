// Verificação por capítulo do template visual (spec 043; ADR 0005).
// Roda APÓS `node build.mjs` e confere, página a página em docs/:
//  - capítulos numerados: C01 presente (badge/kicker/título/meta), h1 único,
//    blockquote de datação removido do corpo, N02 presente;
//  - capítulos cuja fonte tem "### Leitura executiva": C08 aplicado;
//  - páginas do aparato (sem número): SEM C01, selo antigo preservado.
// Qualquer falha encerra com exit 1 (portão de qualidade).
// Uso: node verifica-capitulos.mjs   (a partir de publicar/)

import { readFileSync, existsSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const DOCS = resolve(RAIZ, "docs");

const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome })));
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();

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
    if (!html.includes("min de leitura")) erro("tempo de leitura ausente");
    if (/Estado da arte capturado em/.test(md) && !html.includes("estado da arte")) erro("datação não absorvida no C01");
    const h1s = (html.match(/<h1[\s>]/g) || []).length;
    if (h1s !== 1) erro(`esperado 1 <h1>, encontrado ${h1s}`);
    if (/<blockquote>\s*<p><strong>Estado da arte capturado em/.test(html)) erro("blockquote de datação sobrou no corpo");
    if (/^###\s+Leitura executiva/m.test(md) && !html.includes('class="leitura-exec"')) erro("C08 não aplicado");
    // Downloads por capítulo (spec 045): links no C01 + .md copiado; o PDF é
    // conferido só quando docs/pdf/ existe (gerado por pdf.mjs após o portão).
    if (!html.includes(`href="md/${slug}.md"`)) erro("link de download .md ausente");
    if (!html.includes(`href="pdf/${slug}.pdf"`)) erro("link de download .pdf ausente");
    if (!existsSync(resolve(DOCS, "md", `${slug}.md`))) erro("docs/md/*.md não copiado");
    if (existsSync(resolve(DOCS, "pdf")) && !existsSync(resolve(DOCS, "pdf", `${slug}.pdf`))) erro("docs/pdf/*.pdf ausente");
  } else {
    aparato++;
    if (html.includes('class="cap-hero"')) erro("página do aparato ganhou C01 indevidamente");
    if (/^>\s*\*\*Estado da arte capturado em/m.test(md) && !html.includes('class="selo-data"')) erro("selo de datação (C02) sumiu");
  }
  if (!html.includes('class="pagcards"')) erro("sem N02 (.pagcards)");
}

// Livro completo para download (spec 045)
if (!existsSync(resolve(DOCS, "md", "engenharia-de-harness.md"))) falhas.push("consolidado md/engenharia-de-harness.md ausente");
const sum = readFileSync(resolve(DOCS, "sumario.html"), "utf8");
if (!sum.includes('href="pdf/engenharia-de-harness.pdf"') || !sum.includes('href="md/engenharia-de-harness.md"'))
  falhas.push("entrada sem os botões de download do livro completo");

if (falhas.length) {
  console.error(`✗ verificação do template: ${falhas.length} falha(s)`);
  falhas.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log(`✓ template verificado: ${capitulos} capítulos com C01/N02 + ${aparato} páginas de aparato OK`);
