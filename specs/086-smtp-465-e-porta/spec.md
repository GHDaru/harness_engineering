# Feature Specification: a porta decide o protocolo (465 vs 587), e ela fica visível

**Feature Branch**: `086-smtp-465-e-porta`

**Created**: 2026-08-07

**Status**: Aprovada — desbloqueio da spec 080, terceira e última camada de diagnóstico.

## Problema

Com as variáveis finalmente no serviço certo (spec 085 provou: `smtp: "configurado"`, os quatro
nomes limpos), o envio passou a falhar assim:

```
{"ok":true,"enviado":false,"expira_min":30,"motivo":"conexao"}   — 24 s
```

Vinte e quatro segundos: os 20 s do `timeout` do socket mais o custo do banco. Ele **não chegou
a autenticar** — parou antes, no transporte.

`conexao` tem duas causas possíveis, e elas são **indistinguíveis de fora**:

1. **Porta errada para o protocolo.** O código abria `smtplib.SMTP` (texto claro) e chamava
   `starttls()`. Isso é o certo para **587**. Em **465** o servidor espera o handshake TLS
   **imediatamente**: o EHLO em claro fica pendurado até estourar o timeout — e chega aqui como
   `conexao`, exatamente igual a uma porta bloqueada.
2. **Egresso SMTP bloqueado pela infraestrutura.** Vários PaaS fecham 25/465/587 para conter spam.

Só a segunda é um beco. A primeira é bug nosso, e o código pode eliminá-la sozinho.

## Correção

1. **A porta escolhe o transporte**: `465` → `smtplib.SMTP_SSL` (TLS implícito); qualquer outra →
   `SMTP` + `starttls()`. Deixa de existir a combinação que trava.
2. **`GET /health` publica `smtp_porta`.** Número de porta não é segredo, e é o último dado que
   faltava para fechar o diagnóstico sem pedir print de tela a ninguém.

Se, com o transporte certo, ainda vier `conexao`, a conclusão é a hipótese 2 — e aí a saída é
trocar SMTP por uma API HTTP de envio, não insistir na porta.

## Aceite

- [x] `465` usa `SMTP_SSL`; demais portas usam `STARTTLS`
- [x] `smtp_porta` no `/health`; nenhum valor sensível exposto
- [x] Testes verdes
- [x] Contra produção: **`conexao` com a porta certa** — a hipótese do transporte está eliminada

## Leitura contra produção (2026-08-07)

```
{"smtp":"configurado","smtp_porta":587,"smtp_vars":["'SMTP_HOST'","'SMTP_PASS'","'SMTP_PORT'","'SMTP_USER'"]}
{"ok":true,"enviado":false,"expira_min":30,"motivo":"conexao"}   — 24,06 s
```

Porta **587** com **STARTTLS**, que é exatamente o que o código faz: o transporte está correto.
E o tempo é o `timeout` de socket **inteiro** (20 s) — assinatura de pacote **descartado em
silêncio** por firewall, não de host inexistente (falha de DNS volta em menos de um segundo).

**Conclusão: o egresso SMTP desta infraestrutura está bloqueado.** Nenhum ajuste de porta, host
ou credencial resolve — a senha de app sequer chegou a ser testada, porque a conexão morre antes
do login. A saída é trocar o transporte por uma **API HTTP de envio**; o corpo do e-mail, o
token e toda a lógica do link mágico continuam como estão.
