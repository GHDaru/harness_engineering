# Feature Specification: o envio do link mágico não pode falhar em silêncio

**Feature Branch**: `084-smtp-diagnostico`

**Created**: 2026-08-07

**Status**: Aprovada — defeito encontrado no primeiro uso real da spec 080, com o SMTP já configurado pelo editor.

## Defeito

Com `SMTP_HOST/PORT/USER/PASS` configurados no Railway, `POST /assinar` responde:

```
{"ok":true,"enviado":false,"expira_min":30}
```

E **ninguém sabe por quê**. O `_enviar_link_magico` da spec 080 termina em:

```python
except Exception:
    return False
```

O `except` nu engole a causa — credencial recusada, porta bloqueada, TLS, DNS, tudo vira o
mesmo `False`. O editor fica com um botão que não funciona e sem nenhuma pista; eu fico
adivinhando entre cinco hipóteses igualmente plausíveis.

**A evidência de que ele está mesmo tentando** (e que, portanto, não é `SMTP_HOST` vazio):
o tempo de resposta. `SMTP_HOST` vazio retorna na primeira linha, sem rede.

| Chamada | Tempo |
|---|---|
| `GET /health` (não toca SMTP) | 0,34 s |
| `POST /assinar` — 1ª | 8,20 s |
| `POST /assinar` — 2ª | 7,40 s |
| `POST /assinar` — 3ª | 7,35 s |

Sete segundos consistentes: conecta, negocia e **falha lá dentro**. O `timeout` do código é
20 s, então também não é estouro de tempo de conexão.

Isto viola o anti-checklist do próprio repositório (`.specify/memory/checklist-verificacao.md`):
*"não declarar 'verificado' o que só foi construído"* e, sobretudo, a regra de que uma falha
precisa ser **legível**. A spec 080 acertou em não mentir "enviado"; errou em não dizer o porquê.

## Correção

1. **Log no servidor**: a exceção vai para `stderr` com tipo e mensagem — é o console do
   Railway, do operador, o lugar certo para o detalhe. Nunca a senha, nunca o token.
2. **Classe grosseira na resposta**: `motivo` com um de `auth` · `conexao` · `tls` ·
   `destinatario` · `outro`. Não vaza nada além do que `enviado:false` já revela (que o envio
   está quebrado), e permite diagnosticar **de fora**, sem pedir log a ninguém.
3. **`GET /health` passa a declarar `smtp`**: `configurado` | `desligado`. Distingue "não quis
   enviar" de "tentou e falhou" antes mesmo de tentar.

O token continua fora de log, de resposta e de qualquer artefato — a regra da 080 não muda.

## Requisitos

- `_enviar_link_magico` devolve `(ok: bool, motivo: str)` em vez de só `bool`.
- Mapeamento por exceção do `smtplib`, sem repassar a mensagem do servidor ao cliente:
  `SMTPAuthenticationError → auth`; `SMTPRecipientsRefused/SenderRefused → destinatario`;
  `SMTPNotSupportedError/ssl.SSLError → tls`; `OSError/socket.timeout/SMTPConnectError → conexao`;
  resto → `outro`.
- `POST /assinar` inclui `motivo` **apenas quando `enviado` é falso**.
- O widget usa o `motivo` para dizer algo útil ao leitor, sem jargão de servidor.
- `GET /health` ganha `"smtp": "configurado" | "desligado"`.
- Sem SMTP configurado o comportamento não muda: `enviado:false`, `motivo:"desligado"`.

## Não faz parte

- Retentativa automática de envio (o leitor reenvia clicando de novo).
- Fila de e-mails, provedor alternativo, webhook de entrega.
- Expor a mensagem crua do servidor SMTP ao cliente.

## Aceite

- [ ] `motivo` presente e correto para cada classe de falha (testes com exceção injetada)
- [ ] Nenhum teste vê token ou senha em log ou resposta
- [ ] `GET /health` declara o estado do SMTP
- [ ] Contra o backend em produção, `POST /assinar` passa a dizer **qual** é a falha
- [ ] Testes verdes; build 4 passos verde
- [ ] Checklist de verificação percorrido
