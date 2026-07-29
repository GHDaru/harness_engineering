# Plan — 053 chat-ux

## Arquitetura da mudança

Conteúdo ⟂ apresentação preservado: tudo é widget (`publicar/tema/companion.{js,css}`) + um acréscimo aditivo no backend (`debug` no payload). Nenhuma mudança no motor do livro.

## Backend (1 arquivo + config + teste)
1. `config.py`: `CONTEXT_WINDOW_TOKENS` (default 32000).
2. `app.py`: `_preparar_chat` passa a devolver também `achados`; helper `_debug(achados, history, trace, chapter, mode)` monta o bloco; incluído no retorno do `/chat` e no evento `done` do `/chat/stream`.
3. `tests/test_smoke.py`: asserts do bloco `debug` nos dois endpoints.

## Widget — ordem de implementação
4. **Layout/estados**: CSS dos 3 estados via `data-dock` no root (`float`/`dock`/`max`); JS: botões no cabeçalho (ancorar ◧ / flutuar ❐ / maximizar ⤢ / minimizar –), persistência `cmp_dock`, padding no `html` com transição; media query mobile (dock→fullscreen).
5. **Entrada**: textarea 3 linhas (auto-grow até 10), linha de dicas, botão "Enviar".
6. **Tooltips**: fetch `/capabilities` no open (cache por capítulo/modo); chips com 🔒 e tooltip custom (hover + tap; um por vez; Esc fecha).
7. **Paleta `/`**: lista estática de comandos {nome, descricao, acao}; render acima da entrada; filtro por prefixo; teclado ↑↓/Enter/Esc; ações reusam handlers existentes.
8. **Status bar + Bastidores**: contadores de sessão (chamadas, tools) em memória; `debug` do último turno alimenta barra e painel; painel com 2 abas (Bastidores/Documentos); Documentos usa `location.pathname` para ofertar `md/<slug>.md` e `pdf/<slug>.pdf` + fontes dos trechos.
9. **Compat**: todos os campos de `debug` lidos com fallback; sem `debug` → placeholders.

## Riscos e mitigação
- Header lotado → ícones com `aria-label`/`title`, no máx. 5.
- Conflito dock × sumário/entrada (grid próprio) → padding aplicado no `html` (não no `.layout`), funciona em todas as páginas; splash exclui o companion? (mantém — overlay flutuante).
- Regressão do fluxo existente (stream/byok/sugestão) → e2e cobre os três após a mudança.
