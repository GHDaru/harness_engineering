# HARNESS_EVAL — Aider

## Metadados

- **Repositório / versão avaliada:** github.com/Aider-AI/aider · snapshot 2026-07 (fork GHDaru/aider, commit 5dc9490)
- **Linguagem / stack:** Python
- **Licença:** Apache-2.0
- **Data da avaliação:** 2026-07-24 (rodada 2)
- **Categoria:** harnesses de código
- **Posicionamento declarado:** pair-programmer de terminal
- **Arquétipo observado:** o pioneiro da escola **context-first** — troca autonomia de agente por curadoria de contexto + controle humano + git

## Dimensões

### 1. Loop do agente — Nota: 2
Não é um loop de tool-calling: é REPL chat + edição direta (`aider/coders/base_coder.py`: `run`, `send_message`). O único mecanismo iterativo é a **reflexão** (`reflected_message`, máx. 3): dispara quando o modelo pede arquivos fora do chat, o linter acha erros ou testes falham — sempre com confirmação humana. Auto-correção reativa por design, não agente autônomo.

### 2. Entrega de contexto — Nota: 3 ⭐ (referência da coorte)
O **repo-map** (`aider/repomap.py`): extrai definições/referências de símbolos via tree-sitter (queries `.scm` por linguagem), monta um grafo dirigido arquivo→arquivo e roda **PageRank personalizado** — arquivos no chat e identificadores mencionados enviesam o ranking (multiplicadores: ident mencionado ×10, referenciador no chat ×50, privado ×0.1). Renderiza sob orçamento de tokens com busca binária (~1024 tokens default) e cache por mtime (`.aider.tags.cache`). O modelo "enxerga" a estrutura de um repo grande sem carregar arquivos — o caminho alternativo à exploração por agente, e mais barato.

### 3. Compactação — Nota: 2
`aider/history.py` (`ChatSummary`): mantém a cauda recente (~metade do orçamento) e sumariza a cabeça antiga via LLM, recursivo até profundidade 3, com fallback de modelos. Sólido, mas sumarização clássica — sem prune seletivo de outputs nem camadas.

### 4. Design de ferramentas — Nota: 3 ⭐
Em vez de tools JSON, **formatos de edição** que o modelo emite como texto (`aider/coders/*_coder.py`): `whole` (arquivo inteiro), `diff` (blocos SEARCH/REPLACE com aplicação fuzzy), `udiff` (anti-preguiça do GPT-4 Turbo), `patch`, variantes fenced. A seleção é **por modelo** (`aider/models.py`) e — o detalhe de referência — validada empiricamente: a métrica `percent_cases_well_formed` do benchmark mede qual formato cada modelo aplica bem. É a versão mais rigorosa da lição "a interface de edição depende do modelo" (cap. 05).

### 5. MCP — Nota: 0
Inexistente — primeiro zero do benchmark. Coerente com a filosofia (acesso ao mundo via shell sugerido e arquivos/URLs no chat), mas em 2026 a ausência é uma lacuna objetiva.

### 6. Permissões e sandboxing — Nota: 2
A rede de segurança é o **git** (toda edição vira commit reversível) + confirmações interativas (`io.confirm_ask`: rodar shell, corrigir lint/testes, "Edit the files?"). Sem sandbox de processo (docker só no benchmark). Segurança = git + humano no loop.

### 7. Memória e estado — Nota: 3 ⭐
Estado **git-nativo** (`aider/repo.py`): auto-commit atômico por rodada com mensagem gerada por LLM, atribuição de autoria configurável, `aider_commit_hashes` rastreando o que a IA fez, `dirty_commit` isolando mudanças pendentes. `/undo`, `diff` e `blame` viram a interface de memória. Complementos: `.aider.chat.history.md`, `--restore-chat-history`. Antecipou em anos o "checkpoint git" que o gemini-cli consagrou.

### 8. Planejamento — Nota: 2
Planejamento por modos de coder: `/ask` (discute sem editar), `/architect` (raciocina o "como" antes de delegar a execução), `/context` (usa o repo-map para convergir no conjunto de arquivos a editar). Plan-then-edit leve, sem artefato de plano persistido nem todo list.

### 9. Subagentes / orquestração — Nota: 2
O split **architect→editor** (`architect_coder.py`): um modelo raciocinador produz o plano; após confirmação, um segundo coder (com `editor_model` e `editor_edit_format` próprios) executa. Orquestração de dois papéis com modelos distintos — elegante, profundidade fixa 1.

### 10. Verificação / evals — Nota: 3 ⭐
Dois níveis: (a) **benchmark Polyglot próprio** (`benchmark/benchmark.py`, exercícios Exercism multi-linguagem, em docker), com `pass_rate_1/2` e `percent_cases_well_formed` alimentando o leaderboard público e as escolhas de edit format — engenharia guiada por eval como poucos; harness SWE-bench incluso. (b) **Hooks de lint/test em runtime**: após cada edição, `auto_lint` (default on) e `auto_test` rodam e falhas viram reflexão de auto-correção.

### 11. Extensibilidade — Nota: 3
Provedores via **LiteLLM** (praticamente qualquer LLM), config em camadas (`.aider.model.settings.yml`, metadata JSON, env, dezenas de flags), `ModelSettings` por modelo (edit format, weak/editor model, reasoning) e **scripting API** (`Coder.create()` importável).

### 12. Interfaces — Nota: 3
CLI/REPL rica (prompt_toolkit, streaming markdown), browser UI (Streamlit), **watch mode** (`aider/watch.py`: comentários `ai!`/`ai?` no código de qualquer IDE viram comandos), voz-para-código, imagens/URLs no chat, copy/paste para web-chat.

## Síntese

| # | Dimensão | Nota |
|---|---|---|
| 1 | Loop do agente | 2 |
| 2 | Entrega de contexto | **3** |
| 3 | Compactação | 2 |
| 4 | Ferramentas | **3** |
| 5 | MCP | **0** |
| 6 | Permissões/sandbox | 2 |
| 7 | Memória/estado | **3** |
| 8 | Planejamento | 2 |
| 9 | Subagentes | 2 |
| 10 | Verificação/evals | **3** |
| 11 | Extensibilidade | **3** |
| 12 | Interfaces | **3** |
| | **Total** | **28/36** |

- **Perfil/arquétipo:** a escola context-first em estado puro — as notas 3 estão exatamente onde a filosofia aposta (contexto, formatos de edição, git, evals) e as lacunas exatamente onde ela abre mão (loop autônomo, MCP, sandbox).
- **Pontos mais fortes:** repo-map (tree-sitter + PageRank personalizado + orçamento de tokens); edit formats validados por benchmark próprio; estado git-nativo.
- **Pontos mais fracos:** MCP ausente; autonomia limitada a 3 reflexões com confirmação.
- **Recurso distintivo:** `percent_cases_well_formed` — medir empiricamente qual formato de edição cada modelo domina, e escolher por dados.
- **"O que roubar":** repo-map como alternativa barata à exploração por subagente; watch mode (`ai!` em comentário); benchmark próprio guiando decisões de design.
- **Cláusula de expiração:** o repo-map expira quando contexto de milhões de tokens for utilizável e barato; os edit formats expiram se os modelos convergirem num formato universal confiável — o próprio benchmark do Aider medirá essa expiração.
