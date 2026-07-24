# 07 — Permissões e Sandboxing

## O problema

Um agente com shell é um usuário com shell: pode apagar arquivos, exfiltrar credenciais, fazer chamadas de rede. Os mecanismos de controle são a resposta do harness a duas ameaças distintas: o **erro** (o modelo faz algo destrutivo por engano) e o **ataque** (prompt injection convence o modelo a agir contra o usuário). Esta é a dimensão de maior divergência entre os harnesses estudados — sinal de que a indústria ainda não convergiu.

Dois níveis de defesa, frequentemente confundidos:
1. **Permissões** (política): regras sobre o que o agente *pode pedir* — aprovação interativa, allowlists, modos.
2. **Sandbox** (contenção): limites impostos pelo SO sobre o que o processo *consegue fazer* — mesmo que a política falhe.

## Padrões de implementação

- **Modos de aprovação** — o espectro consagrado: default (pergunta), auto-edit (edições livres, shell pergunta), plan (read-only), yolo/full-auto (tudo).
- **Rulesets com wildcards** — regras `allow | ask | deny` casadas por padrão glob contra tool + argumento.
- **Parsing de comandos shell** — entender o comando antes de julgá-lo (redirecionamentos, wrappers, encadeamentos).
- **Caminhos sensíveis hardcoded** — negar sempre `.ssh`, credenciais, chaves — independente de configuração.
- **Sandbox de SO** — Seatbelt (macOS), Landlock (Linux), containers Docker/Podman.
- **Trusted folders** — o diretório como fronteira de confiança para carregar hooks/agentes/config.

## Como os harnesses estudados implementam

### gemini-cli — o estado da arte entre os estudados
A área mais desenvolvida do projeto. Um **policy engine determinístico** (`packages/core/src/policy/policy-engine.ts`) avalia cada `FunctionCall` contra regras priorizadas (`PolicyRule`, wildcards, regras específicas para MCP), com **parsing real de shell** (`parseCommandDetails`, `stripShellWrapper`, detecção de redirecionamento) — o harness entende o comando antes de decidir. Regras carregáveis de TOML (inclusive via extensions). Quatro `ApprovalMode`: default, autoEdit, yolo, plan. **Sandbox de SO nativo**: 6 perfis Seatbelt no macOS (`sandbox-macos-*.sb`: permissive/restrictive/strict × open/proxied) e Docker/Podman (`services/sandboxManager.ts`), com proxy de rede opcional. **Trusted folders** (`FolderTrustDiscoveryService`) gatekeepam a execução de hooks e agentes por diretório. Confirmações fluem por um message-bus assíncrono.

### OpenHarness — defesa em profundidade pragmática
`src/openharness/permissions/checker.py`: regras de path (glob allow/deny), comandos negados e três modos (`DEFAULT`, `PLAN`, `FULL_AUTO`). O detalhe mais instrutivo: uma lista **hardcoded de caminhos sensíveis sempre negados** (`SENSITIVE_PATH_PATTERNS`: `*/.ssh/*`, `*/.aws/credentials`, `.gnupg`, `.kube/config`, e os próprios arquivos de credencial do harness) — proteção que nenhuma configuração desliga, pensada explicitamente contra prompt injection. Sandbox via wrapper do `sandbox-runtime` (`sandbox/adapter.py`) com allowlist de domínios de rede, backend Docker alternativo, e `trust_env=False` nas tools web contra SSRF.

### opencode — política elegante, contenção fraca
Modelo de **ruleset com wildcards** (`packages/opencode/src/permission/`): `evaluate()` faz last-match-wins de regras `allow | ask | deny` casadas por glob, default `ask`; pedidos pendentes viram `Deferred` + evento para a UI aprovar (com "always"). Agentes têm rulesets próprios (o agente `plan` nega edições) e **subagentes derivam permissões restritas** do pai — um refinamento que os outros não têm. Porém, **sem sandbox de SO no core**: a contenção é só política + aprovação; containers ficam nos pacotes enterprise. É a lacuna relativa mais clara do opencode.

## Síntese

| Aspecto | opencode | gemini-cli | OpenHarness |
|---|---|---|---|
| Modos de aprovação | rulesets por agente | 4 modos + policy engine | 3 modos |
| Parsing de shell | glob sobre comando | parsing estrutural | comandos negados |
| Paths sensíveis fixos | — | via políticas | hardcoded, indesligável |
| Sandbox de SO | — (enterprise) | Seatbelt (6 perfis) + Docker | srt + Docker |
| Trusted folders | — | sim | — |
| Permissões de subagente | derivadas e restritas | por política | sincronizadas (swarm) |

A lição transversal: **política sem contenção é aposta na obediência do modelo**. O gemini-cli é o único dos três que trata as duas camadas como obrigatórias. A lista indesligável de caminhos sensíveis do OpenHarness é a ideia mais barata e mais exportável do capítulo — qualquer harness deveria tê-la. Esta dimensão será o principal critério de avaliação do Codex CLI na próxima rodada do benchmark (seu sandbox Landlock/Seatbelt é referência declarada da categoria).
