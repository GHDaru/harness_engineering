// Knowledge Graph do livro (spec 057) — extração DETERMINÍSTICA, sem LLM.
// Nós: capítulos, harnesses do corpus, conceitos-chave, etapas do harness-zero.
// Arestas: menções reais no texto (peso = nº de ocorrências) — evidência verificável.
// Chamado pelo build.mjs a cada build ⇒ o grafo acompanha toda mudança do livro.

import { readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

// Os 16 sistemas do corpus (apêndice do estudo), com variantes de grafia.
const HARNESSES = [
  { id: "opencode", rotulo: "opencode", re: /\bopencode\b/gi },
  { id: "gemini-cli", rotulo: "gemini-cli", re: /\bgemini-cli\b/gi },
  { id: "openharness", rotulo: "OpenHarness", re: /\bOpenHarness\b/gi },
  { id: "codex-cli", rotulo: "Codex CLI", re: /\bCodex(?:\s+CLI)?\b/g },
  { id: "goose", rotulo: "Goose", re: /\bGoose\b/g },
  { id: "aider", rotulo: "Aider", re: /\bAider\b/gi },
  { id: "openhands", rotulo: "OpenHands", re: /\bOpenHands\b/g },
  { id: "openclaw", rotulo: "OpenClaw", re: /\bOpenClaw\b/g },
  { id: "hermes", rotulo: "Hermes", re: /\bHermes(?:\s+Agent)?\b/g },
  { id: "ironclaw", rotulo: "IronClaw", re: /\bIronClaw\b/g },
  { id: "ohmo", rotulo: "ohmo", re: /\bohmo\b/gi },
  { id: "n8n", rotulo: "n8n", re: /\bn8n\b/gi },
  { id: "langgraph", rotulo: "LangGraph", re: /\bLangGraph\b/gi },
  { id: "crewai", rotulo: "CrewAI", re: /\bCrewAI\b/gi },
  { id: "agents-sdk", rotulo: "OpenAI Agents SDK", re: /\b(?:OpenAI\s+)?Agents\s+SDK\b/g },
  { id: "software-agent-sdk", rotulo: "software-agent-sdk", re: /\bsoftware-agent-sdk\b/gi },
];

// Conceitos/protocolos com página própria de referência (glossário).
const CONCEITOS = [
  { id: "mcp", rotulo: "MCP", re: /\bMCP\b/g },
  { id: "a2a", rotulo: "A2A", re: /\bA2A\b/g },
  { id: "acp", rotulo: "ACP‑Zed/IBM", re: /\bACP\b/g },
  { id: "lsp", rotulo: "LSP", re: /\bLSP\b/g },
  { id: "rag", rotulo: "RAG", re: /\bRAG\b/g },
  { id: "mast", rotulo: "MAST", re: /\bMAST\b/g },
];

const ETAPAS = [
  "00 setup", "01 loop", "02 tools", "03 contexto", "04 sessões", "05 compactação",
  "06 permissões", "07 MCP", "08 plan", "09 subagentes", "10 evals", "11 hooks", "12 skills",
];

const GH = "https://github.com/GHDaru/harness_engineering/tree/main/harness-zero";

function contar(re, texto) {
  const m = texto.match(re);
  return m ? m.length : 0;
}

export function gerarGrafo(itens, RAIZ, versao) {
  const capitulos = itens.filter((i) => /^\s*\d+\s*—/.test(i.titulo));
  const nos = [];
  const arestas = [];
  const addAresta = (de, para, peso) => { if (peso > 0 && de !== para) arestas.push({ de, para, peso }); };

  for (const c of capitulos) {
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    nos.push({ id: "cap-" + num, tipo: "capitulo", rotulo: c.titulo, url: c.slug + ".html" });
  }
  for (const h of HARNESSES) nos.push({ id: h.id, tipo: "harness", rotulo: h.rotulo, url: "apendice-estudo.html" });
  for (const co of CONCEITOS) nos.push({ id: co.id, tipo: "conceito", rotulo: co.rotulo, url: "glossario.html" });
  ETAPAS.forEach((e, i) => {
    const n = String(i).padStart(2, "0");
    nos.push({ id: "etapa-" + n, tipo: "etapa", rotulo: "etapa " + e, url: GH });
  });

  for (const c of capitulos) {
    const caminho = resolve(RAIZ, c.arquivo);
    if (!existsSync(caminho)) continue;
    const num = c.titulo.match(/^\s*(\d+)/)[1];
    const id = "cap-" + num;
    // corpo sem blocos de código (código cita nomes por razões mecânicas, não conceituais)
    const texto = readFileSync(caminho, "utf8").replace(/```[\s\S]*?```/g, " ");

    // capítulo → capítulo ("cap. NN" / "capítulo NN")
    const porCap = {};
    for (const m of texto.matchAll(/\bcap(?:ítulos?|s?\.)\s*(\d{1,2})\b/gi)) {
      const alvo = String(parseInt(m[1], 10)).padStart(2, "0");
      if (alvo !== num && capitulos.some((x) => x.titulo.startsWith(alvo))) porCap[alvo] = (porCap[alvo] || 0) + 1;
    }
    for (const alvo of Object.keys(porCap)) addAresta(id, "cap-" + alvo, porCap[alvo]);

    for (const h of HARNESSES) addAresta(id, h.id, contar(h.re, texto));
    for (const co of CONCEITOS) addAresta(id, co.id, contar(co.re, texto));

    // capítulo → etapa ("etapa N" — tipicamente na Mão na massa)
    const porEtapa = {};
    for (const m of texto.matchAll(/\betapas?\s+(\d{1,2})\b/gi)) {
      const n = String(parseInt(m[1], 10)).padStart(2, "0");
      if (parseInt(n, 10) <= 12) porEtapa[n] = (porEtapa[n] || 0) + 1;
    }
    for (const n of Object.keys(porEtapa)) addAresta(id, "etapa-" + n, porEtapa[n]);
  }

  // poda: nós sem nenhuma aresta saem (mantém o grafo honesto)
  const conectados = new Set();
  arestas.forEach((a) => { conectados.add(a.de); conectados.add(a.para); });
  const nosFinais = nos.filter((n) => conectados.has(n.id));

  return { versao, nos: nosFinais, arestas };
}
