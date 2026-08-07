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

## Diagnóstico quando o link não sai (spec 084)

`POST /assinar` responde `{"enviado": false, "motivo": "<classe>"}` — e `GET /health` traz
`"smtp": "configurado" | "desligado"`. O **detalhe** (tipo e mensagem da exceção) vai para o
`stderr`, ou seja, o log do serviço no Railway. O token nunca entra em nenhum dos dois.

| `motivo` | O que aconteceu | O que conferir |
|---|---|---|
| `desligado` | `SMTP_HOST` vazio — nem tentou | Definir as variáveis e redeploy |
| `auth` | O servidor recusou o login | **A senha de app colada com os espaços** (o Google exibe `abcd efgh ijkl mnop`; tem de ir sem espaço). Depois: `SMTP_USER` é o mesmo endereço da senha de app? A verificação em duas etapas continua ativa? A senha foi revogada? |
| `conexao` | Não chegou a falar com o servidor | `SMTP_HOST`/`SMTP_PORT` (`smtp.gmail.com`/`587`); egresso do Railway na porta 587 |
| `tls` | STARTTLS falhou | Porta trocada (465 é SSL direto, não STARTTLS — este código usa 587) |
| `destinatario` | Remetente ou destinatário recusado | `SMTP_USER` precisa ser um endereço que a conta pode usar como remetente |
| `smtp` | O servidor respondeu com erro de protocolo | Log do Railway; costuma ser limite de envio da conta |
| `outro` | Fora das classes acima | Log do Railway |

Um teste rápido, de fora:

```bash
curl -s -X POST https://harnessengineering-production.up.railway.app/assinar \
  -H 'content-type: application/json' -d '{"email":"SEU@EMAIL","lang":"pt"}'
```

> **NÃO diagnostique pelo tempo de resposta.** Eu tentei, e errei. `/assinar` faz várias idas
> ao Neon **antes** de tocar o SMTP, e cada `self._conn()` abre uma conexão nova — ~2 s cada.
> Medido com o SMTP provadamente desligado: e-mail novo (cria leitor) **7,9 s**; e-mail já
> cadastrado **4,0 s**; `GET /history`, que faz uma só ida ao banco, **2,0 s**. Ou seja: sete
> segundos são o banco, não uma tentativa de envio. Quem responde à pergunta é o campo
> `smtp` do `/health` e o `motivo` do `/assinar` — não o cronômetro.

## Antes de tudo: a variável chegou ao processo? (spec 085)

`GET /health` lista os **nomes** das variáveis de ambiente que começam com `SMTP` — nunca os
valores, e com `repr()` para que espaço em branco no nome apareça:

```bash
curl -s https://harnessengineering-production.up.railway.app/health
```

```json
{"smtp":"desligado","smtp_vars":["'SMTP_HOST '","'SMTP_PASS'","'SMTP_PORT'","'SMTP_USER'"]}
```

| O que a lista mostra | O que significa |
|---|---|
| Lista **vazia** | Nenhuma variável `SMTP*` chegou. Foram para outro **serviço** ou outro **environment** do projeto — ou é variável compartilhada do projeto que este serviço não referencia |
| `"'SMTP_HOST '"` com espaço | O Raw Editor criou a chave a partir de `SMTP_HOST =valor`. É outra chave; nunca casa. Recriar sem espaço |
| Falta `'SMTP_HOST'`, mas há as outras | Só o host ficou de fora |
| Todas presentes e `smtp` ainda `desligado` | O processo não reiniciou depois da mudança — redeploy |

## A porta decide o protocolo (spec 086)

| `SMTP_PORT` | Transporte | Observação |
|---|---|---|
| `587` | `SMTP` + `STARTTLS` | **recomendado** para o Gmail |
| `465` | `SMTP_SSL` (TLS implícito) | funciona; o código detecta pela porta |
| `25` | STARTTLS | quase sempre bloqueado por provedores de nuvem |

Antes da spec 086, a porta `465` com `starttls()` ficava pendurada até o timeout e o erro
chegava como `conexao` — indistinguível de porta bloqueada. Hoje `GET /health` publica
`smtp_porta`, então dá para conferir sem abrir o painel.

**Se, com a porta certa, o `motivo` continuar `conexao`:** o egresso SMTP da infraestrutura está
bloqueado (muitos PaaS fecham 25/465/587 para conter spam) e insistir na porta não resolve. A
saída é trocar SMTP por uma **API HTTP de envio** — o corpo do e-mail e a lógica do link mágico
não mudam, só o transporte em `_enviar_link_magico`.

## Regras de segurança

- **Nunca** commitar a senha de app (nem em `.env` versionado, nem em teste, nem em chat).
- Se a senha vazar: revogue em <https://myaccount.google.com/apppasswords> e gere outra.
- `SMTP_HOST` vazio desliga o email sem quebrar nada: as sugestões continuam no banco
  (visíveis via `GET /suggestions` com `ADMIN_TOKEN`) e a assinatura responde
  `{"enviado": false}` — o leitor é avisado, e a leitura anônima segue completa.
- O token do link mágico é guardado **só como hash SHA-256**, tem uso único e expira.
  Ele não vai para log nem para resposta HTTP.
