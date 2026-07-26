# Spec 008 — Cap. 12 (Extensibilidade) ao esqueleto v3

> Parte da iniciativa spec 003. Ciclo spec-kit completo, na branch `003-reescrita-editorial-v3`; merge ao fim. Princípios I–IV.

## Problema

O capítulo 12 está em pré-v3. O conteúdo atual capta bem a rodada 1 e as **três estratégias de ecossistema** (profundidade · empacotamento · interoperabilidade) e os eixos (hooks · skills/comandos · plugins · provedores). Falta: estrutura v3; fundamentos científicos (a literatura acadêmica dedicada é **rarefeita** — registrar honestamente e ancorar em SE clássica: princípio aberto-fechado, arquitetura de plugins/microkernel, separação mecanismo×política); fontes da indústria (hooks, plugins/marketplaces, comandos custom, settings, provider-agnosticism); e o Apêndice A com rodadas 2, que trazem dados fortes: os formatos (SKILL.md/AgentSkills/.claude-plugin) estão virando **padrões portáveis entre harnesses**, surgiram **marketplaces com scan de segurança** (ClawHub), e a segurança de extensão fechou a lacuna da rodada 1.

## Escopo

Reescrever `livro/capitulos/12-extensibilidade.md` no esqueleto v3 e sincronizar `livro/bibliografia.md` (Cap. 12 + linha de indústria).

## Critérios de aceitação

- [ ] Selo de captura (2026-07); Objetivos (Bloom) ↔ Verificação 1:1.
- [ ] Fundamentos: registrar a lacuna acadêmica; ancorar em SE clássica (aberto-fechado, microkernel/plugin, mecanismo×política) com referências reais; segurança de extensão via literatura adjacente.
- [ ] Fontes da indústria verificadas (hooks, plugins/marketplaces, comandos custom, settings, agnosticismo de provedor), com regra de tradução.
- [ ] Estado da arte: três estratégias; a convergência de formatos (o "MCP da extensibilidade"); marketplaces + scan de segurança; hooks convergindo num vocabulário de eventos; provider-agnosticism declarativo.
- [ ] Mão na massa: etapa 11 do harness-zero (`11-hooks` — hooks pre/post tool).
- [ ] Síntese + "o que roubar"; Apêndice A por repositório (rodadas 1+2+frameworks).
- [ ] Build sem erros; nenhuma URL/ID inventado; não-verificados marcados; lacuna acadêmica registrada.

## Não-objetivos
- Não alterar notas do benchmark. Não mesclar para main. (Skills/aprendizado ficam no cap. 16; MCP no cap. 06 — citados só como vizinhos.)
