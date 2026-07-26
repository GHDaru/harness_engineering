# Plano — Reescrita editorial v3

## Abordagem por capítulo (o mesmo pipeline, repetido)

1. **Reler a evidência de código** — o material por-repositório já existe nas avaliações do benchmark (`benchmark/avaliacoes/*.md`) e no capítulo pré-v3. É a fonte-base; nada é escrito sem path.
2. **Pesquisa dupla** (Princípio III + regra v3): agentes de pesquisa em paralelo levantam (a) fontes da indústria — specs de vendor, blogs de engenharia — e (b) material científico. Cada fonte é traduzida em decisão; URLs verificadas; lacunas registradas.
3. **Escrever no esqueleto v3** — objetivos → problema → fundamentos → indústria → estado da arte → mão na massa → síntese/roubar → verificação → Apêndice A.
4. **Sincronizar bibliografia** — mover as fontes validadas para a seção do capítulo em `bibliografia.md`.
5. **Build + verificação** — `node publicar/build.mjs`; portão de link-check verde; um capítulo por commit.

## Ordem e racional

- **06 MCP primeiro**: é o único buraco na sequência contígua 02–07; e sua bibliografia está explicitamente registrada como lacuna, então o ganho de rigor é maior.
- Depois 08→13 na ordem numérica (cada um é uma dimensão do benchmark, com avaliação de código já feita).

## Datação (livro vivo)

Cada capítulo recebe o selo de captura do mês corrente. Ao fim da iniciativa, registrar uma **edição** no `HISTORICO.md` (ex.: "0.5 — capítulos de funcionalidade unificados no esqueleto v3") e revisar o registro de expiração se alguma previsão mudou de estado.

## Risco/mitigação

- **Proxy bloqueia arxiv/anthropic (403).** Mitigação: pesquisa por busca cruzada; marcar não-verificado; nunca inventar URL/ID (Princípio I).
- **Escopo grande (7 capítulos).** Mitigação: um commit por capítulo; a branch pode ser mesclada incrementalmente ou ao final; cada capítulo é entregável isolado.
