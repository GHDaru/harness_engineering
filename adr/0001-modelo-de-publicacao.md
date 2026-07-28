# 0001 — Modelo de publicação (main=live, branch por spec, release p/ DOI)

- **Status:** Aceito
- **Data:** 2026-07-27
- **Contexto (feature/spec):** processo (relacionado ao CLAUDE.md e à constituição, Princípio VII)

## Contexto
O autor vai auditar o livro e inserir muitas correções; não quer "publicar a cada correção". O GitHub Pages hospeda um site por repositório (staging separado é gambiarra) e o deploy dispara no push à `main` (paths `livro/`, `publicar/`, `benchmark/`). Há também os DOIs por versão via Zenodo (release).

## Decisão
Manter **tudo na `main`**, mas **trabalhar em uma branch por spec** e fazer **um único merge por lote** — o merge na `main` é o que publica. Marcos de edição viram **Release** (tag), que emite o **DOI de versão**. Preview do rascunho é local/por screenshots.

## Alternativas avaliadas
- **A — Deploy só em Release** (gatilho `release: published`): a `main` acumula sem publicar; publica só no release. Prós: controle total; site = última edição liberada. Contras: rascunho invisível na web (depende de preview local); mais cerimônia.
- **B — main=live com branch por spec (escolhida)**: publica no merge do lote. Prós: simples, zero infra, autor vê ao vivo após o merge; DOIs continuam por release. Contras: estados intermediários ficam públicos entre edições.
- **C — Staging separado** (Cloudflare/Netlify + ambiente Railway): preview dedicado. Contras: mais infra para manter; o autor recusou explicitamente.

## Justificativa
B satisfaz "não publicar a cada correção" (o trabalho fica na branch), "ver as melhorias" (ao vivo após o merge + screenshots antes), e "sem mais infra". Para um *livro vivo*, estados intermediários públicos são aceitáveis. Trocar para A depois é um ajuste de ~15 min no gatilho.

## Consequências
- Positivas: fluxo simples, rastreável (branch por spec), DOIs por release preservados.
- Custos aceitos: entre edições, a `main` pública pode conter trabalho ainda em curso.
- Reversibilidade: alta — mudar para "deploy só em release" é trivial.
