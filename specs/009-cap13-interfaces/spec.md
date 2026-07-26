# Spec 009 — Cap. 13 (Interfaces) ao esqueleto v3

> Parte da iniciativa spec 003. Ciclo spec-kit completo, na branch `003-reescrita-editorial-v3`; merge ao fim. Princípios I–IV. Último capítulo de funcionalidade da iniciativa.

## Problema

O capítulo 13 está em pré-v3. O conteúdo atual capta bem a rodada 1 e as **três visões** (produto multi-plataforma · serviço de plataforma · colega no chat) e a lição estrutural (quanto mais cedo a fronteira núcleo/interface, mais interfaces cabem). Falta: estrutura v3; fundamentos (literatura acadêmica dedicada **rarefeita** — registrar; ancorar em HCI: mixed-initiative, Guidelines for Human-AI Interaction, levels of automation, human oversight/automation bias); fontes da indústria (multi-surface, headless/SDK, IDE, UX de aprovação/streaming, ambient/async agents); e o Apêndice A com rodadas 2, que trazem: explosão de **canais de chat + voz** (OpenClaw ~23 canais), o padrão **ProductAdapter/mesmo-contrato-de-turn** (a superfície não pode bypassar a auth do core), superfície **cloud/remota** (Codex), e superfícies de input novas (Aider watch mode, Live Canvas).

## Escopo

Reescrever `livro/capitulos/13-interfaces.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (Cap. 13 + linha de indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07); Objetivos (Bloom) ↔ Verificação 1:1.
- [ ] Fundamentos: registrar a lacuna; ancorar em HCI (mixed-initiative Horvitz; Amershi et al. Guidelines; levels of automation Sheridan-Verplank; automation bias) com referências reais.
- [ ] Fontes da indústria verificadas (multi-surface, headless/SDK, IDE, UX de interação, chat/ambient), com regra de tradução.
- [ ] Estado da arte: três visões; headless estruturado como table-stakes; a explosão de canais + voz; o padrão mesmo-contrato-de-turn (superfície ≠ backdoor); superfície cloud/remota; input escapando do terminal.
- [ ] Mão na massa: a etapa 0 (o chat = janela de observação) e por que uma 2ª superfície (`--print`) é adapter fino, não reescrita.
- [ ] Síntese + "o que roubar"; Apêndice A por repositório (rodadas 1+2+frameworks).
- [ ] Build sem erros; nenhuma URL/ID inventado; não-verificados marcados; lacuna registrada.

## Não-objetivos
- Não alterar notas do benchmark. Não mesclar para main (a iniciativa mescla a branch inteira ao fim, na T608/registro de edição).
