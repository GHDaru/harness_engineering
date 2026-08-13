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
// sincronia e faz a triagem de cada caso, sem escrever nada.
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
import { execFileSync } from "node:child_process";

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

const git = (...args) =>
  execFileSync("git", ["-C", RAIZ, ...args], { encoding: "utf8" }).trim();

// Triagem: um selo fora de sincronia é DUAS dívidas diferentes com o mesmo
// sintoma. Ou a tradução está atrasada (o PT ganhou conteúdo que o EN não tem),
// ou só o selo está atrasado (alguém editou os dois e esqueceu de regravar o
// cabeçalho). O portão reprova as duas igual, e é por isso que na spec 099 eu
// parquei dois apêndices como "tradução atrasada" sem conferir: eram selo.
//
// Isto responde a pergunta que eu deveria ter feito. Localiza o commit em que a
// fonte PT tinha o hash selado e mede o que aconteceu desde então nos dois lados.
// PT mudando pouco + EN tocado depois = dívida de selo. O contrário = tradução.
function triagem(fonte, hashSelo, arqEN) {
  const relEN = relative(RAIZ, arqEN);
  let commitDoSelo = null;
  for (const linha of git("log", "--format=%H %ad", "--date=short", "--", fonte).split("\n")) {
    const [sha, data] = linha.split(" ");
    if (!sha) continue;
    const blob = execFileSync("git", ["-C", RAIZ, "show", `${sha}:${fonte}`]);
    if (createHash("md5").update(blob).digest("hex").slice(0, 8) === hashSelo) {
      commitDoSelo = { sha, data };
      break;
    }
  }
  // Sem commit correspondente o selo nunca descreveu uma versão que existiu:
  // hash escrito à mão, ou fonte reescrita fora do git. Dizer isso é melhor
  // que estimar um número de linhas a partir de um ponto de partida inventado.
  if (!commitDoSelo) return "    nenhum commit da fonte casa com o hash selado — selo nunca foi real";

  const linhasPT = git("diff", "--numstat", commitDoSelo.sha, "HEAD", "--", fonte)
    .split("\t")
    .slice(0, 2)
    .reduce((s, n) => s + (Number(n) || 0), 0);
  const enDepois = git("log", "--format=%H", `${commitDoSelo.sha}..HEAD`, "--", relEN) !== "";
  return (
    `    selo em ${commitDoSelo.sha.slice(0, 8)} (${commitDoSelo.data})` +
    ` · PT: ${linhasPT} linha(s) desde então` +
    ` · EN tocado depois: ${enDepois ? "sim" : "não"}`
  );
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
    try {
      console.log(triagem(fonte, hashSelo, arq));
    } catch (e) {
      console.log(`    triagem indisponível (${e.message.split("\n")[0]})`);
    }
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
