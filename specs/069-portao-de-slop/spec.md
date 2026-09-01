# Spec 069 — Portão de slop: marcas de escrita de IA barradas na fonte, PT e EN

> **Branch:** `claude/educational-material-toc-ai-naotqe` · **ADR:** 0009
> **Origem:** porte do portão do livro *Teoria das Restrições* (spec 009 de lá), a pedido do autor

## O quê

Um portão `publicar/verifica-slop.mjs` que roda **primeiro** no `npm run build`, sobre a
fonte (`livro/**/*.md`), e barra marcas de escrita gerada por IA antes que virem página.

## Por quê

Os capítulos nascem com apoio de IA — o `HISTORICO` registra o modelo de cada edição. O
Princípio I exige **evidência acima de retórica**, e o registro típico de texto gerado é
retórica pura. Nenhum portão olhava a prosa: `verifica-capitulos.mjs` mede esqueleto v3,
datação, downloads e sincronia PT↔EN. Um capítulo inteiro escrito no registro *"esta
arquitetura desempenha um papel crucial no cenário em evolução"* passa hoje com build verde.

Auditar depois custa uma varredura por capítulo, para sempre. Barrar na entrada custa um
portão, uma vez.

## Escopo

**32 padrões lexicais** — 16 em português e 16 em inglês, cada um citando a seção do guia de
origem ("Signs of AI writing", Wikipédia): significância inflada (§1), gerúndio/-ing de
enfeite (§3), promocional (§4), atribuição vaga (§5), vocabulário de IA (§7), paralelismo
negativo (§9), artefato de chat (§20), disclaimer de corte (§21), bajulação (§22), filler
(§23), hedging (§24), conclusão genérica (§25), autoridade retórica (§27), sinalização (§28),
fórmula de aforismo (§32), abre-conversa teatral (§33). Mais **§18** (emoji fora da notação
documentada).

**Fora, por decisão medida:** §14 (travessão) nos dois idiomas — ver ADR 0009. §16 (listas
com rótulo em negrito) — descartada no repositório de origem por acusar notação legítima.

## Critérios de aceite (verificáveis)

| # | Critério | Como verificar |
|---|---|---|
| A1 | Passa limpo nos dois idiomas | `node publicar/verifica-slop.mjs` sai 0 |
| A2 | Está no build | `npm run build` roda o portão antes de tudo e sai 0 |
| A3 | Acusa slop plantado, em PT e em EN | anexar slop a um capítulo de cada → sai 1, com arquivo, linha e tag de idioma |
| A4 | Frase quebrada em duas linhas não escapa | canário dobrado no meio continua acusado (autoteste) |
| A5 | Todo padrão tem canário e o acusa | autoteste falha o build se qualquer expressão for afrouxada |
| A6 | O escape funciona e exige motivo | `<!-- slop-ok: motivo -->` suprime só a linha seguinte |
| A7 | Não mede travessão | arquivo `.md` só de apostos com travessão passa limpo |
| A8 | §18 não confunde notação técnica com emoji | `↔`, `→`, `✓` não são acusados; `🚀` é |
| A9 | Portão vazio falha | menos de 2.000 linhas, ou um idioma sem arquivo → sai 1 |

## Evidência

```
✓ prosa sem marcas de IA: 27 arquivos [pt] + 27 [en], 6053 linhas, 33 padrões
✓ Grafo do livro: 54 nós, 330 arestas
✓ Livro gerado [pt]: 28 páginas + capa em docs/ (links internos OK)
✓ Livro gerado [en]: 27 páginas + capa em docs/en/ (links internos OK)
✓ template verificado [pt]: 18 capítulos com C01/N02 + 10 páginas de aparato OK
✓ template verificado [en]: 18 capítulos com C01/N02 + 9 páginas de aparato OK
```

A3, medido plantando slop no cap. 05 dos dois idiomas e revertendo:

```
livro/capitulos/05-ferramentas.md:110: [pt] §1 significância inflada — "desempenha um papel\ncrucial"
livro/capitulos/05-ferramentas.md:111: [pt] §18 pictograma fora da notação — "🚀"
livro/en/chapters/05-tools.md:2:       [en] §1 significance — "evolving\nlandscape"
livro/en/chapters/05-tools.md:3:       [en] §7 AI vocabulary — "showcasing"
```

As duas frases acusadas estavam quebradas em duas linhas (A4).

## Calibragem

Zero achados nos dois idiomas. Os candidatos que a primeira versão marcou eram todos falso
positivo, e cada um estreitou uma regra:

- **"robusto" / "robust"** — 3 ocorrências entre este livro e o do Maestro, todas técnicas
  ("o modelo de estado mais robusto", "atenção robusta"), e uma delas era o Maestro
  *ensinando* que "o script é robusto" é critério vago. Saiu das duas listas.
- **"showcase" (EN)** — 3 ocorrências, todas substantivo ("the single-vendor showcase"):
  vitrine, uso legítimo. O tell é o verbo; a regra passou a exigir `showcasing/showcases/showcased`.
- **"serves as a" (EN)** — 1 ocorrência, *"a small core that serves as a socket"*: função
  metafórica, não fuga de cópula. Saiu de §1.
- **`↔`** — 36 ocorrências, relação bidirecional em texto técnico. `Extended_Pictographic`
  casava; `Emoji_Presentation` não. A regra trocou de propriedade Unicode.
- **11 pictogramas avulsos** (🏷 📈 🔑 🏁 …) — todos no `HISTORICO` e em nenhum outro
  arquivo. Changelog usa ícone como índice visual; ficou fora de §18.

## Constitution Check

| Princípio | Situação |
|---|---|
| I — evidência acima de retórica | É o princípio que motiva a rodada. |
| II — a fonte-base é o código | Não toca a leitura de código nem o Apêndice A. |
| III — método pedagógico | Não altera esqueleto de capítulo; o portão irmão continua medindo isso. |
| IV — livro vivo | Nenhuma linha do livro muda, então não há nova edição em `HISTORICO.md`. |
| V — segurança | Sem segredo; Node puro, sem dependência nova. |
| VI — neutralidade e acessibilidade | Vendor-agnóstico; custo zero. |
| VII — spec-driven e branch por melhoria | Spec + ADR antes do merge. **Desvio:** a branch é `claude/...`, imposta pelo ambiente, e não `NNN-nome`. O número da spec segue a sequência. |

## Fora de escopo

- Reescrever texto existente: não há o que reescrever (os dois idiomas dão zero).
- Unificar as três cópias do portão (aqui, no livro TOC e no Maestro) num pacote só.
