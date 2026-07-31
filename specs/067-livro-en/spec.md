# Spec 067 — Livro multiidioma: rodada inglês

**Branch**: `067-livro-en` · **Data**: 2026-07-31 · **Status**: aprovada ("prossiga" — escopo total, sincronia no mesmo ciclo, PDFs EN)

## Decisões de UX/UI (aprovadas com mockups)

1. **`/en/` espelhado** com slugs em inglês; PT permanece a **fonte canônica**.
2. **Seletor PT·EN** (pill textual, sem bandeiras) em todas as páginas, levando à
   MESMA página no outro idioma; preferência gravada; na capa PT, navegador em
   inglês ganha um **convite discreto** — nunca redirect forçado.
3. **Selo de sincronia** (a peça central): cada fonte EN declara
   `<!-- i18n fonte:<pt> edicao:X hash:<md5-8> -->`; o build compara com o PT
   atual e mostra "in sync with edition X" ou o aviso âmbar de tradução atrasada.
   Vira portão de qualidade: selo errado = build falha.
4. **Escopo**: 27 páginas traduzidas (18 capítulos + benchmark + aparato);
   ficam em PT com aviso: Histórico, diário do Radar e o conteúdo do card de
   news (registros operacionais).
5. **PDFs e Markdown EN** completos no mesmo CI; `hreflang` correto para SEO.

## Arquitetura

- Fontes: `livro/en/` espelhando `livro/` (+ `comparative.md` do benchmark);
  `publicar/sumario.en.json` espelha o sumário por posição (par de idiomas
  derivado posicionalmente — base do seletor e do hreflang).
- Motor: passada dupla (`node build.mjs` → docs/; `LIVRO_LANG=en node build.mjs`
  → docs/en/), com dicionário T do chrome, regexes de datação/Leitura executiva
  bilíngues, assets compartilhados na raiz, grafo EN remapeado (rótulos/URLs) do
  grafo PT, e portões `verifica-capitulos` por idioma.
- Tradução: 6 agentes em paralelo escrevendo direto em `livro/en/`, sob o
  contrato `kit-traducao.md` (glossário fixo, seções canônicas, estrutura 1:1,
  hash real da fonte).
- Companion: superfície principal do widget em EN (launcher, consent, input,
  botões); demais strings ficam PT — **limitação conhecida** desta rodada.
- RAG: `livro/en/` excluído do corpus (PT canônico responde; o modelo traduz).

## Manutenção viva (regra permanente)

Toda spec futura que edite `livro/` inclui o passo **"traduzir o delta"**
(atualizar os EN afetados + hash). Se ficar para trás, o selo âmbar aparece
sozinho — a dívida é visível, nunca silenciosa.

## Verificação

- Portões PT e EN verdes; e2e Chromium: pill nos dois sentidos página-a-página,
  selo de sincronia em dia (e âmbar quando fonte PT muda), convite por idioma
  do navegador, downloads EN, grafo EN com rótulos/URLs ingleses.
- HISTORICO 0.62; corpus regenerado sem EN; CI com PDFs das duas línguas.
