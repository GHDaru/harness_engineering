# ADR 0008 — Radar diário automatizado (sessão-agente agendada)

- **Status**: aceita (2026-07-29)
- **Feature**: `056-radar-diario`

## Contexto

O livro vivo tem cadência trimestral + gatilho extraordinário (ADR 0007), mas detectar o gatilho dependia de alguém estar olhando. Queremos vigilância diária: buscar novidades (releases do corpus, protocolos, papers, ferramentas novas) e manter um roadmap de auto-atualização — sem abrir mão da curadoria humana sobre o conteúdo.

## Alternativas avaliadas

- **A — GitHub Action diária com chamada de LLM**: roda no CI, mas exige chave de API como secret do repositório, tem contexto raso (sem as ferramentas de agente: busca web, leitura ampla do repo, juízo iterativo) e vira um segundo "motor de agente" para manter.
- **B — Routine de sessão-agente (escolhida)**: o mesmo ambiente destas sessões, agendado por cron, sessão nova a cada disparo; o agente tem WebSearch, o repo e o histórico do radar; o prompt é fino e aponta para um **contrato versionado** (`radar/AGENTE.md`) — mudar o processo é editar arquivo, com diff e revisão.
- **C — Manual (o editor roda quando lembra)**: exatamente o problema que queremos eliminar.

## Decisão

**B.** Routine diária → sessão nova → segue `radar/AGENTE.md` → escreve **somente** em `radar/` → push na main. A promoção de um item do radar a mudança no livro continua exigindo o ciclo spec-kit com humano (fronteira de autonomia: a lição dos caps. 07 e 16 aplicada ao próprio projeto — o agente vigia, o editor decide).

## Consequências

- `radar/` vira a fila de entrada do gatilho extraordinário do ADR 0007.
- O custo é 1 sessão de agente/dia, limitada (~30 min de orçamento declarado no contrato).
- Pausar/ajustar = desabilitar a Routine ou editar `radar/AGENTE.md`; nada disso toca o livro.
