# 05 — Design de Ferramentas

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: completo
>
> Esqueleto v3 — corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Explicar** por que a descrição de uma tool é prompt engineering, não documentação de API;
2. **Derivar** o schema de uma tool a partir de tipos, e justificar por que ninguém mais escreve JSON Schema à mão;
3. **Comparar** os três regimes de escala: catálogo fixo, tool search com carregamento tardio e code-as-action;
4. **Implementar** a `ToolPort` do harness-zero com schema derivado e erro-como-dado (etapa 2);
5. **Avaliar** quando usar tool calls individuais e quando usar código orquestrando tools em sandbox.

## O parâmetro que mudou de nome e ninguém contou ao modelo

Você escreveu a ferramenta de busca há três meses. O JSON Schema está logo acima da função, feito à mão, com o parâmetro chamado `padrao`. Funcionou desde então.

Na semana passada alguém renomeou o parâmetro da função Python para `glob`, porque `padrao` era vago. Os testes passaram: nenhum teste chama a função pelo nome do argumento.

Hoje o agente está travado. Ele lê o schema, obedece com perfeição, monta `{"padrao": "*.py"}`, e recebe de volta `TypeError: buscar_arquivos() got an unexpected keyword argument 'padrao'`. Ele tenta de novo. Tenta uma terceira vez, agora com aspas diferentes, porque o erro não diz o que está errado. Vinte turnos depois você desiste e vai olhar o log.

O modelo não errou. **A documentação da ferramenta e a ferramenta divergiram**, e nada no sistema tinha o dever de notar.

Guarde a cena, porque ela é o argumento inteiro deste capítulo: quando o schema é escrito à mão, ele é uma segunda fonte da verdade — e duas fontes da verdade é uma a mais do que existe.

## O problema

As ferramentas são as mãos do agente: o contrato pelo qual o modelo age sobre o mundo.

Design de ferramentas é decidir **quais** existem, **como** seus parâmetros são descritos ao modelo, **como** os resultados e os erros retornam, e **quando** cada uma está disponível.

Cada uma dessas decisões falha de um jeito diferente. Uma tool mal descrita gera chamadas erradas. Um arsenal grande demais dilui a atenção do modelo *e* estoura o orçamento de contexto antes de qualquer trabalho útil. Um arsenal pequeno demais força gambiarras via shell.

## Fundamentos científicos

- **A evolução do uso de tools** — [arXiv 2603.22862](https://arxiv.org/abs/2603.22862) traça a trajetória de single-tool call a orquestração multi-tool, o pano de fundo do "code-as-action".
- **Tool learning como campo** — o survey de tool learning ([repo](https://github.com/quchangle1/LLM-Tool-Survey)) organiza como agentes aprendem a selecionar e compor ferramentas.

(Bibliografia completa: `livro/bibliografia.md`.)

## Fontes da indústria

- **[Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents)** (Anthropic Engineering): a fonte canônica. Tools são *"contratos entre sistemas determinísticos e agentes não-determinísticos"*; a descrição é prompt engineering, com pequenos refinamentos rendendo grandes ganhos de acerto; o retorno deve ser otimizado por **densidade informacional por token**; e o ciclo é *prototipar → avaliar → colaborar*, com o próprio modelo reescrevendo as tools a partir das transcrições de eval.
- **[Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)** (Anthropic): carregar todas as definições e passar intermediários pelo contexto é o gargalo. Expor cada tool como arquivo TypeScript que o agente orquestra via código levou um caso de **~150.000 a ~2.000 tokens (−98,7%)**.
- **[Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)** + **[Advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use)**: descoberta dinâmica. Envie tudo, marque o não-crítico com `defer_loading: true`, e o modelo vê só a busca mais as essenciais. Um setup multi-servidor gasta ~55k tokens de definições antes de trabalhar, e o tool search corta isso em mais de 85%.
- **[Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)**: o modelo escreve Python que chama as tools em sandbox e devolve só o destilado. Cerca de 38% menos tokens de input num benchmark com 75 tools, e 20–40% típico em produção com 10 a 49 tools.
- **[Code Mode](https://blog.cloudflare.com/code-mode-mcp/)** (Cloudflare): a mesma tese, de um fornecedor de infra, com um argumento diferente — o de **distribuição de treino**. LLMs escrevem código contra APIs conhecidas melhor do que preenchem schemas sintéticos. Convergência de indústria, não peculiaridade de um vendor.
- **[Apply Patch](https://developers.openai.com/api/docs/guides/tools-apply-patch)** + **[GPT-5.1 for developers](https://openai.com/index/gpt-5-1-for-developers/)** (OpenAI): tool de edição **treinada no modelo**, no formato V4A de diffs. Explica por que formatos ad-hoc de search/replace perdem para o formato que o modelo viu em treino.
- **Consulte também**: a coleção viva [Awesome Harness Engineering — Tool Design](https://github.com/GHDaru/awesome-harness-engineering#tool-design) reúne mais recursos desta dimensão, curados por problema.

## Na prática: a mesma ferramenta, três vezes

Vamos escrever `buscar_arquivos` três vezes. A cada versão, um problema diferente aparece — e o terceiro é o que separa uma tool que funciona de uma tool que não estoura o contexto.

**Versão 1: o schema à mão.** É como quase todo mundo começa, e é a cena que abriu o capítulo.

```python
SCHEMA = {
    "name": "buscar_arquivos",
    "description": "Busca arquivos",
    "parameters": {
        "type": "object",
        "properties": {"padrao": {"type": "string"}},   # ← fonte da verdade nº 2
        "required": ["padrao"],
    },
}

def buscar_arquivos(glob: str) -> list[str]:            # ← fonte da verdade nº 1
    return [str(p) for p in Path(".").rglob(glob)]
```

Duas declarações do mesmo contrato, em dois lugares, sem nada que as amarre. Renomeie uma e o agente quebra em runtime, com uma mensagem que não ajuda ninguém. E repare na descrição: *"Busca arquivos"* é tudo o que o modelo sabe. Ele não sabe se aceita glob, se é recursivo, se ignora `.gitignore` — então adivinha.

**Versão 2: o schema derivado.** O contrato passa a ter uma fonte só.

```python
@tools.tool
def buscar_arquivos(glob: str) -> list[str]:
    """Busca arquivos por padrão glob, recursivamente, a partir da raiz do
    projeto. Exemplos de padrão: '*.py', 'src/**/*.ts'. Ignora .git/."""
    return [str(p) for p in Path(".").rglob(glob)]
```

O decorator lê a assinatura e a docstring e **produz** o JSON Schema. É o que a etapa 2 do harness-zero implementa, em três chamadas de `inspect`:

```python
def _schema_da_funcao(fn) -> dict:
    sig = inspect.signature(fn)
    props, req = {}, []
    for nome, par in sig.parameters.items():
        props[nome] = {"type": _json_type(par.annotation)}
        if par.default is inspect.Parameter.empty:
            req.append(nome)
    return {
        "name": fn.__name__,
        "description": inspect.getdoc(fn) or fn.__name__,
        "parameters": {"type": "object", "properties": props, "required": req},
    }
```

Renomear `glob` agora muda o schema junto, porque o schema **é** a assinatura. A cena da abertura deixa de ser possível.

E note onde a docstring foi parar: ela virou a descrição que o modelo lê. Isso muda o que se escreve nela. Deixou de ser documentação para quem mantém o código e virou **prompt**: exemplos de padrão, o que a tool ignora, o que ela não faz. Essa é a frase do capítulo — a descrição de uma tool é prompt engineering, e a docstring é onde ela mora.

**Versão 3: o que volta ao modelo não é o que a função devolve.** Aqui está o problema que só aparece em repositório de verdade.

```python
@tools.tool
def buscar_arquivos(glob: str) -> Observacao:
    """Busca arquivos por padrão glob, recursivamente. Ex.: '*.py'."""
    achados = [str(p) for p in Path(".").rglob(glob)]
    return Observacao(
        dado=achados,                                  # completo, para o harness
        para_o_modelo=_resumir(achados),               # recortado, para o contexto
    )

def _resumir(achados: list[str], teto: int = 50) -> str:
    if len(achados) <= teto:
        return "\n".join(achados)
    return (
        "\n".join(achados[:teto])
        + f"\n… e mais {len(achados) - teto} arquivos."
        + "\n(refine o padrão para ver o resto)"
    )
```

Faça a conta com números reais. Um monorepo médio responde `**/*.ts` com cerca de 4.100 caminhos. A 15 tokens por caminho, são **~60.000 tokens** entrando no contexto de uma vez, para uma pergunta que quase sempre se resolve com os primeiros cinquenta. A versão recortada custa **~400**.

O ganho de 150× não é o ponto principal. O ponto é a separação: o harness continua com a lista inteira em `dado`, para paginar, filtrar ou passar a outra tool; o **modelo** recebe o destilado. Duas audiências, dois formatos, um retorno só.

É a tradução, em código, da regra que a Anthropic chama de densidade informacional por token — e é a ideia que o Apêndice A registra sob o nome `to_llm_content` no software-agent-sdk.

## O estado da arte

### 1. O núcleo consensual, e o fim do schema à mão

Os harnesses convergiram num núcleo de cerca de dez tools: ler, escrever e editar arquivo, glob, grep, shell, web fetch e search, todo e delegar. É o kit mínimo de um agente de código.

E ninguém escreve JSON Schema à mão. A fonte da verdade é o sistema de tipos da linguagem, com um decorator ou uma classe fazendo a derivação. O Apêndice A tem o inventário de qual biblioteca cada projeto usa.

O refinamento moderno de qualidade é o da versão 3 acima: **separar o que volta ao contexto do modelo do dado estruturado**. É onde a diferença entre um harness bom e um harness caro aparece primeiro.

### 2. Contexto de tools virou recurso escasso, e há três regimes de escala

O default de despejar todas as definições no system prompt morreu. A escolha hoje é por tamanho de catálogo.

**Catálogo fixo**, na casa das dezenas de tools: ainda é aceitável mandar tudo.

**Tool search com carregamento tardio**, na casa das centenas, típico de quem pluga vários servidores MCP: mantêm-se três a cinco tools quentes e o resto carrega sob demanda.

**Code-as-action**, para pipelines com dados volumosos: o modelo escreve código que orquestra as tools em sandbox e devolve o destilado. É a versão 3 levada ao extremo, com o recorte feito por programa em vez de por função fixa.

A métrica que a indústria passou a reportar não é acurácia isolada. É **acurácia por token de definição**.

### 3. A interface de edição é treinada, não inventada

A lição mais contraintuitiva do capítulo: o melhor formato de edição de código não é o que você desenha, é o que o **modelo viu em treino**.

Daí o `apply_patch` ser tool nativa de um fornecedor, daí um harness dar `apply_patch` a modelos de uma família e `edit`/`write` a outra, e daí um projeto medir empiricamente qual formato cada modelo aplica bem, com uma métrica dedicada a isso.

O corolário desmonta uma intuição comum: a seleção de tools **varia por família de modelo**. Não existe "a melhor interface"; existe a melhor interface para quem está do outro lado.

E o erro de tool volta como **dado**, para o modelo se autocorrigir, nunca como exceção que derruba o loop. Repare que a versão 1 da seção anterior violava isso duas vezes: o erro subia como `TypeError` *e* não dizia o que fazer.

### Leitura executiva

O que está mais moderno: schema derivado de tipos com separação entre dado e contexto; os três regimes de escala escolhidos por tamanho de catálogo; e a interface de edição como algo treinado, não projetado.

**O que roubar:** a separação `dado` × `para_o_modelo`, que é o controle de densidade por token; tool search com carregamento tardio quando o catálogo passar de dezenas; medir o formato de edição por família de modelo em vez de escolher por gosto; e erro-como-dado, sempre.

## Mão na massa — harness-zero, etapa 2

A etapa 2 (`harness-zero/etapas/02-tools/`) substitui os schemas escritos à mão da etapa 1 por uma `ToolPort`: uma tool é uma função tipada, e o schema é derivado das anotações via `inspect`, exatamente como no bloco acima.

Você acrescenta `read_file` ao lado de `get_time` e `somar`, com erros voltando como texto ao modelo. A janela `/tools` mostra os schemas derivados, para você conferir que a assinatura e o contrato são a mesma coisa.

Exercício de completude: o derivador vem esqueletado para tipos simples. Estenda-o para tipos compostos (`list[str]`, `Optional[int]`), sem duplicar o schema em lugar nenhum.

## Verificação

1. Por que a descrição de uma tool é prompt engineering e não documentação de API?
2. Seu agente tem acesso a oito servidores MCP, mais de 200 tools, e gasta 55k tokens antes de agir. Qual regime de escala você adota, e o que fica carregado?
3. Por que dar `apply_patch` a um modelo pode superar um formato search/replace que você desenhou cuidadosamente?
4. Na versão 3 do exemplo, por que a função devolve os dois campos em vez de simplesmente retornar a lista recortada?

---

## Apêndice A — Como cada repositório trata as ferramentas

> Evidência por harness, com paths — complementação online, expandida a cada rodada.

### opencode (rodada 1)
~14 tools + 3 experimentais (`tool/`), Effect Schema, descrições `.txt` separadas; **seleção por modelo** (`registry.ts`: GPT recebe `apply_patch` em vez de `edit`/`write`); ripgrep embutido; experimentais `lsp`, `plan_exit`, `code-mode` (V8).

### gemini-cli (rodada 1)
~20–25 tools como classes declarativas (`BaseDeclarativeTool` + `Invocation`), registro filtrado (`maybeRegister`), declarações por família de modelo; shell com processos em background, web search com grounding, tracker opcional (6 tools).

### OpenHarness (rodada 1)
**43+ tools** (`tools/`, `BaseTool` + `input_model` Pydantic → `to_api_schema()`); `is_read_only()` alimenta o paralelismo do loop; multimodal, cron, times, `tool_search`.

### Codex CLI (rodada 2)
Crate `tools/` com schemas tipados; `unified_exec` (shell persistente com stdin); **`apply_patch` de primeira classe** (parser streaming + gramática `apply_patch.lark`, variando por modelo); `tool_search`/`tool_discovery`; **code-mode com V8 embutido**.

### Goose (rodada 2) ⭐ MCP-nativo
Toda tool é MCP: built-ins de `goose-mcp` são `rmcp::ServerHandler` servidos in-process sobre `DuplexStream`; até developer/shell/edit são "platform extensions" falando `McpClientTrait`.

### OpenClaw (rodada 2)
Suíte ampla (`openclaw-tools*.ts`): runtime/files/web/browser CDP/mídia; **Tool Search** e **Code Mode** (JS/TS sobre catálogo oculto); 52 AgentSkills injetadas como bloco compacto, lidas sob demanda.

### Hermes (rodada 2)
~40+ tools em **toolsets componíveis** com posturas dinâmicas; `execute_code` (Python chamando tools via RPC (Remote Procedure Call), "turnos de custo-zero-contexto"); `schema_sanitizer` por provider.

### Aider (rodada 2) ⭐ edit formats
Em vez de tools JSON, **formatos de edição** (`*_coder.py`): whole/diff (SEARCH-REPLACE fuzzy)/udiff/patch; seleção por modelo; **validados por benchmark** (`percent_cases_well_formed`).

### software-agent-sdk (rodada frameworks) ⭐ dado×contexto
Contrato Action/Observation/Executor; `Observation.to_llm_content` separa o que volta ao modelo do dado estruturado; toolsets (um `create` → várias tools); anotações MCP-style; `ClientToolSpec` (tool executa na máquina do cliente).

### IronClaw (rodada 2)
Tools como **capabilities com descritores tipados** declarando `EffectKind`, credenciais e política de rede; separação visibilidade × autoridade (capability oculta falha fechado); obligations (redação/limites) antes de qualquer efeito.

### n8n (rodada 2)
`create-node-as-tool.ts`: **qualquer nó `usableAsTool` vira tool** via `$fromAI('chave','desc',tipo)` → schema Zod derivado; ToolWorkflow (sub-workflow como tool), ToolHttpRequest, ToolCode, ToolThink.

### Frameworks (rodada frameworks)
Agents SDK (Software Development Kit): `@function_tool` (Pydantic + griffe com auto-detecção de docstring), 13 tipos incl. hosted; LangGraph: herda `@tool` do langchain-core, adiciona `ToolNode` (execução, injeções); CrewAI: `BaseTool`/`@tool` Pydantic, catálogo `crewai-tools` com 79 diretórios.

---

## Respostas da verificação

**1.** Porque quem lê a descrição é o modelo, e é ela que decide **se** e **como** a tool vai ser chamada. Documentação de API é consultada por quem já decidiu usar a função; a descrição de uma tool é o que produz a decisão. Daí as consequências práticas: pequenos refinamentos de redação mudam a taxa de acerto, exemplos de argumento valem mais que prosa formal, e o que a tool *não* faz precisa estar escrito — porque o silêncio vira suposição. Na versão 1 do exemplo, *"Busca arquivos"* fez o modelo adivinhar; na versão 2, a docstring diz o formato do padrão e o que é ignorado.

**2.** **Tool search com carregamento tardio.** Quente fica o mínimo que o agente usa em quase todo turno — a própria ferramenta de busca de tools, mais as três a cinco do núcleo local (ler arquivo, editar, shell) — e as mais de 200 restantes ficam marcadas para carregar sob demanda. O que se está economizando não é dinheiro em abstrato: são 55k tokens que sairiam da janela **antes** do primeiro trabalho útil, e que competem com o código que o agente precisa enxergar. Se além do catálogo grande houver retorno volumoso, o regime seguinte é code-as-action.

**3.** Por distribuição de treino. O modelo viu um determinado formato de diff milhões de vezes durante o treinamento e praticamente nunca viu o seu formato. A qualidade do design importa menos que a familiaridade: um formato pior, mas conhecido, é aplicado corretamente com mais frequência que um formato melhor e inédito. O corolário incomoda e é verdadeiro — a escolha da interface de edição é uma **medição** por família de modelo, não uma decisão de gosto do arquiteto, e é por isso que existe métrica dedicada a ela.

**4.** Porque as duas audiências têm necessidades opostas e o retorno é um só. O **harness** precisa da lista completa: para paginar, para filtrar, para passar a outra ferramenta, para exibir na interface. O **modelo** precisa do mínimo suficiente para decidir o próximo passo, e cada caminho a mais compete por espaço na janela com o código que ele veio ler. Retornar só a lista recortada resolveria o custo e destruiria a informação; retornar só a lista inteira preserva a informação e estoura o contexto. A separação é o que permite otimizar um lado sem perder o outro — e é a razão pela qual esse campo tem nome próprio nos harnesses maduros.
