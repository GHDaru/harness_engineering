# Implementation Plan: DOI no site e README

**Branch**: `019-doi-badge-site` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary
Fixar o DOI `10.5281/zenodo.21632412` em três lugares: badge no README, link discreto na tela-capa (junto ao selo de versão) e seção "Como citar" na página do autor.

## Constitution Check
PASS. IV (livro vivo): o DOI materializa a citabilidade da obra viva. V: sem segredo. VII: branch `019-…`, merge ao fim. Sem identificador interno de modelo.

## Arquivos
```
README.md                      # badge do DOI (substitui o marcador da 018)
publicar/build.mjs             # paginaSplash(): link do DOI junto ao selo de versão
publicar/tema/estilo.css       # estilo do link do DOI na splash (se preciso)
livro/autor.md                 # seção "Como citar" com referência + DOI
livro/HISTORICO.md             # edição 0.15
```

## Design
- Na capa, **texto-link** ("DOI: 10.5281/zenodo.21632412") em vez de imagem-badge, para não depender de asset externo no fundo escuro.
- No README, o **badge-imagem** padrão do Zenodo (convencional em repositórios).
- "Como citar" no back matter (página do autor) é o lugar acadêmico natural.

## Complexity Tracking
Sem violações.
