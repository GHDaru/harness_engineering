// Motor do livro — Markdown (livro/) -> site HTML navegável (docs/).
// App próprio (não framework): usa markdown-it como biblioteca de parsing;
// o motor em si — navegação, tema, callouts, ilhas de visualização — é nosso.
// Uso: node build.mjs                (passada PT -> docs/)
//      LIVRO_LANG=en node build.mjs  (passada EN -> docs/en/; RODAR APÓS a PT)
//
// i18n (spec 067): o PT é a fonte canônica; o EN é artefato derivado. Cada
// fonte EN carrega na 1ª linha `<!-- i18n fonte:<pt> edicao:X hash:<md5-8> -->`;
// o build compara o hash com o fonte PT atual e gera o SELO DE SINCRONIA
// (em dia / atrasado) — tradução velha nunca finge ser atual.
//
// Convenções de conteúdo reconhecidas:
//  - 1º blockquote "**Estado da arte capturado em/State of the art captured in" -> selo de data
//  - Seções ## de tipos pedagógicos -> callout próprio (Diátaxis/Bloom)
//  - Links internos .md -> reescritos para .html; links .html passam intactos
//  - <div data-viz="..."> -> ilha de visualização

import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync, rmSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, resolve, basename } from "node:path";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";
import MarkdownIt from "markdown-it";
import anchor from "markdown-it-anchor";
import * as esbuild from "esbuild";
import { gerarGrafo } from "./grafo.mjs";
import { gerarJornal } from "./jornal.mjs";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");
const EN = process.env.LIVRO_LANG === "en";
const LANG = EN ? "en" : "pt";
const SAIDA = resolve(RAIZ, EN ? "docs/en" : "docs");
const A = EN ? "../assets/" : "assets/"; // assets são compartilhados na raiz de docs/

const sumario = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.en.json" : "sumario.json"), "utf8"));
const sumarioOutro = JSON.parse(readFileSync(resolve(AQUI, EN ? "sumario.json" : "sumario.en.json"), "utf8"));

// Lista linear de itens publicáveis (para prev/next); itens `externo` ficam só na navegação.
const slugDe = (arquivo) => basename(arquivo).replace(/\.md$/, "").toLowerCase();
const itens = sumario.partes.flatMap((p) => p.itens.map((i) => ({ ...i, parte: p.nome }))).filter((i) => i.arquivo);
itens.forEach((i) => (i.slug = slugDe(i.arquivo)));
const slugsPublicados = new Set(itens.map((i) => i.slug));

// Par de idioma por POSIÇÃO no sumário (os dois sumários são espelhados).
const parDe = { index: "index", sumario: "sumario" };
sumario.partes.forEach((p, pi) =>
  p.itens.forEach((i, ii) => {
    const o = sumarioOutro.partes[pi]?.itens?.[ii];
    if (i.arquivo && o?.arquivo) parDe[slugDe(i.arquivo)] = slugDe(o.arquivo);
  })
);
const hrefOutroIdioma = (slug) => (EN ? `../${parDe[slug] || "sumario"}.html` : `en/${parDe[slug] || "sumario"}.html`);

const GITHUB_BASE = "https://github.com/GHDaru/harness_engineering/blob/main/";
const SITE = "https://ghdaru.github.io/harness_engineering/";
const DOI = "10.5281/zenodo.21632412";

// Dicionário do chrome (spec 067). O conteúdo vem do Markdown; isto é só a moldura.
const T = EN
  ? {
      htmlLang: "en",
      temaAria: "Toggle theme",
      linkCapa: "↩ cover",
      sumarioTitulo: "Contents",
      seloVivo: "Living book — see History",
      estadoArte: "state of the art",
      revisao: "revised",
      minLeitura: "min read",
      dlMd: "Download this chapter's source Markdown",
      dlPdf: "Open this chapter's PDF",
      capKicker: "Ch.",
      anterior: "← previous",
      proximo: "next →",
      rodape: `Living book · generated from Markdown by our own engine · <a href="https://github.com/GHDaru/harness_engineering">source on GitHub</a>`,
      bibliografiaHtml: "bibliography.html",
      verCitacao: "see in the Bibliography",
      splashDesc: "An empirical study of the discipline of building the <em>scaffolding</em> around AI agents — theory, a benchmark of real harnesses, and a hands-on build from scratch.",
      splashAlt: "Cover of Harness Engineering: a glowing amber AI core wrapped in an engineering harness with loop, tool, permission, memory and verification modules, over a dark-blue blueprint background.",
      entrarLivro: "Enter the book →",
      benchmarkBtn: "Benchmark",
      guiaBtn: "Editorial Guide",
      hrefComparativo: "comparative.html",
      hrefGuia: "editorial-guide.html",
      hrefHistorico: "../historico.html",
      newsKicker: "🗞 News",
      newsPt: " · item in Portuguese",
      verRadar: "see the full Radar →",
      nestaEdicao: "This edition",
      historicoNome: "History",
      creditos: `<strong><a href="author.html">Gilsiley Henrique Darú</a></strong> — editing, direction and orchestration · <a class="splash-linkedin" href="https://www.linkedin.com/in/gilsiley-dar%C3%BA/">LinkedIn</a><br><strong>Claude (Anthropic)</strong> — research and text generation (co-authorship) · <strong>GPT (OpenAI)</strong> — cover image`,
      atualizadoEm: "updated on",
      kickerEntrada: "Living book",
      comecar: "▶ Start from the beginning — 00",
      pdfLivro: "pdf/harness-engineering.pdf",
      mdLivro: "md/harness-engineering.md",
      pdfLivroTitulo: "Full book as PDF",
      mdLivroTitulo: "Full book as Markdown (LLM-friendly)",
      continueLendo: "Continue reading",
      retomar: "Resume ▶",
      trilha: [
        ["01-foundations.html", "Track · 1", "Foundations", "The book's vocabulary and thesis."],
        ["02-agent-loop.html", "Track · 2", "Capabilities", "The 16 components, one per chapter."],
        ["comparative.html", "Track · 3", "Benchmark", "Real harnesses, compared."],
        ["https://github.com/GHDaru/harness_engineering/tree/main/harness-zero", "Track · 4", "Hands-on", "Build harness-zero, step by step."],
      ],
      partesCartao: new Set(["Opening", "Chapters by capability"]),
      pillsRotulo: "Benchmark · Apparatus · About",
      dataLocale: "en-US",
      sincOk: (ed) => `🌐 English translation · in sync with the Portuguese original (edition ${ed})`,
      sincAtras: (ed) => `⏳ The Portuguese original has changed since this translation (made at edition ${ed}) — the latest content is in the PT version`,
      lerPt: "read in PT",
      outroIdioma: "PT",
      outroIdiomaTitulo: "Ler em português",
    }
  : {
      htmlLang: "pt-BR",
      temaAria: "Alternar tema",
      linkCapa: "↩ capa",
      sumarioTitulo: "Sumário",
      seloVivo: "Livro vivo — ver Histórico",
      estadoArte: "estado da arte",
      revisao: "revisão",
      minLeitura: "min de leitura",
      dlMd: "Baixar o Markdown-fonte deste capítulo",
      dlPdf: "Abrir o PDF deste capítulo",
      capKicker: "Cap.",
      anterior: "← anterior",
      proximo: "próximo →",
      rodape: `Livro vivo · gerado do Markdown pelo motor próprio · <a href="https://github.com/GHDaru/harness_engineering">fonte no GitHub</a>`,
      bibliografiaHtml: "bibliografia.html",
      verCitacao: "ver na Bibliografia",
      splashDesc: "Um estudo empírico da disciplina de construir o <em>scaffolding</em> que envolve agentes de IA — teoria, benchmark de harnesses reais e uma construção prática do zero.",
      splashAlt: "Capa de Engenharia de Harness: um núcleo de IA luminoso, em âmbar, envolto por um harness de engenharia com módulos de loop, ferramenta, permissões, memória e verificação, sobre fundo azul-escuro com traços de blueprint.",
      entrarLivro: "Entrar no livro →",
      benchmarkBtn: "Benchmark",
      guiaBtn: "Guia Editorial",
      hrefComparativo: "comparativo.html",
      hrefGuia: "guia-editorial.html",
      hrefHistorico: "historico.html",
      newsKicker: "🗞 Novidade",
      newsPt: "",
      verRadar: "ver o Radar completo →",
      nestaEdicao: "Nesta edição",
      historicoNome: "Histórico",
      creditos: `<strong><a href="autor.html">Gilsiley Henrique Darú</a></strong> — edição, direção e orquestração · <a class="splash-linkedin" href="https://www.linkedin.com/in/gilsiley-dar%C3%BA/">LinkedIn</a><br><strong>Claude (Anthropic)</strong> — pesquisa e geração de texto (co-autoria) · <strong>GPT (OpenAI)</strong> — imagem de capa`,
      atualizadoEm: "atualizado em",
      kickerEntrada: "Livro vivo",
      comecar: "▶ Começar do início — 00",
      pdfLivro: "pdf/engenharia-de-harness.pdf",
      mdLivro: "md/engenharia-de-harness.md",
      pdfLivroTitulo: "Livro completo em PDF",
      mdLivroTitulo: "Livro completo em Markdown (bom para LLMs)",
      continueLendo: "Continue lendo",
      retomar: "Retomar ▶",
      trilha: [
        ["01-fundamentos.html", "Trilha · 1", "Fundamentos", "O vocabulário e a tese do livro."],
        ["02-loop-do-agente.html", "Trilha · 2", "Funcionalidades", "Os 16 componentes, um por capítulo."],
        ["comparativo.html", "Trilha · 3", "Benchmark", "10 harnesses reais comparados."],
        ["https://github.com/GHDaru/harness_engineering/tree/main/harness-zero", "Trilha · 4", "Mão na massa", "Construa o harness-zero, etapa a etapa."],
      ],
      partesCartao: new Set(["Abertura", "Capítulos por funcionalidade"]),
      pillsRotulo: "Benchmark · Aparato · Sobre",
      dataLocale: "pt-BR",
      sincOk: null,
      sincAtras: null,
      lerPt: "",
      outroIdioma: "EN",
      outroIdiomaTitulo: "Read in English",
    };

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
const capituloDe = (titulo) => parseInt((String(titulo).match(/^\s*(\d+)/) || [])[1], 10) || 0;
function companionSnippet(chapter) {
  const cfg = JSON.stringify({ backend: COMPANION_BACKEND, chapter, mode: "progressivo", lang: LANG, capabilities: COMPANION_CAPS });
  return `<script>window.COMPANION=${cfg.replace(/</g, "\\u003c")}</script>
<link rel="stylesheet" href="${A}companion.css">
<script src="${A}companion.js" defer></script>`;
}

// linkify: false de propósito — num livro técnico, "AGENTS.md"/"app.py" no texto
// não devem virar links. Links reais já são explícitos no Markdown.
const md = new MarkdownIt({ html: true, linkify: false, typographer: false }).use(anchor, {
  permalink: anchor.permalink.ariaHidden({ symbol: "#", placement: "after" }),
  slugify: (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""),
});

// Reescrita de links internos: .md publicado -> .html local; .html passa
// intacto (links cross-idioma como ../historico.html); resto -> GitHub.
const defaultLinkOpen = md.renderer.rules.link_open || ((t, i, o, e, s) => s.renderToken(t, i, o));
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const href = tokens[idx].attrGet("href");
  if (href && !/^https?:|^#|^mailto:|^\/\//.test(href) && !/\.html(#|$)/.test(href)) {
    const [alvo, hash] = href.split("#");
    const ancora = hash ? "#" + hash : "";
    const slug = basename(alvo).replace(/\.md$/i, "").toLowerCase();
    if (/\.md$/i.test(alvo) && slugsPublicados.has(slug)) {
      tokens[idx].attrSet("href", slug + ".html" + ancora);
    } else {
      const repoRel = path.posix.normalize(path.posix.join(env.srcDir || ".", alvo)).replace(/^(\.\.\/)+/, "");
      tokens[idx].attrSet("href", GITHUB_BASE + repoRel + ancora);
    }
  }
  return defaultLinkOpen(tokens, idx, options, env, self);
};

// Datação (PT e EN): o selo do livro vivo.
const RE_CAPTURA = /(?:Estado da arte capturado em|State of the art captured in)/;
function extrairData(markdown) {
  const m = markdown.match(new RegExp("^>\\s*\\*\\*(" + RE_CAPTURA.source + "[^*]+)\\*\\*([^\\n]*)", "m"));
  return m ? (m[1] + m[2]).replace(/\[.*?\]\(.*?\)/g, "").replace(/·\s*$/, "").trim() : null;
}
function extrairDatas(markdown) {
  const cap = (markdown.match(new RegExp(RE_CAPTURA.source + "\\s+(\\d{4}-\\d{2}(?:-\\d{2})?)")) || [])[1] || null;
  const rev = (markdown.match(/(?:última revisão|last revised)\s+(\d{4}-\d{2}-\d{2})/) || [])[1] || null;
  return { cap, rev };
}

// Selo de sincronia (spec 067): lê o cabeçalho i18n da fonte EN e compara o
// hash com o fonte PT ATUAL. Sem cabeçalho -> sem selo (páginas PT).
function seloDeSincronia(markdown, slug) {
  const m = markdown.match(/^<!--\s*i18n\s+fonte:(\S+)\s+edicao:(\S+)\s+hash:([0-9a-f]{8})\s*-->/);
  if (!m) return "";
  const [, fonte, edicao, hash] = m;
  let atual = "";
  try {
    atual = createHash("md5").update(readFileSync(resolve(RAIZ, fonte))).digest("hex").slice(0, 8);
  } catch {}
  const emDia = atual && atual === hash;
  const alvoPt = `../${parDe[slug] || "sumario"}.html`;
  return emDia
    ? `<div class="sinc sinc-ok">${T.sincOk(edicao)}</div>`
    : `<div class="sinc sinc-atras">${T.sincAtras(edicao)} — <a href="${alvoPt}">${T.lerPt}</a></div>`;
}

// Carga estimada de leitura (Sweller): ~200 palavras/min, sem blocos de código.
function tempoDeLeitura(markdown) {
  const semCodigo = markdown.replace(/```[\s\S]*?```/g, " ");
  const palavras = (semCodigo.match(/\S+/g) || []).length;
  return Math.max(1, Math.round(palavras / 200));
}

// Callouts pedagógicos (PT/EN).
const TIPOS = [
  { re: /objetivos de aprendizagem|learning objectives/i, cls: "callout-objetivos" },
  { re: /^verifica|^check your understanding/i, cls: "callout-verificacao" },
  { re: /mão na massa|hands-on/i, cls: "callout-pratica" },
  { re: /o que roubar|what to steal/i, cls: "callout-roubar" },
  { re: /^apêndice|^appendix/i, cls: "callout-apendice" },
];
function marcarCallouts(html) {
  return html.replace(/<h2([^>]*)>([\s\S]*?)<\/h2>/g, (full, attrs, titulo) => {
    const limpo = titulo.replace(/<[^>]+>/g, "").trim();
    const tipo = TIPOS.find((t) => t.re.test(limpo));
    return tipo ? `<h2${attrs} data-callout="${tipo.cls}">${titulo}</h2>` : full;
  });
}

// Siglas "abertas" (spec 023) — fonte única; o glossário mirroreia.
const SIGLAS = {
  MCP: "Model Context Protocol", ACP: "Agent Client Protocol", A2A: "Agent-to-Agent",
  MRTR: "Multi Round-Trip Requests", CIMD: "Client ID Metadata Documents", DCR: "Dynamic Client Registration",
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
function ligarCitacoes(texto) {
  return texto.replace(/arXiv\s+(\d{4}\.\d{4,5})/g,
    (m, id) => `<a class="cita" href="${T.bibliografiaHtml}" title="${T.verCitacao}">arXiv ${id}</a>`);
}

// C08 LeituraExecutiva (spec 043) — PT/EN.
function marcarLeituraExec(html) {
  return html.replace(/(<h3[^>]*>[\s\S]*?<\/h3>)([\s\S]*?)(?=<h[1-3][\s>]|$)/g, (full, h3, resto) => {
    const limpo = h3.replace(/<[^>]+>/g, "").trim();
    if (!/^(leitura executiva|executive summary)/i.test(limpo)) return full;
    return `<div class="leitura-exec">${h3}${resto}</div>`;
  });
}

function abrirSiglas(html) {
  const re = /<\/?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>/g;
  const sub = (t) => ligarCitacoes(t).replace(RE_SIGLAS, (s) => `<abbr title="${SIGLAS[s]}">${s}</abbr>`);
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

// "02 — Loop do Agente" -> { num: "02", texto: "Loop do Agente" }.
const dividirTitulo = (t) => {
  const p = t.split("—");
  if (p.length < 2) return { num: "", texto: t.trim() };
  return { num: /^\s*\d+\s*$/.test(p[0]) ? p[0].trim() : "", texto: p.slice(1).join("—").trim() };
};

// Seletor de idioma (spec 067): pill PT·EN presente em todas as páginas.
function pillIdioma(slug) {
  const alvo = hrefOutroIdioma(slug);
  const atual = EN ? "EN" : "PT";
  const outro = T.outroIdioma;
  return `<nav class="lang-pill" aria-label="Idioma / Language"><span class="lang-atual">${atual}</span><a href="${alvo}" title="${T.outroIdiomaTitulo}" data-lang-alvo="${EN ? "pt" : "en"}">${outro}</a></nav>`;
}
function hreflangs(slug) {
  const aqui = EN ? `en/${slug}.html` : `${slug}.html`;
  const la = EN ? `${parDe[slug] || "sumario"}.html` : `en/${parDe[slug] || "sumario"}.html`;
  const pt = EN ? la : aqui, en = EN ? aqui : la;
  return `<link rel="alternate" hreflang="pt-BR" href="${SITE}${pt}">
<link rel="alternate" hreflang="en" href="${SITE}${en}">
<link rel="alternate" hreflang="x-default" href="${SITE}${pt}">`;
}

function pagina({ tituloLivro, tituloPagina, corpo, navLateral, prev, next, data, ehIndex, chapter = 0, slug = "", hero = null, sinc = "" }) {
  const navBtn = (item, dir) => {
    if (!item) return `<span></span>`;
    const { num, texto } = dividirTitulo(item.titulo);
    const badge = num ? `<span class="pag-badge">${num}</span>` : "";
    const rotulo = dir === "prev" ? T.anterior : T.proximo;
    return `<a class="pagcard${dir === "next" ? " next" : ""}" href="${item.slug}.html">${badge}<span class="pag-tx"><span class="pag-dir">${rotulo}</span><span class="pag-tt">${texto}</span></span></a>`;
  };
  const selo = data ? `<div class="selo-data" title="${T.seloVivo}">🕒 ${data}</div>` : "";
  return `<!doctype html>
<html lang="${T.htmlLang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${tituloPagina} · ${tituloLivro}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${tituloLivro}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
${hreflangs(slug)}
<link rel="icon" type="image/svg+xml" href="${A}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="${A}favicon-32.png">
<link rel="apple-touch-icon" href="${A}apple-touch-icon.png">
<link rel="stylesheet" href="${A}estilo.css">
</head><body${ehIndex ? ' class="pagina-index"' : hero ? ' class="pagina-capitulo"' : ""} data-slug="${slug}" data-lang="${LANG}" data-titulo="${tituloPagina.replace(/"/g, "&quot;")}">
<button id="alt-tema" aria-label="${T.temaAria}">◐</button>
${pillIdioma(slug)}
<div class="layout">
  <aside class="sidebar">
    <a class="marca" href="sumario.html">${tituloLivro}</a>
    <a class="link-capa" href="index.html">${T.linkCapa}</a>
    ${navLateral}
  </aside>
  <main class="conteudo">
    ${sinc}
    ${hero || selo}
    <article class="markdown">${corpo}</article>
    <nav class="pagcards">${navBtn(prev, "prev")}${navBtn(next, "next")}</nav>
    <footer class="rodape">${T.rodape}</footer>
  </main>
</div>
<script src="${A}app.js"></script>
<script src="${A}viz.js" defer></script>
<script src="${A}uso.js" defer></script>
<script src="${A}grafo.js" defer></script>
${companionSnippet(chapter)}
</body></html>`;
}

// Versão do livro: fonte única = a última edição declarada em HISTORICO.md (PT, canônico).
function versaoDoLivro() {
  try {
    const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
    const m = hist.match(/^###\s+Edição\s+(\d+)\.(\d+)/m);
    if (m) return `v${m[1]}.${m[2]}.0`;
  } catch {}
  return "v0.0.0";
}

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
  return new Intl.DateTimeFormat(T.dataLocale, { dateStyle: "long" }).format(d);
}

// Jornal vivo (specs 061/062): fontes operacionais são PT; na edição EN o
// conteúdo do item permanece PT com marcação honesta (decisão da spec 067).
// A notícia da capa é o achado mais RECENTE do Radar (desempate: maior impacto,
// depois ordem do arquivo). Escolher por dado e não pela primeira linha: o RADAR.md
// é editado por um agente agendado e sua ordem física não é garantia de cronologia.
function noticiaDoRadar() {
  const peso = { A: 3, B: 2, C: 1, "": 0 };
  try {
    const radar = readFileSync(resolve(RAIZ, "radar/RADAR.md"), "utf8");
    let melhor = null;
    for (const linha of radar.split("\n")) {
      const cels = linha.split("|").map((c) => c.trim());
      if (cels.length < 7 || !/^\d{4}-\d{2}-\d{2}$/.test(cels[1])) continue;
      if (cels[2].includes("(inicial)")) continue;
      const impacto = (cels[4].match(/[ABC]/) || [])[0] || "";
      const cand = { data: cels[1], item: cels[2], impacto };
      if (!melhor || cand.data > melhor.data ||
          (cand.data === melhor.data && peso[cand.impacto] > peso[melhor.impacto])) melhor = cand;
    }
    if (melhor) return { data: melhor.data, itemHtml: md.renderInline(melhor.item), impacto: melhor.impacto };
  } catch {}
  return null;
}
function ultimaEdicao() {
  try {
    const hist = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
    const m = hist.match(/^###\s+Edição\s+(\d+\.\d+)\s+—\s+(\d{4}-\d{2}-\d{2})\s+·\s+(.+)$/m);
    if (m) return { versao: `v${m[1]}.0`, data: m[2], titulo: m[3].replace(/\s*\(spec \d+\)\s*$/, "") };
  } catch {}
  return null;
}
const noticia = noticiaDoRadar();
const edicao = ultimaEdicao();
const impactoRotulo = (i) => (EN ? `impact ${i}` : `impacto ${i}`);

// Tela-capa (splash) full-screen: porta de entrada do site, sem sidebar.
function paginaSplash() {
  const versao = versaoDoLivro();
  const atualizado = dataDaUltimaModificacao();
  return `<!doctype html>
<html lang="${T.htmlLang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${sumario.titulo}</title>
<meta name="description" content="${sumario.subtitulo}">
<meta property="og:type" content="website">
<meta property="og:title" content="${sumario.titulo}">
<meta property="og:description" content="${sumario.subtitulo}">
<meta property="og:image" content="${SITE}assets/capa-social.png">
<meta name="twitter:card" content="summary_large_image">
${hreflangs("index")}
<link rel="icon" type="image/svg+xml" href="${A}favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="${A}favicon-32.png">
<link rel="apple-touch-icon" href="${A}apple-touch-icon.png">
<link rel="stylesheet" href="${A}estilo.css">
</head><body class="splash-body" data-lang="${LANG}">
${pillIdioma("index")}
<main class="splash">
  <div class="splash-arte">
    <img src="${A}capa.png" width="1024" height="1536" loading="eager"
      alt="${T.splashAlt}">
  </div>
  <div class="splash-texto">
    <h1>${sumario.titulo}</h1>
    <p class="splash-sub">${sumario.subtitulo}</p>
    <p class="splash-desc">${T.splashDesc}</p>
    <div class="splash-ctas">
      <a class="btn btn-primario btn-grande" href="sumario.html">${T.entrarLivro}</a>
      <a class="btn btn-escuro" href="${T.hrefComparativo}">${T.benchmarkBtn}</a>
      <a class="btn btn-escuro" href="${T.hrefGuia}">${T.guiaBtn}</a>
    </div>
    ${noticia
      ? `<div class="splash-news"><span class="splash-news-k">${T.newsKicker} · ${noticia.data}${noticia.impacto ? ` · <b class="splash-news-imp">${impactoRotulo(noticia.impacto)}</b>` : ""}${T.newsPt}</span><p>${noticia.itemHtml}</p><a class="splash-news-mais" href="${EN ? "../radar.html" : "radar.html"}">${T.verRadar}</a></div>`
      : ""}
    ${edicao
      ? `<p class="splash-vedicao">📖 ${T.nestaEdicao} (<b>${edicao.versao}</b> · ${edicao.data}): ${edicao.titulo} — <a href="${T.hrefHistorico}">${T.historicoNome}</a></p>`
      : ""}
    <p class="splash-creditos">${T.creditos}</p>
    <p class="splash-versao"><span class="splash-versao-num">${versao}</span> · ${T.atualizadoEm} ${atualizado}</p>
    <p class="splash-doi"><a href="https://doi.org/10.5281/zenodo.21632412">DOI: 10.5281/zenodo.21632412</a></p>
  </div>
</main>
<script src="${A}app.js"></script>
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
            if (!i.arquivo) return `<li><a href="${i.externo}">${i.titulo}</a></li>`;
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
mkdirSync(SAIDA, { recursive: true });

if (!EN) {
  mkdirSync(resolve(SAIDA, "assets"), { recursive: true });
  cpSync(resolve(AQUI, "tema/estilo.css"), resolve(SAIDA, "assets/estilo.css"));
  cpSync(resolve(AQUI, "tema/app.js"), resolve(SAIDA, "assets/app.js"));
  cpSync(resolve(AQUI, "tema/capa.png"), resolve(SAIDA, "assets/capa.png"));
  cpSync(resolve(AQUI, "tema/capa-social.png"), resolve(SAIDA, "assets/capa-social.png"));
  cpSync(resolve(AQUI, "tema/autor.png"), resolve(SAIDA, "assets/autor.png"));
  cpSync(resolve(AQUI, "tema/harness-diagrama.svg"), resolve(SAIDA, "assets/harness-diagrama.svg"));
  cpSync(resolve(RAIZ, "harness-um/assets/harness-um.svg"), resolve(SAIDA, "assets/harness-um.svg"));
  cpSync(resolve(AQUI, "tema/companion.css"), resolve(SAIDA, "assets/companion.css"));
  cpSync(resolve(AQUI, "tema/companion.js"), resolve(SAIDA, "assets/companion.js"));
  cpSync(resolve(AQUI, "tema/uso.js"), resolve(SAIDA, "assets/uso.js"));
  cpSync(resolve(AQUI, "tema/grafo.js"), resolve(SAIDA, "assets/grafo.js"));
  cpSync(resolve(AQUI, "tema/favicon.svg"), resolve(SAIDA, "assets/favicon.svg"));
  cpSync(resolve(AQUI, "tema/favicon-32.png"), resolve(SAIDA, "assets/favicon-32.png"));
  cpSync(resolve(AQUI, "tema/apple-touch-icon.png"), resolve(SAIDA, "assets/apple-touch-icon.png"));
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
}

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
  const sinc = EN ? seloDeSincronia(bruto, item.slug) : "";
  let corpo = marcarCallouts(md.render(bruto, { srcDir: dirname(item.arquivo) }));
  corpo = marcarLeituraExec(corpo); // C08 (spec 043)
  if (EN) corpo = corpo.replace(/(src|href)="assets\//g, '$1="../assets/'); // assets compartilhados na raiz
  if (EN) corpo = corpo.replace('<div data-viz="grafo-livro">', '<div data-viz="grafo-livro" data-src="../assets/grafo.en.json">');

  // C01 CabeçalhoDeCapítulo (spec 043, variante B): só páginas numeradas.
  let hero = null;
  const { num, texto } = dividirTitulo(item.titulo);
  if (num) {
    const { cap, rev } = extrairDatas(bruto);
    const chips = [
      cap ? `<span title="${T.seloVivo}">🕒 ${T.estadoArte} ${cap}</span>` : "",
      rev ? `<span>${T.revisao} ${rev}</span>` : "",
      `<span>📖 ~${tempoDeLeitura(bruto)} ${T.minLeitura}</span>`,
      `<a class="cap-dl" href="md/${item.slug}.md" download title="${T.dlMd}">⬇ md</a>`,
      `<a class="cap-dl" href="pdf/${item.slug}.pdf" title="${T.dlPdf}">⬇ pdf</a>`,
    ].join("");
    hero = `<header class="cap-hero"><div class="cap-num" aria-hidden="true">${num}</div>
<div class="cap-kicker">${item.parte} · ${T.capKicker} ${num}</div>
<h1>${texto}</h1>
${item.teaser ? `<p class="cap-teaser">${item.teaser}</p>` : ""}
<div class="cap-meta">${chips}</div></header>`;
    corpo = corpo.replace(/<h1[^>]*>[\s\S]*?<\/h1>\s*/, "");
    corpo = corpo.replace(new RegExp("<blockquote>\\s*<p><strong>" + RE_CAPTURA.source + "[\\s\\S]*?<\\/blockquote>\\s*"), "");
  }

  if (item.slug !== "glossario" && item.slug !== "glossary") corpo = abrirSiglas(corpo);
  const html = pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: item.titulo,
    corpo,
    navLateral: montarNavLateral(item.slug),
    prev: k === 0 ? { slug: "sumario", titulo: T.sumarioTitulo } : itens[k - 1],
    next: itens[k + 1],
    data,
    chapter: capituloDe(item.titulo),
    slug: item.slug,
    hero,
    sinc,
  });
  writeFileSync(resolve(SAIDA, `${item.slug}.html`), html);
  gerados++;
}

// Downloads (spec 045): fontes .md publicados + consolidado (por idioma).
mkdirSync(resolve(SAIDA, "md"), { recursive: true });
{
  const partesMd = [];
  for (const item of itens) {
    const caminho = resolve(RAIZ, item.arquivo);
    if (!existsSync(caminho)) continue;
    const bruto = readFileSync(caminho, "utf8");
    writeFileSync(resolve(SAIDA, "md", `${item.slug}.md`), bruto);
    partesMd.push(bruto.trim());
  }
  const cabecalho = `# ${sumario.titulo}\n\n> ${sumario.subtitulo}\n>\n> ${versaoDoLivro()} · DOI ${DOI} · fonte: https://github.com/GHDaru/harness_engineering · site: ${SITE}\n\n---\n\n`;
  writeFileSync(resolve(SAIDA, T.mdLivro), cabecalho + partesMd.join("\n\n---\n\n") + "\n");
}

// Knowledge Graph (spec 057): derivado do conteúdo PT a cada build. Na passada
// EN, os nós de capítulo são remapeados para rótulos/URLs EN (grafo.en.json).
if (!EN) {
  const grafo = gerarGrafo(itens, RAIZ, versaoDoLivro());
  writeFileSync(resolve(SAIDA, "assets/grafo.json"), JSON.stringify(grafo));
  console.log(`✓ Grafo do livro: ${grafo.nos.length} nós, ${grafo.arestas.length} arestas`);
} else {
  try {
    const grafo = JSON.parse(readFileSync(resolve(RAIZ, "docs/assets/grafo.json"), "utf8"));
    const tituloEnDe = {};
    itens.forEach((i) => (tituloEnDe[parDe[i.slug]] = i)); // slug PT -> item EN
    for (const n of grafo.nos) {
      if (n.tipo !== "capitulo") continue;
      const ptSlug = (n.url || "").replace(/\.html$/, "");
      const itemEn = tituloEnDe[ptSlug];
      if (itemEn) {
        n.url = `${itemEn.slug}.html`;
        n.rotulo = dividirTitulo(itemEn.titulo).num ? `${dividirTitulo(itemEn.titulo).num} ${dividirTitulo(itemEn.titulo).texto}` : itemEn.titulo;
      }
    }
    writeFileSync(resolve(RAIZ, "docs/assets/grafo.en.json"), JSON.stringify(grafo));
  } catch (e) {
    console.warn("  aviso: grafo.en.json não gerado:", e.message);
  }
}

// index = tela-capa (splash); porta de entrada (por idioma).
writeFileSync(resolve(SAIDA, "index.html"), paginaSplash());

// sumario.html = a EXPERIÊNCIA DE ENTRADA (spec 021), por idioma.
const cartaoEnt = (i) => {
  const s = slugDe(i.arquivo);
  const { num, texto } = dividirTitulo(i.titulo);
  return `<a class="ent-card" href="${s}.html">${num ? `<span class="ent-badge">${num}</span>` : ""}<span class="ent-ct">${texto}</span>${i.teaser ? `<span class="ent-cd">${i.teaser}</span>` : ""}</a>`;
};
const pillEnt = (i) =>
  i.arquivo
    ? `<a class="ent-pill" href="${slugDe(i.arquivo)}.html">${dividirTitulo(i.titulo).texto}</a>`
    : `<a class="ent-pill" href="${i.externo}">${dividirTitulo(i.titulo).texto}</a>`;
const blocosCartao = sumario.partes
  .filter((p) => T.partesCartao.has(p.nome))
  .map((p) => `<div class="ent-parte"><span>${p.nome}</span><i></i></div><div class="ent-grid">${p.itens.map(cartaoEnt).join("")}</div>`)
  .join("");
const pillsEnt = sumario.partes.filter((p) => !T.partesCartao.has(p.nome)).flatMap((p) => p.itens).map(pillEnt).join("");

// News da entrada (spec 061) — fontes PT; chrome no idioma da página.
const blocoNews = (noticia
  ? `<div class="ent-news"><span class="ent-news-k">${EN ? "🗞 Living-book Radar" : "🗞 Radar do livro vivo"} · ${noticia.data}${noticia.impacto ? ` · ${impactoRotulo(noticia.impacto)}` : ""}${T.newsPt}</span><p>${noticia.itemHtml}</p><a class="ent-news-mais" href="${EN ? "../radar.html" : "radar.html"}">${T.verRadar}</a></div>`
  : "") + (edicao
  ? `<p class="ent-vedicao">📖 ${T.nestaEdicao} (<b>${edicao.versao}</b> · ${edicao.data}): ${edicao.titulo} — <a href="${T.hrefHistorico}">${T.historicoNome}</a></p>`
  : "");

const trilhaHtml = T.trilha
  .map(([href, n, b, s]) => `<a class="ent-step" href="${href}"><span class="ent-step-n">${n}</span><b>${b}</b><span>${s}</span></a>`)
  .join("\n    ");

const corpoSumario = `<section class="entrada">
  <div class="ent-hero">
    <img class="ent-capa" src="${A}capa.png" width="1024" height="1536" loading="eager" alt="${T.splashAlt}">
    <div class="ent-hero-txt">
      <div class="ent-kicker">${T.kickerEntrada} · ${versaoDoLivro()} · DOI ${DOI}</div>
      <h1 class="ent-titulo">${sumario.titulo}</h1>
      <p class="ent-sub">${sumario.subtitulo}</p>
      <div class="ent-ctas">
        <a class="ent-btn ent-btn-a" href="${itens[0].slug}.html">${T.comecar}</a>
        <a class="ent-btn" href="${T.hrefComparativo}">${T.benchmarkBtn}</a>
        <a class="ent-btn" href="${T.hrefGuia}">${T.guiaBtn}</a>
        <a class="ent-btn" href="${T.pdfLivro}" title="${T.pdfLivroTitulo}">⬇ PDF</a>
        <a class="ent-btn" href="${T.mdLivro}" download title="${T.mdLivroTitulo}">⬇ Markdown</a>
      </div>
    </div>
  </div>
  ${blocoNews}
  <a class="ent-retomar" id="ent-retomar" href="#" hidden>
    <span class="ent-ret-l"><span class="ent-ret-lab">${T.continueLendo}</span><span class="ent-ret-cap" id="ent-ret-cap"></span></span>
    <span class="ent-btn ent-btn-a">${T.retomar}</span>
  </a>
  <div class="ent-trilha">
    ${trilhaHtml}
  </div>
  ${blocosCartao}
  <div class="ent-parte"><span>${T.pillsRotulo}</span><i></i></div>
  <div class="ent-pills">${pillsEnt}</div>
</section>`;
writeFileSync(
  resolve(SAIDA, "sumario.html"),
  pagina({
    tituloLivro: sumario.titulo,
    tituloPagina: T.sumarioTitulo,
    corpo: corpoSumario,
    navLateral: montarNavLateral("sumario"),
    prev: null,
    next: itens[0],
    data: null,
    ehIndex: true,
    slug: "sumario",
  })
);

// Radar-jornal (spec 071): docs/radar.html — o diário do Radar diagramado
// como site de notícias (PT-only; registro operacional, decisão da 067).
if (!EN) {
  const jornal = gerarJornal(RAIZ, md, versaoDoLivro());
  if (jornal) {
    writeFileSync(
      resolve(SAIDA, "radar.html"),
      pagina({
        tituloLivro: sumario.titulo,
        tituloPagina: "Radar — o jornal do livro vivo",
        corpo: jornal,
        navLateral: montarNavLateral("radar"),
        prev: null, next: null, data: null, slug: "radar",
      })
    );
    console.log("✓ Radar-jornal: docs/radar.html");
  }
}

// Portão de qualidade (T402): links internos .html apontam para páginas
// existentes NO MESMO idioma; "../" cruza para o outro idioma (validado lá).
const paginas = new Set(itens.map((i) => `${i.slug}.html`).concat("index.html", "sumario.html", EN ? [] : ["radar.html"]));
const quebrados = [];
for (const i of [...itens, { slug: "index" }, { slug: "sumario" }]) {
  const arq = resolve(SAIDA, `${i.slug}.html`);
  if (!existsSync(arq)) continue;
  const html = readFileSync(arq, "utf8");
  for (const m of html.matchAll(/href="([^"]+)"/g)) {
    const href = m[1];
    if (/^https?:|^#|^mailto:|^\/\//.test(href)) continue;
    if (!/\.html(#|$)/.test(href)) continue;
    if (href.includes("../") || href.startsWith("en/")) continue; // cruza idiomas
    const alvo = basename(href.split("#")[0]);
    if (!paginas.has(alvo)) quebrados.push(`${i.slug}.html → ${href}`);
  }
}
if (quebrados.length) {
  console.error(`✗ ${quebrados.length} link(s) interno(s) quebrado(s):`);
  quebrados.forEach((q) => console.error("   " + q));
  process.exit(1);
}

console.log(`✓ Livro gerado [${LANG}]: ${gerados} páginas + capa em ${EN ? "docs/en/" : "docs/"} (links internos OK)`);
