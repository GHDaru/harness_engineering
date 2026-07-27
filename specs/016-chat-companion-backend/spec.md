# Feature Specification: Chat-companion — backend (harness-zero ao vivo)

**Feature Branch**: `016-chat-companion-backend`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O livro terá um **chat-companion** que ajuda o leitor desde a capa. Esta feature é o **backend**: um serviço FastAPI (o harness-zero rodando ao vivo) hospedado no **Railway**, com persistência em **Postgres (Neon)**, que atende o widget do site. O widget (front-end) é uma feature posterior. Decisões já tomadas com o autor: (a) natureza = tutor + harness-zero ao vivo, faseado; (b) tools seguras/sandbox (sem shell/fs real público); (c) chave do projeto (NVIDIA NIM) + limites + opção BYOK; (d) identidade anônima por navegador + histórico persistido; (e) o chat aparece desde a capa e exibe claramente as capacidades disponíveis **naquele capítulo**.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor conversa com o companion e vê o que ele pode fazer agora (Priority: P1)

Do site (qualquer página, inclusive a capa), o widget envia mensagens ao backend com o **contexto do capítulo atual** e o **modo** (avançado ou progressivo). O backend responde como **tutor** do livro e informa **quais capacidades estão ativas** naquele ponto. A conversa é **persistida** por uma identidade **anônima de navegador**, então o leitor retoma de onde parou.

**Why this priority**: É o núcleo — sem o backend, o widget não existe. Entregue sozinho (testável por HTTP), habilita todo o resto.

**Independent Test**: `POST /chat` com `{session_id, message, chapter, mode}` retorna resposta + capacidades ativas; `GET /history?session_id=…` devolve o histórico; `GET /capabilities?chapter=NN&mode=progressive` devolve o mapa de capacidades com ativas/bloqueadas.

**Acceptance Scenarios**:

1. **Given** o backend no ar, **When** envio `POST /chat` com uma pergunta e `chapter=1, mode=progressive`, **Then** recebo uma resposta de tutor e a lista de capacidades ativas naquele capítulo (só as liberadas até o cap. 1).
2. **Given** `mode=avancado`, **When** envio a mesma pergunta, **Then** todas as capacidades ficam disponíveis (gating desligado).
3. **Given** uma sessão anônima com histórico, **When** chamo `GET /history?session_id=…`, **Then** recebo as mensagens anteriores em ordem.
4. **Given** ausência de `DATABASE_URL`, **When** o backend sobe, **Then** ele funciona com um store em memória (dev), sem quebrar — a persistência real ativa quando a `DATABASE_URL` (Neon) está presente.
5. **Given** o gating progressivo, **When** o capítulo atual é anterior ao que libera uma tool, **Then** aquela tool **não** é oferecida ao modelo (nem executável).

### Edge Cases

- **Sem chave de LLM** (`LLM_ADAPTER=echo`): o backend responde em modo echo (sem rede) — útil para provar o fluxo e para testes.
- **Rate limit** excedido: `POST /chat` retorna 429 com mensagem clara; **BYOK** (chave do próprio leitor) contorna o limite do projeto.
- **CORS**: só as origens permitidas (site publicado + localhost) podem chamar.
- **Tools perigosas**: leitura de arquivo/shell **não existem** na superfície pública (sandbox); só tools seguras são registradas.
- **Identidade anônima**: nenhum dado pessoal exigido; a identidade é um id gerado pelo navegador; há como **apagar** a sessão (LGPD).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O backend DEVE expor `POST /chat` que recebe `{session_id, message, chapter, mode, byok_key?}` e retorna `{reply, trace, capabilities_ativas, mode, chapter}`.
- **FR-002**: O backend DEVE expor `GET /capabilities` (opcional `?chapter=NN&mode=…`) retornando o **mapa de capacidades** por capítulo/etapa, com rótulo, descrição e estado (ativa/bloqueada) — a fonte autoritativa que o widget exibe.
- **FR-003**: O backend DEVE **persistir** sessões e mensagens quando `DATABASE_URL` (Neon Postgres) estiver configurada; sem ela, usa um **store em memória** (fallback de dev) sem quebrar. As tabelas são criadas automaticamente na subida.
- **FR-004**: A identidade é **anônima por navegador** (`session_id` fornecido pelo cliente); `GET /history?session_id=…` retorna o histórico; `DELETE /session/{session_id}` apaga a sessão (direito ao esquecimento).
- **FR-005**: O **gating de capacidades** DEVE ter dois modos: `avancado` (tudo liberado) e `progressivo` (só o que é liberado até o `chapter` atual). Tools cuja capacidade está bloqueada **não** são oferecidas ao modelo nem executadas.
- **FR-006**: O acesso ao LLM DEVE passar por uma **porta** (`LLMPort`) com adapters (`echo` sem rede; `openai` OpenAI-compatible → NVIDIA NIM). A **chave do projeto** vive só em variável de ambiente; **BYOK** permite o leitor usar a própria chave por requisição.
- **FR-007**: DEVE haver **rate limit** por sessão/IP (configurável por env); excedê-lo retorna 429; BYOK isenta do limite do projeto.
- **FR-008**: As **tools** públicas DEVEM ser apenas **seguras/sandbox** (ex.: hora atual, busca no texto do livro, cálculo aritmético seguro). Sem shell, sem leitura arbitrária de disco, sem rede de saída não controlada.
- **FR-009**: DEVE haver `GET /health` para o healthcheck do Railway.
- **FR-010**: **CORS** restrito às origens permitidas (site publicado + localhost), configurável por env.
- **FR-011**: Nenhum segredo em código/commit (Princípio V); toda credencial só em env; `.env` gitignored; `.env.example` documenta as variáveis.
- **FR-012**: DEVE haver artefatos de deploy (Railway) e instruções passo-a-passo (Neon + Railway) no README do backend.
- **FR-013**: Sem identificador interno de modelo em qualquer artefato publicado (política de identidade).

### Key Entities

- **Sessão**: identidade anônima de navegador (`session_id`), com timestamps; agrega mensagens.
- **Mensagem**: `{role, content, ts}` ligada a uma sessão (papéis: user/assistant/tool).
- **Capacidade**: unidade de funcionalidade com `chave`, `rótulo`, `descrição`, `libera_no_capitulo`, e (quando aplicável) as tools que habilita.
- **LLMPort / StorePort / ToolPort**: portas (hexagonal) com adapters plugáveis.

## Success Criteria *(mandatory)*

- **SC-001**: `POST /chat` responde com reply + capacidades ativas coerentes com `chapter`/`mode`.
- **SC-002**: Com `mode=progressivo`, uma tool de capítulo futuro não aparece nas capacidades ativas nem é executada.
- **SC-003**: Com `DATABASE_URL` ausente, o serviço sobe e conversa (memória); com ela presente, o histórico sobrevive a reinício.
- **SC-004**: `GET /capabilities` retorna o mapa completo com estados corretos para um dado `chapter`/`mode`.
- **SC-005**: Rate limit dispara 429 ao exceder; BYOK contorna.
- **SC-006**: Suíte local (adapter `echo`, store memória) passa sem rede e sem banco.
- **SC-007**: README permite subir Neon + Railway seguindo os passos; zero segredo no repositório; zero identificador interno de modelo.

## Assumptions

- **Banco**: **Neon Postgres** (`DATABASE_URL`), decisão do autor.
- **Host**: **Railway** (o autor sobe o deploy; o backend fornece os arquivos e instruções).
- **LLM**: NVIDIA NIM (endpoint gratuito OpenAI-compatible), reutilizando o adapter do harness-zero.
- Esta feature entrega **só o backend** (testável por HTTP); o **widget** é a feature 017.
- O backend é o **harness-zero em produção**: reusa `LLMPort`/loop e antecipa `StorePort`/`ToolPort` (que as etapas didáticas 02/04 formalizarão depois) — a trilha de ensino e a instância de produção convivem, documentado no plano.
- Feature toca o motor/infra → ciclo spec-kit (Princípio VII).
