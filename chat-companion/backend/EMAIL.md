# Email via Gmail — sugestões e link mágico

O mesmo SMTP (STARTTLS + login) serve a **dois** usos, com exigências diferentes:

| Uso | Rota | Se o SMTP falhar |
|---|---|---|
| Sugestões dos leitores | `/suggestion` | **best-effort** — a sugestão já está persistida no banco; o email é bônus |
| Link mágico de leitura (spec 080) | `/assinar` | **falha visível** — sem email não há link, e o widget diz isso ao leitor |

A diferença é deliberada: responder "enviado" quando nada saiu deixaria o leitor esperando
um email que nunca chega. O link **nunca** aparece na resposta HTTP — só no email.

Para usar a conta Gmail do autor tanto para **enviar** (remetente) quanto para **receber**
(destinatário):

## 1. Criar uma senha de app no Google

1. A conta precisa ter **verificação em duas etapas** ativa: <https://myaccount.google.com/security>.
2. Acesse **Senhas de app**: <https://myaccount.google.com/apppasswords>.
3. Crie uma senha com o nome `companion-livro` e **copie os 16 caracteres**.

> A senha normal da conta **não funciona** (o Google bloqueia login SMTP por senha comum).
> A senha de app dá acesso SMTP sem expor a senha real.

## 2. Configurar as variáveis no Railway

No serviço do backend (Railway → Variables), defina:

| Variável | Valor |
|---|---|
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | o endereço Gmail do autor (vira o **remetente**) |
| `SMTP_PASS` | a **senha de app** de 16 caracteres |
| `SUGGESTION_EMAIL_TO` | o endereço que **recebe** as sugestões (default já é a conta do autor) |

E, para o link mágico (spec 080) — os defaults servem, ajuste só se o site mudar de endereço:

| Variável | Default | Para que serve |
|---|---|---|
| `SITE_URL` | `https://ghdaru.github.io/harness_engineering/` | base do link que vai no email (`<SITE_URL>entrar.html?t=…`) |
| `MAGIC_LINK_TTL_MIN` | `30` | validade do link, em minutos |
| `RATE_LIMIT_ASSINAR` | `5` | envios por janela, por email **e** por IP |

Redeploy do serviço e pronto — a próxima sugestão chega na caixa de entrada com
assunto `[Engenharia de Harness] Sugestão de leitor (<página>)`, e o próximo pedido de
link chega ao leitor com assunto `[Engenharia de Harness] Seu link de leitura`.

## Regras de segurança

- **Nunca** commitar a senha de app (nem em `.env` versionado, nem em teste, nem em chat).
- Se a senha vazar: revogue em <https://myaccount.google.com/apppasswords> e gere outra.
- `SMTP_HOST` vazio desliga o email sem quebrar nada: as sugestões continuam no banco
  (visíveis via `GET /suggestions` com `ADMIN_TOKEN`) e a assinatura responde
  `{"enviado": false}` — o leitor é avisado, e a leitura anônima segue completa.
- O token do link mágico é guardado **só como hash SHA-256**, tem uso único e expira.
  Ele não vai para log nem para resposta HTTP.
