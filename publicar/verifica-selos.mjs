// Selo i18n atrasado reprova o build (ADR 0011 §4.5).
//
// Antes disto, "PT mergeado, EN esquecido" passava por todos os portões:
// verifica-capitulos.mjs exige que o selo EXIBIDO seja honesto, não que a
// tradução esteja em dia. Havia dois arquivos atrasados no repositório com o
// build verde — e quando "atrasado" é um estado publicável, ele deixa de ser
// sinal. Numa série de 14 capítulos traduzidos, é o modo de falha dominante.
//
// A lista de dívida declarada nasceu com dois apêndices e está vazia desde a
// spec 103, quando conferir os dois mostrou que o atraso era do SELO e não da
// tradução: o PT tinha mudado uma linha de link cada (migração da spec 083), o
// EN já trazia a forma nova, e ninguém regravou o cabeçalho. Ou seja: a exemção
// existiu por três specs porque eu li o veredito do portão e não o caso.
//
// A lista fica, porque nomear é melhor que tolerar em silêncio. Mas antes de
// pôr um nome nela, rode `node publicar/sela.mjs --conferir` — ele diz qual das
// duas dívidas é. Só a de tradução justifica a exemção; a de selo custa um
// comando.

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { resolve, dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");

// Vazia. Nunca cresce sem uma linha no HISTORICO explicando por quê.
const DIVIDA_DECLARADA = new Set();

const SELO = /^<!--\s*i18n fonte:(\S+)\s+edicao:(\S+)\s+hash:(\w+)\s*-->/;

function todosOsMd(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const p = join(dir, e.name);
    if (e.isDirectory()) return todosOsMd(p);
    return e.name.endsWith(".md") ? [p] : [];
  });
}

function main() {
  const base = resolve(RAIZ, "livro/en");
  const atrasados = [];
  const semSelo = [];
  let conferidos = 0;

  for (const arq of todosOsMd(base)) {
    const nome = relative(base, arq);
    const primeira = readFileSync(arq, "utf8").split("\n", 1)[0];
    const m = SELO.exec(primeira);
    if (!m) { semSelo.push(nome); continue; }

    const [, fonte, , hashSelo] = m;
    const caminhoFonte = resolve(RAIZ, fonte);
    if (!existsSync(caminhoFonte) || !statSync(caminhoFonte).isFile()) {
      atrasados.push(`${nome}: a fonte declarada (${fonte}) não existe`);
      continue;
    }
    const real = createHash("md5").update(readFileSync(caminhoFonte)).digest("hex").slice(0, 8);
    // Conta só o que está de fato em dia. Contando antes da comparação, o
    // arquivo exemptado entrava no número de "em dia" E no de dívida — o
    // relatório somava 31 sobre 29 páginas e ninguém notou.
    if (real === hashSelo) { conferidos++; continue; }

    const nomeBase = nome.split("/").pop();
    if (DIVIDA_DECLARADA.has(nomeBase)) continue;
    atrasados.push(`${nome}: selo ${hashSelo}, fonte ${fonte} está em ${real}`);
  }

  if (semSelo.length) {
    console.error(`\n✗ selos i18n: ${semSelo.length} arquivo(s) EN sem cabeçalho de selo`);
    semSelo.forEach((s) => console.error(`  - ${s}`));
    process.exit(1);
  }
  if (atrasados.length) {
    console.error(`\n✗ selos i18n: ${atrasados.length} tradução(ões) atrasada(s)`);
    atrasados.forEach((a) => console.error(`  - ${a}`));
    console.error(`  (dívida declarada e tolerada: ${[...DIVIDA_DECLARADA].join(", ")})`);
    process.exit(1);
  }
  console.log(
    `✓ selos i18n: ${conferidos} páginas EN em dia com a fonte PT` +
      ` (+${DIVIDA_DECLARADA.size} de dívida declarada)`
  );
}

main();
