# Feature Specification: Sandbox externo no cap. 07

**Feature Branch**: `107-sandbox-externo` (diretório da spec). Branch git desta sessão: `cursor/107-sandbox-externo-7afd`.

**Created**: 2026-11-17

**Status**: Draft — pull request em rascunho para o editor. Sem merge.

**Input**: O editor Gilsiley Darú decidiu em 17/11/2026 promover ao livro o padrão de sandbox externo para agentes de código, com o post da Prime Radiant (16/11/2026) e o repositório `prime-radiant-inc/external-sandbox`. Itens do Radar não entram no livro sozinhos (ADR 0008). Esta spec é o registro dessa curadoria humana.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor situa o padrão (Priority: P1)

Quem lê o cap. 07 encontra o sandbox externo ao lado dos modos de aprovação e da contenção por sistema operacional já descritos (Codex CLI, gemini-cli), com o que o protocolo define, os limites e o motivo pelo qual o padrão importa para a tese do capítulo.

**Why this priority**: É o pedido do editor. Sem essa seção, a promoção não aconteceu.

**Independent Test**: A seção 4 de `livro/capitulos/07-permissoes-sandbox.md` cobre comparação, protocolo, limites e a tese, e a pergunta 5 da verificação tem resposta no fim do capítulo.

**Acceptance Scenarios**:

1. **Given** o capítulo publicado, **When** o leitor abre o estado da arte, **Then** encontra a seção do sandbox externo com data de evento 16/nov/2026 e a ressalva na Leitura executiva.
2. **Given** a mesma seção, **When** o leitor procura o que o Claude Code manda ao sandbox, **Then** lê que o shell atravessa e que Read/Edit ficam no host, com o caminho de arquivo no Apêndice A.

---

### User Story 2 - A promoção fica rastreável (Priority: P2)

O editor e o Radar conseguem ver que o item foi promovido por decisão humana em 17/11/2026, ligado ao cap. 07, e não por iniciativa do agente do Radar.

**Why this priority**: O ADR 0008 faz dessa fronteira a regra do projeto.

**Independent Test**: A primeira linha da tabela de `radar/RADAR.md` tem status `promovido (spec 107)` e nomeia o editor e a data.

**Acceptance Scenarios**:

1. **Given** `radar/RADAR.md`, **When** se busca o item, **Then** o status é `promovido (spec 107)`, o capítulo é 07 e a ação cita a decisão de 17/11/2026.

---

### User Story 3 - A divergência post/código fica escrita (Priority: P1)

Onde o post e o código não dizem a mesma coisa, o capítulo fica com o código e a divergência aparece para o editor.

**Why this priority**: O pedido manda confirmar nas fontes e prevalecer o código.

**Independent Test**: A seção nomeia pelo menos a rede (promessa dos backends, não do núcleo) e o atalho `!` do Codex, além do furo de Read/Edit.

**Acceptance Scenarios**:

1. **Given** a seção 4, **When** se compara com `PROTOCOL.md` e com `claude-code/README.md` no commit `0681c98`, **Then** nenhuma frase do capítulo contradiz esses arquivos.

### Edge Cases

- O post abre com "every command" e o corpo, mais o README da integração, restringem o Claude Code ao shell. O capítulo segue a restrição.
- O núcleo do protocolo não promete rede desligada. Os três backends prometem. O capítulo separa as duas frases.
- O repositório do protocolo não entra no corpus e não recebe nota de benchmark.
- A Leitura executiva não é reescrita. Ganha ressalva. As duas dimensões continuam de pé.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O livro MUST descrever o padrão de sandbox externo no cap. 07, em português, comparando-o aos modos de aprovação e à contenção por sistema operacional já presentes no capítulo.
- **FR-002**: A descrição MUST dizer o que a revisão 1 de `PROTOCOL.md` define (núcleo, perfis, credencial, herança de ambiente), com caminhos de arquivo no Apêndice A.
- **FR-003**: A descrição MUST registrar os limites: protótipo não auditado; no Claude Code, leitura e edição de arquivo ficam fora do sandbox; montagem com escrita é a pasta real; o convidado é Linux.
- **FR-004**: A Leitura executiva MUST ganhar ressalva se a seção nova qualifica a síntese, sem apagar as duas dimensões.
- **FR-005**: `livro/bibliografia.md` e o par EN MUST apontar para o post e para `PROTOCOL.md` no commit lido.
- **FR-006**: `livro/HISTORICO.md` MUST registrar a edição, a data de revisão do cap. 07 e a releitura do placar de expiração.
- **FR-007**: `radar/RADAR.md` MUST marcar o item como promovido pelo editor em 17/11/2026, spec 107, cap. 07.
- **FR-008**: O texto novo de capítulo MUST passar pela régua humanizer do `CLAUDE.md` (leitura, não varredura) e pelo portão de prosa do build.
- **FR-009**: Nenhum segredo e nenhum identificador interno de modelo em commit ou artefato. Assinatura do histórico: "Claude Code (Anthropic)".
- **FR-010**: O par EN do capítulo, da bibliografia e do glossário (menção nova ao MCP no cap. 07) MUST acompanhar o delta, com selo i18n regravado pelo `sela.mjs`.

### Key Entities

- **Sandbox externo**: padrão em que o agente permanece na máquina de quem o usa e o comando vai a um Linux isolado. O adjetivo qualifica o agente, não o computador.
- **Protocolo, revisão 1**: contrato observável em `PROTOCOL.md`, commit `0681c98` (16/nov/2026).
- **Promoção**: decisão humana do editor, registrada no Radar, que autoriza a spec. Não é ação do agente diário.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O cap. 07 tem uma seção nova cujo texto cobre comparação, protocolo, limites e a tese, e a pergunta 5 da verificação tem resposta.
- **SC-002**: A tabela do Radar tem uma linha com status `promovido (spec 107)`, data 2026-11-17 e capítulo 07.
- **SC-003**: O build de `publicar` passa nos quatro passos, inclusive selos i18n e o portão de prosa do capítulo v4.
- **SC-004**: O placar de expiração do cap. 07 foi relido: a linha de sandbox permanece 🔴 e a de policy engine permanece 🔵, com a evidência de 2026-11-17 na linha de sandbox.
- **SC-005**: A pull request é aberta em rascunho e não é mergeada.

## Assumptions

- O próximo número livre de spec é 107. Confirmado: o maior prefixo em `specs/` era 106.
- A fonte-base é o commit `0681c98` de `prime-radiant-inc/external-sandbox` (16/nov/2026, autor Simon Willison) mais o `README.md` de `prime-radiant-inc/external-sandbox-pi`. Os backends v86, container e Quicksand não foram lidos além do que o repositório do protocolo e o post afirmam sobre eles.
- Triagem do repositório do protocolo, lida na API em 17/11/2026: Apache-2.0, Python, criado em 2026-10-09, push em 2026-11-16, não arquivado, 18 estrelas e 1 fork. Não é candidato ao corpus. A razão estrela/fork fica acima do piso do contrato do Radar, e o volume é pequeno demais para afirmar adoção. Esses números ficam na spec, não no capítulo.
- A branch git desta sessão segue o prefixo exigido pelo ambiente (`cursor/…-7afd`). O Princípio VII pede `NNN-nome` e merge na `main`. O conflito está no `plan.md`. O editor pediu rascunho e proibiu o merge.
- O capítulo não vira tutorial de `npx`. Diátaxis: a seção é explicação.
