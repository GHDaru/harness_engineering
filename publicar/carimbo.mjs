// Grava docs/build.json com o commit que gerou este site (spec 104).
//
// Por que existe: em 13/ago o deploy foi recusado por cota, o site ficou na versão
// anterior e o CI reportou verde. O conserto do código de saída (pipefail) pega o
// deploy que falha em voz alta; não pega o que "sucede" sem trocar o conteúdo.
//
// Para perguntar "a página no ar é a que eu construí?" é preciso haver, na página,
// algo que mude a cada build. A edição do HISTORICO não serve: um commit do Radar
// não muda a edição, e a falha de 13/ago foi exatamente num commit do Radar — uma
// conferência por edição teria passado verde na falha que a motivou.
//
// O commit muda sempre. Por isso o carimbo é o commit.

import { writeFileSync, existsSync, mkdirSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";

const RAIZ = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const DOCS = resolve(RAIZ, "docs");

// No CI o commit vem do ambiente; localmente, do git. Sem os dois, o carimbo diz
// que não sabe — melhor que inventar um valor que a conferência vai comparar.
function commit() {
  const doAmbiente = (process.env.GITHUB_SHA || "").trim();
  if (doAmbiente) return doAmbiente;
  try {
    return execFileSync("git", ["-C", RAIZ, "rev-parse", "HEAD"], { encoding: "utf8" }).trim();
  } catch {
    return "desconhecido";
  }
}

if (!existsSync(DOCS)) mkdirSync(DOCS, { recursive: true });

const carimbo = { commit: commit() };
writeFileSync(resolve(DOCS, "build.json"), JSON.stringify(carimbo) + "\n");
console.log(`✓ carimbo do build: ${carimbo.commit.slice(0, 8)} → docs/build.json`);
