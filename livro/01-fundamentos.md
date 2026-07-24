# 01 — Fundamentos

## 1. Definição

A definição de trabalho deste livro vem da lista curada [awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering):

> **Harness engineering** é a disciplina de projetar o scaffolding — entrega de contexto, interfaces de ferramentas, artefatos de planejamento, loops de verificação, sistemas de memória e sandboxes — que envolve um agente de IA e determina se ele tem sucesso ou falha em tarefas reais.

Com o princípio orientador:

> O foco é o *harness*, não o modelo. Cada componente existe porque o modelo não consegue fazê-lo sozinho — e os melhores harnesses são projetados sabendo que esses componentes se tornarão desnecessários conforme os modelos melhoram.

## 2. A definição constitutiva: os quatro elementos

O paper de referência citado na literatura ("What makes a harness a harness") define o harness como uma **camada de runtime** com quatro elementos necessários e suficientes:

1. **Agent loop** — o ciclo que alterna entre invocar o modelo e executar o que ele decidiu, até um critério de parada.
2. **Tool interface** — o contrato pelo qual o modelo age sobre o mundo (ler arquivos, rodar comandos, chamar APIs).
3. **Context management** — a montagem, priorização e compressão do que o modelo enxerga a cada chamada.
4. **Control mechanisms** — permissões, aprovações, sandboxes e limites que restringem o que o agente pode fazer.

Um sistema sem qualquer um dos quatro não é um harness completo: um chatbot com tools mas sem loop é um "function caller"; um loop sem controle é um risco operacional; tools sem gestão de contexto colapsam em tarefas longas.

## 3. Taxonomia por problema

Uma convenção importante herdada do referencial: organizar a disciplina **pelo problema resolvido, não por fabricante ou modelo**. É a taxonomia que estrutura os capítulos deste livro:

| Problema | Capítulo |
|---|---|
| Como o ciclo de decisão-ação funciona e quando para | 02 — Loop do Agente |
| O que o modelo enxerga e como isso é montado | 03 — Entrega de Contexto |
| O que fazer quando a janela de contexto acaba | 04 — Compactação |
| Como o modelo age sobre o mundo | 05 — Design de Ferramentas |
| Como integrar capacidades externas de forma padronizada | 06 — MCP |
| O que o agente pode fazer, e onde | 07 — Permissões e Sandboxing |
| O que persiste entre turnos e entre sessões | 08 — Memória e Estado |
| Como trabalho grande vira passos verificáveis | 09 — Planejamento |
| Como distribuir trabalho entre múltiplos agentes | 10 — Subagentes e Orquestração |
| Como saber se o agente (e o harness) funcionam | 11 — Verificação e Evals |
| Como terceiros estendem o harness | 12 — Extensibilidade |
| Por onde humanos e sistemas usam o agente | 13 — Interfaces |

## 4. Artigos e fontes canônicas

O campo tem um cânone curto e recente. As fontes que mais aparecem nas referências da disciplina:

- **"Building Effective Agents"** (Anthropic) — o texto que popularizou a distinção entre *workflows* (orquestração determinística) e *agentes* (o modelo dirige o próprio processo), e o princípio de começar simples.
- **"Harness Engineering"** (OpenAI) — nomeia a disciplina e descreve a prática interna de construir scaffolding em volta de modelos para tarefas longas.
- **Martin Fowler sobre agentes** — a leitura de engenharia de software clássica: padrões, trade-offs, e ceticismo saudável sobre autonomia sem verificação.
- **"Anatomy of an Agent Harness"** (LangChain) — decomposição estrutural dos componentes de um harness moderno.
- **"What makes a harness a harness"** (arXiv) — a definição constitutiva dos quatro elementos (§2).
- **Model Context Protocol** (spec) — o padrão aberto que virou a lingua franca de integração de ferramentas (capítulo 06).

(A lista completa, com ~426 recursos anotados e organizados pela mesma taxonomia, está no referencial awesome-harness-engineering.)

## 5. A cláusula de expiração

A tese mais importante — e menos praticada — da disciplina: **todo componente de harness é uma prótese temporária**. A compactação existe porque janelas de contexto são finitas; o plan mode existe porque modelos agem precipitadamente; o policy engine existe porque modelos não são confiáveis com comandos destrutivos. Cada uma dessas premissas tem prazo de validade.

O corolário prático (materializado no `HARNESS_CHECKLIST.md` do referencial): todo componente deveria documentar **qual melhoria de capacidade do modelo o tornaria desnecessário**. Harnesses que não fazem isso acumulam scaffolding morto — complexidade que sobrevive à limitação que a justificava. Voltamos a isso no capítulo 14.

## 6. Artefatos operacionais

A disciplina produziu um conjunto pequeno de artefatos-padrão que aparecem, com variações, em quase todos os harnesses estudados:

- **Arquivo de instruções de projeto** (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): regras, convenções e limites que o agente lê antes de qualquer tarefa. Fronteiras claras superam restrições vagas.
- **Artefato de plano** (`PLAN.md`): criado no início da tarefa e atualizado durante a execução, com milestones verificáveis e fronteiras de escopo.
- **Log de implementação** (`IMPLEMENT.md`): registro append-only de decisões e desvios do plano.
- **Checklist de harness** (`HARNESS_CHECKLIST.md`): revisão pré-produção cobrindo instruções, tools, contexto, planejamento, permissões e verificação — com a tabela de expiração do §5.

Esses quatro artefatos são o embrião do nosso instrumento de avaliação (ver `benchmark/template/HARNESS_EVAL.md`).
