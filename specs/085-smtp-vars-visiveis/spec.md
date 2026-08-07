# Feature Specification: `/health` mostra QUAIS variáveis SMTP o processo enxerga

**Feature Branch**: `085-smtp-vars-visiveis`

**Created**: 2026-08-07

**Status**: Aprovada — desbloqueio da spec 080 depois de duas rodadas de palpite falharem.

## Problema

A spec 084 fez o backend dizer **que** o envio falha e em que classe. Ficou faltando a
pergunta anterior: com `smtp: "desligado"`, **a variável chegou a este processo?**

Estado real, medido após o editor configurar as variáveis **e redeployar duas vezes**:

```
{"ok":true,"llm":"openai","store":"postgres","smtp":"desligado"}
{"ok":true,"enviado":false,"expira_min":30,"motivo":"desligado"}
```

`desligado` só diz que `config.SMTP_HOST` está vazio. Não distingue:

- a variável foi para **outro serviço** ou **outro environment** do projeto;
- ela existe com **nome ligeiramente diferente** (`SMTP_HOSTS`, `smtp_host`);
- ela existe com **espaço no nome** (`"SMTP_HOST "` — o Raw Editor cria isso a partir de
  `SMTP_HOST =valor`), que é uma chave diferente e nunca casa;
- o processo simplesmente **não reiniciou** depois da mudança.

Sem essa distinção o ciclo é: editor ajusta → eu testo → `desligado` → ninguém sabe mais nada.
Duas voltas assim já aconteceram.

## Correção

`GET /health` passa a devolver `smtp_vars`: os **nomes** — nunca os valores — das variáveis de
ambiente que começam com `SMTP`, cada um com `repr()` para que espaço em branco no nome
apareça em vez de sumir na renderização.

```
"smtp_vars": ["'SMTP_HOST '", "'SMTP_PASS'", "'SMTP_PORT'", "'SMTP_USER'"]
```

Uma olhada nessa lista responde as quatro hipóteses de uma vez.

## Por que expor isso é aceitável

- **Nome não é segredo.** O valor continua inacessível por qualquer rota.
- O prefixo é fixo e estreito (`SMTP`): não vaza `DATABASE_URL`, `OPENAI_API_KEY` nem
  `ADMIN_TOKEN`.
- `/health` já revelava `llm`, `store` e `smtp` — a superfície não muda de natureza.
- O ganho é encerrar um ciclo de diagnóstico cego que já custou duas rodadas ao editor.

## Aceite

- [x] `smtp_vars` lista apenas nomes com prefixo `SMTP`, com `repr()`
- [x] Nenhum valor de variável aparece em qualquer resposta
- [x] Testes verdes
- [ ] Contra produção: a lista mostra o que o processo enxerga de fato
