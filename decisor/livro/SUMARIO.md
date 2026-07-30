# Sumário — Decisão Multicritério: do julgamento ao algoritmo

> Livro vivo. A sequência didática abaixo é a espinha do projeto: **cada capítulo tem uma
> etapa executável no `decisor-zero/`**, e o diff entre etapas consecutivas é a lição.
> Desenho pedagógico: Backward Design + 4C/ID (ver [GUIA-EDITORIAL](GUIA-EDITORIAL.md));
> espinha de conteúdo apoiada em Belton & Stewart (2002), Ishizaka & Nemery (2013) e
> Greco, Ehrgott & Figueira (2016) — ver [bibliografia](bibliografia.md).
> Racional da sequência: ADR 0003 (`adr/0003-sequencia-didatica.md`).

## Parte I — Fundamentos (estruturar antes de calcular)

| Cap. | Título | O que o leitor passa a saber fazer | Etapa decisor-zero | Estado |
|---|---|---|---|---|
| 00 | [Introdução — por que sua intuição não escala](capitulos/00-introducao.md) | Reconhecer quando um problema é multicritério e por que "pesar de cabeça" falha | `00-esqueleto` — API FastAPI + página que servirão de chassi | ✅ |
| 01 | [O problema multicritério](capitulos/01-problema-multicriterio.md) | Modelar alternativas, critérios e matriz de decisão; classificar o problema (escolha/ordenação/classificação) | `01-matriz` — a matriz de decisão vira código e API | ✅ |
| 02 | Estruturação — de valores a critérios | Derivar critérios mensuráveis de objetivos (value-focused thinking); eliminar dominadas (Pareto) | `02-dominancia` | ⬜ |
| 03 | Normalização e pesos | Comparar grandezas incomensuráveis; extrair pesos (rating direto, ranking/ROC, swing, entropia) | `03-normalizacao-pesos` | ⬜ |

## Parte II — Métodos compensatórios (escola americana)

| Cap. | Título | O que nasce | Etapa | Estado |
|---|---|---|---|---|
| 04 | SAW/WSM e SMART(ER) — o método aditivo | O primeiro ranking completo do caso âncora; premissas da agregação aditiva | `04-saw` | ⬜ |
| 05 | AHP — comparações par a par | Matriz de julgamentos, autovetor, razão de consistência; o debate do rank reversal | `05-ahp` | ⬜ |
| 06 | TOPSIS — distância ao ideal | Solução ideal/anti-ideal, normalização vetorial | `06-topsis` | ⬜ |
| 07 | MAUT/MAVT e Even Swaps | Funções de valor por critério; trade-offs racionais sem pesos mágicos | `07-funcoes-de-valor` | ⬜ |

## Parte III — Métodos de sobreclassificação (escola europeia)

| Cap. | Título | O que nasce | Etapa | Estado |
|---|---|---|---|---|
| 08 | PROMETHEE I/II | Funções de preferência, fluxos de sobreclassificação | `08-promethee` | ⬜ |
| 09 | ELECTRE — concordância, discordância e veto | Quando NÃO compensar: o outranking de Roy | `09-electre` | ⬜ |

## Parte IV — Robustez, grupo e produto

| Cap. | Título | O que nasce | Etapa | Estado |
|---|---|---|---|---|
| 10 | VIKOR e BWM | Solução de compromisso; pesos com menos comparações | `10-vikor-bwm` | ⬜ |
| 11 | Sensibilidade, robustez e rank reversal | Análise de sensibilidade de pesos; por que métodos discordam entre si | `11-sensibilidade` | ⬜ |
| 12 | Decisão em grupo | Agregação de julgamentos e de rankings; votação | `12-grupo` | ⬜ |
| 13 | Do protótipo ao produto | Persistência (Neon/Postgres), contas e deploy — o `decisor-zero` vira o **Decisor** (`app/`) | `13-persistencia` | ⬜ |

## Aparato

- [Bibliografia](bibliografia.md) — fontes com status de verificação (Princípio I)
- [Histórico](HISTORICO.md) — edições, datação e registro de expiração
- [Guia editorial](GUIA-EDITORIAL.md) — esqueleto v3, caso âncora, regras de escrita

## O caso âncora (usado do cap. 00 ao 13)

Escolher um apartamento entre quatro candidatos:

| Alternativa | Preço (R$) ↓ | Área (m²) ↑ | Deslocamento (min) ↓ | Bairro (1–5) ↑ |
|---|---|---|---|---|
| A1 — Centro | 450.000 | 62 | 15 | 4 |
| A2 — Jardim | 380.000 | 70 | 35 | 3 |
| A3 — Parque | 520.000 | 85 | 25 | 5 |
| A4 — Estação | 340.000 | 55 | 20 | 2 |

(↓ = quanto menor, melhor; ↑ = quanto maior, melhor. Nenhuma alternativa domina outra —
por isso o problema é interessante. Os números vivem como fixtures de teste nas etapas.)
