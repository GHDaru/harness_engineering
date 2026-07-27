# Implementation Plan: DOI e citação (Zenodo)

**Branch**: `018-doi-citacao-zenodo` · **Date**: 2026-07-27 · **Spec**: [spec.md](./spec.md)

## Summary

Preparar o repositório para receber um **DOI do Zenodo** (DataCite): licenças (CC BY 4.0 conteúdo + MIT código), `CITATION.cff`, `.zenodo.json` e seções "Como citar"/"Licença" no README, com espaço para o badge. A emissão do DOI é ação do autor no Zenodo (tutorada); o número volta e é fixado num follow-up.

## Technical Context

- **Arquivos-raiz** (o GitHub e o Zenodo os leem por convenção): `LICENSE`, `LICENSE-CODE`, `CITATION.cff`, `.zenodo.json`.
- **CC BY 4.0**: `LICENSE` com o aviso canônico + URLs oficiais do deed/legalcode (a rede bloqueou baixar o texto integral; o identificador SPDX autoritativo vai no `.zenodo.json`/`CITATION.cff`, que é o que o Zenodo usa).
- **MIT**: texto integral (curto e conhecido), com titular "Gilsiley Henrique Darú".
- **Não toca `publicar/`** → não dispara deploy do Pages. O badge no site é follow-up (precisa do número do DOI).

## Constitution Check

| Princípio | Conformidade |
|---|---|
| IV. Livro vivo | ✓ Concept DOI (obra) + DOI por versão (edição) espelham a cláusula de expiração. |
| V. Segurança | ✓ Sem segredo. |
| VI. Neutralidade/acesso | ✓ CC BY 4.0 + MIT maximizam reuso aberto. |
| VII. Spec-driven | ✓ Branch `018-…`, merge ao fim. |
| Autoria (Guia §6, ICMJE/COPE) | ✓ Humano = creator (ORCID); IA declarada na descrição, não como autor. |
| Identidade de modelo | ✓ Sem identificador interno. |

**Resultado**: PASS.

## Project Structure

```
LICENSE            # CC BY 4.0 (conteúdo) — aviso canônico + URLs
LICENSE-CODE       # MIT (código) — texto integral
CITATION.cff       # metadados de citação (autor+ORCID, título, versão, licença)
.zenodo.json       # metadados do depósito Zenodo (creators, tipo, licença, descrição c/ nota de IA)
README.md          # + seções "Como citar" e "Licença" (com espaço p/ badge do DOI)
livro/HISTORICO.md # + edição 0.14
```

## Design decisions

1. **Dual license**: CC BY 4.0 (texto/figuras) + MIT (código) — correto para um repo livro+código; declarado sem ambiguidade no README.
2. **Autoria honesta**: creator humano com ORCID; IA na descrição — coerente com o que o próprio livro defende.
3. **DOI em duas etapas**: arquivos prontos agora; número fixado quando o autor emitir (evita placeholder falso publicado como se fosse real).
4. **Zenodo lê o SPDX** dos metadados; não dependemos do parsing do `LICENSE` pelo GitHub para o depósito.

## Complexity Tracking

*Sem violações.*
