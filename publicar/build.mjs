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
import { execSync } from "node:child_process";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";
import * as esbuild from "esbuild";

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
const SITE = "https://ghdaru.github.io/harness_engineering/"; // base absoluta p/ og:image
const DOI = "10.5281/zenodo.21632412";

// Chat-companion (feature 017): URL do backend + espelho leve do registro de
// capacidades (fonte-de-verdade do gating é o backend; aqui é só exibição).
const COMPANION_BACKEND = sumario.companion_backend || "";
const COMPANION_CAPS = [
  { chave: "tutor", rotulo: "Tutor do livro", libera: 0 },
  { chave: "busca_livro", rotulo: "Busca no livro", libera: 0 },
  { chave: "loop", rotulo: "Loop de agente", libera: 2 },
  { chave: "contexto", rotulo: "Contexto em camadas", libera: 3 },
  { chave: "compactacao", rotulo: "Compactação", libera: 4 },
  { chave: "ferramentas", rotulo: "Ferramentas seguras", libera: 5 },
  { chave: "mcp", rotulo: "MCP", libera: 6 },
  { chave: "permissoes", rotulo: "Permissões", libera: 7 },
  { chave: "memoria", rotulo: "Memória entre sessões", libera: 8 },
  { chave: "planejamento", rotulo: "Planejamento", libera: 9 },
  { chave: "subagentes", rotulo: "Subagentes", libera: 10 },
  { chave: "evals", rotulo: "Verificação", libera: 11 },
];
// Deriva o capítulo da página a partir do título ("02 — …" -> 2; capa/aparato -> 0).
const capituloDe = (titulo) => parseInt((String(titulo).match(/^\s*(\d+)/) || [])[1], 10) || 0;
function companionSnippet(chapter) {
  const cfg = JSON.stringify({ backend: COMPANION_BACKEND, chapter, mode: "progressivo", capabilities: COMPANION_CAPS });
  return `<script>window.COMPANION=${cfg.replace(/</g, "\\u003c")}</script>
<link rel="stylesheet" href="assets/companion.css">
<script src="assets/companion.js" defer></script>`;
}

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

// Siglas "abertas" (spec 023): o motor envolve cada ocorrência conhecida em
// <abbr title="Por Extenso">, de forma NÃO-invasiva (não altera o Markdown-fonte)
// e HTML-safe (pula code/pre/links/títulos). Fonte única aqui; a página do
// glossário mirroreia as mesmas expansões. Só siglas de 3+ letras (evita ruído).
const SIGLAS = {
  MCP: "Model Context Protocol", ACP: "Agent Client Protocol", A2A: "Agent-to-Agent",
  LSP: "Language Server Protocol", RPC: "Remote Procedure Call",
  MAST: "Multi-Agent System Failure Taxonomy", RAG: "Retrieval-Augmented Generation",
  LLM: "Large Language Model", GPT: "Generative Pre-trained Transformer",
  API: "Application Programming Interface", SDK: "Software Development Kit",
  CLI: "Command-Line Interface", TUI: "Text (Terminal) User Interface",
  IDE: "Integrated Development Environment", HCI: "Human-Computer Interaction",
  HTTP: "HyperText Transfer Protocol", SSE: "Server-Sent Events", JSON: "JavaScript Object Notation",
  DDD: "Domain-Driven Design", DOI: "Digital Object Identifier",
  ORCID: "Open Researcher and Contributor ID", ISBN: "International Standard Book Number",
  ICMJE: "International Committee of Medical Journal Editors", COPE: "Committee on Publication Ethics",
  ICLR: "International Conference on Learning Representations", SWE: "Software Engineering",
};
const RE_SIGLAS = new RegExp("\\b(" + Object.keys(SIGLAS).sort((a, b) => b.length - a.length).join("|") + ")\\b", "g");
const TAGS_PROT = /^(pre|code|a|abbr|h[1-6]|script|style)$/i;
function abrirSiglas(html) {
  const re = /<\/?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>/g;
  const sub = (t) => t.replace(RE_SIGLAS, (s) => `<abbr title="${SIGLAS[s]}">${s}</abbr>`);
  let out = "", last = 0, m, prot = 0;
  while ((m = re.exec(html))) {
    const txt = html.slice(last, m.index);
    out += prot > 0 ? txt : sub(txt);
    const tag = m[1].toLowerCase();
    if (TAGS_PROT.test(tag) && !m[0].endsWith("/>")) prot += m[0][1] === "/" ? -1 : 1;
    if (prot < 0) prot = 0;
    out += m[0];
    last = re.lastIndex;
  }
  return out + (prot > 0 ? html.slice(last) : sub(html.slice(last)));
}

function pagina({ tituloLivro, tituloPagina, corpo, navLateral, prev, next, data, ehIndex, chapter = 0, slug = "" }) {
  const rel = ehIndex ? "" : "";
  const navBtn = (item, dir) =>
    item ? `<a class="nav-${dir}" href="${item.slug}.html">${dir === "prev" ? "← " : ""}${item.titulo}${dir === "next" ? " →" : ""}</a>` : `<span></span>`;
  const selo = data ? `<div class="selo-data" title="Livro vivo — ver Histórico">🕒 ${data}</div>` : "";
  return `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${tituloPagina} · ${tituloLivro}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${tituloLivro}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="${rel}assets/estilo.css">
</head><body${ehIndex ? ' class="pagina-index"' : ""} data-slug="${slug}" data-titulo="${tituloPagina.replace(/"/g, "&quot;")}">
<button id="alt-tema" aria-label="Alternar tema">◐</button>
<div class="layout">
  <aside class="sidebar">
    <a class="marca" href="sumario.html">${tituloLivro}</a>
    <a class="link-capa" href="index.html">↩ capa</a>
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
<script src="${rel}assets/viz.js" defer></script>
${companionSnippet(chapter)}
</body></html>`;
}

// Versão do livro: fonte única = a última edição declarada em HISTORICO.md.
// "### Edição 0.11 — …" -> "v0.11.0". Fallback seguro se nada casar.
function versaoDoLivro() {
  try {
    const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
    const m = hist.match(/^###\s+Edição\s+(\d+)\.(\d+)/m);
    if (m) return `v${m[1]}.${m[2]}.0`;
  } catch {}
  return "v0.0.0";
}

// Data da última modificação: data do último commit (fiel à mudança real de
// conteúdo). Sem git / repo raso -> data do build. Nunca quebra o build.
function dataDaUltimaModificacao() {
  let d;
  try {
    const iso = execSync("git log -1 --format=%cI", { cwd: RAIZ, stdio: ["ignore", "pipe", "ignore"] })
      .toString()
      .trim();
    d = iso ? new Date(iso) : new Date();
  } catch {
    d = new Date();
  }
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "long" }).format(d);
}

// Tela-capa (splash) full-screen: porta de entrada do site, sem sidebar.
function paginaSplash() {
  const versao = versaoDoLivro();
  const atualizado = dataDaUltimaModificacao();
  return `<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${sumario.titulo}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${sumario.titulo}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="assets/estilo.css">
</head><body class="splash-body">
<main class="splash">
  <div class="splash-arte">
    <img src="assets/capa.png" width="1024" height="1536" loading="eager"
      alt="Capa de Engenharia de Harness: um núcleo de IA luminoso, em âmbar, envolto por um harness de engenharia com módulos de loop, ferramenta, permissões, memória e verificação, sobre fundo azul-escuro com traços de blueprint.">
  </div>
  <div class="splash-texto">
    <h1>${sumario.titulo}</h1>
    <p class="splash-sub">${sumario.subtitulo}</p>
    <p class="splash-desc">Um estudo empírico da disciplina de construir o <em>scaffolding</em> que envolve agentes de IA — teoria, benchmark de harnesses reais e uma construção prática do zero.</p>
    <div class="splash-ctas">
      <a class="btn btn-primario btn-grande" href="sumario.html">Entrar no livro →</a>
      <a class="btn btn-escuro" href="comparativo.html">Benchmark</a>
      <a class="btn btn-escuro" href="guia-editorial.html">Guia Editorial</a>
    </div>
    <p class="splash-creditos"><strong><a href="autor.html">Gilsiley Henrique Darú</a></strong> — edição, direção e orquestração · <a class="splash-linkedin" href="https://www.linkedin.com/in/gilsiley-dar%C3%BA/">LinkedIn</a><br><strong>Claude (Anthropic)</strong> — pesquisa e geração de texto (co-autoria) · <strong>GPT (OpenAI)</strong> — imagem de capa</p>
    <p class="splash-versao"><span class="splash-versao-num">${versao}</span> · atualizado em ${atualizado}</p>
    <p class="splash-doi"><a href="https://doi.org/10.5281/zenodo.21632412">DOI: 10.5281/zenodo.21632412</a></p>
  </div>
</main>
${companionSnippet(0)}
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
cpSync(resolve(AQUI, "tema/capa.png"), resolve(SAIDA, "assets/capa.png"));
cpSync(resolve(AQUI, "tema/capa-social.png"), resolve(SAIDA, "assets/capa-social.png"));
cpSync(resolve(AQUI, "tema/autor.png"), resolve(SAIDA, "assets/autor.png"));
cpSync(resolve(AQUI, "tema/harness-diagrama.svg"), resolve(SAIDA, "assets/harness-diagrama.svg"));
cpSync(resolve(AQUI, "tema/companion.css"), resolve(SAIDA, "assets/companion.css"));
cpSync(resolve(AQUI, "tema/companion.js"), resolve(SAIDA, "assets/companion.js"));
writeFileSync(resolve(SAIDA, ".nojekyll"), "");

// Bundle das ilhas de visualização React (P2). Dados embutidos em build-time.
await esbuild.build({
  entryPoints: [resolve(AQUI, "viz/index.jsx")],
  bundle: true,
  minify: true,
  format: "iife",
  loader: { ".json": "json" },
  jsx: "automatic",
  outfile: resolve(SAIDA, "assets/viz.js"),
  logLevel: "warning",
});

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
  let corpo = marcarCallouts(md.render(bruto, { srcDir: dirname(item.arquivo) }));
  if (item.slug !== "glossario") corpo = abrirSiglas(corpo); // "abre" siglas fora do próprio glossário
  const html = pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: item.titulo,
    corpo,
    navLateral: montarNavLateral(item.slug),
    prev: k === 0 ? { slug: "sumario", titulo: "Sumário" } : itens[k - 1],
    next: itens[k + 1],
    data,
    chapter: capituloDe(item.titulo),
    slug: item.slug,
  });
  writeFileSync(resolve(SAIDA, `${item.slug}.html`), html);
  gerados++;
}

// index = tela-capa (splash) full-screen; porta de entrada.
writeFileSync(resolve(SAIDA, "index.html"), paginaSplash());

// sumario.html = a EXPERIÊNCIA DE ENTRADA (spec 021): hero + retomar + trilha +
// cartões por parte + pills do aparato. A sidebar (índice completo) vem de pagina().
const dividirTitulo = (t) => {
  const p = t.split("—");
  return p.length >= 2 ? { num: p[0].trim(), texto: p.slice(1).join("—").trim() } : { num: "", texto: t.trim() };
};
const cartaoEnt = (i) => {
  const s = slugDe(i.arquivo);
  const { num, texto } = dividirTitulo(i.titulo);
  return `<a class="ent-card" href="${s}.html">${num ? `<span class="ent-badge">${num}</span>` : ""}<span class="ent-ct">${texto}</span>${i.teaser ? `<span class="ent-cd">${i.teaser}</span>` : ""}</a>`;
};
const pillEnt = (i) => `<a class="ent-pill" href="${slugDe(i.arquivo)}.html">${dividirTitulo(i.titulo).texto}</a>`;
const partesCartao = new Set(["Abertura", "Capítulos por funcionalidade"]);
const blocosCartao = sumario.partes
  .filter((p) => partesCartao.has(p.nome))
  .map((p) => `<div class="ent-parte"><span>${p.nome}</span><i></i></div><div class="ent-grid">${p.itens.map(cartaoEnt).join("")}</div>`)
  .join("");
const pillsEnt = sumario.partes.filter((p) => !partesCartao.has(p.nome)).flatMap((p) => p.itens).map(pillEnt).join("");

const corpoSumario = `<section class="entrada">
  <div class="ent-hero">
    <img class="ent-capa" src="assets/capa.png" width="1024" height="1536" loading="eager" alt="Capa do livro Engenharia de Harness">
    <div class="ent-hero-txt">
      <div class="ent-kicker">Livro vivo · ${versaoDoLivro()} · DOI ${DOI}</div>
      <h1 class="ent-titulo">${sumario.titulo}</h1>
      <p class="ent-sub">${sumario.subtitulo}</p>
      <div class="ent-ctas">
        <a class="ent-btn ent-btn-a" href="00-introducao.html">▶ Começar do início — 00</a>
        <a class="ent-btn" href="comparativo.html">Benchmark</a>
        <a class="ent-btn" href="guia-editorial.html">Guia Editorial</a>
      </div>
    </div>
  </div>
  <a class="ent-retomar" id="ent-retomar" href="#" hidden>
    <span class="ent-ret-l"><span class="ent-ret-lab">Continue lendo</span><span class="ent-ret-cap" id="ent-ret-cap"></span></span>
    <span class="ent-btn ent-btn-a">Retomar ▶</span>
  </a>
  <div class="ent-trilha">
    <a class="ent-step" href="01-fundamentos.html"><span class="ent-step-n">Trilha · 1</span><b>Fundamentos</b><span>O vocabulário e a tese do livro.</span></a>
    <a class="ent-step" href="02-loop-do-agente.html"><span class="ent-step-n">Trilha · 2</span><b>Funcionalidades</b><span>Os 16 componentes, um por capítulo.</span></a>
    <a class="ent-step" href="comparativo.html"><span class="ent-step-n">Trilha · 3</span><b>Benchmark</b><span>10 harnesses reais comparados.</span></a>
    <a class="ent-step" href="https://github.com/GHDaru/harness_engineering/tree/main/harness-zero"><span class="ent-step-n">Trilha · 4</span><b>Mão na massa</b><span>Construa o harness-zero, etapa a etapa.</span></a>
  </div>
  ${blocosCartao}
  <div class="ent-parte"><span>Benchmark · Aparato · Sobre</span><i></i></div>
  <div class="ent-pills">${pillsEnt}</div>
</section>`;
writeFileSync(
  resolve(SAIDA, "sumario.html"),
  pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: "Sumário",
    corpo: corpoSumario,
    navLateral: montarNavLateral("sumario"),
    prev: null,
    next: itens[0],
    data: null,
    ehIndex: true,
  })
);

// Portão de qualidade (T402): todo link interno .html gerado deve apontar para
// uma página que existe. Link quebrado FALHA o build (e, portanto, o CI).
const paginas = new Set(itens.map((i) => `${i.slug}.html`).concat("index.html", "sumario.html"));
const quebrados = [];
for (const i of [...itens, { slug: "index" }, { slug: "sumario" }]) {
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
