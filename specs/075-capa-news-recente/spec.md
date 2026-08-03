# Feature Specification: A capa noticia o achado mais recente do Radar

**Feature Branch**: `075-capa-news-recente`

**Created**: 2026-08-03

**Status**: Aprovada (defeito relatado pelo editor: "Na capa, aparece ainda 02/08")

## Defeito

O card de novidades da capa (spec 062) e da página de entrada mostravam **02/08** no dia
03/08, mesmo com o Radar do dia publicado e o jornal (`radar.html`) correto.

**Causa raiz**: `noticiaDoRadar()` em `publicar/build.mjs` retorna a **primeira linha válida**
da tabela de `radar/RADAR.md` (`return` dentro do laço), assumindo que o arquivo está sempre
em ordem cronológica reversa. Na execução de 2026-08-03 as linhas novas foram inseridas logo
abaixo de uma linha de 02/08 (a do Traycer, adicionada pela spec 074) — a ordem do arquivo
deixou de refletir a cronologia e a capa passou a noticiar um item mais antigo, e **descartado**.

A ordenação manual de um arquivo editado por um agente agendado é uma premissa frágil: o
motor precisa escolher por **dado**, não por posição.

## Requisitos

1. `noticiaDoRadar()` escolhe a linha de **data mais recente**; empate resolvido pelo maior
   impacto (A > B > C) e, persistindo, pela ordem do arquivo (estável).
2. Comportamento atual preservado no resto: item `(inicial)` ignorado; data, item renderizado
   e rótulo de impacto iguais; PT e EN.
3. `radar/RADAR.md` reordenado por data decrescente (higiene da mesa de edição; sem alterar
   conteúdo de nenhuma linha).

## Fora de escopo

- Filtrar itens por status (um achado `descartado` continua elegível: a recusa é notícia).
- Mudanças no jornal (`jornal.mjs`), que já ordena por edição/impacto.

## Aceite

- [ ] Com o RADAR.md atual, a capa PT e EN mostra **2026-08-03**.
- [ ] Teste do motor: tabela fora de ordem → escolhe a data maior (verificação executada e
      registrada nesta spec).
- [ ] Build 4 passos verde; CI verde na main.
