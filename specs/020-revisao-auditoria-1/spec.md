# Feature Specification: Rodada de auditoria e revisão 1

**Feature Branch**: `020-revisao-auditoria-1`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O autor está auditando o livro e inserindo observações que se tornam **correções**. Esta feature é a **1ª rodada de revisão**: acumular as observações do autor numa branch (sem publicar), aplicá-las como correções mantendo o rigor do projeto, e ao final **merge único** para a `main` (que publica) — opcionalmente seguido de um Release (DOI de versão).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O autor audita e as correções entram sem publicar a cada passo (Priority: P1)

O autor passa observações (por capítulo/seção/trecho). Cada observação vira uma **correção rastreável** aplicada na branch. O autor **revê antes de publicar** (screenshots/preview). Quando o lote está bom, um **único merge** publica tudo.

**Independent Test**: aplicar uma observação → ver o trecho corrigido no build local (screenshot) → nada publicado até o merge.

**Acceptance Scenarios**:

1. **Given** uma observação do autor ("cap. X, trocar A por B"), **When** aplico na branch, **Then** o trecho é corrigido e registrado na lista de correções (tasks), sem publicar.
2. **Given** o lote de correções, **When** o autor aprova (via preview), **Then** faço o merge único na `main` e o site publica uma vez.
3. **Given** uma correção que muda um fato/afirmação sobre um harness, **When** aplico, **Then** mantenho a evidência (caminho de arquivo/fonte); nada de afirmação sem lastro (Princípio I).

### Edge Cases

- Observação ambígua ("aqui está confuso"): eu proponho a correção e confirmo com o autor antes de fixar.
- Correção que afeta um número/tabela do benchmark: manter a rastreabilidade (rodada/data), nunca sobrescrever silenciosamente (Princípio IV).
- Correção grande (reescrever seção inteira): se virar uma melhoria estrutural, pode sair desta rodada para um spec próprio.

## Requirements *(mandatory)*

- **FR-001**: Cada observação do autor DEVE virar uma **task rastreável** em `tasks.md` (o quê, onde, correção aplicada).
- **FR-002**: As correções DEVEM preservar o rigor: **evidência** para afirmações (Princípio I); nada inventado; tom e método do livro (Guia Editorial).
- **FR-003**: O trabalho DEVE ficar **na branch** `020-…` até a aprovação; **nada publica** antes do merge.
- **FR-004**: O autor DEVE conseguir **rever antes de publicar** (screenshots/preview do build local).
- **FR-005**: Ao concluir, `livro/HISTORICO.md` DEVE registrar a **edição de revisão** (0.16) com o resumo das correções + modelo de IA (A3).
- **FR-006**: O build DEVE ficar **verde** (link-check) antes do merge; sem identificador interno de modelo.
- **FR-007**: O merge para a `main` (`--no-ff`) é **único** por lote (publica uma vez); Release/DOI é ação subsequente do autor, se desejar.

## Success Criteria *(mandatory)*

- **SC-001**: Toda observação do autor tem uma task correspondente e uma correção aplicada (ou uma decisão registrada de não aplicar).
- **SC-002**: Nada foi publicado durante a rodada; o merge final publica o lote de uma vez.
- **SC-003**: Build verde; `HISTORICO` com a edição de revisão; zero identificador interno de modelo.
- **SC-004**: Correções factuais mantêm evidência (Princípio I).

## Assumptions

- Rodada **rolante**: as tasks são adicionadas conforme o autor manda observações; a rodada fecha quando o autor disser "pode publicar".
- Correções triviais isoladas ainda poderiam ir direto ao main; aqui, por serem um **lote de auditoria**, ficam na branch e publicam juntas.
- Feature toca `livro/` (e possivelmente `benchmark/`, `publicar/`) → ciclo spec-kit (Princípio VII).
