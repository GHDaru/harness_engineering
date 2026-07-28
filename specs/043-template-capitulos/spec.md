# Spec 043: Template visual dos capitulos (design system)

> Decisões de arquitetura: [ADR 0005](../../adr/0005-template-capitulos-um-spec.md) (1 spec de motor + verificação por capítulo) e [ADR 0006](../../adr/0006-design-system-componentes.md) (design system de componentes). Catálogo: [`publicar/DESIGN-SISTEMA.md`](../../publicar/DESIGN-SISTEMA.md).

## Requisitos

- FR-001: páginas de capítulo (título numerado no `sumario.json`) ganham **C01 CabeçalhoDeCapítulo**: kicker da parte, título, teaser, datação absorvida (C02) e tempo de leitura estimado (~200 palavras/min, descontando blocos de código).
- FR-002: o `h1` e o blockquote de datação do Markdown saem do corpo renderizado nessas páginas (o C01 já os mostra); aparato/sumário/splash intactos.
- FR-003: paginação anterior/próximo vira **N02 PaginaçãoEmCartões** em todas as páginas com sidebar.
- FR-004: a seção `### Leitura executiva` vira **C08 LeituraExecutiva** (painel destacado; âncora preservada).
- FR-005: theme-aware (claro/escuro por `--vars`), responsivo; build + link-check verdes; **verificação por capítulo** (`publicar/verifica-capitulos.mjs`, 18 capítulos + aparato) conforme ADR 0005.

## Gate humano (mockups aprovados em 2026-07-28)

| Componente | Alternativas apresentadas | Aprovado |
|---|---|---|
| C01 CabeçalhoDeCapítulo | A herói-cartão · B faixa editorial · C margem editorial | **B — faixa editorial** (fio âmbar, número em marca d'água, kicker) |
| C08 LeituraExecutiva | V1 painel âmbar · V2 editorial sem caixa · V3 cartão com chip | **V1 — painel âmbar** |
| N02 PaginaçãoEmCartões | V1 cartões simples · V2 cartões com badge · V3 fio editorial | **V2 — cartões com badge** (linguagem dos cartões da entrada) |

Método de validação: **página-espécime** (uma tela compondo todos os componentes do catálogo) + 3 modelos por componente novo. Componentes já em produção (C02–C07, C09–C12, N01, N03–N05) foram considerados aprovados pelos gates das specs anteriores.

## Verificação

- `node build.mjs` → ✓ 25 páginas, links internos OK.
- `node verifica-capitulos.mjs` → ✓ 18 capítulos com C01/N02 (badge correto, 1 só `h1`, datação absorvida, C08 onde a fonte declara) + 7 páginas de aparato sem C01 e com selo preservado.
- Screenshots conferidos nos dois temas (cap. 02, cap. 00, glossário).
