# Spec 048: BYOK no widget do companion

**Feature Branch**: `048-byok-widget` · **Criada em**: 2026-07-29

## Contexto

O backend já suporta BYOK (`ChatIn.byok_key`, `ALLOW_BYOK=True`, isenção de rate-limit, chave efêmera por chamada — spec 016/017). Falta a superfície no widget.

## Requisitos

- FR-001: comando **`/chave`** no chat abre um formulário discreto (input `type=password`) para colar a chave; **`/chave limpar`** remove. Intenção explícita ("usar minha chave", "byok") também abre. Sem botão permanente (mesmo padrão da sugestão, spec 044).
- FR-002: a chave fica **somente no `localStorage` do navegador** (`cmp_byok`); nunca aparece em texto claro na tela (mascarada como `…últimos 4`); enviada como `byok_key` no corpo de `/chat` e `/chat/stream`.
- FR-003: com chave ativa, o cabeçalho do painel mostra um selo 🔑 (tooltip com o mascarado) que permite remover com um clique + confirmação.
- FR-004: a mensagem de rate-limit (429) do backend já sugere BYOK; o widget acrescenta a dica do comando `/chave` quando detecta 429.
- FR-005: e2e local (uvicorn echo): salvar chave → payload contém `byok_key` → limpar → payload sem a chave.

## Segurança

- A chave nunca vai a logs, store ou HISTORICO; é lida do localStorage no momento do envio. Colar chave no chat "normal" não é suportado (o comando existe para não induzir o usuário a mandar a chave como mensagem — mensagem vira histórico persistido).
