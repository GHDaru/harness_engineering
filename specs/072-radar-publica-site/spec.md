# Feature Specification: Publicar o site a cada commit do Radar

**Feature Branch**: `072-radar-publica-site`

**Created**: 2026-08-02

**Status**: Aprovada (promoção pedida pelo editor: "promova")

**Input**: Nota de manutenção do diário do Radar de 2026-08-02.

## Problema

O Radar-jornal (`docs/radar.html`, spec 071) é gerado no CI a partir de `radar/diario/*.md`,
mas o workflow `publicar.yml` não lista `radar/**` nos paths do gatilho. Consequência: o
commit diário do agente (`radar: AAAA-MM-DD`) **não** reconstrói o site, e a página do
jornal fica defasada até o próximo push em `livro/`/`publicar/`. Detectado pela execução
agendada de 2026-08-02 — o agente do Radar não pôde corrigir por regra dura do contrato
(escrita somente em `radar/`).

## Requisitos

1. Push na `main` que altere `radar/**` deve disparar o workflow de publicação.
2. Nenhuma outra mudança de comportamento (mesmos passos de build/verificação/deploy).
3. Registro no HISTORICO (edição de infraestrutura) e status "promovida (spec 072)" na
   nota de manutenção do diário de 2026-08-02.

## Fora de escopo

- Qualquer mudança no motor (`publicar/`) ou no contrato do agente (`radar/AGENTE.md`).
- Os itens editoriais da tabela do RADAR (QM, ZCode, Aider, papers) — rodada 2026-10.

## Aceite

- [ ] `publicar.yml` com `radar/**` nos paths.
- [ ] YAML válido (parse local).
- [ ] Após o merge, o run do workflow dispara e conclui verde; `docs/radar.html` passa a
      refletir a edição mais recente do diário sem depender de push em `livro/`.
