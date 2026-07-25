// Motor do livro — Markdown (livro/) -> site HTML navegável (docs/).
// App próprio (não framework): usa markdown-it como biblioteca de parsing;
// o motor em si — navegação, tema, callouts, ilhas de visualização — é nosso.
// Uso: node build.mjs   (a partir de publicar/)
//
// Convenções de conteúdo reconhecidas:
//  - 1º blockquote iniciando com "**Estado da arte capturado em" -> selo de data (livro vivo)
//  - Seções ## cujo título casa um tipo pedagógico -> callout com estilo próprio (Diátaxis/Bloom)
//  - Links internos .md -> reescritos para .html
//  - <div data-viz="..."> -> ilha reservada para componente React (P2); no MVP vira placeholder

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync, rmSync } from "node:fs";
import { dirname, resolve, basename } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const SAIDA = resolve(RAIZ, "docs");

const sumario = JSON.parse(readFileSync(resolve(AQUI, "sumario.json"), "utf8"));

// Lista linear de itens (para prev/next) + slug estável por arquivo.
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome })));
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();
itens.forEach((i) => (i.slug = slugDe(i.arquivo)));
const slugsPublicados = new Set(itens.map((i) => i.slug));
const GITHUB_BASE = "https://github.com/GHDaru/harness_engineering/blob/main/";

// linkify: false de propósito — num livro técnico, "AGENTS.md"/"app.py" no texto
// não devem virar links. Links reais já são explícitos no Markdown.
const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(anchor, {
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
  slugify: (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""),
});

// Reescrita de links internos, resolvida a partir do diretório do arquivo-fonte
// (env.srcDir): página publicada -> .html local; qualquer outro alvo do repo
// (estudos/, código, arquivos não publicados) -> fonte no GitHub. Assim nenhum
// link interno fica quebrado e o que não é capítulo aponta para o código-fonte.
const defaultLinkOpen = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href && !/^https?:|^#|^mailto:|^\/\//.test(href)) {
    const [alvo, hash] = href.split("#");
    const ancora = hash ? "#" + hash : "";
    const slug = basename(alvo).replace(/\.md$/i, "").toLowerCase();
    if (/\.md$/i.test(alvo) && slugsPublicados.has(slug)) {
      tokens[idx].attrSet("href", slug + ".html" + ancora);
    } else {
      // caminho relativo ao arquivo-fonte -> caminho relativo à raiz do repo
      const repoRel = path.posix.normalize(path.posix.join(env.srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");
      tokens[idx].attrSet("href", GITHUB_BASE + repoRel + ancora);
    }
  }
  return defaultLinkOpen(tokens, idx, options, env, self);
};

// Extrai a data de captura do 1º blockquote, se houver.
function extrairData(markdown) {
  const m = markdown.match(/^>\s*\*\*Estado da arte capturado em([^*]+)\*\*([^\n]*)/m);
  return m ? ("Estado da arte capturado em" + m[1] + m[2]).replace(/\[.*?\]\(.*?\)/g, "").replace(/·\s*$/, "").trim() : null;
}

// Callouts: marca seções pedagógicas conhecidas com uma classe para o CSS estilizar.
const TIPOS = [
  { re: /objetivos de aprendizagem/i, cls: "callout-objetivos", rotulo: "Objetivos" },
  { re: /^verifica/i, cls: "callout-verificacao", rotulo: "Verificação" },
  { re: /mão na massa/i, cls: "callout-pratica", rotulo: "Mão na massa" },
  { re: /o que roubar/i, cls: "callout-roubar", rotulo: "O que roubar" },
  { re: /^apêndice/i, cls: "callout-apendice", rotulo: "Apêndice" },
];
function marcarCallouts(html) {
  // Envolve cada bloco <h2>..</h2> ... até o próximo <h2> quando o título casa um tipo.
  return html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/g, (full, attrs, titulo) => {
    const limpo = titulo.replace(/<[^>]+>/g, "").trim();
    const tipo = TIPOS.find((t) => t.re.test(limpo));
    return tipo ? `<h2${attrs} data-callout="${tipo.cls}">${titulo}</h2>` : full;
  });
}

function pagina({ tituloLivro, tituloPagina, corpo, navLateral, prev, next, data, ehIndex }) {
  const rel = ehIndex ? "" : "";
  const navBtn = (item, dir) =>
    item ? `<a class="nav-${dir}" href="${item.slug}.html">${dir === "prev" ? "← " : ""}${item.titulo}${dir === "next" ? " →" : ""}</a>` : `<span></span>`;
  const selo = data ? `<div class="selo-data" title="Livro vivo — ver Histórico">🕒 ${data}</div>` : "";
  return `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${tituloPagina} · ${tituloLivro}</title>
<link rel="stylesheet" href="${rel}assets/estilo.css">
</head><body>
<button id="alt-tema" aria-label="Alternar tema">◐</button>
<div class="layout">
  <aside class="sidebar">
    <a class="marca" href="index.html">${tituloLivro}</a>
    ${navLateral}
  </aside>
  <main class="conteudo">
    ${selo}
    <article class="markdown">${corpo}</article>
    <nav class="paginacao">${navBtn(prev, "prev")}${navBtn(next, "next")}</nav>
    <footer class="rodape">Livro vivo · gerado do Markdown pelo motor próprio · <a href="https://github.com/GHDaru/harness_engineering">fonte no GitHub</a></footer>
  </main>
</div>
<script src="${rel}assets/app.js"></script>
</body></html>`;
}

function montarNavLateral(atualSlug) {
  return sumario.partes
    .map(
      (p) =>
        `<div class="nav-parte">${p.nome}</div><ul>` +
        p.itens
          .map((i) => {
            const s = slugDe(i.arquivo);
            const ativo = s === atualSlug ? ' class="ativo"' : "";
            return `<li><a${ativo} href="${s}.html">${i.titulo}</a></li>`;
          })
          .join("") +
        `</ul>`
    )
    .join("");
}

// --- build ---
if (existsSync(SAIDA)) rmSync(SAIDA, { recursive: true, force: true });
mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
writeFileSync(resolve(SAIDA, ".nojekyll"), "");

let gerados = 0;
for (let k = 0; k < itens.length; k++) {
  const item = itens[k];
  const caminho = resolve(RAIZ, item.arquivo);
  if (!existsSync(caminho)) {
    console.warn(`  aviso: ausente, pulando -> ${item.arquivo}`);
    continue;
  }
  const bruto = readFileSync(caminho, "utf8");
  const data = extrairData(bruto);
  const corpo = marcarCallouts(md.render(bruto, { srcDir: dirname(item.arquivo) }));
  const html = pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: item.titulo,
    corpo,
    navLateral: montarNavLateral(item.slug),
    prev: itens[k - 1],
    next: itens[k + 1],
    data,
  });
  writeFileSync(resolve(SAIDA, `${item.slug}.html`), html);
  gerados++;
}

// index / capa
const capa = `<div class="capa">
<h1>${sumario.titulo}</h1>
<p class="subtitulo">${sumario.subtitulo}</p>
<p>Um estudo empírico da disciplina de construir o <em>scaffolding</em> que envolve agentes de IA — teoria, benchmark de harnesses reais e uma construção prática do zero.</p>
</div>
${sumario.partes
  .map(
    (p) =>
      `<h2>${p.nome}</h2><ul class="sumario">` +
      p.itens.map((i) => `<li><a href="${slugDe(i.arquivo)}.html">${i.titulo}</a></li>`).join("") +
      `</ul>`
  )
  .join("")}`;
writeFileSync(
  resolve(SAIDA, "index.html"),
  pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: "Sumário",
    corpo: capa,
    navLateral: montarNavLateral(null),
    prev: null,
    next: itens[0],
    data: null,
    ehIndex: true,
  })
);

// Portão de qualidade (T402): todo link interno .html gerado deve apontar para
// uma página que existe. Link quebrado FALHA o build (e, portanto, o CI).
const paginas = new Set(itens.map((i) => `${i.slug}.html`).concat("index.html"));
const quebrados = [];
for (const i of [...itens, { slug: "index" }]) {
  const arq = resolve(SAIDA, `${i.slug}.html`);
  if (!existsSync(arq)) continue;
  const html = readFileSync(arq, "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^https?:|^#|^mailto:|^\/\//.test(href)) continue; // externos não são conferidos aqui
    if (!/\.html(#|$)/.test(href)) continue;
    const alvo = basename(href.split("#")[0]);
    if (!paginas.has(alvo)) quebrados.push(`${i.slug}.html → ${href}`);
  }
}
if (quebrados.length) {
  console.error(`✗ ${quebrados.length} link(s) interno(s) quebrado(s):`);
  quebrados.forEach((q) => console.error("   " + q));
  process.exit(1);
}

console.log(`✓ Livro gerado: ${gerados} capítulos + capa em docs/ (links internos OK)`);
