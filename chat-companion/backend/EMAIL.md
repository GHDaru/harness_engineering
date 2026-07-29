# Email de sugestões via Gmail

As sugestões dos leitores são **sempre persistidas** no banco (`/suggestion`); o email é
best-effort por SMTP (`_enviar_email_sugestao` em `app.py`: STARTTLS + login). Para usar
a conta Gmail do autor tanto para **enviar** (remetente) quanto para **receber**
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
| `SUGGESTION_EMAIL_TO` | o endereço que **recebe** (default já é a conta do autor) |

Redeploy do serviço e pronto — a próxima sugestão chega na caixa de entrada com
assunto `[Engenharia de Harness] Sugestão de leitor (<página>)`.

## Regras de segurança

- **Nunca** commitar a senha de app (nem em `.env` versionado, nem em teste, nem em chat).
- Se a senha vazar: revogue em <https://myaccount.google.com/apppasswords> e gere outra.
- `SMTP_HOST` vazio desliga o email sem quebrar nada (as sugestões continuam no banco,
  visíveis via `GET /suggestions` com `ADMIN_TOKEN`).
