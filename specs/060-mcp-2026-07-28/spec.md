# Spec 060: MCP 2026-07-28 — revisão do cap. 06 (gatilho extraordinário)

**Feature Branch**: `060-mcp-2026-07-28` · **Criada em**: 2026-07-31 · **Origem**: radar/diario/2026-07-31.md (impacto A) · ADR 0007 (gatilho: Leitura executiva invalidada)

## Requisitos

- FR-001 (cap. 06, impacto A): nova seção do estado da arte "A guinada stateless (2026-07-28)" com as mudanças da spec (núcleo stateless sem `initialize`/`Mcp-Session-Id`, MRTR, extensões, cache `ttlMs`, depreciações com janela de 12 meses), com fontes oficiais; **Leitura executiva reescrita**; "o que roubar" corrigido (fallback SSE → transporte depreciado); fonte da indústria adicionada; datação atualizada (revisão 2026-07-31).
- FR-002 (cap. 17, impacto B): nota no estado da arte — a guinada stateless + primeira política formal de depreciação como sinal de protocolo entrando em fase de infraestrutura.
- FR-003 (etapa 07, impacto B): nota na docstring do `ClienteMCP` e no "Mão na massa" do cap. 06 — o handshake ensinado é o protocolo 2025-06 (válido na janela de 12 meses); a 2026-07-28 o removeu.
- FR-004 (cap. 04, impacto C): uma frase — o `ttlMs` no `tools/list` é o protocolo absorvendo cache como contrato.
- FR-005: siglas novas (MRTR, CIMD, DCR) no mapa do motor + glossário; entrada da release na Bibliografia; RADAR status → promovido (spec 060); HISTORICO 0.55.
- FR-006: Princípio I — toda afirmação nova com fonte verificada NESTA sessão (anúncio oficial + changelog); nada de memória.
