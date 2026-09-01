// Portão de slop: marcas de escrita gerada por IA no texto-fonte do livro.
//
// Existe porque os capítulos nascem com apoio de IA (o HISTORICO registra o
// modelo de cada edição) e o Princípio I exige EVIDÊNCIA acima de retórica. O
// portão irmão `verifica-capitulos.mjs` mede estrutura — esqueleto v3, datação,
// downloads, sincronia PT↔EN — e não olha a PROSA. Um capítulo inteiro escrito
// no registro "esta arquitetura desempenha um papel crucial no cenário em
// evolução dos harnesses" passa hoje com build verde.
//
// Roda ANTES do build, sobre a fonte (`livro/**/*.md`), não sobre a página
// gerada: o que se quer é barrar na entrada, não auditar depois.
//
// Portado do livro Teoria das Restrições (mesmo autor, ADR 0006 de lá), com duas
// diferenças que este repositório impôs — as duas estão documentadas abaixo, e
// as duas nasceram de medição, não de gosto.
//
// ---------------------------------------------------------------------------
// O QUE ESTE PORTÃO DELIBERADAMENTE NÃO MEDE
//
// 1. TRAVESSÃO (§14 do guia de origem).
//
// A regra manda cortar todos, como restrição dura. Ela vem do "Signs of AI
// writing" da Wikipédia EM INGLÊS, onde o em dash é ornamento opcional. Em
// português é pontuação: aposto explicativo, intercalação, fala.
//
// Medido aqui: 2.744 travessões no livro PT (48,7 por mil palavras) e 1.265 no
// EN (26,3 por mil). A queda de 46% na tradução mostra que o tradutor já
// converteu boa parte em vírgula e ponto; o que sobrou no EN herda a pontuação
// do original, não hábito de composição em inglês. Aplicar §14 ao EN seria
// punir tradução fiel de aposto português — 1.265 achados de uma vez, que é
// como se ensina uma pessoa a ignorar a saída inteira do portão.
//
// (No EN a regra se aplicaria de verdade se o texto fosse composto em inglês.
// Quando houver capítulo escrito direto em inglês, vale reabrir.)
//
// 2. EMOJI EM DOCUMENTO DE APARATO (§18, parcial).
//
// O livro usa pictogramas como NOTAÇÃO DOCUMENTADA: ⭐ marca o caso âncora do
// capítulo (116 ocorrências, quase todas em título de seção), ⏳ marca fonte não
// confirmada na bibliografia, 🔵🟡🟢🔴 são o placar do registro de expiração, e
// ✅/❌ são marcas de verificação. Todos definidos no GUIA-EDITORIAL e na
// legenda da bibliografia. Esses passam.
//
// O HISTORICO fica fora do §18 inteiro: é changelog (§30 isenta documento
// versionado) e usa ícone como índice visual (🏷 release, 📈 métrica, 🔑 chave,
// 🏁 marco). São 11 pictogramas avulsos, todos lá dentro e em nenhum outro
// arquivo — medido, não suposto.
//
// 3. LISTAS COM RÓTULO EM NEGRITO (§16). Descartada no repositório de origem por
//    acusar notação legítima; não foi reintroduzida aqui.
//
// O critério que une os três: portão com falso positivo conhecido é portão que
// se aprende a ignorar. Zero achado no texto limpo é o que faz um achado futuro
// significar alguma coisa.
// ---------------------------------------------------------------------------
//
// Calibragem (2026-08 — PT: 27 arquivos, 56.321 palavras · EN: 27 arquivos,
// 48.131 palavras): ZERO achados nos dois idiomas. Os candidatos que a primeira
// versão marcou eram todos falso positivo, e cada um estreitou uma regra:
//
//   "robusto" / "robust"  — 3 ocorrências entre este livro e o do Maestro, todas
//        técnicas ("o modelo de estado mais robusto", "atenção robusta"), e uma
//        delas era o Maestro ENSINANDO que "o script é robusto" é critério vago.
//        Saiu das duas listas de vocabulário.
//   "showcase" (EN)  — 3 ocorrências, todas SUBSTANTIVO ("the showcase of one
//        ecosystem", "the single-vendor showcase"): vitrine, uso legítimo. O tell
//        é o verbo, então a regra passou a exigir showcasing/showcases/showcased.
//   "serves as a" (EN)  — 1 ocorrência, "a small core that serves as a socket":
//        função metafórica, não fuga de cópula. Saiu de §1.
//
// Fronteira de palavra é Unicode, não `\b`. Em JS (como em grep no locale C)
// `\b` é ASCII: `/\brico/` casa dentro de "histórico", porque "ó" não é
// [A-Za-z0-9_] e vira fronteira.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { dirname, resolve, relative } from "node:path";
import { fileURLToPath } from "node:url";

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, "..");

// Fronteira Unicode-aware. Todo espaço literal do padrão vira `\s+`: em Markdown
// a linha quebra onde o parágrafo mandar, e "desempenha um papel\ncrucial" é o
// mesmo slop que "desempenha um papel crucial".
const entre = (corpo) =>
  new RegExp(`(?<![\\p{L}\\p{N}_])(?:${corpo.replace(/ /g, "\\s+")})(?![\\p{L}\\p{N}_])`, "giu");

// Cada padrão cita a seção do guia de origem (para a discussão "isso é mesmo
// slop?" acontecer contra um texto, e não contra gosto pessoal) e carrega uma
// AMOSTRA-CANÁRIO que ele tem obrigação de acusar. O autoteste roda todos os
// canários a cada build: padrão afrouxado quebra na hora, e não seis capítulos
// depois, calado.
const P = (nome, corpo, canario) => [nome, entre(corpo), canario];
const PR = (nome, re, canario) => [nome, re, canario];

const PT = [
  P("§1 significância inflada",
    "desempenha(?:m|ndo)? um papel (?:crucial|fundamental|vital|central|essencial)" +
    "|marca(?:ndo)? um (?:momento|marco) (?:decisivo|crucial|histórico)" +
    "|é um testemunho d[aeo]|reflete (?:uma|a) tendência mais ampla" +
    "|deixando uma marca indelével|cenário em (?:constante )?evolução" +
    "|profundamente enraizad[oa]|(?:abrindo|pavimentando) o caminho para",
    "As ferramentas desempenham um papel crucial no cenário em constante evolução."),

  // O tell não é o gerúndio (comum e correto em português), é a oração
  // participial PENDURADA no fim da frase para simular profundidade.
  PR("§3 gerúndio de enfeite",
    /,\s+(?:destacando|ressaltando|enfatizando|garantindo|refletindo|simbolizando|contribuindo\s+para|promovendo|fomentando|abrangendo|demonstrando|evidenciando|consolidando)(?![\p{L}\p{N}_])/giu,
    "O harness reduz o retrabalho, contribuindo para uma cultura mais forte."),

  P("§4 promocional",
    "vibrante|de tirar o fôlego|imperdível|deslumbrante|renomad[oa]" +
    "|revolucionári[oa]|inigualável|incomparável|no coração d[aeo]",
    "Uma abordagem revolucionária, no coração da engenharia moderna."),

  P("§5 atribuição vaga",
    "especialistas (?:afirmam|acreditam|apontam|dizem|sugerem)" +
    "|observadores (?:apontam|notam)|relatórios do setor|alguns críticos" +
    "|muitos acreditam|é amplamente reconhecido|é sabido que" +
    "|(?:estudos|pesquisas) (?:mostram|indicam|sugerem) que",
    "Especialistas afirmam que o ganho é imediato, e estudos mostram que funciona."),

  // "fundamental", "essencial" e "robusto" ficaram DE FORA: são corretas e
  // frequentes em texto técnico português. Ver a nota de calibragem no topo.
  P("§7 vocabulário de IA",
    "crucial|mergulhar (?:fundo|mais fundo)|aprimorar|abrangente" +
    "|intrincad[oa]|tapeçaria|sublinhar|fomentar|alinhar-se com" +
    "|adicionalmente|multifacetad[oa]|holístic[oa]",
    "Adicionalmente, a solução é abrangente e vai aprimorar o fluxo."),

  PR("§9 paralelismo negativo",
    /(?<![\p{L}\p{N}_])(?:não\s+(?:apenas|só|somente)[^.!?]{0,80}mas\s+(?:também|sim)(?![\p{L}\p{N}_])|não\s+se\s+trata\s+apenas\s+de)/giu,
    "Não se trata apenas de medir: não é só uma técnica, mas também uma cultura."),

  P("§20 artefato de chat",
    "espero que (?:isso )?ajude|gostaria que eu|quer que eu" +
    "|me avise se|posso (?:detalhar|expandir) (?:qualquer|alguma)",
    "Espero que isso ajude! Me avise se quiser que eu detalhe algum ponto."),

  P("§21 disclaimer de corte",
    "até (?:a )?minha última atualização|com base n[ao]s informações disponíveis" +
    "|embora (?:os )?detalhes específicos sejam (?:limitados|escassos)" +
    "|não (?:está|estão) publicamente disponí(?:vel|veis)",
    "Até minha última atualização, os dados não estão publicamente disponíveis."),

  P("§22 bajulação",
    "ótima pergunta|excelente (?:ponto|observação)|ótimo ponto|você está absolutamente cert[oa]",
    "Ótima pergunta! Você está absolutamente certo nesse ponto."),

  P("§23 filler",
    "devido ao fato de que|neste momento em que|tem a capacidade de" +
    "|é importante (?:notar|ressaltar|destacar) que" +
    "|vale (?:a pena )?(?:notar|ressaltar|destacar) que" +
    "|cabe (?:notar|ressaltar|destacar) que",
    "É importante ressaltar que o agente tem a capacidade de replanejar."),

  P("§24 hedging empilhado",
    "poderia potencialmente|pode possivelmente|talvez possa|eventualmente poderia",
    "A mudança poderia potencialmente reduzir o custo por tarefa."),

  P("§25 conclusão genérica",
    "o futuro (?:é|parece) promissor|tempos empolgantes|um passo na direção certa" +
    "|jornada rumo à excelência",
    "O futuro é promissor, e este é um passo na direção certa."),

  P("§27 autoridade retórica",
    "a (?:verdadeira|real) (?:questão|pergunta) é|em sua essência" +
    "|o que (?:realmente|de fato) importa|o cerne da questão",
    "A verdadeira questão é outra: em sua essência, o que realmente importa é o loop."),

  P("§28 sinalização",
    "vamos (?:mergulhar|explorar|destrinchar|desvendar)" +
    "|veja o que você precisa saber|sem mais delongas",
    "Vamos mergulhar no assunto. Veja o que você precisa saber."),

  P("§32 fórmula de aforismo",
    "é a linguagem d[aeo]|é a moeda d[aeo]|torna-se uma armadilha",
    "O contexto é a moeda do agente, e a eficiência torna-se uma armadilha."),

  PR("§33 abre-conversa teatral",
    /(?:^|\n)\s*(?:honestamente\?|sinceramente\?|olha,|vamos ser honestos|verdade seja dita)/giu,
    "\nHonestamente? Depende do harness."),
];

// A lista inglesa é a original do guia, menos §14 (ver o cabeçalho) e com as
// três regras que a calibragem estreitou.
const EN = [
  P("§1 significance",
    "stands as|is a testament|a (?:vital|crucial|pivotal|key) role" +
    "|underscores its (?:importance|significance)|reflects (?:a )?broader" +
    "|symboliz(?:ing|es) its|setting the stage for|marks a shift" +
    "|key turning point|evolving landscape|indelible mark|deeply rooted",
    "The tool stands as a testament to an evolving landscape."),

  PR("§3 superficial -ing",
    /,\s+(?:highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|contributing\s+to|cultivating|fostering|encompassing|showcasing)(?![\p{L}\p{N}_])/giu,
    "The harness cuts rework, contributing to a stronger culture."),

  P("§4 promotional",
    "boasts a|vibrant|nestled|in the heart of|breathtaking|must-visit" +
    "|stunning|renowned|groundbreaking",
    "Nestled in the heart of the stack, a groundbreaking design."),

  P("§5 vague attribution",
    "industry reports|observers have (?:cited|noted)|experts (?:argue|say|believe)" +
    "|some critics argue|(?:studies|research) (?:show|shows|indicate) that",
    "Experts argue that it works, and studies show that adoption is rising."),

  // "robust" saiu (ver calibragem); "showcase" só como VERBO — o substantivo
  // ("the single-vendor showcase") é vitrine, uso legítimo.
  P("§7 AI vocabulary",
    "delve|intricate|intricacies|tapestry|testament|underscore" +
    "|pivotal|showcas(?:ing|es|ed)|garner|interplay|multifaceted|holistic",
    "A pivotal testament that showcases the intricate interplay."),

  PR("§9 negative parallelism",
    /(?<![\p{L}\p{N}_])(?:not\s+only[^.!?]{0,80}but\s+also(?![\p{L}\p{N}_])|it(?:'s|\s+is)\s+not\s+just\s+about)/giu,
    "It's not just about speed: not only fast but also cheap."),

  P("§20 chat artifact",
    "i hope this helps|certainly!|of course!|would you like|want me to|let me know if",
    "I hope this helps! Let me know if you would like more detail."),

  P("§21 cutoff disclaimer",
    "as of my last (?:training )?update|based on available information" +
    "|while specific details are (?:limited|scarce)|maintains a low profile",
    "As of my last update, based on available information, details are scarce."),

  P("§22 sycophancy",
    "great question|excellent point|you(?:'re| are) absolutely right",
    "Great question! You're absolutely right about that."),

  P("§23 filler",
    "in order to achieve|due to the fact that|at this point in time" +
    "|in the event that|has the ability to|it is important to note that",
    "It is important to note that the agent has the ability to replan."),

  P("§24 hedging", "could potentially possibly|might potentially|may possibly",
    "The change might potentially reduce cost."),

  P("§25 generic conclusion",
    "the future looks bright|exciting times|a step in the right direction" +
    "|journey toward excellence",
    "The future looks bright, and this is a step in the right direction."),

  P("§27 authority trope",
    "the real question is|at its core|what really matters|the deeper issue" +
    "|the heart of the matter",
    "The real question is this: at its core, what really matters is the loop."),

  P("§28 signposting",
    "let(?:'s| us) (?:dive|explore|break this down)" +
    "|here(?:'s| is) what you need to know|without further ado",
    "Let's dive in. Here's what you need to know."),

  P("§32 aphorism formula",
    "is the language of|is the currency of|becomes a trap",
    "Context is the currency of agents, and efficiency becomes a trap."),

  PR("§33 conversational opener",
    /(?:^|\n)\s*(?:honestly\?|look,|here's the thing|the thing is,|let's be honest)/giu,
    "\nHonestly? It depends on the harness."),
];

// §18: emoji. `Emoji_Presentation` e não `Extended_Pictographic`, porque este
// último casa ↔ (36 ocorrências no livro, todas relação bidirecional em texto
// técnico: "cliente ↔ servidor"), além de → ✓ ⚠. Seta não é decoração.
//
// A whitelist é a notação que o GUIA-EDITORIAL e a legenda da bibliografia
// definem — vale em qualquer posição, título inclusive, porque ⭐ marca o caso
// âncora justamente no título da seção.
const EMOJI = /\p{Emoji_Presentation}/gu;
const NOTACAO = new Set(["⭐", "✅", "❌", "🔵", "🟡", "🟢", "🔴", "⏳"]);
// Changelog usa ícone como índice visual (§30 isenta documento versionado).
const SEM_EMOJI = new Set(["livro/HISTORICO.md"]);

// Os dois idiomas, cada um com sua lista. O EN mora em livro/en/.
const IDIOMAS = [
  { tag: "pt", raiz: "livro", pular: (r) => r.startsWith("livro/en/"), padroes: PT },
  { tag: "en", raiz: "livro/en", pular: () => false, padroes: EN },
];

const falhas = [];
const semCodigo = (t) => t
  .replace(/^```[\s\S]*?^```/gm, (m) => m.replace(/[^\n]/g, " "))
  .replace(/`[^`\n]*`/g, (m) => " ".repeat(m.length));

const varrer = (dir, acc = []) => {
  for (const d of readdirSync(dir, { withFileTypes: true })) {
    const p = resolve(dir, d.name);
    if (d.isDirectory()) varrer(p, acc);
    else if (d.name.endsWith(".md")) acc.push(p);
  }
  return acc;
};

const contagem = {};
let linhasTotal = 0;

for (const { tag, raiz, pular, padroes } of IDIOMAS) {
  const base = resolve(RAIZ, raiz);
  if (!existsSync(base)) { falhas.push(`${raiz}/ não existe — o portão não está medindo nada`); continue; }
  let n = 0;
  for (const arq of varrer(base)) {
    const rel = relative(RAIZ, arq).replace(/\\/g, "/");
    if (pular(rel)) continue;
    n++;
    const bruto = readFileSync(arq, "utf8");
    const texto = semCodigo(bruto);
    const linhas = texto.split("\n");
    const linhasBrutas = bruto.split("\n");
    linhasTotal += linhas.length;

    // Escape por linha: `<!-- slop-ok: motivo -->` na anterior. Exige motivo
    // escrito — silenciar um achado tem de custar uma frase.
    const isenta = (i) => /<!--\s*slop-ok:\s*\S+.*-->/.test(linhasBrutas[i - 1] || "");
    const posLinha = (idx) => texto.slice(0, idx).split("\n").length - 1;

    for (const [nome, re] of padroes) {
      re.lastIndex = 0;
      for (const m of texto.matchAll(re)) {
        const i = posLinha(m.index);
        if (isenta(i)) continue;
        falhas.push(`${rel}:${i + 1}: [${tag}] ${nome} — ${JSON.stringify(m[0].trim())}`);
      }
    }

    if (!SEM_EMOJI.has(rel)) {
      linhas.forEach((linha, i) => {
        if (isenta(i)) return;
        for (const e of linha.match(EMOJI) || []) {
          if (NOTACAO.has(e)) continue;
          falhas.push(`${rel}:${i + 1}: [${tag}] §18 pictograma fora da notação — ${JSON.stringify(e)}`);
        }
      });
    }
  }
  contagem[tag] = n;
}

// ---------------------------------------------------------------------------
// Autoteste. Um portão que nunca acusa nada é indistinguível de um portão
// quebrado, e este passa limpo nos dois idiomas — então a única prova de que as
// expressões funcionam é rodá-las contra texto que DEVE falhar.
for (const [tag, lista] of [["pt", PT], ["en", EN]]) {
  for (const [nome, re, canario] of lista) {
    if (!canario) { falhas.push(`AUTOTESTE [${tag}]: "${nome}" sem amostra-canário`); continue; }
    re.lastIndex = 0;
    if (!re.test(canario)) falhas.push(`AUTOTESTE [${tag}]: "${nome}" não acusou o próprio canário — expressão afrouxada`);
    // A quebra de linha não pode salvar o slop.
    const dobrado = canario.replace(/ /g, (m, i) => (i === Math.floor(canario.length / 2) ? "\n" : m));
    re.lastIndex = 0;
    if (dobrado !== canario && !re.test(dobrado)) falhas.push(`AUTOTESTE [${tag}]: "${nome}" perde o achado quando a frase quebra linha`);
  }
}
{
  EMOJI.lastIndex = 0;
  if (!EMOJI.test("🚀")) falhas.push("AUTOTESTE: §18 não reconhece mais pictograma");
  EMOJI.lastIndex = 0;
  if (NOTACAO.size !== 8) falhas.push(`AUTOTESTE: a notação documentada mudou de tamanho (${NOTACAO.size} ≠ 8) sem revisão`);
  // ↔ → ✓ ⚠ são notação técnica, não emoji: `Emoji_Presentation` já os deixa de fora,
  // e é por isso que a regra não usa `Extended_Pictographic` (que casa ↔).
  if (EMOJI.test("↔") || EMOJI.test("✓")) falhas.push("AUTOTESTE: §18 voltou a casar seta/marca técnica");
  EMOJI.lastIndex = 0;
}
if (!contagem.pt || !contagem.en) falhas.push(`idioma sem arquivo (pt: ${contagem.pt || 0}, en: ${contagem.en || 0}) — o portão não está medindo nada`);
if (linhasTotal < 2000) falhas.push(`só ${linhasTotal} linhas analisadas — o portão não está medindo nada`);
// ---------------------------------------------------------------------------

if (falhas.length) {
  console.error(`✗ marcas de escrita de IA: ${falhas.length} achado(s)`);
  falhas.forEach((f) => console.error("   " + f));
  console.error(`\n   Cada achado é um trecho que soa gerado. Reescreva, ou — se o uso for`);
  console.error(`   legítimo — declare na linha anterior: <!-- slop-ok: motivo -->`);
  process.exit(1);
}
console.log(`✓ prosa sem marcas de IA: ${contagem.pt} arquivos [pt] + ${contagem.en} [en], ${linhasTotal} linhas, ${PT.length + EN.length + 1} padrões (travessão fora, por decisão — ver cabeçalho)`);
