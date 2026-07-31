# Plano — Spec 062 (Novidades na capa)

## Abordagem

Reuso máximo da 061: os parsers `noticiaDoRadar()` e `ultimaEdicao()` já existem em
`publicar/build.mjs`, mas hoje são declarados **depois** de `paginaSplash()` ser
escrita (linha ~436). O trabalho é (1) **hoistar** o cálculo da notícia/edição para
antes da escrita do index e (2) injetar um bloco novo no splash com classes próprias
(`splash-news` / `splash-vedicao`) — a entrada continua com `ent-news`/`ent-vedicao`
intocadas (R4).

## Mudanças por arquivo

1. **`publicar/build.mjs`**
   - Mover `noticiaDoRadar()`, `ultimaEdicao()` e as consts `noticia`/`edicao` para
     antes de `paginaSplash()` (as funções são puras sobre arquivos; sem efeito
     colateral). `blocoNews` (entrada) permanece onde está, consumindo as consts.
   - Em `paginaSplash()`, após `.splash-ctas` e antes de `.splash-creditos`:
     - `noticia` ⇒ `<div class="splash-news">` com kicker (🗞 Novidade · data ·
       badge `<b class="splash-news-imp">impacto X</b>`), o `itemHtml` e o link
       "ver o Radar completo →".
     - `edicao` ⇒ `<p class="splash-vedicao">` "📖 Nesta edição (vX · data): título —
       Histórico" (link relativo `historico.html`).
   - Qualquer uma `null` ⇒ string vazia (R3).

2. **`publicar/tema/estilo.css`** — bloco novo "News na capa (spec 062)":
   - `.splash-news`: card âmbar translúcido (mesma família da `.ent-news`), mas
     denso — padding menor, `max-width` alinhado à coluna `.splash-texto`,
     `text-align: left` (o splash centraliza em telas estreitas; o card mantém
     leitura de card).
   - `.splash-news-k` kicker uppercase âmbar; `.splash-news-imp` badge de impacto.
   - `.splash-vedicao`: linha `.8rem` na cor `--muted`, margem curta — hierarquia
     visivelmente menor que o card (R2/R5).
   - Media query estreita: card ocupa 100% da coluna.

3. **`publicar/verifica-capitulos.mjs`** — portão novo: se `radar/RADAR.md` tem
   linha de notícia válida, `docs/index.html` deve conter `splash-news`; se o
   HISTORICO parseia, deve conter `splash-vedicao`. (Condicional para respeitar R3 —
   o portão não pode exigir o que o parse legitimamente omite.)

4. **`livro/HISTORICO.md`** — edição 0.57 (nota A3: Claude Code (Anthropic)).

## Verificação

- `npm run build` (roda o portão) — 18 caps + downloads + grafo + news na capa.
- e2e Playwright/Chromium (flags PNA de teste local): asserts case-insensitive
  (CSS pode usar `text-transform`), 5 checagens: card com conteúdo real do RADAR,
  impacto A, linha da edição com v0.57.0, links, e `.ent-news` intacta na entrada.
- Corpus: `livro/` muda (HISTORICO) ⇒ `python3 build_corpus.py`.

## Riscos

- **Ordem do build**: hoistar os parsers muda posição de leitura de arquivos, não
  o resultado (funções puras). Mitigação: e2e compara conteúdo real nas duas páginas.
- **Splash lotado**: card + linha empurram créditos para baixo em telas baixas.
  Mitigação: card compacto (1 notícia, sem parágrafos extras) e media queries.
