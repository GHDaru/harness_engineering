# Spec 056: Radar diário — roadmap de auto-atualização do livro vivo

**Feature Branch**: `056-radar-diario` · **Criada em**: 2026-07-29

## Conceito

Uma **sessão de agente agendada (Routine, 1×/dia)** roda de forma autônoma e alimenta o livro vivo: busca novidades do ecossistema, avalia o impacto contra o corpus e as Leituras executivas, e mantém um **roadmap de auto-atualização** versionado em `radar/`. O agente diário **não edita o livro** — ele produz o insumo priorizado; quem promove item do radar a edição é o ciclo editorial normal (spec-kit + humano), conforme o ADR 0007 (gatilho extraordinário) e o ADR 0008 (fronteira de autonomia).

## Requisitos

- FR-001: contrato do agente diário versionado em **`radar/AGENTE.md`** (o prompt-fonte da Routine): o que buscar (releases dos 16 harnesses do corpus, protocolos MCP/A2A/ACP, papers, ferramentas novas candidatas ao estudo), como avaliar (dimensões do benchmark; qual capítulo/Leitura executiva é afetado), onde escrever, e as **regras duras** (só `radar/`; sem segredos; sem identificador de modelo; commits `radar: AAAA-MM-DD`).
- FR-002: **`radar/RADAR.md`** — o roadmap vivo: tabela priorizada (item · fonte · capítulo afetado · impacto A/B/C · ação sugerida · status) + seção "⚠ Leituras executivas possivelmente invalidadas" (aciona o gatilho do ADR 0007).
- FR-003: entradas diárias em **`radar/diario/AAAA-MM-DD.md`** (o bruto do dia: o que foi buscado, achados, descartes com motivo) — auditável como tudo no projeto.
- FR-004: Routine criada (cron diário, sessão nova por disparo, mesmo ambiente) com o prompt apontando para `radar/AGENTE.md` como fonte da verdade — mudar o processo = editar o arquivo, sem tocar no agendamento.
- FR-005: ADR 0008 registra a decisão e as alternativas (GitHub Action com LLM × Routine de sessão-agente × manual).

## Fronteira de autonomia (a regra de ouro do cap. 07 aplicada a nós)

O agente diário tem escrita **apenas** em `radar/` (+ push na main desses arquivos). Qualquer mudança em `livro/`, `publicar/`, `chat-companion/` exige o ciclo spec-kit com curadoria humana. Skills auto-aprovadas são prompt injection persistente (cap. 16) — o mesmo vale para radar auto-promovido a edição.
