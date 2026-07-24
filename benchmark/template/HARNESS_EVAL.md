# HARNESS_EVAL — <nome do harness>

<!-- Instrumento padrão do benchmark. Copie este arquivo para benchmark/avaliacoes/<harness>.md e preencha.
     Regra de ouro: toda afirmação exige evidência (caminho de arquivo no código-fonte). Sem evidência, não pontua.
     Escala: 0 Ausente · 1 Básico · 2 Sólido · 3 Referência (ver benchmark/README.md). -->

## Metadados

- **Repositório / versão ou commit avaliado:**
- **Linguagem / stack:**
- **Licença:**
- **Data da avaliação:**
- **Posicionamento declarado** (produto, port didático, pesquisa, framework):
- **Arquétipo observado** (pode divergir do declarado):

## Dimensões

<!-- Para cada dimensão: Existe? / Onde (paths) / Como (2–4 frases) / Nota 0–3 -->

### 1. Loop do agente — Nota: _
Como o ciclo prompt→tool→resultado é estruturado? Streaming? Limite de turnos? Retry/backoff?
Detecção de loop? Quem decide quando parar (heurística, LLM-check, contador)? O loop é durável?

### 2. Entrega de contexto — Nota: _
Como monta o system prompt? Arquivo de regras de projeto (AGENTS.md/equivalente)? Descoberta
hierárquica? Prompt varia por modelo? Injeção mid-conversation? Cache-awareness?

### 3. Compactação / janela de contexto — Nota: _
Disparo automático (limiar)? Sumarização via LLM? Prune/truncamento de tool outputs?
Caminho reativo para "prompt too long"? O que é preservado?

### 4. Design de ferramentas — Nota: _
Quantas built-in e em quais categorias? Schema derivado de tipos ou manual? Tools variam
por modelo/modo? Read-only explícito? Execução paralela?

### 5. MCP — Nota: _
Cliente e/ou servidor? Transportes (stdio/HTTP/SSE)? OAuth? Reconexão/resiliência?
Resources, prompts, roots?

### 6. Permissões e sandboxing — Nota: _
Modos de aprovação? Regras/wildcards? Parsing de comandos shell? Caminhos sensíveis fixos?
Sandbox de SO (Seatbelt/Landlock/Docker)? Trusted folders? Permissões de subagente?

### 7. Memória e estado — Nota: _
Persistência de sessão (formato)? Resume/revert? Memória de longo prazo (formato, seleção
por relevância)? Checkpointing do workspace (git)? Compartilhamento?

### 8. Planejamento — Nota: _
Plan mode (read-only imposto)? Artefato de plano persistido? Aprovação gatekeepa execução?
Todo list? Decomposição com dependências?

### 9. Subagentes / orquestração — Nota: _
Mecanismo de delegação? Isolamento (sessão-filha, processo, worktree)? Permissões derivadas?
Comunicação inter-agente? Limites de terminação? Delegação remota (A2A)?

### 10. Verificação / evals — Nota: _
Testes do harness (cobertura, política de mocks)? Evals comportamentais (juiz LLM)?
Baselines de regressão (perf/memória)? Verificação em runtime (LSP, lint pós-edição)?
Segurança testada (injection)?

### 11. Extensibilidade — Nota: _
Hooks (quantos eventos, que profundidade)? Plugins/skills/comandos custom (formatos)?
Compatibilidade com ecossistemas externos? Provedores de modelo suportados?
Segurança do código de extensão?

### 12. Interfaces — Nota: _
TUI? Headless com saída estruturada (JSON/NDJSON)? IDE? CI (Actions)? Protocolos de agente
(ACP/A2A)? Chat? SDK embutível?

## Dimensões suplementares (não entram no total 0–36; reportar sempre que houver evidência)

### 13. Aprendizado / auto-melhoria — Nota: _
O agente escreve skills/procedimentos reutilizáveis a partir da própria experiência? Quem
decide capturar (gatilho autônomo)? Onde salva (formato — SKILL.md/agentskills.io)? Como
reencontra (índice/busca)? Há curadoria/manutenção (consolidação, poda, anti-padrões)?
(Dimensão promovida pela evidência do Hermes Agent; suplementar até haver massa crítica.)

### 14. Proatividade / agendamento — Nota: _ (obrigatória na categoria agentes pessoais)
Heartbeat/turnos periódicos? Cron/rotinas persistentes? Wake por eventos externos (webhooks,
e-mail)? Controle de custo da proatividade (contexto leve, activeHours)?

## Síntese

### Tabela de notas

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | |
| 2 | Entrega de contexto | |
| 3 | Compactação | |
| 4 | Ferramentas | |
| 5 | MCP | |
| 6 | Permissões/sandbox | |
| 7 | Memória/estado | |
| 8 | Planejamento | |
| 9 | Subagentes | |
| 10 | Verificação/evals | |
| 11 | Extensibilidade | |
| 12 | Interfaces | |
| | **Total (0–36)** | |

### Leitura

- **Perfil/arquétipo:**
- **3 pontos mais fortes** (com evidência):
- **2 pontos mais fracos:**
- **Recurso distintivo** (o que ele tem que nenhum outro avaliado tem):
- **"O que roubar"** (1–3 ideias que outros harnesses deveriam adotar):
- **Cláusula de expiração** (quais componentes existem por limitação atual dos modelos e tendem a desaparecer):
