# Spec 042: harness-zero etapa 12 — skills (cap. 16)

- FR-001: salvar_skill -> skills/pendentes/ (NUNCA em vigor sozinha: anti-padrao prompt-injection persistente); humano aprova (POST /skills/aprovar) ou rejeita.
- FR-002: aprovadas entram como CAMADA do MontadorDeContexto (so nome+quando_usar; conteudo sob demanda via ler_skill — progressive disclosure).
- FR-003: janela /skills; smoke (pendente fora do contexto; aprovada dentro; ler_skill); README (12 ✅).
