# Data Model — Estudo sobre metodologias de escrita

> Feature de documentação: as "entidades" são conceitos que estruturam a seção e suas fontes, não tabelas de banco. Servem para garantir consistência e testabilidade (mapeiam para os FRs/SCs da spec).

## Entidade: Metodologia

Uma prática/escola de escrita ou editoração.

| Campo | Tipo | Regra |
|---|---|---|
| `nome` | texto | obrigatório, único na seção |
| `periodo` | enum {`tradicional`, `era-IA`} | obrigatório |
| `familia` | texto | agrupamento (ex.: "estrutura científica", "craft/estilo", "co-escrita humano-IA") |
| `estabelece` | frase | **obrigatório** — o que a metodologia ensina/estabelece (nunca só o nome) — FR-001/FR-002 |
| `quando_aplica` | frase | contexto de uso |
| `fontes` | ≥1 referência | **obrigatório** — sem fonte não entra (FR-001/002/005) |
| `status_evidencia` | enum {`✓ validada`, `⏳ pendente`, `lacuna`} | FR-005/FR-007 |

**Regras derivadas dos requisitos:**
- FR-010 / SC-003: ≥5 metodologias com `periodo=tradicional` e ≥4 com `periodo=era-IA`, distribuídas por ≥3 famílias cada.
- Uma metodologia com `status_evidencia=lacuna` é declarada como tal, nunca apresentada como consolidada (FR-007).

## Entidade: Fonte

Referência que sustenta uma metodologia.

| Campo | Tipo | Regra |
|---|---|---|
| `titulo` | texto | obrigatório |
| `autor_veiculo` | texto | obrigatório |
| `ano` | número | quando conhecido |
| `identificador` | DOI \| ISBN \| URL | obrigatório (alcançável) |
| `status` | enum {`✓`, `⏳`} | ✓ = confirmada por ≥2 fontes independentes (busca cruzada); ⏳ = não-confirmada, **marcada como tal** |

**Regra:** nenhuma `Fonte` inventada (FR-005 / Princípio I / SC-002). Toda `⏳` fica explicitamente marcada no texto.

## Entidade: Prática do livro

Uma decisão de processo *deste* livro, ligada a um princípio e a uma metodologia.

| Campo | Tipo | Regra |
|---|---|---|
| `nome` | texto | ex.: "pesquisa dupla verificada", "spec-driven", "livro vivo" |
| `principio` | ref → Constituição (I–VII) | obrigatório |
| `origem` | ref → Metodologia(s) | de onde a prática deriva (tradicional e/ou IA) |
| `manifestacao` | frase + evidência do repo | onde se vê no repositório (specs/, HISTORICO, commits) — Princípio II adaptado |
| `co_autoria` | booleano/nota | se envolve o agente de IA; a divulgação de FR-009 |

**Regra:** a seção "método deste livro" deve permitir a um leitor nomear ≥4 práticas e o porquê (SC-001), e declarar a co-autoria humano+IA (FR-009/SC-006).

## Relações

- `Metodologia` —cita→ `Fonte` (1..N)
- `Prática do livro` —deriva de→ `Metodologia` (1..N) e —cumpre→ `Princípio` (1)
- A seção contrasta `Metodologia[periodo=tradicional]` × `Metodologia[periodo=era-IA]` (Parte C da outline).
