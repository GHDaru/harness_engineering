# 00 — Introdução

## Agente = modelo + harness

Quando um agente de IA resolve uma tarefa real — corrigir um bug, migrar um módulo, responder com base em dezenas de arquivos — duas coisas distintas estão trabalhando. A primeira é o **modelo**: a rede que lê contexto e decide o próximo passo. A segunda é tudo o que está em volta dele: quem monta o contexto que ele lê, quem executa as ferramentas que ele invoca, quem decide o que ele pode ou não fazer, quem lembra o que aconteceu ontem, quem verifica se o resultado está certo. Esse "tudo em volta" é o **harness** — em tradução livre, o arreio, o andaime, o *scaffolding*.

A fórmula que organiza este livro é simples:

> **agente = modelo + harness**

<figure class="figura">
  <img src="assets/harness-diagrama.svg" alt="Diagrama esquemático: o modelo de IA no centro, envolto pelos seis blocos do harness — loop do agente, contexto, ferramentas, memória, permissões e verificação — dentro de uma moldura tracejada rotulada 'harness (o andaime)'; à direita, o mundo (arquivos, APIs, terminal) com setas de ida e volta.">
  <figcaption>O modelo no centro; o harness — o andaime — em volta. Cada bloco é um capítulo deste livro.</figcaption>
</figure>

O modelo é intercambiável e melhora a cada geração. O harness é engenharia de software clássica — e é nele que a maioria dos agentes falha ou tem sucesso. Dois produtos usando exatamente o mesmo modelo entregam resultados radicalmente diferentes conforme a qualidade do harness: como o contexto chega ao modelo, quais ferramentas ele tem, como os erros retornam, o que acontece quando a janela de contexto acaba.

**Engenharia de harness** é a disciplina de projetar esse scaffolding: entrega de contexto, interfaces de ferramentas, artefatos de planejamento, loops de verificação, sistemas de memória e sandboxes.

## Por que um livro — e por que agora

Entre 2024 e 2026, os harnesses de agentes de código deixaram de ser experimentos e viraram uma categoria de produto: Claude Code, Codex CLI, Gemini CLI, opencode, Aider, Cline, Goose, OpenHands e dezenas de outros. O mais notável não é a quantidade, mas a **convergência**: projetos independentes, em linguagens diferentes, chegaram às mesmas soluções — arquivos de contexto hierárquicos, compactação em camadas, plan mode como modo de permissão, hooks de ciclo de vida, MCP como padrão de integração.

Quando implementações independentes convergem, existe uma disciplina por trás. Este livro documenta essa disciplina.

## O método: ler código, não marketing

Este livro é empírico. Cada capítulo trata de uma funcionalidade do harness (o loop, o contexto, a compactação, as permissões...) e é escrito a partir da leitura do código-fonte de harnesses reais de código aberto. A regra editorial mais importante do projeto:

> Afirmações sobre um harness exigem **evidência**: o caminho do arquivo no código-fonte onde a funcionalidade está implementada.

READMEs prometem; código entrega. Vários projetos anunciam dimensões que o código não tem — a exigência de evidência é o que separa avaliação de marketing.

## Nota de autoria e método

Por transparência — e coerência com a regra de evidência acima — este livro é **co-escrito com um agente de IA** (Claude Code, da Anthropic) operando sob **autoria, curadoria e responsabilidade humanas**. O agente executa a pesquisa, a redação e o ciclo de produção; o autor humano define o escopo, decide, **verifica cada fonte** e responde pelo conteúdo. Seguindo as políticas editoriais de autoria (ICMJE, COPE, *Nature*, *Science*), a IA **não** é listada como autora — não pode ser responsável — e seu uso é divulgado aqui, na abertura.

Isso não é um detalhe: um livro sobre a disciplina de instrumentar bem os agentes de IA usa essa mesma disciplina para se escrever, e a expõe. O método completo — pesquisa dupla verificada por busca cruzada, ciclo spec-driven, revisão e datação — está documentado no [Guia Editorial §6](GUIA-EDITORIAL.md), com um *survey* das metodologias de escrita tradicionais e da era-IA que o fundamentam.

## Estrutura do livro

- **Fundamentos** (capítulo 01): as definições formais, os artigos canônicos e a taxonomia de problemas que organiza tudo o que vem depois.
- **Capítulos 02–13**: uma funcionalidade por capítulo. Cada um define o problema, apresenta os padrões de implementação conhecidos e mostra, com evidência, como cada harness estudado implementa.
- **Convergências e tendências** (capítulo 14): o que a indústria já padronizou, onde ainda há divergência real, e a "cláusula de expiração" — a tese de que todo componente de harness existe porque o modelo ainda não faz aquilo sozinho, e deve ser desenhado sabendo que um dia será desnecessário.
- **Benchmark** (`benchmark/`): a seção empírica — avaliações padronizadas, por dimensão, com notas 0–3 e evidência, de cada harness estudado, mais o comparativo consolidado.

## Os harnesses da primeira rodada

| Harness | Stack | Por que foi escolhido |
|---|---|---|
| **opencode** | TypeScript + Effect-TS | Produto maduro, cliente-servidor, o mais agnóstico de provedor (~26 loaders + centenas de modelos) |
| **gemini-cli** | TypeScript (Google) | Produto de big tech com o regime de controle (policy engine, sandbox) e verificação (4 suítes de eval) mais rigoroso |
| **OpenHarness** | Python | Port declarado e legível do Claude Code — expõe os mecanismos que os produtos escondem — mais um subsistema multi-agente ambicioso |

E, como referencial teórico, a lista curada **awesome-harness-engineering** (~426 recursos organizados por problema), de onde vem a definição de harness usada no capítulo 01 e a taxonomia que estrutura os capítulos.

As próximas rodadas incorporam Codex CLI (Rust, sandbox-first), Goose (Rust, MCP-nativo), Aider (Python, context-first) e OpenHands (Python, event-stream + cultura de eval acadêmica) — cada um escolhido por representar um *arquétipo* diferente de harness.
