// Verifica o endereço canônico do site gerado (spec 095).
//
// Existe porque a ausência de `rel="canonical"` sobreviveu a 428 ocorrências de
// SITE_URL, a um build verde e a dois registros escritos afirmando que a tag
// estava lá. Nada no processo perguntava se ela existia — então agora pergunta,
// no mesmo passo que já verifica os capítulos.
//
// Uso: node verifica-canonical.mjs   (roda depois das duas passadas do build)

import { readdirSync, readFileSync, existsSync } from "node:fs";
import { dirname, resolve, join } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const DOCS = resolve(AQUI, "..", "docs");
const SITE = (process.env.SITE_URL || "https://harness.ghdaru.com.br/").replace(/\/*$/, "/");

const falhas = [];
// As únicas páginas que podem ser noindex: transacionais, de uso único, com token
// na query. Qualquer outra marcada assim é engano e o verificador reclama.
const naoIndexaveis = ["entrar.html", "sair.html"];
const htmls = (dir, prefixo = "") =>
  readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory()
      ? e.name === "en" ? htmls(join(dir, e.name), "en/") : []
      : e.name.endsWith(".html") ? [prefixo + e.name] : []
  );

const paginas = htmls(DOCS);
if (!paginas.length) {
  console.error("✗ nenhum HTML em docs/ — rode o build antes");
  process.exit(1);
}

let comCanonical = 0;
for (const rel of paginas) {
  if (rel.endsWith("_print.html")) continue;   // temporário de impressão
  const html = readFileSync(join(DOCS, rel), "utf8");

  // `entrar.html` e `sair.html` são transacionais, de uso único e marcadas
  // `noindex`. Elas NÃO levam canonical de propósito: dizer "não me indexe" e
  // "esta é a versão canônica" na mesma página é sinal contraditório. A isenção
  // vem com a contrapartida — para ser dispensada do canonical, a página precisa
  // mesmo estar marcada como noindex, senão sai do índice sem ninguém pedir.
  const noindex = /<meta name="robots" content="[^"]*noindex/.test(html);
  const m = html.match(/<link rel="canonical" href="([^"]+)">/);
  if (noindex) {
    if (m) falhas.push(`${rel}: é noindex e mesmo assim declara canonical (sinal contraditório)`);
    if (naoIndexaveis.every((n) => !rel.endsWith(n)))
      falhas.push(`${rel}: marcada noindex sem estar na lista de páginas transacionais`);
    continue;
  }
  if (!m) { falhas.push(`${rel}: sem rel="canonical"`); continue; }
  comCanonical++;

  // A regra que importa: cada página aponta para SI MESMA. Uma edição que se
  // declara cópia da outra renuncia à própria indexação — é o erro clássico de
  // i18n, e é o que este teste existe para impedir.
  const esperado = `${SITE}${rel}`;
  if (m[1] !== esperado) falhas.push(`${rel}: canonical → ${m[1]} (esperado ${esperado})`);

  // O endereço abandonado não pode voltar como LINK ou como METADADO. Citá-lo em
  // prosa é outra coisa e é legítimo: o `HISTORICO.md` precisa contar que houve
  // duas cópias vivas do livro, e um livro que corrige em público tem de poder
  // escrever o endereço que abandonou.
  //
  // A primeira versão desta regra olhava o HTML inteiro e reprovou exatamente
  // esse registro. Segunda vez no dia em que uma regra minha ficou larga demais e
  // a página estava certa — vale o registro: um verificador que reprova o uso
  // legítimo é desligado, e aí verifica zero.
  for (const m2 of html.matchAll(/(?:href|src|content)="([^"]*ghdaru\.github\.io[^"]*)"/g))
    falhas.push(`${rel}: aponta para o endereço antigo em ${m2[1]}`);
}

for (const arq of ["sitemap.xml", "robots.txt"]) {
  const caminho = resolve(DOCS, arq);
  if (!existsSync(caminho)) { falhas.push(`${arq} não foi gerado`); continue; }
  const txt = readFileSync(caminho, "utf8");
  if (!txt.includes(SITE)) falhas.push(`${arq}: não cita ${SITE}`);
}

// O sitemap sai da mesma lista do verificador de links; se divergir do que foi
// escrito em disco, uma das duas está mentindo.
const sitemap = readFileSync(resolve(DOCS, "sitemap.xml"), "utf8");
const noMapa = new Set([...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(SITE, "")));
for (const p of ["index.html", "sumario.html", "en/index.html", "en/sumario.html"])
  if (!noMapa.has(p)) falhas.push(`sitemap.xml: falta ${p}`);
for (const p of noMapa)
  if (!existsSync(resolve(DOCS, p))) falhas.push(`sitemap.xml: aponta ${p}, que não existe`);

if (falhas.length) {
  console.error(`✗ ${falhas.length} problema(s) de endereço canônico:`);
  falhas.slice(0, 20).forEach((f) => console.error("   " + f));
  if (falhas.length > 20) console.error(`   … e mais ${falhas.length - 20}`);
  process.exit(1);
}

console.log(`✓ endereço canônico: ${comCanonical} páginas apontam para si mesmas (+${naoIndexaveis.length * 2} transacionais noindex) em ${SITE} · sitemap com ${noMapa.size} URLs · robots OK`);
