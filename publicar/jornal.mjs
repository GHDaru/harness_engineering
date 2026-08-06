// Radar-jornal (specs 071 e 076): transforma radar/diario/*.md num jornal com
// duas camadas — a CAPA (últimas 7 edições, sempre leve) e o ACERVO (uma página
// por mês). Filosofia: o diário É a apuração; o jornal é só a diagramação — parse
// tolerante, e se algo não casar o bloco cai no modo "matéria corrida" (o jornal
// nunca quebra por causa do formato). Página PT-only (decisão da spec 067).
//
// Por que paginar por mês (076): com uma página só, a fita de abas vira parede de
// datas em ~3 semanas e o HTML passa de 3 MB em um ano. Paginando, o crescimento é
// horizontal (mais páginas) e nenhuma página passa de ~300 KB. A capa também deixa
// de ser só cronologia: ganha o placar da semana e a mesa de edição (RADAR.md),
// que respondem "o que mudou?" e "o que espera decisão?" — as perguntas reais.

import { readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

const IMPACTO_RE = /\*\*Impacto\s+([ABC])[^*]*\*\*|\*\*([ABC])(?:\/[ABC])?\*\*\s*(?:—|\()/;
const EDICOES_NA_CAPA = 7; // decisão do editor (076): cobre a semana
const MESA_MAX = 5;        // decisão do editor (076): chamado à ação, não inventário
const GH = "https://github.com/GHDaru/harness_engineering/blob/main/";

const MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
  "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"];
const pesoImp = { A: 3, B: 2, C: 1, "": 0 };
const rotuloMes = (ym) => {
  const [a, m] = ym.split("-");
  return `${MESES[Number(m) - 1]} de ${a}`;
};
const curtaData = (d) => {
  const [, m, dia] = d.split("-");
  return `${dia}/${MESES[Number(m) - 1].slice(0, 3)}`;
};

function dominio(url) {
  try { return new URL(url).hostname.replace(/^www\./, ""); } catch { return url.slice(0, 30); }
}

// Um bloco "# Título" -> { titulo, achados[], caixas[] }
function parseBloco(bloco, md) {
  const tituloBloco = (bloco.match(/^#\s+(.+)$/m) || [])[1] || "";
  const secoes = bloco.split(/^##\s+/m).slice(1);
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
  if (!achados.length && !caixas.length && bloco.trim()) {
    caixas.push({ tipo: "outra", nome: tituloBloco || "Registro", html: md.render(bloco.replace(/^#\s+.+$/m, "").trim()) });
  }
  return { tituloBloco, achados, caixas };
}

function lerEdicoes(RAIZ, md) {
  const dir = resolve(RAIZ, "radar/diario");
  let arquivos = [];
  try {
    arquivos = readdirSync(dir).filter((f) => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).sort().reverse();
  } catch { return []; }
  return arquivos.map((f) => {
    const data = f.replace(".md", "");
    const texto = readFileSync(resolve(dir, f), "utf8");
    const blocos = ("\n" + texto).split(/\n(?=#\s)/).filter((b) => b.trim()).map((b) => parseBloco(b, md));
    const achados = blocos.flatMap((b) => b.achados);
    const caixas = blocos.flatMap((b) => b.caixas);
    achados.sort((x, y) => (pesoImp[y.impacto] || 0) - (pesoImp[x.impacto] || 0));
    return { data, mes: data.slice(0, 7), achados, caixas };
  });
}

// A mesa é chamado à ação, não inventário: o item da tabela é longo por natureza
// (descreve o achado inteiro), então aqui fica só a cabeça dele. Corta no primeiro
// travessão — que nessas linhas separa o "o quê" do "por quê" — e, se ainda ficar
// longo, no último fecha-parênteses antes do limite (nunca no meio de um link).
function resumo(fonte, limite = 150) {
  let t = fonte.split(" — ")[0];
  if (t.length < 20) t = fonte;
  if (t.length > limite) {
    const corte = t.lastIndexOf(")", limite);
    t = (corte > 40 ? t.slice(0, corte + 1) : t.slice(0, limite)) + "…";
  }
  // O corte pode cair dentro de um link (os parênteses do texto enganam o
  // lastIndexOf): se sobrou "[" sem "]", volta para antes dele — melhor perder
  // meia frase do que vazar sintaxe de markdown na tela.
  const abre = (t.match(/\[/g) || []).length, fecha = (t.match(/\]/g) || []).length;
  if (abre > fecha) t = t.slice(0, t.lastIndexOf("[")).replace(/[\s:·,]+$/, "") + "…";
  return t;
}

// A mesa de edição: a tabela do RADAR.md é o dado mais acionável do Radar e não
// aparecia no site. Aqui entram só os itens ABERTOS de impacto A/B (decisão 076).
function lerMesa(RAIZ, md) {
  const abertos = [], promovidos = [];
  let texto = "";
  try { texto = readFileSync(resolve(RAIZ, "radar/RADAR.md"), "utf8"); } catch { return { abertos, promovidos }; }
  for (const linha of texto.split("\n")) {
    const c = linha.split("|").map((x) => x.trim());
    if (c.length < 7 || !/^\d{4}-\d{2}-\d{2}$/.test(c[1])) continue;
    if (c[2].includes("(inicial)")) continue;
    const impacto = (c[4].match(/[ABC]/) || [])[0] || "";
    const status = c[6] || "";
    const item = { data: c[1], html: md.renderInline(resumo(c[2])), cap: c[3], impacto, acao: md.renderInline(resumo(c[5] || "", 100)), status };
    if (/^promovid/i.test(status)) promovidos.push(item);
    else if (!/descartad|conferid|confirmado|datado/i.test(status) && (impacto === "A" || impacto === "B")) abertos.push(item);
  }
  abertos.sort((x, y) => (pesoImp[y.impacto] - pesoImp[x.impacto]) || y.data.localeCompare(x.data));
  return { abertos: abertos.slice(0, MESA_MAX), promovidos, totalAbertos: abertos.length };
}

// ---------- componentes ----------

const badge = (i) => (i ? `<span class="jr-imp jr-imp-${i.toLowerCase()}">impacto ${i}</span>` : "");

const chipsFontes = (fontes) => {
  const vistos = new Set();
  const chips = fontes.filter((f) => !vistos.has(f.url) && vistos.add(f.url)).slice(0, 5)
    .map((f) => `<a class="jr-fonte" href="${f.url}" title="${f.nome.replace(/"/g, "&quot;")}">${dominio(f.url)}</a>`).join("");
  return chips ? `<div class="jr-fontes"><span>Fontes</span>${chips}</div>` : "";
};

const artigo = (a, lead = false) => `<article class="jr-card${lead ? " jr-lead" : ""}" data-imp="${a.impacto || "-"}">
    <div class="jr-kicker">${badge(a.impacto)}${lead ? '<span class="jr-manchete-tag">manchete</span>' : ""}</div>
    <h3>${a.titulo}</h3>
    <div class="jr-corpo">${a.html}</div>
    ${chipsFontes(a.fontes)}
  </article>`;

const caixasHtml = (caixas) => caixas.map((c) =>
  c.tipo === "consultas"
    ? `<details class="jr-caixa jr-consultas"><summary>${c.nome}</summary>${c.html}</details>`
    : `<aside class="jr-caixa jr-${c.tipo}"><h4>${c.nome}</h4>${c.html}</aside>`
).join("\n");

const masthead = (sub) => `<header class="jr-masthead">
    <div class="jr-marca">🗞 <b>RADAR</b> — o jornal do livro vivo</div>
    <p class="jr-tagline">Apurado diariamente por um agente sob <a href="${GH}radar/AGENTE.md">contrato editorial</a>; nada entra no livro sem curadoria humana. Toda afirmação com fonte verificável — itens incertos levam ⏳.</p>
    ${sub}
  </header>`;

// ---------- a capa ----------

function montarCapa(edicoes, mesa, meses, versao) {
  const recentes = edicoes.slice(0, EDICOES_NA_CAPA);
  const achados = recentes.flatMap((e) => e.achados);
  const ab = achados.filter((a) => a.impacto === "A" || a.impacto === "B").length;
  const janela = recentes.length ? recentes[recentes.length - 1].data : null;
  const promovidosRecentes = mesa.promovidos.filter((p) => janela && p.data >= janela).length;

  const placar = `<div class="jr-placar">
    <div><b>${recentes.length}</b><span>edições</span></div>
    <div><b>${achados.length}</b><span>achados</span></div>
    <div><b>${ab}</b><span>impacto A/B</span></div>
    <div><b>${promovidosRecentes}</b><span>promovidos</span></div>
  </div>`;

  const mesaHtml = mesa.abertos.length ? `<section class="jr-mesa">
    <h2>Na mesa <small>— o que espera decisão editorial</small></h2>
    <ul>${mesa.abertos.map((i) => `<li><i class="jr-imp jr-imp-${i.impacto.toLowerCase()}">${i.impacto}</i><div><b>cap. ${i.cap}</b> · ${i.html}<em>${i.acao}</em></div></li>`).join("")}</ul>
    <a class="jr-mesa-mais" href="${GH}radar/RADAR.md">mesa completa${mesa.totalAbertos > MESA_MAX ? ` — mais ${mesa.totalAbertos - MESA_MAX} em aberto` : ""} ↗</a>
  </section>` : "";

  const [lead, ...resto] = recentes[0] ? recentes[0].achados : [];
  const demais = recentes.slice(1);

  // Chips com contagem e desabilitados quando vazios: um filtro que zera a página
  // sem aviso é beco sem saída — o número diz de antemão o que há para ver.
  const conta = (i) => achados.filter((a) => a.impacto === i).length;
  const chip = (f, rotulo, n) =>
    `<button class="jr-chip${f === "todos" ? " ativo" : ""}" data-f="${f}"${n === 0 ? " disabled" : ""}>${rotulo}<span class="jr-chip-n">${n}</span></button>`;
  const filtros = `<div class="jr-filtros" role="group" aria-label="Filtrar por impacto">
    ${chip("todos", "todos", achados.length)}
    ${chip("A", "impacto A", conta("A"))}
    ${chip("B", "impacto B", conta("B"))}
    ${chip("C", "impacto C", conta("C"))}
  </div>`;

  const diasHtml = demais.map((e) => `<section class="jr-dia" id="ed-${e.data}">
      <h3 class="jr-dia-t"><span>${curtaData(e.data)}</span><small>${e.data}</small></h3>
      <div class="jr-grid">${e.achados.map((a) => artigo(a)).join("\n")}</div>
    </section>`).join("\n");

  const acervoLink = meses.length ? `<a class="jr-acervo-cta" href="radar-${meses[0].mes}.html">📚 Acervo completo — ${edicoes.length} edições em ${meses.length} ${meses.length === 1 ? "mês" : "meses"} →</a>` : "";

  return `<div class="jornal">
  ${masthead(placar)}
  ${mesaHtml}
  ${recentes[0] ? `<section class="jr-edicao jr-hoje-bloco">
    <div class="jr-data"><span>Edição de</span><b>${recentes[0].data}</b><span class="jr-hoje">mais recente</span></div>
    ${filtros}
    ${lead ? artigo(lead, true) : ""}
    ${resto.length ? `<div class="jr-grid">${resto.map((a) => artigo(a)).join("\n")}</div>` : ""}
    ${caixasHtml(recentes[0].caixas)}
  </section>` : "<p>Sem edições ainda.</p>"}
  ${demais.length ? `<h2 class="jr-secao-t">Dias anteriores</h2>${diasHtml}` : ""}
  ${acervoLink}
  <footer class="jr-rodape">A <a href="${GH}radar/RADAR.md">mesa de edição</a> (tabela priorizada, com status de promoção) · ${versao} · <a href="index.html">↩ capa</a></footer>
</div>
<script>
(function () {
  var chips = document.querySelectorAll(".jr-chip");
  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      var f = c.dataset.f;
      chips.forEach(function (o) { o.classList.toggle("ativo", o === c); });
      document.querySelectorAll(".jr-card").forEach(function (card) {
        card.hidden = f !== "todos" && card.dataset.imp !== f;
      });
      document.querySelectorAll(".jr-dia").forEach(function (d) {
        d.hidden = !d.querySelector(".jr-card:not([hidden])");
      });
    });
  });
})();
</script>`;
}

// ---------- uma página de acervo por mês ----------

function montarAcervo(mes, edicoes, meses, versao) {
  const i = meses.findIndex((m) => m.mes === mes);
  const ant = meses[i + 1], prox = meses[i - 1]; // meses vêm do mais novo para o mais antigo
  const achados = edicoes.flatMap((e) => e.achados).length;

  const nav = `<nav class="jr-acervo-nav">
    ${ant ? `<a href="radar-${ant.mes}.html">‹ ${rotuloMes(ant.mes)}</a>` : "<span></span>"}
    <b>${rotuloMes(mes)}</b>
    ${prox ? `<a href="radar-${prox.mes}.html">${rotuloMes(prox.mes)} ›</a>` : "<span></span>"}
  </nav>`;

  const corpo = edicoes.map((e, k) => `<details class="jr-arq-ed" id="ed-${e.data}"${k === 0 ? " open" : ""}>
      <summary>
        <span class="jr-arq-data">${curtaData(e.data)}</span>
        <span class="jr-arq-resumo">${e.achados.slice(0, 3).map((a) => a.titulo).join(" · ") || "registro"}</span>
        <span class="jr-arq-imps">${e.achados.map((a) => a.impacto).filter(Boolean).map((x) => `<i class="jr-imp jr-imp-${x.toLowerCase()}">${x}</i>`).join("")}</span>
      </summary>
      ${e.achados.map((a) => artigo(a)).join("\n")}
      ${caixasHtml(e.caixas)}
    </details>`).join("\n");

  return `<div class="jornal jornal-acervo">
  ${masthead(`<p class="jr-acervo-k">📚 Acervo · ${edicoes.length} ${edicoes.length === 1 ? "edição" : "edições"} · ${achados} achados</p>`)}
  ${nav}
  ${corpo}
  ${nav}
  <footer class="jr-rodape"><a href="radar.html">↩ capa do Radar</a> · <a href="${GH}radar/RADAR.md">mesa de edição</a> · ${versao}</footer>
</div>`;
}

// ---------- API ----------

/** Devolve [{ arquivo, titulo, html }] — a capa e uma página por mês. */
export function gerarJornal(RAIZ, md, versao) {
  const edicoes = lerEdicoes(RAIZ, md);
  if (!edicoes.length) return null;

  const porMes = new Map();
  for (const e of edicoes) {
    if (!porMes.has(e.mes)) porMes.set(e.mes, []);
    porMes.get(e.mes).push(e);
  }
  const meses = [...porMes.keys()].sort().reverse().map((mes) => ({ mes, edicoes: porMes.get(mes) }));
  const mesa = lerMesa(RAIZ, md);

  return [
    { arquivo: "radar.html", titulo: "Radar — o jornal do livro vivo", html: montarCapa(edicoes, mesa, meses, versao) },
    ...meses.map(({ mes, edicoes: eds }) => ({
      arquivo: `radar-${mes}.html`,
      titulo: `Radar — acervo de ${rotuloMes(mes)}`,
      html: montarAcervo(mes, eds, meses, versao),
    })),
  ];
}
