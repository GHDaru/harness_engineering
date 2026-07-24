# FRAMEWORK_EVAL — <nome do framework>

<!-- Instrumento da categoria "frameworks de harness". Diferente do HARNESS_EVAL: aqui não se
     avalia um agente pronto, e sim um kit para construir agentes. As perguntas centrais são
     "o que impõe" (e com que qualidade) e "o que deixa aberto" (e com que ergonomia).
     Escala 0–3 igual à do benchmark; evidência por arquivo obrigatória. -->

## Metadados

- **Repositório / versão avaliada:**
- **Linguagem / stack:**  | **Licença:**  | **Data:**
- **Filosofia declarada** (grafo, papéis, handoffs, code-as-action, harness-como-SDK...):
- **Origem** (vendor único, fundação, comunidade):

## Eixo A — Primitivas oferecidas (nota 0–3 cada)

### A1. Loop / orquestração — Nota: _
O que o framework dá de loop? Grafo explícito, executor de handoffs, crew de papéis?
Determinismo vs. model-driven? Paralelismo? Detecção de loop/limites?

### A2. Estado e durabilidade — Nota: _
Checkpointing? Persistência plugável? Resume/replay? Time-travel? O estado sobrevive a
reinício de processo?

### A3. Tools e schemas — Nota: _
Como se define uma tool (decorator, classe, derivação de tipos)? Conversão automática?
Paralelismo de tools? Tratamento de erro padronizado?

### A4. Multi-agente — Nota: _
Subagentes/handoffs/crews nativos? Isolamento? Comunicação? Hierarquia?

### A5. Human-in-the-loop — Nota: _
Interrupção/aprovação como primitiva? Pausa durável (sobrevive a dias)? Ou cabe ao usuário
construir?

### A6. Streaming e eventos — Nota: _
Eventos tipados do ciclo de vida? Streaming de tokens e de tool-calls? Fácil de plugar numa UI?

## Eixo B — Fronteiras (descritivo, sem nota)

- **O que o framework IMPÕE** (e não dá para trocar):
- **O que deixa ABERTO** (e o custo de preencher — contexto, compactação, permissões,
  memória, verificação costumam ficar por conta do usuário; liste o que este deixa):
- **Vendor lock-in** (modelos suportados; acoplamento a plataforma/observabilidade paga):

## Eixo C — Protocolos falados (matriz, cap. 17)

| MCP client | MCP server | A2A | ACP | SKILL.md | AGENTS.md |
|---|---|---|---|---|---|
| | | | | | |

## Eixo D — Qualidade de produção (nota 0–3 cada)

### D1. Observabilidade — Nota: _
Tracing nativo? Padrão aberto (OTel) ou plataforma própria?

### D2. Testes e evals — Nota: _
O framework testa a si mesmo? Oferece harness de eval para os agentes construídos?

### D3. Ergonomia — Nota: _
Quantas linhas até um agente útil? Qualidade de docs/exemplos? Curva de aprendizado?

### D4. Ecossistema — Nota: _
Integrações, templates, comunidade, cadência de release, governança.

## Síntese

- **Total A (0–18):**  | **Total D (0–12):**
- **Perfil:** para que classe de harness este framework é a escolha certa?
- **O que roubar** (ideias para harnesses prontos):
- **Teste decisivo:** o que seria mais difícil de construir COM ele do que sem ele?
