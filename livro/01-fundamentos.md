# 01 — Fundamentos

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](GUIA-EDITORIAL.md).
> andaime: completo

## Três coisas chamadas "agente"

Peça a três engenheiros a definição de "agente de IA" e você recebe três respostas incompatíveis.

O primeiro diz que é um modelo com acesso a ferramentas. O segundo diz que é um sistema que persegue um objetivo sem supervisão. O terceiro mostra o produto que usa no dia a dia e diz "isto".

As três respostas descrevem coisas diferentes, e é por isso que discussões sobre agentes andam em círculos: os interlocutores não estão falando do mesmo objeto. Pior, a confusão tem consequência prática. Se você não sabe dizer onde termina o modelo e começa o resto, não sabe a quem atribuir uma falha, e passa semanas trocando de modelo para resolver um problema de contexto.

Este capítulo existe para tornar a conversa possível. Ele responde três perguntas: **o que é** um harness, **de onde ele veio** e o que havia antes, e **com que rigor** este livro o estuda.

## 1. O que é um harness (definição)

A definição de trabalho vem da lista curada [awesome-harness-engineering](https://github.com/GHDaru/awesome-harness-engineering):

> **Engenharia de harness** é a disciplina de projetar o *scaffolding* — andaime ou estrutura de suporte — que envolve um agente de IA (entrega de contexto, interfaces de ferramentas, artefatos de planejamento, loops de verificação, sistemas de memória e sandboxes) e determina se ele tem sucesso ou falha em tarefas reais.

Com o princípio orientador:

> O foco é o *harness*, não o modelo. Cada componente existe porque o modelo não consegue fazê-lo sozinho, e os melhores harnesses são projetados sabendo que esses componentes se tornarão desnecessários conforme os modelos melhoram.

Note o termo central: **scaffolding**, andaime. É a metáfora do livro, a estrutura provisória erguida em volta de algo em construção, que sustenta o trabalho e depois é removida.

Guarde a palavra. Ela reaparece no subtítulo, no título de cada parte e na §8, quando o andaime ganhar prazo de validade.

> **Para quem está chegando agora, uma imagem que sustenta o livro inteiro.** Pense no modelo como um profissional brilhante no primeiro dia numa empresa que ele não conhece: capaz, mas sem mesa, sem acesso aos sistemas, sem saber as regras da casa, e com memória que zera a cada conversa.
>
> O harness é tudo que a empresa monta em volta dele. O dossiê do projeto que ele lê ao chegar é o contexto (cap. 03). As ferramentas na bancada são as tools (cap. 05). O crachá que define onde ele pode entrar são as permissões (cap. 07). O caderno que sobrevive ao fim do expediente é a memória (cap. 08). O supervisor que revisa a entrega antes de ela sair é a verificação (cap. 11). E o expediente em si, o ritmo de trabalhar, conferir e continuar, é o loop (cap. 02).
>
> Quando os capítulos ficarem técnicos, volte a esta imagem: cada dimensão do livro é uma peça desse escritório.

## 2. O que havia antes, e por que não eram agentes

"Software que age por você" é uma ideia antiga. As gerações anteriores resolviam o problema **sem um modelo de linguagem no centro do laço de decisão**, e é isso que as separa de um agente.

- **Sistemas especialistas** (anos 1980): regras `if-then` escritas à mão. Automatizavam decisões, mas não interpretavam objetivos em linguagem natural nem se recuperavam de exceções não previstas.
- **RPA, Robotic Process Automation** (UiPath, Automation Anywhere): robôs que repetem cliques e digitações por *script* fixo. Frágeis a qualquer mudança de tela, sem objetivo e sem recuperação.
- **Chatbots** de intenção, de ELIZA às árvores de diálogo: produziam texto, mas **não executavam ações** no mundo.
- **Assistentes de código como autocomplete**: o **GitHub Copilot** (technical preview em jun/2021), movido pelo modelo **OpenAI Codex**, descendente do GPT-3 ajustado em código, sugeria a próxima linha *dentro do editor*, sem plano, sem ferramentas e sem laço de verificação.

Nenhum deles tinha as **quatro peças** que hoje definem um harness (§4). Faltava-lhes autonomia orientada a objetivos e a capacidade de agir sobre o ambiente **e corrigir o próprio rumo**.

## 3. Como chegamos aqui: a linhagem técnica

A passagem de "modelo que responde" para "agente que age" foi construída em camadas, cada uma removendo um obstáculo.

1. **Raciocínio explícito.** O *Chain-of-Thought* (Wei et al., 2022) mostrou que pedir ao modelo para "pensar passo a passo" melhora tarefas de raciocínio.
2. **O loop.** O marco decisivo foi **ReAct**, *Synergizing Reasoning and Acting in Language Models* (Yao et al., [arXiv:2210.03629](https://arxiv.org/abs/2210.03629), out/2022; ICLR 2023), que intercalou **Pensamento → Ação → Observação**. O modelo raciocina, chama uma ferramenta, observa o resultado e continua. Esse ciclo é o esqueleto de praticamente todo harness moderno (capítulo 02).
3. **A chamada de ferramentas.** Faltava um modo confiável de o modelo *invocar* ferramentas, resolvido quando a OpenAI lançou o **function calling** (jun/2023): o modelo emite JSON estruturado para acionar funções (capítulo 05).
4. **A onda autônoma, e a lição dela.** Com raciocínio, ação e ferramentas, veio 2023: **AutoGPT** (Significant Gravitas, mar/2023) e **BabyAGI** (Yohei Nakajima, abr/2023), loops que se decompunham em subtarefas e se executavam sozinhos. Eles "falharam" no sentido prático, entrando em círculos, gastando tokens e perdendo o fio, porque tinham *o loop* mas **não** as outras três peças: gestão de contexto, ferramentas bem projetadas e controle. A lição fundadora da disciplina nasce aí: **o modelo sozinho não basta, o andaime em volta é que decide o sucesso.**
5. **O amadurecimento, os CLIs de código.** As quatro peças foram embutidas em ferramentas de terminal ligadas ao sistema de arquivos e ao Git: **Aider** (Paul Gauthier, abr/2023), **Claude Code** (Anthropic, research preview em fev/2025), **OpenAI Codex CLI** (open source, abr/2025), além de projetos como **Cline**, **OpenHands** e **SWE-agent**.
6. **A padronização.** Com agentes proliferando, vieram os protocolos. O **Model Context Protocol (MCP)**, aberto pela Anthropic (nov/2024), padronizou a conexão a ferramentas e dados (capítulo 06). O **AGENTS.md** consolidou-se como "README para agentes". O **Agent2Agent (A2A (Agent-to-Agent))** (Google, abr/2025; depois doado à Linux Foundation) endereçou a comunicação *entre* agentes (capítulo 17).

**Linha do tempo (marcos):** 1980s sistemas especialistas · 2000s–2010s RPA e chatbots · **jun/2021** Copilot (autocomplete) · **out/2022** ReAct · **mar–abr/2023** GPT-4, AutoGPT, BabyAGI, Aider · **jun/2023** function calling · **nov/2024** MCP · **fev/2025** Claude Code · **abr/2025** Codex CLI e A2A.

> **Nota de rigor.** "Codex" designa três coisas distintas: o *modelo* de 2021 (base do Copilot), a *linha de produto* Codex da OpenAI e o *Codex CLI* open source de 2025. O texto as mantém separadas. Datas e fontes desta seção estão na [Bibliografia](bibliografia.md), e itens ainda a verificar estão marcados lá.

## 4. A definição constitutiva: os quatro elementos

A literatura da disciplina converge numa definição do harness como uma **camada de runtime** com quatro elementos necessários e suficientes:

1. **Loop do agente** — o ciclo que alterna entre invocar o modelo e executar o que ele decidiu, até um critério de parada (cap. 02).
2. **Interface de ferramentas** — o contrato pelo qual o modelo age sobre o mundo: ler arquivos, rodar comandos, chamar APIs (cap. 05).
3. **Gestão de contexto** — a montagem, priorização e compressão do que o modelo enxerga a cada chamada (caps. 03–04).
4. **Mecanismos de controle** — permissões, aprovações, sandboxes e limites que restringem o que o agente pode fazer (cap. 07).

Um sistema sem qualquer um dos quatro **não é um harness completo**. Um chatbot com ferramentas mas sem loop é um "function caller". Um loop sem controle é um incidente esperando acontecer. Ferramentas sem gestão de contexto colapsam em tarefas longas.

Esta é a definição operacional que serve de **teste de inclusão** do estudo (§5 e §6), e a próxima seção mostra como ela decide na prática.

### A definição está convergindo por fora, e de cinco lados que não se coordenaram

Vale enumerar, porque a força do argumento está no número de fontes independentes.

A **Microsoft**, ao anunciar seu Agent Framework, define harness como *"the **scaffolding** that turns a language model into an agent"*.

O survey de **Meng et al.** formaliza `H = (E, T, C, S, L, V)`: loop, ferramentas, contexto, estado, ciclo de vida, avaliação.

O survey do **RUCAIBox** organiza o campo em quatro eixos com a mesma espinha.

O diretório `best-of-Agent-Harnesses` sintetiza *"the model thinks; the harness decides what that thinking is allowed to touch"*, e é o único que põe permissão **dentro** da definição, não como capítulo à parte.

E a mais operacional de todas, porque define pelo que se pode **verificar no sistema de arquivos**: o [Harness Score](https://github.com/paladini/harness-score) mede seis dimensões (contexto, skills, guarda-corpos, sensores, CI, higiene) que caem quase limpo sobre os capítulos deste livro. O [Apêndice — Meça o seu harness](apendice-harness-score.md) aplica a régua a este próprio repositório, com o resultado incômodo que ela produziu.

Cinco grupos independentes chegando aos mesmos elementos é o melhor argumento disponível de que a definição descreve algo real, e não um recorte editorial nosso. As quatro peças acima são a forma que este livro dá a esse consenso.

## Na prática: usando a definição para decidir

Uma definição só vale se decide casos difíceis. Vamos aplicar o teste das quatro peças a três sistemas, um por vez, olhando o que existe no código.

**Caso 1: um script que chama a API do modelo e executa o que ele pedir.**

```python
resposta = modelo.chamar(mensagens, tools=[rodar_shell])
for chamada in resposta.tool_calls:
    subprocess.run(chamada.args["comando"], shell=True)   # sem confirmação
```

- Loop? **Não.** Uma passagem só, sem realimentar o resultado.
- Ferramentas? **Sim**, uma.
- Gestão de contexto? **Não.** As mensagens vão como estão.
- Controle? **Não.** `shell=True` sem confirmação nem sandbox.

Veredito: **um function caller**, não um harness. Falta o laço, que é o que transforma uma resposta em trabalho, e falta o freio.

**Caso 2: o mesmo script, agora com laço e limite.**

```python
for turno in range(MAX_TURNOS):
    resposta = modelo.chamar(recortar(mensagens, limite=100_000), tools=TOOLS)
    if not resposta.tool_calls:
        break
    for chamada in resposta.tool_calls:
        if not politica.permite(chamada):        # controle
            resultado = "recusado pela política"
        else:
            resultado = executar(chamada)
        mensagens.append(resultado)              # realimenta
```

- Loop? **Sim**, com critério de parada e teto.
- Ferramentas? **Sim.**
- Gestão de contexto? **Sim**, ainda que primitiva: `recortar` decide o que cabe.
- Controle? **Sim**, `politica.permite` antes de qualquer efeito.

Veredito: **harness completo**, e propositalmente feio. As quatro peças não exigem sofisticação, exigem existência. É por isso que o teste de inclusão é útil: ele separa categoria de qualidade.

**Caso 3: um framework que expõe loop, estado e ferramentas como primitivas, mas não roda nada por conta própria.**

Aqui as quatro peças estão presentes **como possibilidade**, não como decisão tomada. Quem escolhe a política de parada, o recorte de contexto e a regra de permissão é quem usa a biblioteca.

Veredito: entra no corpus como **framework**, arquétipo próprio (§5), e é avaliado por outra régua. Comparar a nota de permissões de um framework com a de um produto acabado seria comparar potencial com escolha, que é a razão pela qual as notas do benchmark **só comparam dentro da mesma categoria**.

Guarde o método deste exercício, porque o livro o repete quinze vezes: **pergunte pelas quatro peças, procure a linha de código que prova cada resposta, e só então classifique.**

## 5. De onde vêm os harnesses deste estudo

O corpus é **de código aberto** (o Princípio II do livro: a fonte-base é o código) e se divide em cinco arquétipos, os mesmos do capítulo 00:

- **Harnesses de código** (opencode, gemini-cli, OpenHarness, Codex CLI, Goose, Aider, OpenHands, Grok Build, Pi, Kimi Code, Prime Agent): implementações de referência que juntam as quatro peças num executável.
- **Agentes pessoais self-hosted** (OpenClaw, Hermes Agent, IronClaw, ohmo): o harness a serviço de uma pessoa, com identidade, memória e canais próprios.
- **Agentes organizacionais** (QM): o harness a serviço de uma organização, com escopos, permissões por audiência e auditoria como primitivas, e o loop do agente como motor trocável.
- **Harnesses embutidos** (n8n, nó AI Agent): o loop como componente dentro de um produto maior.
- **Frameworks** (LangGraph, CrewAI, OpenAI Agents SDK, Software Agent SDK): expõem loop, estado e ferramentas como primitivas programáveis.

O **teste de inclusão** é a definição da §4: entra quem tem loop, ferramentas, gestão de contexto e controle. Ficam de fora bibliotecas de modelo puro e meros *wrappers* de uma ferramenta.

Um critério merece leitura atenta, porque já foi testado por um caso-limite: exige-se código **aberto e inspecionável** na data de corte, não código **aberto à contribuição**. Um projeto pode publicar a fonte sob licença permissiva e recusar contribuição externa por política escrita, e ainda assim entrar, porque o que o estudo precisa é **ler**, não participar.

A lista avaliada, com o repositório e o commit lido de cada sistema, está no [Comparativo](../benchmark/comparativo.md) e no apêndice do estudo. Recursos consultáveis além do corpus estão na coleção viva [Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering).

## 6. O método do estudo (rigor)

Este livro **lê o código-fonte de harnesses reais**, os compara por dimensões e depois **constrói um harness do zero**. Isso não é "opinião de engenheiro": é um desenho de pesquisa híbrido apoiado em tradições metodológicas consolidadas. Explicitá-las converte o livro de coletânea de impressões em **estudo empírico auditável**, coerente com o Princípio I.

**Em linguagem simples, antes dos nomes técnicos.** O método tem quatro passos:

1. escolher sistemas que representem *tipos* diferentes de harness, não os mais famosos;
2. ler o código de cada um seguindo **o mesmo roteiro de perguntas**, anotando o arquivo exato que prova cada resposta;
3. dar notas por uma régua fixa e publicada, para que qualquer pessoa possa discordar olhando a mesma evidência;
4. construir um harness do zero, para testar se os padrões extraídos se sustentam.

Os parágrafos a seguir dão os nomes formais dessas escolhas e a procedência de cada uma. São a genealogia do rigor, e podem ser lidos em diagonal na primeira passada.

**Duas fases, dois motores.**

- **Fase 1, descritiva e comparativa:** um **estudo de casos múltiplos** (Yin) apoiado em **Mining Software Repositories** (Hassan, 2008), tratando cada repositório como *dado primário*. A unidade de análise é **o código-fonte**, não o material de marketing nem o comportamento observado em uso.
- **Fase 2, construtiva e prescritiva:** o `harness-zero` é um exercício de **Design Science Research** (Hevner et al., 2004; processo DSRM de Peffers et al., 2007), que projeta e avalia um artefato instanciando os princípios extraídos na Fase 1.

**Como as dimensões viram medida.** As dimensões de comparação descem pelo método **Goal–Question–Metric** (Basili, Caldiera & Rombach). Para cada objetivo de harness (contexto, ferramentas, permissões, memória, verificação, loop, orquestração) formulam-se perguntas e, para cada pergunta, **indicadores observáveis no código**: existe mecanismo de compactação? qual a granularidade do modelo de permissões? há camada de verificação pós-ação?

**Seleção por replicação, não por amostragem.** Os casos são escolhidos pela **lógica de replicação** de Yin, *literal* quando se espera o mesmo padrão e *teórica* quando se espera diferença previsível. Os critérios são explícitos: código aberto e inspecionável na data de corte; pertencer à classe "harness" (§4); relevância de adoção **ou** singularidade arquitetural; diversidade de arquétipos (§5). Para cada caso registram-se **URL, commit ou tag e data de leitura**.

**Codificação e síntese.** A leitura segue um protocolo comum a todos os casos (Runeson & Höst, 2009). Ela combina codificação indutiva inspirada em *grounded theory* (Stol, Ralph & Fitzgerald, 2016) na descoberta das dimensões com *análise de conteúdo* (Hsieh & Shannon, 2005) de grade fixa na pontuação. A síntese comparativa é uma **feature analysis** no estilo **DESMET** (Kitchenham, Linkman & Law, 1997), na tradição do *benchmarking* como motor de progresso científico (Sim, Easterbrook & Holt, 2003).

**Ameaças à validade** (taxonomia de Cook & Campbell, 1979, adaptada a estudo de caso):

| Tipo | Ameaça | Mitigação declarada |
|---|---|---|
| Constructo | as "dimensões" não capturarem o que define um harness | derivação por GQM; definições operacionais publicadas |
| Interna | atribuir a "boa prática" o que é acaso histórico do projeto | protocolo único; cada afirmação rastreada a trecho/commit |
| Externa / **obsolescência** | não generalizar; o campo muda em meses | seleção por arquétipos; **data de corte + commits fixos**; a **cláusula de expiração** (§8) é a mitigação declarada, não um enfeite |
| Conclusão | tratar notas qualitativas como métrica exata | escala e critérios explícitos (DESMET); sem agregação numérica espúria |

Assim cada afirmação do livro remete a **um dado no repositório** e a **um procedimento nomeado**. O detalhamento operacional está no [Comparativo](../benchmark/comparativo.md) e no template de avaliação; as referências, na [Bibliografia](bibliografia.md).

## 7. Taxonomia por problema

Convenção herdada do referencial: organizar a disciplina **pelo problema resolvido, não por fabricante ou modelo**. É a taxonomia que estrutura os capítulos.

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

## 8. A cláusula de expiração

A tese mais importante e menos praticada da disciplina: **todo componente de harness é uma prótese temporária.**

A compactação existe porque janelas de contexto são finitas. O *plan mode* existe porque modelos agem precipitadamente. O *policy engine* existe porque modelos não são confiáveis com comandos destrutivos. Cada premissa tem prazo de validade.

O corolário prático é uma exigência de projeto: todo componente deveria documentar **qual melhoria de capacidade do modelo o tornaria desnecessário**. Harnesses que não fazem isso acumulam *scaffolding* morto, complexidade que sobrevive à limitação que a justificava.

Como visto na §6, essa cláusula é também a **mitigação declarada** da ameaça de obsolescência: o livro se assume datado. Voltamos a ela no capítulo 14, onde ela ganha um placar.

## 9. Artefatos operacionais

A disciplina produziu artefatos-padrão que reaparecem, com variações, em quase todos os harnesses estudados:

- **Arquivo de instruções de projeto** (`AGENTS.md` / `CLAUDE.md` / `GEMINI.md`): regras, convenções e limites que o agente lê antes de qualquer tarefa. Fronteiras claras superam restrições vagas.
- **Artefato de plano** (`PLAN.md`): criado no início da tarefa e atualizado durante a execução, com marcos verificáveis e fronteiras de escopo.
- **Log de implementação** (`IMPLEMENT.md`): registro *append-only* de decisões e desvios do plano.
- **Checklist de harness** (`HARNESS_CHECKLIST.md`): revisão pré-produção cobrindo instruções, ferramentas, contexto, planejamento, permissões e verificação, com a tabela de expiração da §8.

Esses artefatos são o embrião do nosso instrumento de avaliação (ver `benchmark/template/HARNESS_EVAL.md`).

## Verificação

1. Um sistema tem loop, ferramentas e gestão de contexto, mas executa qualquer comando sem confirmação nem sandbox. Ele é um harness pelo teste da §4? E ele é um bom harness?
2. Por que as notas do benchmark só comparam sistemas dentro da mesma categoria?
3. O critério de inclusão exige código "aberto e inspecionável", não "aberto à contribuição". Que tipo de projeto essa distinção admite, e por que ela é a escolha certa para este estudo?
4. Escolha um componente de harness qualquer e escreva a cláusula de expiração dele: qual melhoria de capacidade do modelo o tornaria desnecessário?

---

*As fontes deste capítulo, históricas e metodológicas, estão consolidadas na [Bibliografia](bibliografia.md), separando as **confirmadas** das que ainda pedem verificação, fiel ao Princípio I.*

---

## Respostas da verificação

**1.** Pelo teste da §4, **não**: faltam os mecanismos de controle, que são uma das quatro peças necessárias. O sistema é um loop sem freio, e o capítulo o descreve como "um incidente esperando acontecer". Repare que a pergunta separa duas coisas que costumam ser confundidas: o teste das quatro peças decide **categoria**, não **qualidade**. Um harness pode ter as quatro peças e ser ruim em todas; um sistema pode ser excelente em três e não ser um harness.

**2.** Porque as categorias respondem perguntas diferentes. Um framework expõe as quatro peças como **possibilidade programável**, e quem decide a política de parada e a regra de permissão é quem o usa. Um produto acabado já **tomou** essas decisões, e é por elas que pode ser julgado. Dar a mesma nota de permissões aos dois seria comparar potencial com escolha. Por isso a régua vale dentro do arquétipo, e o comparativo nunca agrega os cinco numa nota única.

**3.** Admite o projeto que publica a fonte sob licença permissiva e, ao mesmo tempo, **recusa contribuição externa** por política escrita, publicando o código para transparência e builds locais. É a escolha certa porque o que este estudo precisa fazer com o código é **lê-lo**: a unidade de análise da Fase 1 é o código-fonte, e ler não exige direito de participar. Um critério que exigisse abertura à contribuição excluiria sistemas perfeitamente inspecionáveis e mediria governança em vez de arquitetura.

**4.** Não há resposta única, e o valor está na forma. Uma cláusula bem escrita nomeia a **capacidade ausente**, não o desconforto. "A compactação deixa de ser necessária quando a janela de contexto exceder o tamanho típico de uma sessão inteira de trabalho **e** o custo por token deixar de crescer com o comprimento" é uma cláusula. "A compactação some quando os modelos melhorarem" não é: não dá para saber se já aconteceu. O teste de uma boa cláusula de expiração é se ela pode ser **verificada como cumprida**.
