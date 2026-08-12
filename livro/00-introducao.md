# 00 — Introdução

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](GUIA-EDITORIAL.md).
> andaime: completo

## O conselho perfeito que não conserta nada

Você cola um erro no chat e recebe uma resposta impecável. O diagnóstico está certo, o trecho de código sugerido está certo, a explicação é melhor que a da documentação. Você agradece, fecha a aba, abre o editor e faz tudo à mão: encontra o arquivo, aplica a mudança, roda o teste. O teste falha por outro motivo. Você volta ao chat e recomeça a conversa, agora explicando de novo o que já tinha explicado.

Repare no que aconteceu. O conselho era bom. O trabalho continuou sendo seu.

Agora a mesma tarefa num agente de código. Você digita a mesma frase. Ele localiza o arquivo, aplica a mudança, roda o teste, vê a falha nova, corrige também aquela, roda outra vez e só então responde: "pronto, eram dois problemas". Você não explicou nada duas vezes.

O modelo dos dois casos pode ser exatamente o mesmo. A diferença toda está no que existe **em volta** dele.

## Agente = modelo + harness

Quando um agente resolve uma tarefa real, duas coisas distintas estão trabalhando.

A primeira é o **modelo**: a rede que lê contexto e decide o próximo passo. É a parte que raciocina, e é a que melhora sozinha a cada geração.

A segunda é tudo o que está em volta dele. Quem monta o contexto que ele lê. Quem executa as ferramentas que ele invoca. Quem decide o que ele pode e não pode fazer. Quem lembra o que aconteceu ontem. Quem verifica se o resultado está certo e quem decide que já é hora de parar. Esse "tudo em volta" é o **harness**, que em tradução livre é o arreio, o andaime, o *scaffolding*.

A fórmula que organiza este livro é simples:

> **agente = modelo + harness**

<figure class="figura">
  <img src="assets/harness-diagrama.svg" alt="Diagrama esquemático: o modelo de IA no centro, envolto pelos seis blocos do harness — loop do agente, contexto, ferramentas, memória, permissões e verificação — dentro de uma moldura tracejada rotulada 'harness (o andaime)'; à direita, o mundo (arquivos, APIs, terminal) com setas de ida e volta.">
  <figcaption>O modelo no centro; o harness em volta. Cada bloco é um capítulo deste livro.</figcaption>
</figure>

O modelo é intercambiável. O harness é engenharia de software clássica, e é nele que a maioria dos agentes falha ou tem sucesso.

Dois produtos com exatamente o mesmo modelo entregam resultados radicalmente diferentes conforme a qualidade do harness: como o contexto chega ao modelo, quais ferramentas ele tem, como os erros retornam, e o que acontece quando a **janela de contexto** (o limite de texto que o modelo consegue enxergar de uma vez) acaba.

**Engenharia de harness** é a disciplina de projetar esse scaffolding: entrega de contexto, interfaces de ferramentas, artefatos de planejamento, loops de verificação, sistemas de memória e sandboxes.

## Na prática: a mesma pergunta, dois destinos

Vale ver a diferença em texto, porque ela não é abstrata. Você pede: *"o teste `test_login` está falhando, conserta"*.

**Sem harness**, o modelo só pode devolver linguagem:

```text
Provavelmente o cookie de sessão está expirando antes da
verificação. Tente ajustar o `max_age` em auth.py:

    session.set_cookie(..., max_age=3600)

Se não resolver, verifique se o fuso horário do servidor…
```

Está correto e é inútil sozinho. O modelo não sabe se `auth.py` existe, não leu a linha, não rodou o teste e não tem como saber se acertou. Ele **supôs**, porque supor era a única coisa disponível.

**Com harness**, a mesma decisão sai em outro formato:

```text
→ executar_shell("pytest test_login -x")
← FAILED test_login - assert 401 == 200

→ ler_arquivo("auth.py")
← ...  session.set_cookie(..., max_age=0)  ...

→ editar_arquivo("auth.py", max_age=0 → max_age=3600)
← ok, 1 linha alterada

→ executar_shell("pytest test_login -x")
← FAILED test_login - assert 500 == 200      ← erro NOVO

→ ler_arquivo("auth.py")
← ...
→ editar_arquivo("auth.py", ...)
→ executar_shell("pytest test_login -x")
← 1 passed

"Pronto. Eram dois: o cookie nascia expirado e o handler
 quebrava quando a sessão vinha vazia."
```

Sete pedidos de ação e uma frase no fim. Agora observe o que o harness fez neste roteiro, porque cada item é um capítulo deste livro:

- decidiu **continuar** depois de cada resultado, e decidiu **parar** quando o modelo respondeu sem pedir nada (cap. 02);
- montou o que o modelo veria a cada passo, sem despejar o repositório inteiro (cap. 03 e 04);
- ofereceu as ferramentas `ler_arquivo`, `editar_arquivo` e `executar_shell`, com esses nomes e esses argumentos (cap. 05 e 06);
- deixou passar a edição, ou pediu sua aprovação antes dela (cap. 07);
- devolveu o **erro** ao modelo como texto em vez de derrubar o processo, o que é a razão pela qual a segunda falha virou conserto e não abandono (cap. 02 e 11).

E há um detalhe fácil de não notar: **o modelo não sabia que havia dois problemas**. Ninguém sabia. O segundo só apareceu porque o primeiro foi consertado e o teste rodou de novo. Essa é a diferença entre aconselhar e trabalhar, e ela não vem do raciocínio. Vem do laço.

## Por que um livro, e por que agora

Entre 2024 e 2026, os harnesses de agentes de código deixaram de ser experimentos e viraram categoria de produto: Claude Code, Codex CLI, Gemini CLI, opencode, Aider, Cline, Goose, OpenHands e dezenas de outros.

O mais notável não é a quantidade, é a **convergência**. Projetos independentes, em linguagens diferentes, sem combinar nada, chegaram às mesmas soluções: arquivos de contexto hierárquicos, compactação em camadas, plan mode como modo de permissão, hooks de ciclo de vida, MCP (Model Context Protocol) como padrão de integração.

Quando implementações independentes convergem, existe uma disciplina por trás. Este livro documenta essa disciplina.

## O método: ler código, não marketing

Este livro é empírico. Cada capítulo trata de uma funcionalidade do harness e é escrito a partir da leitura do código-fonte de harnesses reais de código aberto.

A regra editorial mais importante do projeto:

> Afirmações sobre um harness exigem **evidência**: o caminho do arquivo no código-fonte onde a funcionalidade está implementada.

READMEs prometem; código entrega. Vários projetos anunciam dimensões que o código não tem, e a exigência de evidência é o que separa avaliação de marketing.

## Nota de autoria e método

Por transparência, e por coerência com a regra de evidência acima: este livro é **co-escrito com um agente de IA** (Claude Code, da Anthropic) operando sob **autoria, curadoria e responsabilidade humanas**. O agente executa a pesquisa, a redação e o ciclo de produção. O autor humano define o escopo, decide, **verifica cada fonte** e responde pelo conteúdo.

Seguindo as políticas editoriais de autoria (ICMJE, COPE, *Nature*, *Science*), a IA **não** é listada como autora, porque não pode ser responsabilizada, e seu uso é divulgado aqui, na abertura.

Isso não é um detalhe. Um livro sobre a disciplina de instrumentar bem agentes de IA usa essa mesma disciplina para se escrever, e a expõe. O método completo (pesquisa dupla verificada por busca cruzada, ciclo spec-driven, revisão e datação) está no [Guia Editorial §6](GUIA-EDITORIAL.md), com um *survey* das metodologias de escrita tradicionais e da era-IA que o fundamentam.

## Como ler este livro: três portas de entrada

O livro é denso de propósito. Esta seção existe para que a densidade não seja uma parede. Escolha a sua porta.

**Se você está chegando agora** e nunca construiu um agente: leia 00, 01 e 02 em sequência, sem pressa, com o [Glossário](glossario.md) ao lado. Toda sigla do livro está lá, por extenso e explicada, e na versão online basta passar o mouse. Depois do capítulo 02, os capítulos 03 a 13 podem ser lidos em qualquer ordem, porque cada um é autocontido e abre definindo o próprio problema.

**Se você já opera um agente** e quer entender o que há por dentro: a **Leitura executiva** ao fim de cada capítulo é o seu atalho, com o estado da arte da dimensão em um parágrafo e a seção "o que roubar". Vá direto ao capítulo que interessa e desça ao corpo quando quiser a evidência.

**Se você constrói harnesses**: o livro inteiro é seu, incluindo os Apêndices A com evidência por repositório e caminho de arquivo, o [Benchmark](../benchmark/comparativo.md) e as duas trilhas práticas. O **harness-zero** é a construção didática, uma funcionalidade por etapa; o **harness-um** é a implementação de referência completa, com [apêndice próprio](apendice-harness-um.md).

## Estrutura do livro

- **Fundamentos** (capítulo 01): as definições formais, os artigos canônicos e a taxonomia de problemas que organiza tudo o que vem depois.
- **Capítulos 02–13**: uma funcionalidade por capítulo. Cada um define o problema, apresenta os padrões de implementação conhecidos e mostra, com evidência, como cada harness estudado implementa.
- **Convergências e tendências** (capítulo 14): o que a indústria já padronizou, onde ainda há divergência real, e a **cláusula de expiração**, a tese de que todo componente de harness existe porque o modelo ainda não faz aquilo sozinho, e deve ser desenhado sabendo que um dia será desnecessário.
- **Capítulos 15–17**: as fronteiras. O harness embutido em produto (15), o harness que aprende com o uso (16) e a camada de protocolos que une o ecossistema (17).
- **Benchmark** (`benchmark/`): a seção empírica, com avaliações padronizadas por dimensão, notas 0–3 e evidência de cada harness estudado, mais o comparativo consolidado.

## Os harnesses do estudo

O estudo cobre, até esta edição, **vinte e um sistemas de código aberto**, avaliados por leitura sistemática de código em cinco arquétipos (o método está no [capítulo 01, §6](01-fundamentos.md)):

- **Harnesses de código** — opencode, gemini-cli, OpenHarness, Codex CLI, Goose, Aider, OpenHands, Grok Build, Pi, Kimi Code e Prime Agent;
- **Agentes pessoais self-hosted** — OpenClaw, Hermes Agent, IronClaw, ohmo;
- **Agentes organizacionais** — QM;
- **Harnesses embutidos** — n8n (nó AI Agent);
- **Frameworks** — LangGraph, CrewAI, OpenAI Agents SDK (Software Development Kit), Software Agent SDK.

Cada um foi escolhido por representar um *arquétipo* diferente. A lógica é de replicação, não de amostragem: produto maduro agnóstico de provedor (opencode), regime de controle de big tech (gemini-cli), port didático legível (OpenHarness), sandbox-first (Codex CLI), MCP-nativo (Goose), context-first (Aider), cultura de eval acadêmica (OpenHands), agente da organização inteira com o loop trocável (QM), e assim por diante.

A lista completa, com **origem, versão, fork e commit exatos lidos** em cada avaliação e o link para a análise e o diagnóstico de cada sistema, está no **[Apêndice — O estudo](apendice-estudo.md)**. O placar consolidado por dimensão está no [Comparativo](../benchmark/comparativo.md).

Como referencial teórico, e para explorar o ecossistema além do corpus, soma-se a coleção viva **[Awesome Harness Engineering](https://github.com/GHDaru/awesome-harness-engineering)**, com cerca de 426 recursos organizados por problema, na mesma estrutura deste livro. De lá vêm a definição de harness usada no capítulo 01 e a taxonomia que organiza os capítulos.
