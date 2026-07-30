# Constituição — Decisor (livro vivo + aplicação de decisão multicritério)

> A lei do projeto. Em conflito entre um pedido pontual e esta constituição, a constituição
> prevalece — ou o conflito é explicitado ao usuário antes de agir.
>
> **Versão 1.0.0** · Ratificada em 2026-07-30 · Linhagem: constituição do
> [Engenharia de Harness](https://github.com/ghdaru/harness_engineering) (v1.2.0) +
> princípios do [Maestro](https://github.com/ghdaru/maestro) (v1.0.0).

O projeto tem três corpos inseparáveis:

1. **O livro** (`livro/`) — ensina decisão multicritério (MCDA) do zero: o leitor aprende lendo.
2. **A construção prática** (`decisor-zero/`) — uma etapa executável por capítulo: o leitor aprende construindo.
3. **A aplicação** (`app/`) — o produto (backend FastAPI + banco Neon/Postgres + frontend web): o leitor aprende usando.

## Princípios

### I. Evidência acima de retórica (NÃO-NEGOCIÁVEL)

Toda afirmação metodológica sobre um método MCDA exige fonte primária com status
validado (✓) em `livro/bibliografia.md`. Toda fórmula apresentada no livro exige um
**exemplo numérico resolvido** cujo resultado é reproduzido por um teste automatizado no
`decisor-zero` — o worked example do capítulo é fixture de teste. Toda fonte de indústria
ou software exige URL verificável. Sem evidência, não entra no corpo do livro.

### II. Nenhum método sem implementação; nenhuma implementação sem fonte

A fonte-base do livro é a **literatura seminal de MCDA lida na origem** (Keeney & Raiffa,
Saaty, Roy, Brans, Hwang & Yoon…), e a prova de compreensão é o **código executável**.
Um método só ganha capítulo quando sua implementação no `decisor-zero` passa nos testes
que reproduzem exemplos da literatura; um algoritmo só entra no código citando no
docstring a fonte da formulação. Surveys e material didático de terceiros contextualizam,
mas não substituem a fonte seminal.

### III. Método pedagógico combinado

Todo capítulo e toda etapa seguem **Backward Design** (objetivos → evidências → conteúdo),
**4C/ID** (etapas do `decisor-zero` = learning tasks; capítulos = supportive information;
docstrings = just-in-time; exercícios = part-task practice), **Diátaxis** (tutorial,
how-to, referência e explicação nunca misturados na mesma seção) e **Carga Cognitiva**
(worked example antes de exercício; uma ideia nova por vez). O **esqueleto v3 de
capítulo** (ver `livro/GUIA-EDITORIAL.md`) é obrigatório. Um único **caso âncora**
(a escolha de um apartamento) atravessa o livro inteiro — todo método novo é aplicado
primeiro ao caso âncora, para que o leitor compare métodos sobre o mesmo problema.

### IV. Livro vivo (datação e expiração)

Todo capítulo declara **data de captura** no cabeçalho
(`> **Estado da arte capturado em AAAA-MM** · última revisão AAAA-MM-DD`). Toda edição
atualiza `livro/HISTORICO.md` — changelog, tabela de snapshot por capítulo e **registro
do modelo de IA usado** (saídas de LLM são não-determinísticas; o registro é parte da
rastreabilidade). Reavaliar = nova rodada, nunca sobrescrever silenciosamente.

### V. Segurança e credenciais

Nenhum segredo (connection string do Neon, chave de API, token) entra em arquivo, commit
ou texto publicado. Credenciais vivem só em variáveis de ambiente / `.env` gitignored;
todo diretório executável tem `.env.example` sem valores reais. Chave exposta é chave
comprometida: alertar e orientar revogação. O código didático demonstra a prática correta.

### VI. Neutralidade metodológica e acessibilidade

**Nenhum método MCDA é "o melhor"**: cada capítulo declara premissas, condições de uso e
limitações conhecidas do método (compensação, independência preferencial, rank reversal,
escolha de normalização) com fonte. A trilha prática roda a **custo zero**: tudo executa
localmente sem banco (fallback SQLite/memória) e o produto usa o free tier do Neon.
Prosa em português; termos técnicos consagrados (trade-off, outranking, rank reversal)
sem tradução forçada, expandidos na primeira ocorrência.

### VII. Spec-driven, raias e gates (NÃO-NEGOCIÁVEL — herdado do Maestro)

Toda melhoria passa pelo ciclo `spec → plan (Constitution Check) → tasks → implement →
DoD verificável → revisão em contexto fresco → gate humano → merge`, cada uma na sua
branch/rodada, registrada em `specs/NNN-nome/`. **Raias**: *leve* (typo, link, bug com
teste que o reproduz — o PR é o artefato), *plena* (capítulo, etapa, feature — spec
completa), *infra* (banco, deploy, migração — sempre plena + gates de reversibilidade:
backup, dry-run, rollback documentado). Regras permanentes: na dúvida, é plena; quem
executa não verifica (revisão independente em contexto fresco); **"prove, não declare"**
(todo "pronto" vem com o output do teste/build que o comprova); toda decisão relevante
vira ADR em `adr/` (imutável — superada, nunca editada no mérito). Exceções que vão
direto ao main: emendas a esta constituição e correções triviais.

## Restrições da construção (decisor-zero e app)

1. **Uma etapa por capítulo, autocontida** — cada `decisor-zero/etapas/NN-tema/` roda
   sozinha (`uvicorn app:app --reload`); o diff entre etapas consecutivas é a lição do
   capítulo. O frontend das etapas é HTML+JS sem build (carga cognitiva mínima).
2. **Motor de cálculo puro** — os algoritmos MCDA são funções puras sem I/O, testáveis
   sem servidor e sem banco; FastAPI e persistência são camadas por fora (hexagonal por
   refatoração, como no harness-zero).
3. **O produto congela a stack**: backend Python + FastAPI; banco Postgres (Neon) com
   fallback SQLite local; frontend conforme ADR 0002. Nada de framework novo sem ADR.
4. **Anti-apodrecimento**: o acesso a banco fica atrás de uma camada de repositório;
   trocar Neon por outro Postgres (ou SQLite) não toca o motor nem as rotas.

## Governança

Emendas a esta constituição: versão semântica (MAJOR remoção/redefinição de princípio,
MINOR princípio novo, PATCH clarificação), registro em `livro/HISTORICO.md` e ADR quando
a decisão for material. Todo agente e humano DEVE ler este arquivo antes de qualquer
trabalho no projeto.
