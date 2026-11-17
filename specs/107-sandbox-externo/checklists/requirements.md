# Specification Quality Checklist: Sandbox externo no cap. 07

**Purpose**: Validar a spec antes da escrita do capítulo
**Created**: 2026-11-17
**Feature**: [spec.md](../spec.md)

## Content Quality

- [x] O texto da spec diz o que o leitor do livro ganha e por que o editor pediu
- [x] Seções obrigatórias do template preenchidas com o caso editorial, não com placeholder
- [x] CHK de "sem detalhe de implementação" do template genérico não se aplica: o Princípio I exige caminho de arquivo. Os paths ficam no Apêndice A, e a spec os nomeia

## Requirement Completeness

- [x] Nenhum marcador [NEEDS CLARIFICATION]
- [x] FR-001 a FR-010 são testáveis
- [x] Critérios de sucesso verificáveis (seção presente, linha do Radar, build, placar, PR em rascunho)
- [x] Casos de borda: lead do post, rede, corpus, Leitura executiva
- [x] Escopo fechado: uma seção no cap. 07, sem nota de benchmark e sem tutorial de instalação
- [x] Premissas registradas, inclusive o commit lido e a triagem do repositório

## Feature Readiness

- [x] Cada história tem teste independente
- [x] A divergência post/código é história própria (US3), não nota de rodapé
- [x] O conflito com o Princípio VII (nome da branch e merge) está no plano, não escondido

## Notes

- Validado na escrita, antes do build. O build é tarefa T013, não item desta lista.
