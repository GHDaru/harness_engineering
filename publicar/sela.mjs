// Regrava os selos i18n a partir da fonte declarada em cada arquivo EN.
//
// Por que existe: o selo é um md5 do arquivo PT, e o ciclo natural de trabalho
// é escrever PT → traduzir → selar → rodar o build → o portão reprovar o PT →
// ajustar o PT. Nesse ponto o selo, gravado antes, aponta para um hash que já
// não existe. Selo escrito à mão é selo estimado; este script torna a estimativa
// impossível em vez de proibida.
//
// Uso: `node publicar/sela.mjs livro/en/<arquivo>.md ...` — os arquivos que você
// ACABOU de traduzir, nomeados um a um. `--conferir` lista o que está fora de
// sincronia, sem escrever nada.
//
// Por que exige nomes explícitos: rodado sem argumentos, na primeira versão,
// ele reselou também dois apêndices cuja tradução estava atrasada de verdade —
// e um selo regravado sobre texto não traduzido não conserta o atraso, ele o
// APAGA, declarando uma sincronia que não existe. O selo é uma afirmação sobre
// o conteúdo; só quem traduziu pode fazê-la. A ferramenta calcula o hash, o
// humano (ou o agente) diz de qual arquivo.

import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { resolve, dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SO_CONFERIR = process.argv.includes("--conferir");
const SELO = /^<!--\s*i18n fonte:(\S+)\s+edicao:(\S+)\s+hash:(\w+)\s*-->/;

// A edição corrente sai do HISTORICO, para não haver dois lugares dizendo qual é.
function edicaoCorrente() {
  const h = readFileSync(resolve(RAIZ, "livro/HISTORICO.md"), "utf8");
  const m = /^### Edição (\d+\.\d+)/m.exec(h);
  if (!m) throw new Error("não achei a edição corrente em livro/HISTORICO.md");
  return m[1];
}

function todosOsMd(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = join(dir, e.name);
    if (e.isDirectory()) return todosOsMd(p);
    return e.name.endsWith(".md") ? [p] : [];
  });
}

const edicao = edicaoCorrente();
const base = resolve(RAIZ, "livro/en");
const nomeados = process.argv.slice(2).filter((a) => !a.startsWith("--"));

if (!SO_CONFERIR && nomeados.length === 0) {
  console.error("uso: node publicar/sela.mjs <arquivo EN traduzido> [...]  |  --conferir");
  console.error("selar em massa apagaria atrasos reais em vez de consertá-los.");
  process.exit(2);
}

const alvos = SO_CONFERIR
  ? todosOsMd(base)
  : nomeados.map((n) => resolve(RAIZ, n));

let regravados = 0;
let emDia = 0;

for (const arq of alvos) {
  const texto = readFileSync(arq, "utf8");
  const linhas = texto.split("\n");
  const m = SELO.exec(linhas[0]);
  if (!m) { console.error(`  ! ${relative(base, arq)}: sem selo`); continue; }

  const [, fonte, edSelo, hashSelo] = m;
  const caminhoFonte = resolve(RAIZ, fonte);
  if (!existsSync(caminhoFonte)) { console.error(`  ! ${relative(base, arq)}: fonte ${fonte} não existe`); continue; }

  const real = createHash("md5").update(readFileSync(caminhoFonte)).digest("hex").slice(0, 8);
  if (real === hashSelo) { emDia++; continue; }

  if (SO_CONFERIR) {
    console.log(`  ~ ${relative(base, arq)}: ${hashSelo} → ${real} (edição ${edSelo} → ${edicao})`);
    regravados++;
    continue;
  }
  linhas[0] = `<!-- i18n fonte:${fonte} edicao:${edicao} hash:${real} -->`;
  writeFileSync(arq, linhas.join("\n"));
  console.log(`  ✎ ${relative(base, arq)}: selo ${hashSelo} → ${real}`);
  regravados++;
}

console.log(
  SO_CONFERIR
    ? `\n${regravados} selo(s) a regravar · ${emDia} em dia (edição ${edicao})`
    : `\n${regravados} selo(s) regravado(s) · ${emDia} já em dia (edição ${edicao})`
);
