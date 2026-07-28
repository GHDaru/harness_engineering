# 0004 — Cross-link de citações (MVP) e Apêndice "O estudo"

- **Status:** Aceito
- **Data:** 2026-07-28
- **Contexto (feature/spec):** `028-estudo-citacoes` (E01+E03+E04 da auditoria)

## Contexto
O editor pediu: (a) toda menção a paper deve levar à Bibliografia, e a Bibliografia à fonte; (b) registrar quando cada harness foi forkado/sincronizado; (c) um apêndice mostrando todo o trabalho do estudo (cada harness com análise/diagnóstico e o template usado).

## Decisão
1) **Citações (MVP)**: o motor converte menções textuais `arXiv NNNN.NNNNN` em link para a Bibliografia (que já linka as fontes). Menções que já são links diretos à fonte permanecem.
2) **Apêndice "O estudo"** (`livro/apendice-estudo.md`): tabela gerada dos **metadados reais** das 16 avaliações (origem, versão/snapshot, **fork GHDaru + commit lido** — o dado de fork/sync pedido —, data/rodada, link à avaliação completa), + template + ponte para o Comparativo.
3) Fork/sync **por avaliação** (commit da leitura) em vez de uma data global de sincronização.

## Alternativas avaliadas
- **A — Âncoras por entrada na Bibliografia + resolver todo (Autor, Ano)**: ideal acadêmico; alto custo (parser de citações; manutenção). Adiado, não descartado.
- **B — MVP arXiv→Bibliografia + apêndice com dados reais (escolhida)**: cobre o fluxo pedido com dado verificável hoje.
- **C — Gerar páginas HTML para cada avaliação**: 16 páginas novas no site; adiado para quando as avaliações forem revisadas editorialmente (hoje linkam à fonte no GitHub).

## Justificativa
B entrega o requisito com evidência real (commits dos forks já registrados nas avaliações) sem construir um sistema de citações completo prematuramente. A e C ficam como evolução natural.

## Consequências
- Positivas: rastreabilidade fork/commit por harness; o "trabalho todo" visível numa página; menções soltas de arXiv agora levam à Bibliografia.
- Custos: citações "(Autor, Ano)" ainda não são linkadas automaticamente (passada editorial da 020/O001).
- Reversibilidade: alta.
