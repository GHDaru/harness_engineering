# Spec 068 — Release automatizada por tag + v0.62.0

**Branch**: `068-release-v062` · **Data**: 2026-07-31 · **Status**: aprovada ("sim, vamos fazer uma release")

## Contexto

Última release: **v0.14.0** (2026-07-27) — a que criou o DOI-conceito no Zenodo
(10.5281/zenodo.21632412). Desde então o livro andou 48 edições (0.15→0.62) sem
release. A API do GitHub desta sessão não cria releases diretamente; a solução é
**automação por tag**: um workflow que transforma toda tag anotada `v*` em
GitHub Release (título padrão + notas = mensagem da tag), o que dispara o
webhook do Zenodo e cunha o **DOI de versão** — e fica reutilizável para todas
as releases futuras (criar release = criar tag anotada).

## O que muda

1. `.github/workflows/release.yml` — `on: push: tags [v*]` → `gh release create
   --notes-from-tag --verify-tag` com o token do Actions (`contents: write`).
2. Tag anotada **v0.62.0** na main, com notas de release cobrindo o arco
   0.15→0.62 (destaques por tema + o dia 2026-07-31 em detalhe) — fonte única
   das notas é a mensagem da tag.

## Verificação

- Workflow verde na tag; Release v0.62.0 publicada com as notas; Zenodo com
  DOI de versão (confirmação visual do editor — o webhook é externo).
