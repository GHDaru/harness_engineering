# Implementation Plan: Estudo sobre processos e metodologias de escrita editorial e acadêmica

**Branch**: `010-estudo-metodologias-escrita` | **Date**: 2026-07-26 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/010-estudo-metodologias-escrita/spec.md`

## Summary

Incorporar ao `livro/GUIA-EDITORIAL.md` uma nova seção grande — um **survey standalone** das metodologias de escrita editorial e acadêmica, tradicionais e da era-IA — que também torna explícito, com transparência de co-autoria humano+IA, o método com que este livro é escrito. Abordagem: rodar a **Fase 0 de pesquisa** (levantamento verificado das duas famílias de metodologia), modelar as entidades (Metodologia / Fonte / Prática do livro), e escrever a seção seguindo Diátaxis (referência + explicação), sob o gate de link-check do build.

## Technical Context

**Language/Version**: Português (prosa) + Markdown; sem código de produto novo.

**Primary Dependencies**: motor do livro `publicar/` (markdown-it) para publicação; skill `academic-research` (localizar → validar → integrar fontes); `livro/bibliografia.md` existente (pedagogia já validada).

**Storage**: N/A — arquivos Markdown versionados em git.

**Testing**: gate de link-check do build (`node publicar/build.mjs` falha em link interno quebrado); verificação de fontes por **busca cruzada** (≥2 menções independentes; nada de URL/ID inventado).

**Target Platform**: site GitHub Pages (`docs/`) + Markdown no repositório.

**Project Type**: documentação/livro (nova seção do Guia Editorial — texto tipo *reference*+*explanation* na taxonomia Diátaxis).

**Performance Goals**: N/A (prosa).

**Constraints**: coerência com a constituição (esp. Princípio I — evidência); sem segredos (Princípio V); prosa PT com termos técnicos sem tradução (Princípio VI).

**Scale/Scope**: abrangência de survey — ≥5 metodologias tradicionais e ≥4 orientadas a IA, organizadas por famílias, cada uma com fonte real; profundidade de seção longa (não um livro à parte).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Avaliação dos 7 princípios (v1.1.0) contra esta feature:

| Princípio | Status | Justificativa |
|---|---|---|
| **I. Evidência acima de retórica** (NÃO-NEGOCIÁVEL) | ✅ PASS | O survey exige fonte real por metodologia (FR-001/002/005/007); afirmações sobre o método deste livro são ancoradas em artefatos reais do repo (specs, constituição, commits). Fontes validadas por busca cruzada; lacunas registradas, não preenchidas com fonte fraca. |
| **II. A fonte-base é o código** | ✅ PASS (adaptado) | Esta feature não é uma dimensão de harness, então "fonte-base = código dos harnesses" não se aplica literalmente. A regra análoga vale: as afirmações sobre o *processo deste livro* são evidenciadas pelos **artefatos do próprio repositório** (os `specs/`, a constituição, o histórico, os commits) — o repo é a espinha empírica do meta-relato. Adaptação registrada, não violação. |
| **III. Método pedagógico combinado** | ✅ PASS (Diátaxis) | O esqueleto v3 de *capítulo* não se aplica: pela própria regra Diátaxis do Princípio III, o Guia Editorial é texto de **referência/explicação**, não um capítulo. A seção segue Diátaxis (não mistura tipos) e pode usar Backward Design na sua micro-estrutura (o que o leitor deve saber ao fim), sem os requisitos de *learning task*/kata de um capítulo. |
| **IV. Livro vivo** | ✅ PASS | A seção recebe data de captura/atualização; práticas de IA são datadas (expiram); `HISTORICO.md` ganha entrada de edição. |
| **V. Segurança e credenciais** | ✅ PASS | Sem segredos; a divulgação de autoria (FR-009) não expõe chaves; descreve processo, não credenciais. |
| **VI. Neutralidade e acessibilidade** | ✅ PASS | Metodologias, não produtos; vendor-agnóstico; prosa PT, termos técnicos sem tradução. |
| **VII. Spec-driven e branch-per-melhoria** (NÃO-NEGOCIÁVEL) | ✅ PASS | Esta é *a execução do ciclo oficial* (`/speckit-specify` → `clarify` → `plan` → `tasks` → `analyze` → `implement`) na branch `010-estudo-metodologias-escrita`; merge ao fim, verificado. |

**Resultado do gate: PASS** — nenhuma violação. Complexity Tracking vazio.

## Project Structure

### Documentation (this feature)

```text
specs/010-estudo-metodologias-escrita/
├── spec.md              # /speckit-specify (feito)
├── checklists/
│   └── requirements.md  # /speckit-specify (feito)
├── plan.md              # Este arquivo (/speckit-plan)
├── research.md          # Fase 0 (/speckit-plan)
├── data-model.md        # Fase 1 (/speckit-plan)
├── quickstart.md        # Fase 1 (/speckit-plan)
├── contracts/
│   └── outline.md       # Fase 1 — o "contrato" desta feature é a estrutura da seção
└── tasks.md             # /speckit-tasks (próximo)
```

### Source Code (repository root)

Feature de documentação — o "código-fonte" alterado é o conteúdo do livro e o manifesto de publicação:

```text
livro/
├── GUIA-EDITORIAL.md    # ALVO: recebe a nova seção "Estudo sobre metodologias de escrita"
├── bibliografia.md      # atualizada: nova subseção de fontes (tradicionais + IA)
└── HISTORICO.md         # atualizado: entrada de edição (livro vivo)

publicar/
└── sumario.json         # (sem mudança — o "Guia Editorial" já está publicado)
```

**Structure Decision**: A seção vive em `livro/GUIA-EDITORIAL.md` (decisão do `/speckit-clarify`), que já é uma página publicada. Não há arquivo novo em `livro/apendices/` nem mudança no motor `publicar/`. As fontes vão para uma subseção nova de `livro/bibliografia.md`.

## Complexity Tracking

> Sem violações de constituição a justificar — seção vazia.
