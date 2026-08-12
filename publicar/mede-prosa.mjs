// Medidor de prosa didática — camada v4 (specs 097/098, ADR 0011).
//
// Por que isto existe: o GUIA-EDITORIAL prescreve "uma ideia nova por vez" e
// "worked example antes de exercício" desde a primeira edição, e nada no
// processo perguntava se o texto cumpria. Prosa não é sensor — é a mesma lição
// do verifica-canonical.mjs (edição 0.79), aplicada ao próprio texto do livro.
//
// O que ele NÃO é: um detector de texto de IA. Os limiares vêm do
// writing_quality_check da suíte academic-research-skills, recalibrados para
// prosa didática em português: o travessão é pontuação normal em pt-BR, e o
// que se combate aqui é o empilhamento de apostos numa frase só, não o sinal.
//
// O que ele NÃO mede, e é preciso dizer: se o capítulo ensina. Todos os testes
// abaixo são sintáticos e medem AUSÊNCIA de defeito. O critério de parada da
// série (ADR 0011 §5) exige, por isso, leitura humana de capítulos sorteados.
//
// Capítulos ainda não reescritos apenas REPORTAM. Só os marcados como v4
// reprovam o build — caso contrário o portão nasceria vermelho e seria
// ignorado, que é o pior destino de um verificador.

import { readFileSync, existsSync, readdirSync } from "node:fs";
import { resolve, dirname, basename, join } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const LIMITES = {
  travessoesPor1k: 8,     // medido: 22,0 no livro inteiro antes da spec 097
  fraseMedia: 20,         // palavras
  fraseMaxima: 60,        // nenhuma frase acima disto sobrevive à leitura em voz alta
  linhasDoExemplo: 6,     // piso do bloco de código do exemplo trabalhado
};

// Andaime declarado no cabeçalho (ADR 0011 §3): o exemplo trabalhado desvanece
// ao longo do livro. Piso constante aplicaria metade da lição de Sweller —
// worked-example effect sem expertise-reversal effect.
const ANDAIMES = ["completo", "lacuna", "proprio"];

// Um capítulo `proprio` (síntese) não precisa de código novo: o exemplo é o
// harness que o leitor já construiu.
const EXIGE_CODIGO = new Set(["completo", "lacuna"]);

// --- as duas línguas, e tudo o que difere entre elas -------------------------
// Antes do ADR 0011 o medidor só enumerava PT, e três strings suas eram
// PT-hardcoded: metade do livro publicado não tinha portão nenhum, e o EN, se
// medido, seria medido errado (o "## Appendix A" não casava com o corte, então
// o apêndice inteiro entrava na conta de prosa).
const IDIOMAS = {
  pt: {
    dir: "livro",
    subdir: "capitulos",
    apendice: /^## Apêndice A/m,
    verificacao: /^## Verificação/m,
    gabarito: /^## Respostas da verificação/m,
    pratica: /^#{2,3} +Na prática/,
    marcador: /camada didática v4/i,
    andaime: /^> +andaime: *(\w+)/im,
  },
  en: {
    dir: "livro/en",
    subdir: "chapters",
    apendice: /^## Appendix A/m,
    verificacao: /^## (Verification|Check your understanding)/m,
    gabarito: /^## Verification answers/m,
    pratica: /^#{2,3} +In practice/,
    marcador: /didactic layer v4/i,
    andaime: /^> +scaffold: *(\w+)/im,
  },
};

// A lista de capítulos era montada com .filter(existsSync): um arquivo
// renomeado saía da medição SEM FALHAR. Agora ela é descoberta e conferida.
function capitulosDe(lang) {
  const c = IDIOMAS[lang];
  const raiz = resolve(RAIZ, c.dir);
  const soltos = readdirSync(raiz)
    .filter((f) => /^\d\d-.*\.md$/.test(f))
    .map((f) => join(c.dir, f));
  const emPasta = readdirSync(resolve(raiz, c.subdir))
    .filter((f) => /^\d\d-.*\.md$/.test(f))
    .map((f) => join(c.dir, c.subdir, f));
  return [...soltos, ...emPasta].sort((a, b) => basename(a).localeCompare(basename(b)));
}

// O Apêndice A é inventário por repositório: denso de propósito, e medi-lo
// como prosa de ensino seria medir a coisa errada.
function corpoDe(markdown, c) {
  return markdown.split(c.apendice)[0].replace(/```[\s\S]*?```/g, "");
}

// Frase é unidade de leitura em voz alta, e um item de lista termina no fim da
// linha mesmo sem ponto. Colapsar `\n` antes de dividir gluava uma lista inteira
// numa "frase" de 90 palavras. Linha de tabela, citação, cabeçalho e HTML não
// são prosa corrida — a matriz do cap. 17 usa `—` como célula de "não se
// aplica", e contá-la como pontuação punia o capítulo por ter tabela.
function frasesDe(texto) {
  return texto
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !/^([|>#]|<|!\[)/.test(l))
    .flatMap((linha) => linha.split(/(?<=[.!?])\s+/))
    .map((s) => s.replace(/^[-*\d.]+\s*/, "").trim())
    .filter((s) => s.split(/\s+/).length > 2);
}

// O exemplo trabalhado precisa de FORMA, não só de existir: um YAML de três
// linhas em qualquer lugar satisfazia o regex antigo (/```/). Isso é o
// reward hacking que o cap. 11 descreve — o portão não seria burlado por
// má-fé, seria satisfeito por um bloco que estava ali de qualquer jeito.
// Varre por linha com estado de cerca, e não por regex sobre o texto inteiro:
// um comentário `# ...` DENTRO de um bloco Python é indistinguível de um
// cabeçalho markdown para quem olha só o começo da linha, e isso encerrava a
// seção no meio do primeiro exemplo. Terceiro falso positivo deste medidor, e
// da mesma família dos outros dois — estrutura lida como se fosse marcação.
function exemploTrabalhado(md, c) {
  const linhas = md.split("\n");
  let dentro = false;
  let inicio = -1;
  let nivel = 0;
  const blocos = [];
  let atual = null;

  for (let i = 0; i < linhas.length; i++) {
    const l = linhas[i];
    const cerca = /^```(\w*)/.exec(l);

    if (cerca) {
      if (!dentro) { dentro = true; atual = { lang: cerca[1], linhas: 0 }; }
      else {
        dentro = false;
        if (inicio !== -1) blocos.push(atual);
        atual = null;
      }
      continue;
    }
    if (dentro) { if (atual) atual.linhas++; continue; }

    const h = /^(#+) /.exec(l);
    if (!h) continue;
    if (inicio === -1) {
      if (c.pratica.test(l)) { inicio = i; nivel = h[1].length; }
    } else if (h[1].length <= nivel) {
      break; // fim da seção
    }
  }

  if (inicio === -1) return { ok: false, motivo: "sem seção de exemplo trabalhado (Na prática / In practice)" };
  const comLingua = blocos.filter((b) => b.lang);
  if (!comLingua.length) return { ok: false, motivo: "seção de exemplo sem bloco de código com linguagem declarada" };
  const maior = Math.max(...comLingua.map((b) => b.linhas));
  if (maior < LIMITES.linhasDoExemplo)
    return { ok: false, motivo: `maior bloco do exemplo tem ${maior} linhas (piso ${LIMITES.linhasDoExemplo})` };
  return { ok: true, blocos: comLingua.length, linhas: maior };
}

// Caminhos de arquivo são a evidência do Princípio I. A reescrita pode MOVER
// um caminho do corpo para o Apêndice A; não pode apagá-lo. Sem baseline isso
// dependeria de atenção humana, uma vez por capítulo, catorze vezes.
// Um caminho de evidência tem extensão (`core/loop.rs`) ou termina em barra
// (`crates/ironclaw_agent_loop/`). Sem esse aperto, a contagem incluía comandos
// de barra (`/memory`), enumerações (`view/create/str_replace/…`) e até `/` —
// e o portão reprovava a reescrita do cap. 08 por "perder evidência" que nunca
// foi evidência. Quarto falso positivo desta família de medidores.
function caminhosDe(md) {
  const brutos = md.match(/`[^`\n]*\/[^`\n]*`/g) || [];
  return new Set(
    brutos
      .map((s) => s.replace(/`/g, "").trim())
      .filter((s) => !/^https?:/.test(s))
      .filter((s) => !s.includes("…") && !s.includes(" "))
      .filter((s) => /\.\w{1,5}$/.test(s) || s.endsWith("/"))
  );
}

export function medir(caminho, lang) {
  const c = IDIOMAS[lang];
  const md = readFileSync(resolve(RAIZ, caminho), "utf8");
  const frases = frasesDe(corpoDe(md, c));
  const prosa = frases.join(" ");
  const palavras = prosa.split(/\s+/).filter(Boolean).length;
  const travessoes = (prosa.match(/—/g) || []).length;
  const comp = frases.map((f) => f.split(/\s+/).length);

  const andaime = (c.andaime.exec(md) || [])[1]?.toLowerCase() || null;

  return {
    arquivo: basename(caminho),
    caminho,
    lang,
    palavras,
    travessoesPor1k: (travessoes * 1000) / Math.max(palavras, 1),
    fraseMedia: comp.length ? comp.reduce((a, b) => a + b, 0) / comp.length : 0,
    frasesLongas: comp.filter((x) => x > LIMITES.fraseMaxima).length,
    v4: c.marcador.test(md),
    andaime,
    exemplo: exemploTrabalhado(md, c),
    temVerificacao: c.verificacao.test(md),
    gabaritoSeparado: c.gabarito.test(md),
    // estrutura, para a paridade PT/EN
    h2: (md.match(/^## /gm) || []).length,
    h3: (md.match(/^### /gm) || []).length,
    cercas: (md.match(/^```/gm) || []).length,
    caminhos: caminhosDe(md),
  };
}

function main() {
  const falhas = [];
  const linhas = [];
  const porLang = {};

  for (const lang of ["pt", "en"]) {
    const arquivos = capitulosDe(lang);
    if (arquivos.length !== 18)
      falhas.push(`[${lang}] a lista de capítulos tem ${arquivos.length}, esperados 18 (arquivo renomeado sai da medição em silêncio)`);
    porLang[lang] = arquivos.map((a) => medir(a, lang));
  }

  for (const lang of ["pt", "en"]) {
    for (const m of porLang[lang]) {
      linhas.push(
        `  ${m.v4 ? "v4" : "  "} ${lang} ${m.arquivo.padEnd(36)} ${String(m.palavras).padStart(5)}p ` +
          `${m.travessoesPor1k.toFixed(1).padStart(5)}—/1k ` +
          `${m.fraseMedia.toFixed(1).padStart(5)} pal/frase ` +
          `${String(m.frasesLongas).padStart(2)} longas ` +
          `${(m.andaime || "--").padEnd(8)} ${m.exemplo.ok ? "ex " : "-- "}${m.gabaritoSeparado ? "gab" : "---"}`
      );

      if (!m.v4) continue;
      const p = `[${lang}] ${m.arquivo}`;

      if (m.travessoesPor1k > LIMITES.travessoesPor1k)
        falhas.push(`${p}: ${m.travessoesPor1k.toFixed(1)} travessões/1k (limite ${LIMITES.travessoesPor1k})`);
      if (m.fraseMedia > LIMITES.fraseMedia)
        falhas.push(`${p}: frase média ${m.fraseMedia.toFixed(1)} palavras (limite ${LIMITES.fraseMedia})`);
      if (m.frasesLongas > 0)
        falhas.push(`${p}: ${m.frasesLongas} frase(s) acima de ${LIMITES.fraseMaxima} palavras`);
      if (!m.andaime || !ANDAIMES.includes(m.andaime))
        falhas.push(`${p}: sem andaime declarado no cabeçalho (${ANDAIMES.join(" | ")})`);
      else if (EXIGE_CODIGO.has(m.andaime) && !m.exemplo.ok)
        falhas.push(`${p}: ${m.exemplo.motivo}`);
      if (m.temVerificacao && !m.gabaritoSeparado)
        falhas.push(`${p}: gabarito da verificação não está em seção própria`);
    }
  }

  // Paridade estrutural PT/EN: pega o modo de falha dominante da tradução em
  // série — uma seção ou um bloco de código que não atravessou.
  const parEn = new Map(porLang.en.map((m) => [m.arquivo.replace(/^(\d\d)-.*/, "$1"), m]));
  for (const pt of porLang.pt) {
    const chave = pt.arquivo.replace(/^(\d\d)-.*/, "$1");
    const en = parEn.get(chave);
    if (!en) { falhas.push(`[par] capítulo ${chave} sem contraparte EN`); continue; }
    if (!pt.v4 && !en.v4) continue;
    if (pt.v4 !== en.v4)
      falhas.push(`[par ${chave}] marcado v4 em ${pt.v4 ? "PT" : "EN"} e não no outro — tradução em atraso`);
    for (const [rot, a, b] of [["##", pt.h2, en.h2], ["###", pt.h3, en.h3], ["cercas", pt.cercas, en.cercas]])
      if (a !== b) falhas.push(`[par ${chave}] ${rot}: PT ${a} × EN ${b}`);
    if (pt.andaime !== en.andaime)
      falhas.push(`[par ${chave}] andaime: PT ${pt.andaime} × EN ${en.andaime}`);
  }

  // Evidência não some: baseline de caminhos de arquivo por capítulo PT.
  const arqBase = resolve(RAIZ, "publicar/evidencia-baseline.json");
  if (existsSync(arqBase)) {
    const base = JSON.parse(readFileSync(arqBase, "utf8"));
    for (const m of porLang.pt) {
      const esperado = base[m.arquivo];
      if (esperado === undefined) continue;
      if (m.caminhos.size < esperado)
        falhas.push(`[evidência] ${m.arquivo}: ${m.caminhos.size} caminhos de arquivo, baseline ${esperado} — mover para o Apêndice A passa, apagar não`);
    }
  }

  const v4 = [...porLang.pt, ...porLang.en].filter((m) => m.v4).length;
  console.log(`\nProsa didática — 18 capítulos × 2 idiomas (v4 = reprova o build):`);
  console.log(linhas.join("\n"));

  if (falhas.length) {
    console.error(`\n✗ prosa: ${falhas.length} problema(s)`);
    falhas.forEach((f) => console.error(`  - ${f}`));
    process.exit(1);
  }
  console.log(`\n✓ prosa: ${v4} capítulo(s) v4 dentro dos limites`);
}

if (import.meta.url === `file://${process.argv[1]}`) main();
