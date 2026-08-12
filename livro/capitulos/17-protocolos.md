# 17 — A Camada de Protocolos: o tecido conjuntivo entre harnesses

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que a camada de protocolos é o que transforma um mercado de silos em um ecossistema, e por que cada protocolo padroniza uma *fronteira* diferente do harness;
2. **Distinguir** as fronteiras cobertas por MCP (Model Context Protocol), A2A (Agent-to-Agent), ACP (Agent Client Protocol), agentskills.io e AGENTS.md, incluindo as duas confusões clássicas;
3. **Analisar** a matriz de adoção medida no código e localizar um harness real nela;
4. **Avaliar** a saúde de um protocolo por adoção medida e governança, em vez de por marketing;
5. **Decidir** quais protocolos um harness novo precisa falar para não ficar fora das arquiteturas de composição dos outros.

## O melhor harness da comparação, e ninguém consegue plugá-lo

Suponha que você avaliou seis harnesses de código com rigor. Leu o código de todos, montou a régua, deu as notas. Um deles ganhou em três dimensões técnicas: o formato de edição é o mais bem medido do mercado, a gestão de contexto é a mais econômica, o comportamento em repositório grande é o mais previsível.

Você o adota. Seis meses depois, a equipe está migrando para outro.

Não porque ele piorou. Porque a arquitetura mudou em volta dele. O time passou a rodar o agente dentro do editor, e ele não fala o protocolo que o editor usa. Depois passou a orquestrar dois agentes em paralelo, um dirigindo o outro, e ele não pode ser dirigido. Depois padronizou as ferramentas internas atrás de servidores comuns, e ele não sabe consumi-los.

O harness continua sendo tecnicamente excelente. Ele só não **encaixa**.

Este capítulo é sobre o encaixe. Os capítulos 02 a 16 tratam do que acontece *dentro* de um harness; este trata do que acontece **entre** eles.

## O problema

Sem protocolos compartilhados, cada harness é um silo. Suas ferramentas, suas instruções de projeto, seus subagentes e suas skills só funcionam dentro dele.

A camada de protocolos é o que transforma esse mercado de silos em ecossistema. Cada protocolo padroniza uma fronteira diferente: agente↔ferramenta, agente↔agente, agente↔editor, agente↔usuário. Somam-se a eles os formatos transversais de conhecimento procedural (SKILL.md) e de instruções de projeto (AGENTS.md).

A consequência prática é a da cena acima. Em um mercado que *compõe* harnesses, não falar os protocolos não é perder uma feature. É ficar de fora das arquiteturas dos outros.

## Fontes da indústria

- [ecosystem map 2026](https://www.digitalapplied.com/blog/ai-agent-protocol-ecosystem-map-2026-mcp-a2a-acp-ucp)
- [Zylos: convergência MCP/A2A/ACP](https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence/)
- [Zuplo: onde foi parar o ACP](https://zuplo.com/blog/agent-protocol-stack-mcp-a2a-acp-2026)
- [Agent Skills: formato e adoção](https://atlan.com/know/ai-agent/ai-agent-skills/what-are-agent-skills/)
- [AGENTS.md guide 2026](https://codersera.com/blog/agents-md-complete-guide-2026/)
- [Zed ACP](https://tessl.io/blog/zed-debuts-agent-client-protocol-to-connect-ai-coding-agents-to-any-editor/)
- **Consulte também**: a coleção viva [Awesome Harness Engineering — Skills & MCP](https://github.com/GHDaru/awesome-harness-engineering#skills--mcp) reúne mais recursos desta dimensão, curados por problema.

A matriz de adoção da próxima seção é evidência própria do benchmark (`benchmark/avaliacoes/`).

## Na prática: um protocolo é isto, em bytes

"Protocolo" soa abstrato até você ver o tráfego. Vale olhar duas fronteiras diferentes, lado a lado, porque a diferença entre elas fica óbvia no formato das mensagens.

**Fronteira vertical, MCP.** O agente quer uma ferramenta que não é dele. Primeiro pergunta o que existe:

```jsonc
// agente → servidor MCP
{"jsonrpc":"2.0","id":1,"method":"tools/list"}

// servidor → agente
{"jsonrpc":"2.0","id":1,"result":{"tools":[
  {"name":"buscar_ticket",
   "description":"Busca um ticket do suporte por id",
   "inputSchema":{"type":"object","properties":{"id":{"type":"string"}},
                  "required":["id"]}}
]}}
```

E depois usa:

```jsonc
// agente → servidor MCP
{"jsonrpc":"2.0","id":2,"method":"tools/call",
 "params":{"name":"buscar_ticket","arguments":{"id":"T-4471"}}}

// servidor → agente
{"jsonrpc":"2.0","id":2,"result":{"content":[
  {"type":"text","text":"T-4471: login falha após troca de senha. Aberto."}
]}}
```

Repare no que o protocolo padroniza: **a descoberta** (`tools/list`) e **a chamada** (`tools/call`), com o schema vindo do servidor. É exatamente o contrato do capítulo 05, agora atravessando um processo. O agente não precisa saber quem implementa `buscar_ticket`, e o servidor não precisa saber qual modelo está do outro lado.

**Fronteira de composição, ACP.** Aqui não é o agente pedindo ferramenta. É um **cliente dirigindo um agente inteiro**:

```jsonc
// cliente (editor, ou outro harness) → agente
{"jsonrpc":"2.0","id":7,"method":"session/prompt",
 "params":{"sessionId":"s-19","prompt":[
   {"type":"text","text":"o teste test_login está falhando, conserta"}]}}

// agente → cliente, em fluxo, enquanto trabalha
{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s-19",
 "update":{"sessionUpdate":"tool_call","title":"pytest test_login",
           "status":"in_progress"}}}

{"jsonrpc":"2.0","method":"session/update","params":{"sessionId":"s-19",
 "update":{"sessionUpdate":"tool_call_update","status":"completed"}}}

// e quando termina
{"jsonrpc":"2.0","id":7,"result":{"stopReason":"end_turn"}}
```

As duas trocas usam o mesmo transporte, JSON-RPC, e resolvem problemas de natureza oposta.

Em MCP, quem manda é o agente e quem obedece é a ferramenta. Em ACP, quem manda é o cliente e **quem obedece é o agente**. Note o `stopReason` da última linha: é o rótulo tipado de terminação do capítulo 02, agora exposto na fronteira, porque quem dirige precisa saber *por que* o turno acabou.

E note o `session/update`. O protocolo não devolve só o resultado, devolve o **andamento**. Um agente que só sabe responder no fim não pode ser dirigido por um editor, porque o editor precisa mostrar algo enquanto espera. Essa exigência de observabilidade é a razão pela qual o ACP se espalhou entre harnesses e não só entre editores: quem orquestra outro agente tem o mesmo problema de quem o exibe.

## O estado da arte

### O mapa: um protocolo por fronteira

| Protocolo | Fronteira | Origem / governança | Estado (2026) |
|---|---|---|---|
| **MCP** (Model Context Protocol) | agente ↔ **ferramentas/dados** | Anthropic → adoção universal (OpenAI, Google, Microsoft) | maduro; ~97M downloads |
| **A2A** (Agent-to-Agent) | agente ↔ **agente** (delegação entre organizações) | Google → **Linux Foundation** (v1.0 em 2026) | consolidando; absorveu o ACP (Agent Communication Protocol) da IBM |
| **ACP** (Agent Client Protocol) | agente ↔ **editor/cliente** | Zed | adoção rápida entre harnesses de código |
| **agentskills.io** (Agent Skills / SKILL.md) | **conhecimento procedural** portável | Anthropic (spec aberta, dez/2025) | ~40 produtos compatíveis em 6 meses |
| **AGENTS.md** | **instruções de projeto** portáveis | comunidade → **Agentic AI Foundation** (Linux Foundation) | 60.000+ repositórios; 20+ ferramentas leem nativamente |
| AG-UI | agente ↔ **interface de usuário** | comunidade (CopilotKit) | emergente |
| ACP-IBM (Agent Communication Protocol) | agente ↔ agente | IBM | **encerrado**, fundido ao A2A (ago/2025) |

Duas confusões a desfazer, e as duas custam tempo de quem chega agora.

A primeira: **"ACP" designa dois protocolos distintos**. O da IBM cobria comunicação agente-agente e foi descontinuado em favor do A2A. O da Zed cobre agente-editor, está vivo e em expansão. Neste livro, ACP significa o da Zed.

A segunda: **MCP e A2A não competem**. MCP é a conexão vertical, do agente para a ferramenta. A2A é a horizontal, de agente para agente par. Um sistema real usa os dois, como o empilhamento adiante deixa ver.

### A matriz de adoção, medida no código e não no marketing

O diferencial deste capítulo é cruzar os protocolos com as **11 avaliações de harnesses do benchmark**, mais os 4 frameworks da rodada frameworks-1, com evidência por arquivo em `benchmark/avaliacoes/`. Nenhum comparativo externo tem esta coluna de verdade.

| Harness | MCP client | MCP server | ACP | A2A | SKILL.md / agentskills | AGENTS.md (ou equiv.) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| opencode | ✅ | — | ✅ (Zed) | — | parcial | ✅ AGENTS.md |
| gemini-cli | ✅ | — | ✅ | ✅ **client+server** | ✅ | GEMINI.md |
| OpenHarness | ✅ | — | — | — | ✅ (formato Claude) | CLAUDE.md |
| Codex CLI | ✅ | ✅ | — | — | ✅ | ✅ AGENTS.md |
| Goose | ✅ | ✅ (`goose mcp`) | ✅ (desktop inteiro) | — | ✅ | ✅ AGENTS.md + .goosehints |
| Aider | ❌ | ❌ | — | — | — | ✅ (leitura) |
| OpenHands | ✅ | ✅ (FastMCP) | ✅ (perfis) | — | ✅ (repos org) | microagents |
| OpenClaw | ✅ | ✅ | ✅ (orquestra terceiros) | — | ✅ (52 bundled) | ✅ AGENTS.md + SOUL.md |
| Hermes | ✅ | ✅ | ✅ | — | ✅ (núcleo do learning) | ✅ AGENTS.md + SOUL.md |
| IronClaw | ✅ | — | — | — | ✅ (compat OpenClaw) | identity files |
| n8n | ✅ | ✅ (Trigger) | — | — | — | — |
| *frameworks:* | | | | | | |
| LangGraph | ❌ | ❌ (só no servidor pago) | ❌ | ❌ | ❌ | — |
| OpenAI Agents SDK (Software Development Kit) | ✅ | — | ❌ | — | parcial | só sandbox agents |
| CrewAI | ✅ (obrigatório) | — | ✅ **client+server** | — | ✅ | ✅ **auto-gerado** |
| software-agent-sdk | ✅ (OAuth) | — | ❌ | ✅ (usa harnesses como motor) | ✅ (spec) | ✅ |

**MCP venceu de fato.** Dez de onze o falam, e a única exceção é escolha filosófica declarada. Entre as rodadas 1 e 2 o padrão migrou de "cliente" para "cliente e servidor": o harness deixou de só consumir ferramentas e passou a ser, ele mesmo, serviço consumível.

**agentskills.io é a padronização mais rápida que já medimos.** Spec de dezembro de 2025, oito dos nossos onze compatíveis em julho de 2026. A previsão do cap. 12, de que "um MCP da extensibilidade está se formando", se cumpriu. E com um detalhe estrutural que vale reter: skills são markdown portável, então a mesma skill roda em harnesses diferentes. O aprendizado auto-evolutivo do cap. 16 escreve *nesse* formato, o que torna o conhecimento aprendido por um agente transferível a outro, em tese.

**ACP é o protocolo silencioso mais importante da coorte.** Seis de onze o falam, e três deles (OpenClaw, OpenHands, Goose) o usam para **orquestrar outros harnesses** como subagentes, fazendo de Claude Code, Codex, Gemini CLI e opencode peças intercambiáveis. O que nasceu como "agente↔editor" virou, na prática, o barramento de composição entre harnesses. Foi o `session/update` do exemplo acima que permitiu isso.

**O A2A saiu da aposta de um só**, atualizado na rodada frameworks-1. O gemini-cli era o único harness a implementá-lo, e o **CrewAI** entrou com client e server nativos (AgentCard completo, JWS, gRPC/REST), o segundo implementador medido e o primeiro framework. A governança na Linux Foundation e a absorção do ACP-IBM seguem apontando o A2A como candidato à fronteira inter-organizacional. Nos harnesses de produto, porém, essa fronteira ainda quase não existe.

**AGENTS.md consolidou como padrão neutro.** A fragmentação AGENTS/CLAUDE/GEMINI.md descrita no cap. 03 está se resolvendo: Codex, Goose, opencode, OpenClaw e Hermes convergiram para AGENTS.md, agora sob a Agentic AI Foundation, com os arquivos proprietários virando alias.

### O empilhamento: como os protocolos compõem

Um sistema agêntico completo em 2026 usa a pilha inteira, uma camada por fronteira:

```
[usuário]
   │  AG-UI / canais de chat / TUI          (interface)
[harness A]
   │  ACP                                    (composição: A dirige B como subagente)
[harness B]
   │  A2A                                    (delegação a agente de outra organização)
[agente remoto]
   │  MCP                                    (cada agente alcança suas ferramentas)
[ferramentas/dados]

transversais: AGENTS.md (instruções por projeto) · SKILL.md (procedimentos portáveis)
```

### Implicações para a engenharia de harness

**Protocolo é dimensão de sobrevivência, não de feature.** O Aider é referência técnica em três dimensões e está fora do ecossistema de composição inteiro por não falar MCP nem ACP. É a cena que abriu o capítulo, com nome.

**A cláusula de expiração não se aplica aqui.** Protocolos são fronteira com o mundo, e não prótese para uma limitação do modelo. São o scaffolding que *resta* quando os modelos melhoram, e por isso investir em protocolo é o investimento de harness com maior meia-vida (cap. 14).

**Para o benchmark**, a matriz acima vira seção permanente do comparativo, atualizada a cada rodada. Protocolos não recebem nota 0–3 como harnesses. São avaliados por **adoção medida**, que é a matriz, e por **saúde de governança**, em que fundação neutra vale mais que fornecedor único.

**Adendo (2026-07-31).** A spec MCP **2026-07-28** ([anúncio](https://blog.modelcontextprotocol.io/posts/2026-07-28/)) reforça a tese deste capítulo por outro ângulo. Núcleo stateless, framework de extensões e a **primeira política formal de depreciação**, de 12 meses, são o comportamento típico de um protocolo saindo da adolescência e entrando na fase de infraestrutura: versionamento disciplinado passa a importar mais que features novas. A adoção da nova versão pela coorte entra na matriz na próxima rodada.

No mesmo dia, na outra fronteira (spec 065): a [especificação do A2A](https://a2a-protocol.org/latest/specification/) confirma o **v1.0 estável sob a Linux Foundation**, organizado em três camadas — modelo de dados em Protobuf/JSON Schema, operações abstratas e bindings JSON-RPC/gRPC/REST — com o **v1.0.1 já trazendo um mecanismo formal de extensões**. Os dois vencedores de fronteira chegaram, no mesmo trimestre, ao mesmo estágio: extensões formais em vez de features no núcleo.

### Leitura executiva

A camada de protocolos já tem um vencedor por fronteira. MCP na vertical, agente para ferramenta, com adoção quase total. ACP como barramento de composição entre harnesses. agentskills.io como formato portável de conhecimento procedural. AGENTS.md como padrão neutro de instruções de projeto. O A2A segue como aposta em consolidação para a fronteira inter-organizacional, sustentada mais pela governança (Linux Foundation, absorção do ACP-IBM) do que pela adoção medida nos harnesses de produto.

A decisão de engenharia é assimétrica: protocolos são o componente de maior meia-vida do harness, imune à cláusula de expiração, e a matriz de adoção, não o marketing, é o instrumento para reavaliá-los a cada rodada.

**O que roubar:**

- **Exponha o rótulo de terminação na fronteira**, como o `stopReason` do ACP. Quem dirige o seu agente precisa saber por que ele parou.
- **Emita andamento em fluxo** (`session/update`), não só resultado final. É isso que torna um agente dirigível.
- **Deixe o servidor declarar o schema da ferramenta** (`tools/list`), em vez de embuti-lo no cliente.
- **Prefira o formato transversal em markdown** (AGENTS.md, SKILL.md) ao arquivo proprietário, porque é o que atravessa harness.

## Verificação

1. Um colega afirma que "o A2A vai substituir o MCP". Por que a afirmação confunde as fronteiras, e como o empilhamento mostra que um sistema real usa os dois?
2. "ACP" aparece duas vezes na tabela de protocolos, com estados opostos, "adoção rápida" e "encerrado". Explique a diferença entre os dois protocolos e diga qual deles este livro chama de ACP.
3. Você está desenhando um harness novo. Quais protocolos são obrigatórios hoje, qual ainda é aposta, e o que a exceção do Aider ensina sobre o custo de não falar nenhum?
4. Por que a cláusula de expiração (cap. 14) não se aplica à camada de protocolos, quando se aplica a quase todo o resto do harness?
5. Olhando as duas trocas de mensagens da seção "Na prática": qual delas você implementaria primeiro num harness novo, e por quê?

---

## Respostas da verificação

**1.** Porque os dois resolvem fronteiras diferentes, e substituição só faz sentido entre coisas que resolvem a mesma. MCP é vertical: o agente alcança ferramentas e dados, e quem obedece é a ferramenta. A2A é horizontal: um agente delega a outro agente, tipicamente de outra organização, e os dois lados são pares. No empilhamento, um agente remoto alcançado por A2A usa **o seu próprio** MCP para chegar às ferramentas dele. Os dois aparecem na mesma pilha, em camadas distintas, e nenhum ocupa o lugar do outro.

**2.** O ACP da IBM (Agent Communication Protocol) cobria comunicação agente-agente e foi **encerrado em agosto de 2025**, com seus recursos absorvidos pelo A2A. O ACP da Zed (Agent Client Protocol) cobre agente-cliente, isto é, um editor ou outro harness dirigindo um agente, e está em adoção rápida: seis dos onze harnesses medidos o falam. Neste livro, **ACP significa sempre o da Zed**, e a tabela mantém o outro com o rótulo `ACP-IBM` justamente para que a sigla não engane.

**3.** Obrigatórios hoje: **MCP como cliente**, para alcançar ferramentas de terceiros, e cada vez mais **MCP como servidor**, para que o seu harness seja consumível por outros. Depois **ACP**, se você quer que o seu agente rode dentro de editores ou seja orquestrado por outro harness. E **AGENTS.md**, que é barato e já é padrão neutro sob fundação. Ainda aposta: **A2A**, cuja fronteira inter-organizacional quase não existe nos harnesses de produto, embora a governança seja a mais sólida do conjunto. A lição do Aider é a mais dura do capítulo: excelência técnica em dimensões internas **não compensa** ausência de protocolo, porque o custo não aparece como feature faltando, aparece como ausência nas arquiteturas que os outros montam.

**4.** Porque a cláusula de expiração vale para componentes que existem **para suprir uma limitação do modelo**, e desaparecem quando a limitação desaparece: compactação existe porque a janela é finita, plan mode existe porque o modelo age precipitadamente. Protocolo não supre limitação de modelo. Ele resolve a **fronteira entre sistemas distintos**, que continua existindo independentemente de quão bom o modelo fique. Dois processos separados vão precisar de um contrato mesmo que ambos sejam perfeitos, e é por isso que protocolo é o investimento de maior meia-vida do harness.

**5.** A resposta defensável é **MCP como cliente**, e a razão é assimetria de retorno: com poucas linhas o seu harness ganha acesso a todo um ecossistema de ferramentas que você não escreveu, e a adoção medida (dez de onze) garante que o investimento não fica órfão. ACP vem depois, e depende de ambição: ele exige que o seu agente saiba **relatar andamento em fluxo**, o que costuma forçar refatoração no loop, não só a adição de um adaptador. Se a sua resposta foi ACP porque você quer ser orquestrado desde o começo, ela também se sustenta — desde que você tenha notado que o custo real está no `session/update`, e não no transporte.
