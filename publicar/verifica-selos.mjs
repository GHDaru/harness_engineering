// Selo i18n atrasado reprova o build (ADR 0011 §4.5).
//
// Antes disto, "PT mergeado, EN esquecido" passava por todos os portões:
// verifica-capitulos.mjs exige que o selo EXIBIDO seja honesto, não que a
// tradução esteja em dia. Havia dois arquivos atrasados no repositório com o
// build verde — e quando "atrasado" é um estado publicável, ele deixa de ser
// sinal. Numa série de 14 capítulos traduzidos, é o modo de falha dominante.
//
// Baseline nomeada: os dois apêndices já atrasados em 2026-08-12 entram como
// dívida declarada, no mesmo padrão da lista de páginas transacionais do
// verifica-canonical.mjs. Dívida nomeada é dívida; dívida anônima é ruído.

import { readFileSync, readdirSync, existsSync, statSync } from "node:fs";
import { resolve, dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");

// Atraso conhecido em 2026-08-12. Some da lista quando a tradução for feita;
// nunca cresce sem uma linha no HISTORICO explicando por quê.
const DIVIDA_DECLARADA = new Set(["appendix-study.md", "appendix-usage.md"]);

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
    conferidos++;
    if (real === hashSelo) continue;

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
