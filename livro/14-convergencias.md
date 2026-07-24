# 14 — Convergências e Tendências

## O achado central da primeira rodada

Três harnesses, três stacks (Effect-TS, TypeScript, Python), três origens (startup independente, big tech, academia/porta didática) — e uma convergência arquitetural notável. Sem coordenação, os três chegaram a:

1. **Arquivo de contexto hierárquico na raiz do projeto** — `AGENTS.md` / `GEMINI.md` / `CLAUDE.md`: o mesmo artefato com três nomes (cap. 03).
2. **Compactação em escada** — truncar tools → prune → sumarizar via LLM, com disparo automático por limiar (cap. 04).
3. **Schema de tools derivado de tipos** — Effect Schema, classes declarativas, Pydantic: ninguém escreve JSON Schema à mão (cap. 05).
4. **MCP como integração padrão** — três clientes completos sobre os SDKs oficiais (cap. 06).
5. **Plan mode como modo de permissão** — read-only imposto pelo sistema de permissões, não pedido ao modelo (cap. 09).
6. **Hooks de ciclo de vida** — before/after tool, compactação, sessão (cap. 12).
7. **Headless com saída estruturada** — `-p` + JSON/NDJSON para scripting e CI (cap. 13).
8. **Parada por ausência de tool-call + limite de turnos** — a mecânica universal do loop (cap. 02).

Quando implementações independentes convergem assim, a anatomia está consolidada: **isto é a disciplina**, não mais um conjunto de escolhas idiossincráticas. Um harness novo que não implemente os oito itens acima precisa justificar cada ausência.

## Onde ainda há divergência real

As dimensões sem consenso são o mapa das apostas em aberto:

- **Contenção** (cap. 07): política + sandbox de SO obrigatórios (gemini-cli), política + paths sensíveis fixos (OpenHarness), ou só política (opencode)? A divergência mais consequente — é a que define o risco operacional.
- **Multi-agente** (cap. 10): ferramenta pontual, serviço com registry, ou time persistente com mailbox? Três filosofias incompatíveis; o vencedor depende de quão bons os modelos ficarão em coordenação.
- **Quem decide continuar** (cap. 02): heurística estrutural ou uma inferência extra por turno (next-speaker check)?
- **Neutralidade de modelo** (cap. 12): ~26 provedores (opencode) contra vitrine de um ecossistema (gemini-cli). Aposta comercial, não técnica — mas define quem sobrevive à comoditização dos modelos.
- **Evals comportamentais** (cap. 11): só um dos três trata comportamento do agente como superfície de regressão. Previsão fácil: em dois anos, isso será tão obrigatório quanto CI.

## A cláusula de expiração, aplicada

Retomando a tese do capítulo 01 — todo componente de harness é uma prótese para uma limitação atual do modelo. O exercício que todo harness deveria fazer, aplicado ao que estudamos:

| Componente | Existe porque... | Expira quando... |
|---|---|---|
| Compactação | janelas são finitas e caras | contexto longo ficar barato e confiável |
| Plan mode | modelos agem precipitadamente | modelos planejarem espontaneamente sob risco |
| Next-speaker check | o modelo não sinaliza bem o fim do turno | protocolos de turno nativos do modelo |
| Policy engine / aprovações | modelos não são confiáveis com ações destrutivas | confiabilidade calibrada e verificável |
| Prompt por família de modelo | modelos respondem diferente a instruções | convergência de instruction-following |
| Subagente para exploração | dumps de arquivos poluem o contexto | contexto abundante + atenção robusta |
| Repo-map / índices de código | o modelo não "carrega" o repo inteiro | contexto de milhões de tokens utilizável |

O que **não** expira: sandbox (contenção é sobre o mundo, não sobre a capacidade do modelo), interfaces, verificação do trabalho (testes/LSP — verdade externa ao modelo), e os protocolos de interoperabilidade (MCP, A2A, formatos de skill). A engenharia de harness de longo prazo mora aí: **na fronteira entre o agente e o mundo, não na muleta para a limitação do modelo**.

## Tendências a acompanhar nas próximas rodadas

1. **Padronização do arquivo de contexto** — a pressão por `AGENTS.md` neutro cross-vendor.
2. **Skills/plugins portáveis** — o OpenHarness já carrega skills do formato Claude Code; um "MCP da extensibilidade" está se formando.
3. **Agente-como-serviço** — A2A server, agent cards, SDKs: harnesses expondo-se uns aos outros.
4. **Segurança como dimensão de primeira classe** — parsing de shell, trusted folders, evals de injection: hoje exceção, amanhã baseline (hipótese a testar no Codex CLI, próximo da fila).
5. **Reversibilidade** — checkpoint git com `/rewind`: quando desfazer é barato, a política pode ser mais frouxa; espere mais harnesses copiando.
6. **O harness mínimo** — na contramão da sofisticação, projetos como mini-swe-agent (~100 linhas) testam quanto do scaffolding o modelo moderno já dispensa. É a cláusula de expiração virando experimento.

---

*Este capítulo é vivo: cada nova rodada do benchmark (`benchmark/`) o atualiza — confirmando convergências, resolvendo divergências ou aposentando componentes expirados.*
