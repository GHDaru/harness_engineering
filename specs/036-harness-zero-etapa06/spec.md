# Spec 036: harness-zero etapa 06 — permissoes (cap. 07)

- FR-001: PermissionPolicy como DOMINIO PURO (funcao decide(tool,args) -> permitir|perguntar|negar): paths sensiveis fixos NEGADOS (.env, .ssh, chaves); write_file exige APROVACAO humana; resto permite.
- FR-002: aprovacao inline: "perguntar" pausa o turno (pendencia com id); POST /aprovar|/negar retoma o loop do ponto exato; botoes no chat (evolucao justificada).
- FR-003: negacao vira TEXTO para o modelo (ele decide o que fazer); trace 🛡; etapa autocontida sobre a 05; smoke verificado; README (06 ✅).
