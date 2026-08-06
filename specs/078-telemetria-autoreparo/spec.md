# Feature Specification: Telemetria auto-reparável

**Feature Branch**: `078-telemetria-autoreparo`

**Created**: 2026-08-05

**Status**: Aprovada (defeito relatado pelo editor: "Os registros da usabilidade do site está zerado para mim")

## Defeito

O [Apêndice — Uso do livro](../../livro/apendice-uso.md) e o contador do rodapé mostravam **zero**.
Diagnóstico: o backend está de pé e o caminho funciona — testado ao vivo, `/consent` seguido de
`/telemetry` grava e o agregado sobe. O defeito é de **contrato entre cliente e servidor**:

- o cliente guarda `cmp_consent` no **localStorage** e, com o flag presente, **nunca mais mostra
  o banner**;
- o servidor exige uma **linha de consentimento** para o `session_id`, senão descarta a
  navegação e responde `{"ok": false}`;
- o POST de consentimento era `fetch(...).catch(function(){})` — **falha em silêncio**.

Basta o backend estar hibernando (Railway) ou quebrado (a janela do bug do `tx`, edição 0.64) no
instante do aceite: o flag local grava, o servidor não registra, e **toda telemetria daquele
navegador é descartada para sempre** — porque o banner nunca mais aparece para reenviar o aceite.
Silencioso e permanente, exatamente o que o editor observou.

## Correção

`{"ok": false}` deixa de ser ignorado e passa a significar *"reenvie o aceite e tente de novo"*:
o cliente re-posta `/consent` (o flag local é a prova de que a pessoa aceitou) e repete a
navegação **uma vez por carregamento**. O `postConsent()` passa a devolver promessa, de modo que
o reparo só tenta a segunda vez se o registro realmente funcionou.

Efeito colateral necessário: **sai o `sendBeacon`**. Beacon não devolve resposta, e sem resposta
não há como detectar a dessincronia. Fica `fetch` com `keepalive: true`, que preserva o envio na
saída da página.

Quem já está dessincronizado (o editor, entre outros) **repara sozinho na próxima visita** — não
é preciso limpar nada no navegador.

## Aceite

- [x] Estado dessincronizado reproduzido em navegador real; sequência observada:
      `telemetry → RECUSADO`, `consent → ok`, `telemetry → ok`, navegação gravada
- [x] Zero erro de JS; nenhuma variável `tx` sombreando a função (guarda-corpo da 0.64)
- [ ] Build 4 passos verde e CI verde na main
