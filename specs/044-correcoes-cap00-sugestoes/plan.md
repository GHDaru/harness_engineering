# Plan — 044

1. **Cap. 00**: `livro/00-introducao.md` — "em três arquétipos" → "em quatro arquétipos" (única ocorrência com a lista de 4).
2. **Companion** (`publicar/tema/companion.js`):
   - remover `sugBtn` do cabeçalho (e o listener);
   - `pedirSugestao()`: mostra o `sugForm` + mensagem de sistema; foco no textarea;
   - interceptação em `submit` do chat: regex de comando `^/suge(rir|stao|stão)` OU intenção (`sugest` + `autor|enviar|mandar`) → `pedirSugestao()` sem chamar o backend;
   - `greet()` menciona o comando `/sugerir`;
   - envio/cancelamento continuam como estão (form some após enviar).
3. **Email Gmail**: `chat-companion/backend/EMAIL.md` — passo a passo: senha de app do Google (requer verificação em 2 etapas) + variáveis no Railway (`SMTP_HOST=smtp.gmail.com`, `SMTP_PORT=587`, `SMTP_USER`, `SMTP_PASS`, `SUGGESTION_EMAIL_TO`). Comentário no `config.py` apontando para o doc. Sem mudanças de lógica (o `_enviar_email_sugestao` já faz STARTTLS+login).
4. **Fechamento**: rebuild + `verifica-capitulos.mjs`, corpus regenerado, HISTORICO edição 0.39 (A3), merge `--no-ff`, push.
