# Feature Specification: o e-mail sai por API HTTP, não por SMTP

**Feature Branch**: `087-email-por-api`

**Created**: 2026-08-07

**Status**: Aprovada pelo editor — escolha do provedor: **Resend**.

## Problema

A spec 086 fechou o diagnóstico: com `SMTP_PORT=587` e STARTTLS (o transporte **correto**), o
envio ainda morre com `motivo: "conexao"` após o **timeout de socket inteiro** — assinatura de
pacote descartado em silêncio por firewall. **O egresso SMTP desta infraestrutura está
bloqueado**, política comum de PaaS para conter spam.

Consequência: a spec 080 está completa e verificada, mas o leitor não recebe o link. E as
sugestões dos leitores (E05), que usam o mesmo transporte, também não chegam ao autor desde
sempre — o que passava despercebido porque ali o envio é best-effort.

## Solução

O e-mail passa a sair por **API HTTP**, o mesmo caminho de rede que o backend já usa para falar
com o LLM — e que comprovadamente funciona nesta infra.

- `RESEND_API_KEY` presente → transporte **`resend`**;
- senão, `SMTP_HOST` presente → transporte **`smtp`** (preservado para quem hospedar noutro
  lugar; não é código morto, é portabilidade);
- nenhum dos dois → **`desligado`**, com a honestidade que a 084 estabeleceu.

Uma **porta única de saída**, `_enviar_email(para, assunto, corpo) -> (ok, motivo)`, passa a
servir tanto o link mágico quanto as sugestões. Quem chama não sabe qual é o transporte — sabe
se foi e, se não foi, por quê.

## Requisitos

- `config.transporte_email()` é a fonte única da decisão; `GET /health` publica em `email`.
- Classes de falha do Resend, sem repassar o corpo do provedor ao cliente:
  `401/403 → auth`; `400/422 → destinatario`; `429 → limite`; demais `→ api`;
  exceção de rede cai no mesmo `_classe_da_falha` do SMTP.
- A chave da API vai no header e **nunca** em log, resposta ou artefato — mesmo tratamento da
  chave do LLM.
- O corpo do e-mail, o token, o uso único, a expiração e a fusão de sessões **não mudam**.
- Sem dependência nova: `httpx` já está em `requirements.txt` (é o cliente do LLM).

## Aceite

- [x] `resend` tem precedência sobre `smtp`; sem os dois, `desligado`
- [x] Envio bem-sucedido entrega o link no corpo e não devolve `motivo`
- [x] Cada status HTTP vira a classe certa; o corpo do provedor fica só no log
- [x] Nem o token nem a chave da API aparecem na resposta
- [x] `GET /health` declara o transporte
- [x] 45 testes verdes
- [ ] Contra produção: o link chega à caixa de entrada do editor

## Ação do editor

`RESEND_API_KEY` no serviço do backend (o mesmo em que `DATABASE_URL` já está). Com o domínio de
teste do Resend o `EMAIL_FROM` default já serve; para enviar do domínio próprio, verificá-lo no
painel do Resend e definir `EMAIL_FROM`.
