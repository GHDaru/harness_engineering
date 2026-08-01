// Radar-jornal (spec 071): transforma radar/diario/*.md numa página estilo
// site de notícias (docs/radar.html). Filosofia: o diário É a apuração; o
// jornal é só a diagramação — parse tolerante, e se algo não casar o bloco
// cai no modo "matéria corrida" (o jornal nunca quebra por causa do formato).
// Página PT-only (registro operacional, decisão da spec 067).

import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

const IMPACTO_RE = /\*\*Impacto\s+([ABC])[^*]*\*\*|\*\*([ABC])(?:\/[ABC])?\*\*\s*(?:—|\()/;

function dominio(url) {
  try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return url.slice(0, 30); }
}

// Um bloco "# Título" -> { titulo, achados[], caixas[] }
function parseBloco(bloco, md) {
  const tituloBloco = (bloco.match(/^#\s+(.+)$/m) || [])[1] || "";
  const secoes = bloco.split(/^##\s+/m).slice(1); // cada uma começa com o título da seção
  const achados = [], caixas = [];
  for (const s of secoes) {
    const nome = (s.match(/^(.+)$/m) || [])[1].trim();
    const corpo = s.slice(s.indexOf("\n") + 1).trim();
    if (/^achados/i.test(nome)) {
      const artigos = corpo.split(/^###\s+/m).filter((a) => a.trim());
      for (const a of artigos) {
        if (!/^\S/.test(a)) continue;
        const t = (a.match(/^(.+)$/m) || [])[1].trim();
        const corpoArt = a.slice(a.indexOf("\n") + 1).trim();
        if (!t || !corpoArt) continue;
        const impacto = (corpoArt.match(IMPACTO_RE) || []).slice(1).find(Boolean) || "";
        const fontes = [...corpoArt.matchAll(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g)]
          .map((m) => ({ nome: m[1].replace(/[*_`]/g, ""), url: m[2] }));
        achados.push({ titulo: t.replace(/[*_`]/g, "").replace(/^\d+\.\s*/, ""), html: md.render(corpoArt), impacto, fontes });
      }
    } else if (/^consultas/i.test(nome)) {
      caixas.push({ tipo: "consultas", nome: "Como esta edição foi apurada", html: md.render(corpo) });
    } else if (/^descartes/i.test(nome)) {
      caixas.push({ tipo: "descartes", nome: "Da redação: o que ficou de fora — e por quê", html: md.render(corpo) });
    } else if (/leituras executivas/i.test(nome)) {
      caixas.push({ tipo: "risco", nome: "Leituras executivas em risco", html: md.render(corpo) });
    } else {
      caixas.push({ tipo: "outra", nome, html: md.render(corpo) });
    }
  }
  // Bloco sem estrutura reconhecível -> matéria corrida
  if (!achados.length && !caixas.length && bloco.trim()) {
    caixas.push({ tipo: "outra", nome: tituloBloco || "Registro", html: md.render(bloco.replace(/^#\s+.+$/m, "").trim()) });
  }
  return { tituloBloco, achados, caixas };
}

export function gerarJornal(RAIZ, md, versao) {
  const dir = resolve(RAIZ, "radar/diario");
  let arquivos = [];
  try {
    arquivos = readdirSync(dir).filter((f) => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort().reverse();
  } catch {}
  if (!arquivos.length) return null;

  const pesoImp = { A: 3, B: 2, "": 0, C: 1 };
  const edicoes = arquivos.map((f) => {
    const data = f.replace(".md", "");
    const texto = readFileSync(resolve(dir, f), "utf8");
    // blocos de nível 1 (execuções/adendos do mesmo dia)
    const blocos = ("\n" + texto).split(/\n(?=#\s)/).filter((b) => b.trim()).map((b) => parseBloco(b, md));
    const achados = blocos.flatMap((b) => b.achados);
    const caixas = blocos.flatMap((b) => b.caixas);
    achados.sort((x, y) => (pesoImp[y.impacto] || 0) - (pesoImp[x.impacto] || 0));
    return { data, achados, caixas };
  });

  const badge = (i) => (i ? `<span class="jr-imp jr-imp-${i.toLowerCase()}">impacto ${i}</span>` : "");
  const chipsFontes = (fontes) => {
    const vistos = new Set();
    const chips = fontes.filter((f) => !vistos.has(f.url) && vistos.add(f.url)).slice(0, 5)
      .map((f) => `<a class="jr-fonte" href="${f.url}" title="${f.nome.replace(/"/g, "&quot;")}">${dominio(f.url)}</a>`).join("");
    return chips ? `<div class="jr-fontes"><span>Fontes</span>${chips}</div>` : "";
  };
  const artigo = (a, lead = false) => `<article class="jr-card${lead ? " jr-lead" : ""}">
    <div class="jr-kicker">${badge(a.impacto)}${lead ? '<span class="jr-manchete-tag">manchete</span>' : ""}</div>
    <h3>${a.titulo}</h3>
    <div class="jr-corpo">${a.html}</div>
    ${chipsFontes(a.fontes)}
  </article>`;

  const nav = edicoes.map((e, i) => `<a class="jr-tab${i === 0 ? " ativo" : ""}" href="#ed-${e.data}">${e.data}</a>`).join("");

  const corpoEdicoes = edicoes.map((e, i) => {
    const [lead, ...resto] = e.achados;
    const caixasHtml = e.caixas.map((c) =>
      c.tipo === "consultas"
        ? `<details class="jr-caixa jr-consultas"><summary>${c.nome}</summary>${c.html}</details>`
        : `<aside class="jr-caixa jr-${c.tipo}"><h4>${c.nome}</h4>${c.html}</aside>`
    ).join("\n");
    return `<section class="jr-edicao" id="ed-${e.data}">
      <div class="jr-data"><span>Edição de</span><b>${e.data}</b>${i === 0 ? '<span class="jr-hoje">mais recente</span>' : ""}</div>
      ${lead ? artigo(lead, true) : ""}
      ${resto.length ? `<div class="jr-grid">${resto.map((a) => artigo(a)).join("\n")}</div>` : ""}
      ${caixasHtml}
    </section>`;
  }).join("\n");

  return `<div class="jornal">
  <header class="jr-masthead">
    <div class="jr-marca">🗞 <b>RADAR</b> — o jornal do livro vivo</div>
    <p class="jr-tagline">Apurado diariamente por um agente sob <a href="${"https://github.com/GHDaru/harness_engineering/blob/main/radar/AGENTE.md"}">contrato editorial</a>; nada entra no livro sem curadoria humana. Toda afirmação com fonte verificável — itens incertos levam ⏳.</p>
    <nav class="jr-tabs">${nav}</nav>
  </header>
  ${corpoEdicoes}
  <footer class="jr-rodape">A <a href="${"https://github.com/GHDaru/harness_engineering/blob/main/radar/RADAR.md"}">mesa de edição</a> (tabela priorizada, com status de promoção) · ${versao} · <a href="index.html">↩ capa</a></footer>
</div>`;
}
