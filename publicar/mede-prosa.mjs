// Medidor de prosa didática (spec 097).
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
// Enquanto a reescrita da spec 097 estiver em curso, capítulos ainda não
// reescritos apenas REPORTAM. Só os listados em REESCRITOS reprovam o build —
// caso contrário o portão nasceria vermelho e seria ignorado, que é o pior
// destino de um verificador.

import { readFileSync, existsSync } from "node:fs";
import { resolve, dirname, basename } from "node:path";
import { fileURLToPath } from "node:url";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");

// Capítulos já passados pela camada didática v4. Cresce a cada reescrita.
const REESCRITOS = new Set([
  "00-introducao.md",
  "01-fundamentos.md",
  "02-loop-do-agente.md",
  "17-protocolos.md",
]);

const LIMITES = {
  travessoesPor1k: 8,     // medido: 22,0 no livro inteiro antes da spec 097
  fraseMedia: 20,         // palavras
  fraseMaxima: 60,        // nenhuma frase acima disto sobrevive à leitura em voz alta
};

const CAPITULOS = [
  "livro/00-introducao.md",
  "livro/01-fundamentos.md",
  ...Array.from({ length: 16 }, (_, i) => i + 2)
    .map((n) => String(n).padStart(2, "0"))
    .flatMap((n) => {
      const achado = [
        `livro/capitulos/${n}-loop-do-agente.md`,
        `livro/capitulos/${n}-entrega-de-contexto.md`,
        `livro/capitulos/${n}-compactacao.md`,
        `livro/capitulos/${n}-ferramentas.md`,
        `livro/capitulos/${n}-mcp.md`,
        `livro/capitulos/${n}-permissoes-sandbox.md`,
        `livro/capitulos/${n}-memoria-estado.md`,
        `livro/capitulos/${n}-planejamento.md`,
        `livro/capitulos/${n}-subagentes-orquestracao.md`,
        `livro/capitulos/${n}-verificacao-evals.md`,
        `livro/capitulos/${n}-extensibilidade.md`,
        `livro/capitulos/${n}-interfaces.md`,
        `livro/capitulos/${n}-harness-embutido.md`,
        `livro/capitulos/${n}-aprendizado-auto-evolutivo.md`,
        `livro/capitulos/${n}-protocolos.md`,
      ].filter((p) => existsSync(resolve(RAIZ, p)));
      return achado;
    }),
  "livro/14-convergencias.md",
];

// O Apêndice A é inventário por repositório: denso de propósito, e medi-lo
// como prosa de ensino seria medir a coisa errada.
function corpoDe(markdown) {
  const semApendice = markdown.split(/^## Apêndice A/m)[0];
  return semApendice.replace(/```[\s\S]*?```/g, "");
}

// Frase é unidade de leitura em voz alta, e um item de lista termina no fim da
// linha mesmo sem ponto. Colapsar `\n` antes de dividir gluava uma lista inteira
// numa "frase" de 90 palavras — falso positivo que apareceu na reescrita do
// cap. 00. Então: cada linha é uma fronteira, e linha de tabela, citação,
// cabeçalho e HTML não são prosa corrida.
function frasesDe(texto) {
  return texto
    .split("\n")
    .map((l) => l.trim())
    .filter((l) => l && !/^([|>#]|<|!\[)/.test(l))
    .flatMap((linha) => linha.split(/(?<=[.!?])\s+/))
    .map((s) => s.replace(/^[-*\d.]+\s*/, "").trim())
    .filter((s) => s.split(/\s+/).length > 2);
}

export function medir(caminho) {
  const md = readFileSync(resolve(RAIZ, caminho), "utf8");
  // Só prosa corrida entra nas métricas. Fora: tabela, citação, cabeçalho, HTML.
  // A matriz do cap. 17 usa `—` como célula de "não se aplica", e contar isso
  // como pontuação punia o capítulo por ter tabela — segundo falso positivo do
  // medidor, mesma causa do primeiro: estrutura medida como se fosse prosa.
  const frases = frasesDe(corpoDe(md));
  const prosa = frases.join(" ");
  const palavras = prosa.split(/\s+/).filter(Boolean).length;
  const travessoes = (prosa.match(/—/g) || []).length;
  const comprimentos = frases.map((f) => f.split(/\s+/).length);
  const media = comprimentos.length
    ? comprimentos.reduce((a, b) => a + b, 0) / comprimentos.length
    : 0;

  return {
    arquivo: basename(caminho),
    palavras,
    travessoesPor1k: (travessoes * 1000) / Math.max(palavras, 1),
    fraseMedia: media,
    frasesLongas: comprimentos.filter((c) => c > LIMITES.fraseMaxima).length,
    // Um exemplo trabalhado é bloco de código no corpo, não no Apêndice A.
    temExemplo: /```/.test(md.split(/^## Apêndice A/m)[0]),
    // Gabarito fora da pergunta: seção própria no fim. Só se aplica a capítulo
    // que TEM verificação — a introdução não tem, e exigir dela seria exigir
    // resposta de pergunta que não existe.
    temVerificacao: /^## Verificação/m.test(md),
    gabaritoSeparado: /^## Respostas da verificação/m.test(md),
  };
}

function main() {
  const linhas = [];
  const falhas = [];

  for (const caminho of CAPITULOS) {
    const m = medir(caminho);
    const reescrito = REESCRITOS.has(m.arquivo);
    const marca = reescrito ? "v4" : "  ";
    linhas.push(
      `  ${marca} ${m.arquivo.padEnd(38)} ${String(m.palavras).padStart(5)}p ` +
        `${m.travessoesPor1k.toFixed(1).padStart(5)}—/1k ` +
        `${m.fraseMedia.toFixed(1).padStart(5)} pal/frase ` +
        `${String(m.frasesLongas).padStart(2)} longas ` +
        `${m.temExemplo ? "ex" : "--"} ${m.gabaritoSeparado ? "gab" : "---"}`
    );

    if (!reescrito) continue;

    if (m.travessoesPor1k > LIMITES.travessoesPor1k)
      falhas.push(`${m.arquivo}: ${m.travessoesPor1k.toFixed(1)} travessões/1k (limite ${LIMITES.travessoesPor1k})`);
    if (m.fraseMedia > LIMITES.fraseMedia)
      falhas.push(`${m.arquivo}: frase média ${m.fraseMedia.toFixed(1)} palavras (limite ${LIMITES.fraseMedia})`);
    if (m.frasesLongas > 0)
      falhas.push(`${m.arquivo}: ${m.frasesLongas} frase(s) acima de ${LIMITES.fraseMaxima} palavras`);
    if (!m.temExemplo)
      falhas.push(`${m.arquivo}: sem exemplo trabalhado (bloco de código) no corpo`);
    if (m.temVerificacao && !m.gabaritoSeparado)
      falhas.push(`${m.arquivo}: gabarito da verificação não está em seção própria`);
  }

  console.log(`\nProsa didática — ${CAPITULOS.length} capítulos (v4 = reprova o build):`);
  console.log(linhas.join("\n"));

  if (falhas.length) {
    console.error(`\n✗ prosa: ${falhas.length} problema(s) em capítulo v4`);
    falhas.forEach((f) => console.error(`  - ${f}`));
    process.exit(1);
  }
  console.log(`\n✓ prosa: ${REESCRITOS.size} capítulo(s) v4 dentro dos limites`);
}

if (import.meta.url === `file://${process.argv[1]}`) main();
