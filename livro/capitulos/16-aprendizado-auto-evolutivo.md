# 16. Aprendizado e Auto-melhoria: o harness que se escreve

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4, ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: proprio
>
> Dimensão suplementar (13) do template do benchmark, promovida por força de evidência: o **Hermes Agent** (Nous Research) implementa o ciclo completo. Tratamento por repositório no Apêndice A; avaliação completa em `../../benchmark/avaliacoes/hermes-agent.md`.

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que o aprendizado auto-evolutivo quebra o pressuposto do *scaffolding* estático, e como ele inverte a cláusula de expiração do livro;
2. **Descrever** as etapas do ciclo fechado de captura de skills (gatilho, curadoria, isolamento, formato portável, reencontro indexado, manutenção contra a entropia);
3. **Comparar** os dois designs concorrentes de aplicação do aprendizado (autônoma × promoção humana) e **localizar** um harness real na escada de maturidade da dimensão;
4. **Avaliar** os riscos da dimensão (superstição, entropia, contaminação, prompt injection como aprendizado permanente) e as engenharias que os previnem.

## A terceira semana corrigindo o mesmo erro

Segunda-feira: *"não use `print`, use o logger do projeto"*. O agente corrige, agradece, segue.

Semana seguinte, tarefa nova, mesmo `print`. Você corrige de novo.

Terceira semana. Mesmo `print`.

O agente não está sendo teimoso. Ele **não tem onde guardar** o que aprendeu: cada sessão começa do zero, e a correção da semana passada morreu junto com a janela de contexto que a continha.

Repare em quem está fazendo o trabalho de memória de longo prazo aqui. É você. Três semanas seguidas, de graça, num loop que nenhum sistema mede e ninguém contabiliza, e que vai continuar até alguém escrever a regra num arquivo.

Este capítulo é sobre fechar esse laço: o agente escrever a própria regra. E é também sobre por que fechá-lo **sem freio** é a pior ideia do livro.

## O problema

As doze dimensões dos capítulos 02–13 descrevem *scaffolding* (andaime) *estático*: alguém (o autor do harness, o usuário, um plugin) escreve as instruções, tools e políticas, e o agente as consome. Este capítulo documenta a dimensão emergente que quebra esse pressuposto: o agente que **escreve o próprio scaffolding**, capturando procedimentos aprendidos como skills reutilizáveis.

A dimensão foi promovida a suplementar do template do benchmark (dimensão 13) por força de uma evidência: o **Hermes Agent** (Nous Research) implementa o ciclo completo. A leitura do código confirma cada etapa (Apêndice A).

## Na prática: o que o seu harness já sabe fazer

Este capítulo não pede código novo. O que ele pede é olhar para as peças que você já construiu e ver que **o laço de aprendizado é a composição delas**.

Você já tem as quatro partes. O **arquivo de contexto** do cap. 03, que é lido a cada turno e é onde uma regra aprendida caberia. A **memória durável** do cap. 08, que sobrevive à sessão. A **política** do cap. 07, que decide o que pode ser escrito. E os **hooks** do cap. 12, que dão o gatilho no momento certo.

O laço fecha assim: um hook percebe que uma correção do usuário se repetiu, escreve a lição como arquivo de skill. O montador de contexto passa a incluí-la no turno seguinte. Nenhuma peça é nova.

**E aqui está a razão pela qual o freio não é opcional.** Uma lição salva entra no contexto de *todos* os turnos futuros. Se o agente puder aprovar as próprias lições, um texto plantado num repositório clonado (o mesmo vetor do cap. 07) deixa de ser um problema de uma sessão e vira **prompt injection persistida**: ela volta amanhã, e depois de amanhã, e continua voltando depois que a sessão original foi esquecida.

Por isso a skill nasce **pendente**, e a promoção é ato humano:

```text
.skills/
  pendentes/
    2026-08-12-usar-logger.md      ← escrita pelo agente, NÃO entra no contexto
  ativas/
    conventions.md                  ← promovida por humano, entra em todo turno
```

Duas pastas. É o freio inteiro, e ele é a diferença entre um agente que aprende e um agente que pode ser ensinado por qualquer um.

## O estado da arte

### O ciclo fechado: as seis etapas

O mecanismo de referência, verificado no código do Hermes (evidência detalhada no Apêndice A), fecha o ciclo em seis etapas:

1. **Gatilho autônomo**, a revisão de aprendizado dispara sozinha, em background, sem o usuário pedir (com gatilho manual como complemento).
2. **Curadoria por um fork isolado** (um clone do agente, com um prompt curatorial que define o que capturar e) o mais importante — **anti-padrões do que NÃO aprender**. Sem essa lista, o sistema degeneraria em superstição acumulada.
3. **Isolamento do meta-trabalho**, o fork curador tem tools restritas e persistência desligada, para não contaminar a sessão real.
4. **Escrita em formato portável**, a skill vira um `SKILL.md` sob standards rígidos, com a restrição de contexto moldando o formato do conhecimento.
5. **Reencontro barato**, índice compacto sempre no system prompt; conteúdo integral só entra no contexto sob demanda. Aprendizado indexado, não despejado.
6. **Manutenção contra a entropia**, um curador periódico consolida, arquiva por inatividade e protege o que está fixado. Memória que só cresce vira ruído; o curador é o coletor de lixo do conhecimento.

### A escada de maturidade na coorte avaliada

| Harness | Nota 13 | O que tem |
|---|---|---|
| **Hermes** | **3** | O ciclo fechado completo (Apêndice A), com aplicação autônoma |
| **gemini-cli** | **3** (retro) | Auto Memory: agente extrator com gates anti-ruído ("Default to NO SKILL", 5 perguntas de bloqueio) produzindo SKILL.md + patches de memória, mas com **promoção humana via inbox** (`/memory inbox`); dedupe, sandbox de escrita, evals dedicados |
| IronClaw | 2 | Extração automática de skills (`learning.rs`) com métricas de uso/confiança e versionamento |
| OpenClaw | 1 | Dreaming (consolidação autônoma de memória); Skill Workshop com fila de propostas |
| OpenHarness | 1 (retro) | Auto-extração de fatos por turno, com staleness por uso (60 dias), fatos, não procedimentos |
| Codex CLI | 1 | Memórias automáticas com pruning (fatos, não procedimentos) |
| Goose | 1 | chatrecall (recall semântico de conversas passadas) |
| opencode, demais | 0 (retro) | Skills são consumo/distribuição; nada é escrito pela experiência |

A escada é nítida: **memória de fatos** (nível 1) → **extração de procedimentos** (nível 2) → **ciclo curado com anti-padrões e manutenção** (nível 3). O que separa o nível 3 não é capturar mais, é a engenharia de *não* capturar errado e de podar o que envelheceu.

### Os dois designs concorrentes do nível 3

O nível 3 já tem **dois designs concorrentes**, com a divergência exatamente onde importa: *quem aplica o que foi aprendido*. O Hermes aplica autonomamente (com o curador limpando depois); o gemini-cli exige promoção humana (inbox, nada entra no contexto sem `/memory inbox`). É o trade-off clássico autonomia × controle do capítulo 07, reaparecendo na dimensão mais nova: o Hermes aposta que anti-padrões bastam para prevenir aprendizado ruim; o gemini-cli aposta que não. As próximas rodadas dirão qual escala melhor.

### Por que isso muda a tese do livro

A cláusula de expiração (cap. 01, 14) diz: todo componente de harness é uma prótese para uma limitação atual do modelo, e expira quando o modelo melhora. O aprendizado auto-evolutivo **inverte a cláusula**: em vez de esperar o modelo dispensar o scaffolding, o par modelo+harness *escreve scaffolding novo para si mesmo*. Cada skill aprendida é um pedaço de harness gerado em runtime, específico ao usuário e ao ambiente, algo que nenhum autor de harness poderia ter escrito de fábrica.

Isso cria uma terceira via na taxonomia:

1. **Scaffolding de fábrica**, escrito pelo autor do harness; expira com a evolução dos modelos.
2. **Scaffolding de fronteira**, sandbox, permissões, interfaces; não expira (é sobre o mundo).
3. **Scaffolding auto-gerado**, skills escritas pelo agente; *cresce* com o uso, e sua qualidade depende da engenharia de curadoria, não da capacidade bruta do modelo.

### Os riscos: o espelho das promessas

Cada promessa tem o risco que lhe corresponde: sem anti-padrões, superstição; sem curadoria, entropia; sem isolamento do meta-trabalho, contaminação; e (apontado pela avaliação do IronClaw (prompt-write safety; cf. cap. 07)) sem fronteira de escrita protegida, **prompt injection vira aprendizado permanente**: um atacante que convence o agente a "aprender" uma skill maliciosa persiste na memória procedural. A dimensão 13 madura exigirá a dimensão 6 madura.

### Leitura executiva

A dimensão é a mais nova do template e a menos convergida: dois harnesses no nível 3 com designs opostos sobre quem aplica o aprendizado. O resto da coorte entre memória de fatos e nada. O que já é consenso de engenharia entre os que chegaram lá: a peça central não é o mecanismo de captura. Sim os **anti-padrões do que não aprender** e a **manutenção** (consolidar, arquivar, nunca deletar). **O que roubar** hoje: lista de anti-padrões no prompt curatorial. Isolamento do meta-trabalho em fork sem persistência; índice compacto com conteúdo sob demanda; curador periódico como coletor de lixo; fronteira de escrita protegida contra prompt injection.

*Reavaliação retroativa da coorte de código pendente; a dimensão sai de "suplementar" quando ≥3 harnesses atingirem nível 2+.*

> **Consulte também**: a coleção viva [Awesome Harness Engineering. Skills & MCP](https://github.com/GHDaru/awesome-harness-engineering#skills--mcp) reúne mais recursos consultáveis desta dimensão, curados por problema.

## Mão na massa, harness-zero, etapa 12

A etapa 12 (`harness-zero/etapas/12-skills/`) fecha a trilha com o mecanismo deste capítulo: `salvar_skill` grava a lição em `pendentes/`, e nada do que está lá entra no contexto. A promoção é um ato humano, e só depois dela o índice da skill aparece no system prompt.

O corpo da skill **não** vai junto: o índice anuncia nome e descrição, e o conteúdo é carregado sob demanda pela tool de leitura. É a divulgação progressiva do cap. 03 aplicada ao que o agente escreveu.

Exercício de completude: o mecanismo de promoção vem pronto. Você acrescenta o **portão automático** do cap. 11, um eval que roda antes de a skill poder ser promovida, medindo se ela reduz a reincidência que a motivou.

## Verificação

1. Por que a lista de **anti-padrões** ("o que NÃO aprender") é descrita como a peça central da engenharia curatorial, e não o mecanismo de captura em si? O que acontece com um sistema que captura sem ela?
2. Localize na escada de maturidade um harness que extrai fatos automaticamente com staleness por uso, mas não captura procedimentos. Que nota ele recebe, e o que faltaria para subir um nível?
3. Hermes e gemini-cli estão ambos no nível 3, mas divergem em *quem aplica* o que foi aprendido. Reconstrua o trade-off autonomia × controle nesse contexto: qual é a aposta de cada design?
4. Explique a frase "a dimensão 13 madura exigirá a dimensão 6 madura": por que prompt injection é qualitativamente mais grave num harness que aprende do que num harness estático?

---

## Apêndice A — Hermes Agent

> Evidência por repositório, com paths — material de complementação (versão online), expandido a cada rodada do benchmark. Avaliação completa: `../../benchmark/avaliacoes/hermes-agent.md`.

### O ciclo fechado do Hermes (evidência: `agent/background_review.py` e afins)

O mecanismo, verificado no código do fork avaliado:

**1. Gatilho autônomo.** A cada ~10 iterações de tool-calling (`skill_nudge_interval`, em `agent/turn_finalizer.py`), o harness dispara uma revisão em background — sem o usuário pedir. Há também o gatilho manual `/learn`.

**2. Curadoria por um fork isolado.** Um clone do agente roda em thread separada com o snapshot da conversa e um prompt curatorial (`_SKILL_REVIEW_PROMPT`) que é a peça central da engenharia. Ele instrui o curador a ser ativo ("um passe que não faz nada é aprendizado perdido"), define ordem de preferência (atualizar skill existente > criar nova; skills novas só class-level, nunca "fix-bug-1234") e — o mais importante — lista **anti-padrões do que NÃO aprender**: falhas dependentes de ambiente, claims negativos sobre tools ("o browser não funciona"), erros transitórios, narrativas one-off. Sem essa lista, o sistema degeneraria em superstição acumulada.

**3. Isolamento do meta-trabalho.** O fork tem whitelist de tools restrita (`memory` + `skills`), memória e persistência desligadas — para a curadoria não contaminar a sessão real — e herda o prefixo de prompt cacheado do pai (redução de ~26% no custo da revisão).

**4. Escrita em formato portável.** A skill vira um `SKILL.md` compatível com **agentskills.io** em `~/.hermes/skills/<categoria>/<nome>/` (com `references/`, `templates/`, `scripts/`), sob standards rígidos — descrição ≤60 caracteres *porque o índice no system prompt trunca em 60*: a restrição de contexto moldando o formato do conhecimento.

**5. Reencontro barato.** O índice compacto (nome + descrição) está sempre no system prompt; o conteúdo integral só entra no contexto quando o agente chama `skill_view` — aprendizado indexado, não despejado.

**6. Manutenção contra a entropia.** Um **curador** periódico (`agent/curator.py`) roda quando o agente está ocioso: consolida skills em umbrellas, arquiva por inatividade (90 dias — arquivar, nunca deletar), protege skills fixadas. Memória que só cresce vira ruído; o curador é o coletor de lixo do conhecimento.

---

## Respostas da verificação

**1.** Porque capturar é fácil e **descartar é a decisão difícil**. Um mecanismo de captura sem lista de anti-padrões aprende tudo o que parece útil no momento: o caminho absoluto da máquina de quem estava usando, o segredo que apareceu numa saída de tool, a solução de um caso particular escrita como se fosse regra geral, e a preferência de estilo de uma pessoa apresentada como convenção do projeto. O que acontece com esse sistema é previsível e caro: o diretório de skills só cresce, cada turno carrega mais tokens de regras que ninguém revisou, e a taxa de acerto **cai** — porque instrução ruim é pior que instrução ausente. A curadoria é a engenharia; o gatilho é o detalhe fácil.

**2.** Ele fica no **nível 2** da escada: extrai fato automaticamente e já tem gestão de ciclo de vida por uso, que é o que separa memória de um depósito. O que falta para subir é a captura de **procedimento** — não "o projeto usa o logger X", mas "quando o teste de integração falha por timeout, rode com `-x` e olhe o container antes". Fato é semântico e cabe numa linha; procedimento é episódico e precisa de forma própria, que é o formato de skill portável. A diferença prática aparece na hora de aplicar: fato entra no contexto, procedimento precisa ser **encontrado** quando a situação se repete.

**3.** A divergência é sobre **quem aplica o aprendizado**. Um design aposta que o agente aplica sozinho: a lição entra no contexto e passa a valer sem intervenção, o que dá ganho imediato e transfere o risco para a curadoria — se a lição for ruim, ela já está agindo. O outro aposta que o humano promove: a lição fica visível e só passa a valer depois de aprovada, o que custa latência e uma decisão a mais, e em troca mantém a lista de regras auditável e pequena.

A aposta de cada um é sobre **onde o erro é mais barato**. Autonomia é melhor quando o custo de uma regra ruim é baixo e reversível; controle é melhor quando a regra ruim persiste, se acumula e entra em todo turno futuro — que é exatamente a condição deste capítulo. Não há resposta universal, mas há uma assimetria: o design autônomo pode ser convertido em controlado ligando um portão, e o controlado só vira autônomo desligando-o.

**4.** Porque num harness estático a injection tem **escopo de sessão** e num harness que aprende ela tem **escopo de sistema**. No estático, o texto malicioso lido de um arquivo age enquanto aquele contexto existir, e a próxima sessão começa limpa. No que aprende, o mesmo texto pode ser **promovido a skill**, e a partir daí volta em todo turno de toda sessão, inclusive em tarefas sem nenhuma relação com o repositório de onde veio, muito depois de qualquer um lembrar de onde veio. A duração deixa de ser a da janela e passa a ser a do arquivo.

Some-se que o vetor é mais barato para o atacante: ele não precisa acertar o momento, basta plantar o texto e esperar que o mecanismo de captura o considere útil. Daí a frase: um harness que aprende **precisa** da maturidade de permissões e contenção, porque a memória virou superfície de ataque durável, e a defesa que sobra é a mesma do cap. 07 — separar escrever de ativar, e nunca confiar na filtragem do próprio modelo.
