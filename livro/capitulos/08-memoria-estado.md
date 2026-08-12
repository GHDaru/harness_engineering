# 08 — Memória e Estado

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: completo
>
> Esqueleto v3 — corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Distinguir** as três camadas do problema — estado de sessão, memória de longo prazo e estado do workspace — e o requisito próprio de cada uma;
2. **Explicar** por que memória **não é** RAG (Retrieval-Augmented Generation), e por que markdown versionável venceu bancos vetoriais no domínio de código;
3. **Derivar** uma política de recall a partir da fórmula recência × importância × relevância, e uma de esquecimento a partir do uso;
4. **Avaliar** o impacto da **reversibilidade** sobre o cálculo de risco de permissões;
5. **Implementar** a persistência de sessão do harness-zero (adapter SQLite mais `/resume`) na etapa 4.

## Quarenta minutos, nove arquivos, e o terminal que fechou

O agente trabalhou quarenta minutos. Editou nove arquivos, rodou a suíte três vezes, descobriu que o bug estava em dois lugares e consertou os dois. Você foi tomar café.

Quando voltou, o terminal tinha fechado. Atualização do sistema, sessão SSH caída, tanto faz.

Você roda `--resume`. E funciona: a conversa volta inteira, com as tool calls, os resultados, o raciocínio. Alívio.

Então você roda `git status`.

```
modified:   auth.py
modified:   session.py
modified:   tests/test_login.py
Untracked:  auth.py.orig
```

Três arquivos modificados **no meio da edição**, e nenhuma pista de qual era o estado bom. A conversa foi restaurada; o **workspace** não. E o pior: a conversa restaurada diz que o trabalho terminou, porque do ponto de vista dela terminou mesmo.

Repare que duas coisas diferentes precisavam sobreviver ao mesmo acidente, e só uma sobreviveu. É isso que este capítulo separa: **estado de sessão** e **estado de workspace** são dois problemas, com dois donos e duas trilhas de reversão.

## O problema

O modelo esquece tudo entre chamadas; o harness lembra por ele.

"Memória e estado" cobre três camadas com requisitos diferentes.

**Estado de sessão** é a conversa em si: mensagens, tool-calls, metadados. Precisa sobreviver a reinícios e permitir retomar, ramificar e reverter.

**Memória de longo prazo** são fatos que atravessam sessões: preferências do usuário, decisões do projeto, aprendizados. Precisa ser **selecionável**, porque nem tudo entra em todo contexto, e **atualizável**, porque fatos mudam.

**Estado do workspace** é o que o agente *fez* nos arquivos. Precisa ser **reversível**: desfazer as mudanças de um agente é tão importante quanto fazê-las. É a camada que faltou na cena da abertura.

A tese que unifica as três: a janela de contexto é memória volátil e cara, tudo o que precisa durar vive **fora** dela, e o harness decide o que trazer de volta e quando.

## Fundamentos científicos

A memória de agentes tem literatura madura, e ela dá o vocabulário exato para o que os harnesses fazem na prática.

- **A janela como RAM**. [MemGPT: LLMs as Operating Systems, arXiv 2310.08560](https://arxiv.org/abs/2310.08560) trata o contexto como memória principal escassa, apoiada por dois níveis externos (*recall* de histórico recente e *archival* pesquisável), com o **agente** paginando dados via tool calls. Quem decide o que despejar e o que buscar é o agente, não um pipeline fixo.
- **A taxonomia canônica**. [CoALA, arXiv 2309.02427](https://arxiv.org/abs/2309.02427) separa memória **episódica** (experiência passada), **semântica** (conhecimento do mundo ou do usuário) e **procedural** (habilidades e código), mais a working memory. No momento da escrita, decida *que tipo* de memória aquele fato é, porque cada tipo se recupera diferente. O [survey de mecanismos de memória, arXiv 2404.13501](https://arxiv.org/abs/2404.13501) organiza o subsistema por fontes, formas e operações — orce esforço por operação, não só pelo índice de busca.
- **A fórmula de recall**. [Generative Agents, arXiv 2304.03442](https://arxiv.org/abs/2304.03442) guarda observações num *memory stream* datado e recupera por um score composto de **recência × importância × relevância**, com decaimento exponencial de recência, importância pontuada por LLM (Large Language Model) e relevância por embedding. É a fórmula concreta que um harness deve implementar, e ela introduz a **consolidação por reflexão**: sintetizar reflexões de alto nível a partir de aglomerados de observações.
- **Esquecimento controlado**. [MemoryBank, arXiv 2305.10250](https://arxiv.org/abs/2305.10250) decai ou reforça a força de cada memória por uma curva de Ebbinghaus, cruzando tempo decorrido com frequência de acesso. Memória não usada é candidata a poda, e o rastreamento de uso é o que fecha o ciclo.
- **Memória como aprendizado**. [Reflexion, arXiv 2303.11366](https://arxiv.org/abs/2303.11366) converte feedback de resultado em auto-reflexão verbal, persistida num buffer episódico e reinjetada na próxima tentativa: melhorar sem atualizar pesos. Arquiteturas recentes ([A-MEM, arXiv 2502.12110](https://arxiv.org/abs/2502.12110); [Mem0, arXiv 2504.19413](https://arxiv.org/abs/2504.19413)) tratam a escrita como pipeline de extrair, consolidar e ligar, com a rede de memórias se auto-organizando. É a ponte para o cap. 16.

(Bibliografia completa e ponteiros: `livro/bibliografia.md`.)

## Fontes da indústria

- **Sessão como log de eventos durável**. [Manage sessions](https://code.claude.com/docs/en/sessions): cada sessão é gravada continuamente em disco como **JSONL** por projeto, uma linha por mensagem, tool-use ou metadado. "Retomar" é **restaurar estado completo** — tool calls, resultados, modo de permissão, objetivo ativo — e não replay de texto. O harness é dono de um log durável privado, não de um schema público estável.
- **Reversão do workspace como trilha separada**. [Checkpointing](https://code.claude.com/docs/en/checkpointing) captura o estado do código antes de cada prompt, e `/rewind` restaura código, conversa **ou** ambos. O [file-checkpointing do Agent SDK](https://platform.claude.com/docs/en/agent-sdk/file-checkpointing) expõe isso como primitiva reusável. Desfazer o *código* é um store separado de desfazer a *conversa*, ligados pelo índice do prompt. É a resposta direta à cena da abertura.
- **Memória durável como arquivos com precedência**. [How Claude remembers your project](https://code.claude.com/docs/en/memory): hierarquia de arquivos markdown com precedência declarada, atalho `#` para anexar uma linha de memória, e `/memory` para editar. Memória cross-sessão é **markdown em camadas de precedência**, versionável, auditável e escopada, relida no início como contexto sempre ligado.
- **A memory tool e o "assuma interrupção"**. [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool): o modelo pede operações (`view`, `create`, `str_replace`) num diretório `/memories` que persiste entre conversas, mas a execução é **do lado do cliente** — o seu app implementa o armazenamento, e com ele a proteção contra travessia de caminho, os limites de tamanho e a expiração. O sistema injeta a instrução de assumir que a janela pode ser resetada a qualquer momento. Pareada com o [context management](https://www.anthropic.com/news/context-management), dá dois níveis: higiene de curto prazo dentro da janela e store externo de longo prazo fora dela. O padrão do ensaio sobre [harnesses de longa duração](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) é o mesmo: log de progresso estruturado, lido no início e atualizado no fim de cada sessão.
- **Memória não é RAG**. a distinção virou tese de indústria. RAG é leitura *sem estado*; memória é leitura **mais caminho de escrita mais gestão de estado**: admissão, resolução de fatos conflitantes, invalidação. Produtos expõem blocos auto-editáveis com camadas core, recall e archival; roteiam cada fato por camada com tempo de vida próprio; modelam memória como **grafo bi-temporal**, em que fato desatualizado é *invalidado* e não deletado; e separam curto prazo por thread de longo prazo por namespace ([AWS Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/memory-ltm-rag.html); [mem0](https://docs.mem0.ai/core-concepts/memory-types)). Não dá para "comprar" memória pregando um banco vetorial: é preciso um pipeline de escrita, atualização e invalidação.
- **Consulte também**: a coleção viva [Awesome Harness Engineering — Memory & State](https://github.com/GHDaru/awesome-harness-engineering#memory--state) reúne mais recursos desta dimensão, curados por problema.

## Na prática: a porta que separa o efêmero do durável

O harness-zero até aqui guarda a conversa numa lista em memória. Fechou o processo, acabou. A etapa 4 introduz a terceira porta do livro, e ela tem três métodos:

```python
class StorePort(Protocol):
    def append(self, session_id: str, msg: Message) -> None: ...
    def history(self, session_id: str) -> list[Message]: ...
    def sessions(self) -> list[dict]: ...
```

Repare no que **não** está aqui. Não há `salvar_tudo()`, não há `flush()`, não há transação explícita. O contrato é **append-only**: cada mensagem é gravada quando acontece, e o histórico é derivado da leitura. Essa escolha é o capítulo inteiro em três linhas — o durável é um log, e o estado é uma **projeção** dele.

O adapter em memória serve de contraste, e existe para o leitor ver a porta funcionando antes de acreditar nela:

```python
class StoreEmMemoria:
    def __init__(self) -> None:
        self._por_sessao: dict[str, list[Message]] = {}

    def append(self, session_id, msg):
        self._por_sessao.setdefault(session_id, []).append(msg)

    def history(self, session_id):
        return list(self._por_sessao.get(session_id, []))
```

Correto, rápido e inútil para o problema da abertura. Trocar por SQLite não muda nenhuma linha do loop:

```python
class StoreSQLite:
    def __init__(self, caminho="sessoes.db"):
        self._db = sqlite3.connect(caminho, check_same_thread=False)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS mensagens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                papel      TEXT NOT NULL,
                conteudo   TEXT NOT NULL,
                criado_em  TEXT NOT NULL DEFAULT (datetime('now'))
            )""")
        self._db.execute("CREATE INDEX IF NOT EXISTS ix_sessao ON mensagens(session_id, id)")

    def append(self, session_id, msg):
        self._db.execute(
            "INSERT INTO mensagens (session_id, papel, conteudo) VALUES (?,?,?)",
            (session_id, msg.papel, json.dumps(msg.conteudo)))
        self._db.commit()          # commit por mensagem: durabilidade > throughput
```

O `commit()` por mensagem é a decisão que a cena da abertura justifica. Ele é lento em benchmark e certo em incidente: o que estiver gravado **está** gravado quando a energia cai.

E agora a parte que fecha a cena. Persistir a conversa **não** persiste o workspace, e a segunda trilha é de outra natureza:

```python
def checkpoint(projeto: Path, rotulo: str) -> str:
    """Snapshot do workspace antes de cada turno, fora do histórico do git do usuário."""
    subprocess.run(["git", "add", "-A"], cwd=projeto, check=True)
    sha = subprocess.run(["git", "stash", "create"], cwd=projeto,
                         capture_output=True, text=True).stdout.strip()
    if sha:                                     # vazio quando nada mudou
        subprocess.run(["git", "update-ref", f"refs/harness/{rotulo}", sha], cwd=projeto)
    return sha
```

Três detalhes valem a leitura. O `stash create` **não** mexe no índice nem no working tree do usuário: ele só produz um objeto. O `update-ref` guarda esse objeto sob `refs/harness/`, fora de `refs/heads/`, então nenhum `git log` ou `git branch` do usuário fica poluído. E o retorno vazio quando nada mudou evita criar checkpoint de turno que só conversou.

Duas trilhas, dois stores, um índice em comum — o número do turno. É isso que permite `/rewind` restaurar **código, conversa ou ambos**, que é a primitiva que o estado da arte consolidou.

## O estado da arte

### 1. Três camadas, três campeões, e nenhum banco vetorial

As três camadas receberam campeões diferentes na coorte. **Estado de sessão** foi resolvido com durabilidade de banco: eventos replayáveis, rollout por turno, event-stream. **Memória de longo prazo** foi resolvida com relevância e rigor de formato: diretório de memória versionado, com módulos separados para relevância e uso. **Estado de workspace** foi resolvido com git.

E o achado que persiste: **nenhum dos harnesses de código usa banco vetorial** para memória.

No domínio de código, markdown versionável venceu embeddings. O motivo é exatamente o que a tese "memória não é RAG" prevê: memória de código precisa de *caminho de escrita*, porque o agente edita o arquivo, e de auditabilidade, porque alguém vai querer saber por que ele acredita naquilo.

### 2. A fórmula de recall e o esquecimento saíram do paper para o código

Um harness do corpus tem os dois lados implementados em arquivos separados: um seleciona por relevância o que entra no contexto, o outro marca uso, e memória não usada vira candidata a poda. É a curva de esquecimento na prática.

Outro formaliza a **manutenção ativa**: uma única tool edita os arquivos de memória, com lembretes periódicos a cada dez turnos, e uma busca textual sobre o banco de sessões dá **recall entre sessões**. É a camada archival do MemGPT construída sobre busca textual, não vetorial.

### 3. Reversibilidade virou primitiva, e muda o cálculo de risco

O checkpoint de workspace deixou de ser feature e virou primitiva. Um harness foi pioneiro anos atrás, com estado git-nativo e commit atômico por rodada; outro consagrou o comando de restauração por snapshot; e o mais maduro do corpus expõe trilhas separadas para código e conversa, como no exemplo acima.

A consequência de projeto é a mais interessante do capítulo: **um agente cujas ações são reversíveis muda o cálculo de risco de tudo o mais**. Permissões podem ser mais frouxas quando desfazer é barato, o que liga esta dimensão diretamente ao cap. 07.

### 4. Providers plugáveis, e o harness como servidor de memória

A fronteira emergente é memória como serviço plugável, com harnesses aceitando provedores externos por trás da própria camada e produtos se posicionando como camada universal consumível por qualquer harness.

A tensão de projeto para as próximas rodadas: manter a memória como **arquivo local versionável**, auditável e portável, ou terceirizá-la para um store gerenciado, com grafo bi-temporal e escala. No código, o arquivo ainda vence; fora dele, o pêndulo é menos claro.

### Leitura executiva

O que está mais moderno: a moldura de camadas de sistema operacional, com o agente paginando entre janela, recall e archival; recall por recência, importância e relevância, com esquecimento por uso; reversão de workspace como primitiva que afrouxa permissões; e a distinção dura entre memória e RAG.

**O que roubar:**

- **Persista a sessão como log append-only**, e derive o estado da leitura. Retomar é restaurar estado, não repetir texto.
- **Trate memória como markdown versionável** com rastreamento de uso.
- **Separe a trilha de reversão do código da trilha da conversa**, ligadas pelo índice do turno.
- **Guarde o checkpoint fora de `refs/heads/`**, para não poluir o histórico de quem usa o repositório.
- **Para agentes longos, escreva um log de progresso durável** assumindo que a janela some a qualquer momento.

## Mão na massa — harness-zero, etapa 4

A etapa 4 (`harness-zero/etapas/04-sessoes/`) dá persistência ao harness-zero: o `StorePort` do exemplo acima, com adapter SQLite guardando mensagens e tool-calls como linhas tipadas, e `/resume` restaurando o estado completo de uma sessão anterior.

É fiel ao hexagonal *por refatoração*: a dor que faz a porta nascer é reabrir o processo e perder a conversa, e ela só nasce depois de doer.

Exercício de completude: a persistência cobre o caminho feliz. Você acrescenta um arquivo de memória mínimo, lido no início, e um log de progresso atualizado no fim — o padrão "assuma interrupção" na forma mais simples.

## Verificação

1. Por que memória de agente não é a mesma coisa que RAG, e o que isso explica sobre a escolha de markdown versionável em vez de banco vetorial nos harnesses de código?
2. Você tem 10.000 memórias e espaço para 20 no contexto. Que score usa para escolher, e como decide o que podar com o tempo?
3. Seu agente ganhou checkpoint de workspace. Que decisão *de outra dimensão* isso permite afrouxar, e por quê?
4. No exemplo, por que o checkpoint é guardado em `refs/harness/` e não como um commit numa branch?

---

## Apêndice A — Como cada repositório trata memória e estado

> Evidência por harness, com paths — complementação online, expandida a cada rodada.

### opencode (rodada 1) — estado como banco de dados
Persistência em **SQLite via Drizzle** (`packages/core/database`, `core/session/sql.ts`): sessões, mensagens e partes são linhas tipadas. Sessões têm `parentID` (hierarquia para subagentes), suportam revert (`session/revert.ts`) e **compartilhamento** (`share/`, `sync/`). A V2 (`CONTEXT.md`) leva o desenho a "infra de dados": inbox durável de prompts, eventos replayáveis com cursores (`sessions.events({sessionID, after})`), snapshots de contexto persistidos entre reinícios. O modelo de estado mais robusto da rodada 1 — o harness como sistema distribuído com estado durável.

### gemini-cli (rodada 1) — o workspace reversível
Memória de longo prazo nos próprios `GEMINI.md` (tool `save_memory`, global em `~/.gemini` + índice de projeto, com auto-memory testada em evals). O recurso distintivo é o **checkpointing baseado em git** (`services/gitService.ts` + `chatRecordingService.ts`): snapshots do workspace antes de edições, habilitando `/restore` e `/rewind` — desfazer as mudanças do agente no disco, não só na conversa — além de `/resume`.

### OpenHarness (rodada 1) — memória como arquivo, com disciplina
`src/openharness/memory/` (13 módulos): memória persistente em markdown (`MEMORY.md`/memdir por projeto) com **schema versionado, escrita atômica com file-lock e assinaturas**. `relevance.py` seleciona o que entra no contexto; `usage.py` marca uso (memória não usada é candidata a poda). Sessões persistidas com metadados ricos (`services/session_storage.py`): modo de permissão, estado de arquivos lidos, skills invocadas, checkpoints de compactação. Retomada via `-c/--continue`, `-r/--resume`, `/resume`.

### Aider (rodada 2) ⭐ estado git-nativo — o pioneiro da reversão
`aider/repo.py`: **auto-commit atômico por rodada** com mensagem gerada por LLM, atribuição de autoria configurável, `aider_commit_hashes` rastreando o que a IA fez, `dirty_commit` isolando mudanças pendentes. `/undo`, `diff` e `blame` viram a interface de memória; complementos `.aider.chat.history.md` e `--restore-chat-history`. **Antecipou em anos** o "checkpoint git" que o gemini-cli e o Claude Code consagraram.

### Hermes (rodada 2) ⭐ memória multicamada com recall cross-session
`MEMORY.md` (notas do agente) + `USER.md` (perfil do usuário) editados por tool única com **nudges periódicos** (a cada 10 turnos); provedores externos plugáveis (**Honcho, mem0, supermemory**); e **`session_search`** — índice FTS5 sobre o SQLite de sessões com três modos (discovery/BM25, recall janelado, sumarização por LLM) para recall cross-session. A camada archival do MemGPT sobre busca textual.

### Codex CLI (rodada 2) — rollout jsonl por turno
Cada turno é persistido em **rollout jsonl** (recuperável); `SessionTask` (Regular/Review/Compact/UserShell) organiza a máquina de tarefas. Estado de sessão durável e resumível integrado ao loop (`core/src/session/`).

### OpenHands (rodada 2) — event-stream persistido
`openhands/app_server/event/` persiste cada `Event` como JSON por conversa, com paginação, filtros e export de trajetória. O control-plane consome/persiste eventos; o loop ação-observação roda no SDK. Event-sourcing como coluna vertebral do estado.

### OpenClaw (rodada 2) — session lanes e arquivos de workspace
Runs serializados por *session lane* com write-lock file-based entre processos; arquivos de workspace (`MEMORY.md`, `USER.md`, `IDENTITY.md`…) injetados com orçamentos (20k chars/arquivo, 60k total) e truncamento marcado. Persistência de conversa por canal.

### ohmo (rodada 2) — backends de sessão/memória como plugins
Implementa `SessionBackend` e `MemoryCommandBackend` do OpenHarness como plugins de primeira classe (sem tocar no core), mais um **pool multi-sessão** (`RuntimeBundle` por `session_key`, recriado quando o cwd muda). Prova de que a fronteira app/engine foi desenhada.

### IronClaw (rodada 2) — estado resumível por checkpoints
Estado resumível por **checkpoints**; máquina de estados Queued→Running→Blocked→Completed com **leases/heartbeats** e "one active run per canonical thread". O `LoopExit` carrega apenas referências duráveis — o loop nunca muta estado; o `LoopExitApplier` valida evidência host-owned antes de aplicar.

### n8n (rodada 2) — memória do motor de workflow
Memória via *memory sub-nodes* (janela `contextWindowLength`, corte `maxTokensFromMemory`); estado do workflow persistido pelo motor entre execuções. Curto por natureza — execuções acionadas por evento não acumulam contexto longo (compactação nota 1, por design).

### Frameworks (rodada frameworks)
LangGraph: **checkpointer** (short-term, thread-scoped) + **store** por namespace (long-term cross-thread); LangMem: memórias semântica/episódica/procedural como tools; Agents SDK e CrewAI: estado de sessão/curto-prazo com hooks de persistência. A distinção short × long term é primitiva de framework — o que os harnesses de código implementam à mão, os frameworks expõem como API.

---

## Respostas da verificação

**1.** Porque RAG é **leitura sem estado**: uma consulta recupera trechos e os injeta no contexto, e nada do que o agente conclui volta para o índice. Memória é leitura **mais caminho de escrita mais gestão de estado** — admissão do que merece ser lembrado, resolução de fatos que se contradizem, e invalidação do que deixou de ser verdade. No domínio de código isso explica a escolha do markdown versionável: o agente **edita** o arquivo de memória, o diff mostra o que ele passou a acreditar e quando, e o `git blame` responde por quê. Um banco vetorial dá recuperação e não dá nenhuma das três: escrever nele é reindexar, e ninguém consegue auditar o que mudou.

**2.** O score é **recência × importância × relevância**: recência com decaimento exponencial, importância pontuada uma vez na escrita, relevância calculada contra a tarefa atual. As três são necessárias porque cada uma sozinha falha de um jeito conhecido — só recência esquece o que é permanente, só importância traz sempre as mesmas vinte, só relevância traz o que casa por palavra e não por utilidade. A poda é por **falta de uso**, não por idade: registre acesso, deixe a força decair com o tempo e reforce a cada leitura. Uma memória antiga e consultada toda semana é mais valiosa que uma recente que ninguém abriu, e a curva de esquecimento é exatamente o que codifica isso.

**3.** Permite afrouxar **permissões** (cap. 07). O custo de uma decisão errada é o produto de duas coisas: a probabilidade de acontecer e o custo de reverter. Quando reverter passa a ser um comando, a segunda cai perto de zero para toda a classe de ações que mexem só em arquivos do projeto, e insistir em aprovação humana para cada uma delas gasta atenção onde não há mais risco proporcional. A ressalva que impede a leitura preguiçosa: isso vale **só** para efeitos que o checkpoint alcança. Rede, banco de dados de produção, e-mail enviado e chave publicada não voltam com `/rewind`, e para esses o cálculo não mudou nada.

**4.** Por três motivos, e o terceiro é o que decide. Primeiro, **não poluir**: refs sob `refs/heads/` aparecem em `git branch`, em `git log --all` e no autocompletar, e o usuário passaria a conviver com dezenas de branches que não são dele. Segundo, **não interferir**: `stash create` produz o objeto sem tocar no índice nem no working tree, então o agente pode tirar um snapshot no meio de um `rebase` do usuário sem estragá-lo. Terceiro, e decisivo: `refs/harness/` é um **namespace do harness**, o que torna a limpeza trivial e sem risco — apagar a referência de tudo que está sob ele nunca apaga trabalho de ninguém. Guardar estado de ferramenta no namespace do usuário é a mesma classe de erro que gravar cache dentro do diretório de código-fonte.
