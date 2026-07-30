# Contrato do agente do Radar Diário

> Este arquivo é a **fonte da verdade** do agente agendado (Routine diária). O prompt da
> Routine manda ler este contrato e segui-lo — mudar o processo = editar este arquivo.
> Decisão e fronteiras: [ADR 0008](../adr/0008-radar-diario-automatizado.md) · cadência: [ADR 0007](../adr/0007-cadencia-livro-vivo.md).

## Missão (1 execução por dia)

Alimentar o livro vivo com um roadmap de auto-atualização priorizado. Você **não edita o livro** — você produz insumo auditável para o ciclo editorial.

## Passos

1. **Contexto**: leia `radar/RADAR.md`, a entrada diária anterior em `radar/diario/`, o placar de expiração em `livro/HISTORICO.md` e as "Leituras executivas" dos capítulos que for avaliar.
2. **Busca** (WebSearch; 6–10 consultas objetivas):
   - releases/mudanças relevantes dos 16 sistemas do corpus (ver `livro/apendice-estudo.md`);
   - protocolos (MCP, A2A, ACP) e specs novas;
   - ferramentas/harnesses novos candidatos ao estudo (teste de inclusão do cap. 01 §4);
   - papers novos sobre as dimensões do benchmark.
3. **Avaliação**: para cada achado, responda — afeta qual capítulo? Invalida alguma Leitura executiva (⇒ gatilho extraordinário do ADR 0007)? Impacto **A** (invalida síntese), **B** (atualiza seção/Apêndice A), **C** (nota de rodapé/observação).
4. **Escrita**:
   - `radar/diario/AAAA-MM-DD.md`: consultas feitas, achados, descartes **com motivo** (Princípio I: sem fonte verificada, não entra);
   - `radar/RADAR.md`: atualize a tabela priorizada (deduplicando; um item já registrado só muda de status) e a seção de Leituras executivas em risco.
5. **Publicação**: commit `radar: AAAA-MM-DD` **apenas com arquivos de `radar/`** e push na `main` (retry com backoff se falhar).

## Regras duras

- **Escrita somente em `radar/`**. Nunca edite `livro/`, `publicar/`, `chat-companion/`, `benchmark/` ou specs — mesmo que o achado pareça urgente: registre como impacto A e pare.
- **Sem fabricação**: todo item com link verificado nesta execução; incerteza marcada como ⏳.
- **Sem segredos** em arquivos/commits; **sem identificador de modelo** em commits ou artefatos (assinatura: "Claude Code (Anthropic)" quando necessário).
- Falhou a busca/rede? Registre a execução com o que houve — execução vazia também é dado.
- Orçamento: ~30 min de trabalho; priorize profundidade sobre cobertura quando precisar cortar.

## Formato da tabela do RADAR.md

| Data | Item (com link) | Capítulo | Impacto | Ação sugerida | Status |
|---|---|---|---|---|---|

Status: `novo` → `avaliando` → `promovido (spec NNN)` | `descartado (motivo)`.
