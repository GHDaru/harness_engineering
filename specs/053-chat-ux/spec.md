# Spec 053: Chat companion — repaginação de usabilidade (UX)

**Feature Branch**: `053-chat-ux` · **Criada em**: 2026-07-29 · **Gate humano**: 3 padrões de tela (A flutuante ampliado · B dock lateral · C bastidores) apresentados e **aprovados como 3 estados do mesmo design**.

## Cenários de usuário

1. O leitor estuda um capítulo com o chat **ancorado como sidebar direita**, livro e conversa lado a lado; pode **maximizar** para respostas longas e voltar ao flutuante quando quiser — a escolha persiste entre páginas.
2. O leitor digita `/` e vê a **paleta de comandos** com descrição; nunca mais precisa "saber de cor" que `/sugerir` e `/chave` existem.
3. O leitor passa o mouse num chip de capacidade e entende **o que ela faz e quando libera** (🔒 + "libera no cap. X" nos bloqueados).
4. O leitor abre os **Bastidores** e vê o harness funcionando: tokens estimados, chamadas, tools, os trechos do livro injetados no turno e a memória da sessão — o livro se demonstrando.

## Requisitos funcionais

### Widget — layout (estados A/B)
- FR-001: painel flutuante ampliado (~480px × 78vh, máx. responsivo) como default; **3 estados persistidos** em `localStorage` (`cmp_dock`: `float` | `dock` | `max`): dock = sidebar direita de altura total (~430px) que **empurra o conteúdo** (padding no `html`, com transição); max = dock alargado (~640px). Botões no cabeçalho; mobile (≤820px): dock vira overlay de tela cheia.
- FR-002: entrada de mensagem como **textarea de 3 linhas** com auto-crescimento (até ~10), linha de dicas ("Enter envia · Shift+Enter quebra linha · / comandos") e botão **Enviar** rotulado.

### Widget — explicabilidade
- FR-003: chips de capacidade com **tooltip no hover/tap**: descrição + status ("✓ liberado no cap. X" / "🔒 libera no cap. X"). Fonte da verdade: `GET /capabilities` (que já devolve `descricao` e `libera_no_capitulo`), buscado ao abrir e cacheado; fallback ao espelho local se offline.
- FR-004: **paleta de `/`**: digitar `/` no início abre menu filtrado por prefixo (↑↓ navega, Enter aplica, Esc fecha) com `/sugerir`, `/chave`, `/chave limpar`, `/limpar`, `/bastidores` — cada um com descrição de uma linha. `/limpar` executa a limpeza existente (com confirmação).

### Bastidores (estado C)
- FR-005: **barra de status** no rodapé do chat: `🧠 ~tokens · 🔁 chamadas · 📎 trechos injetados` (valores do último turno + contadores da sessão); clique (ou `/bastidores`) abre/fecha o painel.
- FR-006: painel **Bastidores** acoplado (à esquerda do chat; overlay no flutuante/mobile) com blocos: **Janela de contexto** (tokens estimados/limite com barra, mensagens no histórico, chamadas, tools executadas), **Injetado neste turno** (capacidades ativas, modo, trechos RAG com fonte e preview), **Memória da sessão** (id abreviado, persistência, status BYOK). Aba **Documentos**: downloads do capítulo atual (.md/.pdf) + fontes dos trechos citados.
- FR-007 (backend): `/chat` e o evento `done` do `/chat/stream` ganham o bloco **`debug`**: `{trechos: [{fonte, titulo, preview}], historico_msgs, prompt_chars, tokens_estimados (~chars/4), tools_executadas, capacidades_ativas, janela_tokens}` — dados que o backend já computa e descartava. `janela_tokens` vem de config (`CONTEXT_WINDOW_TOKENS`, default 32000). Tokens sempre exibidos com "~" (estimativa honesta).

## Requisitos não-funcionais
- NFR-001: zero dependências novas no widget (JS puro); theme-aware pelas variáveis existentes; nenhum dado novo persistido no servidor (privacidade inalterada; BYOK continua só no navegador).
- NFR-002: compatibilidade — backend antigo sem `debug` → bastidores mostram "sem dados deste turno" e o resto funciona; widget antigo contra backend novo ignora `debug`.

## Verificação
- Suíte do backend (novo teste: `debug` presente e coerente no `/chat` e no `done` do stream).
- E2E Playwright contra uvicorn echo: os 3 estados alternam e persistem; paleta de `/` filtra e aplica; tooltip aparece; bastidores abrem com dados reais do turno; input auto-cresce.
- Screenshots dos 3 estados nos 2 temas.
