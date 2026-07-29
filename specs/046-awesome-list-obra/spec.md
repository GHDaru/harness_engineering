# Spec 046: Awesome Harness Engineering ligado à obra

**Feature Branch**: `046-awesome-list-obra` · **Criada em**: 2026-07-29

## Contexto

O autor mantém a coleção viva [Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering) — recursos, padrões e templates curados **por problema** (mesma lógica de organização do livro). A obra deve apontar para ela onde houver elementos consultáveis.

## Requisitos

- FR-001: cada capítulo com dimensão correspondente na lista ganha um item **"Consulte também"** apontando para a **seção específica** (âncora) da lista — não para a raiz genérica.
- FR-002: o cap. 00 apresenta a lista na seção "Os harnesses do estudo"; o cap. 01 na §5 (origem do corpus); o Apêndice do estudo aponta para *Reference Implementations*.
- FR-003: a Bibliografia ganha a entrada da coleção (fonte da indústria, viva).
- FR-004: build + link-check + portão por capítulo verdes; corpus regenerado.

## Mapeamento capítulo → seção da lista

| Capítulo | Âncora |
|---|---|
| 00, 01, 14 | `#foundations` |
| 02 | `#agent-loop` |
| 03, 04 | `#context-delivery--compaction` |
| 05 | `#tool-design` |
| 06, 17 | `#skills--mcp` |
| 07 | `#permissions--authorization` (+ `#security-sandbox--permissions`) |
| 08 | `#memory--state` |
| 09 | `#planning--task-decomposition` |
| 10 | `#task-runners--orchestration` |
| 11 | `#verification--ci-integration` (+ `#evals--verification`) |
| 12 | `#debugging--developer-experience` |
| 13 | `#human-in-the-loop` |
| 15 | `#production-infrastructure--operations` |
| 16 | `#skills--mcp` |
| Apêndice do estudo | `#reference-implementations` |

Ponto de inserção: fim de **"## Fontes da indústria"** quando existir; senão, parágrafo antes de **"## Verificação"** (14/15/16) ou fim da seção temática (00/01/apêndice).
