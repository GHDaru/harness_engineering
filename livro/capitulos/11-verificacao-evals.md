# 11. Verificação e Evals

> **Estado da arte capturado em 2026-07** · última revisão 2026-08-12 · [histórico e registro de expiração](../HISTORICO.md)
>
> Camada didática v4 — ver [Guia Editorial §2.1](../GUIA-EDITORIAL.md).
> andaime: lacuna
>
> Esqueleto v3, corpo com o estado da arte; tratamento por repositório no Apêndice A (complementação online).

## Objetivos de aprendizagem

Ao final deste capítulo, você deve ser capaz de:
1. **Distinguir** as três perguntas da verificação (o harness funciona? · o agente se comporta? · o trabalho está certo?) e a resposta técnica de cada;
2. **Explicar** por que a auto-correção *intrínseca* não basta e a verificação precisa ser externa e ancorada em sinal (testes, LSP (Language Server Protocol), tools);
3. **Avaliar** o *reward hacking*: o agente jogando contra o verificador, e as defesas (held-out, testes imutáveis, anti-mock, verificar o estado final);
4. **Reconhecer** os vieses do juiz LLM (Large Language Model) (posição, verbosidade, self-preference) e como mitigá-los;
5. **Implementar** uma suíte de evals do harness-zero (juiz + respostas gravadas) na etapa 10.

## O agente que fazia os testes passarem

A suíte estava verde havia três semanas. Todo commit do agente entrava com o mesmo relatório: *"corrigido, testes passando"*.

Aí a regressão apareceu em produção, num caminho que a suíte cobria. Alguém foi ler o transcript do dia em que aquele código foi tocado, e encontrou o passo que "consertou":

```python
@pytest.mark.skip(reason="flaky in CI")
def test_expiracao_de_sessao():
```

O agente não mentiu. Ele fez o que foi pedido, com uma interpretação impecável do enunciado: *"faça os testes passarem"*. Um teste marcado como pulado passa.

Repare no que aconteceu com o verificador. Enquanto ele era só um observador, media qualidade. No momento em que virou **alvo**, quando "verde" passou a ser o objetivo do agente e não a consequência do trabalho —, ele deixou de medir qualquer coisa.

É a Lei de Goodhart num arquivo de teste, e é o problema central deste capítulo. Verificação de agente não é sobre ter testes. É sobre ter testes que **continuam significando alguma coisa** quando alguém está otimizando contra eles.

## O problema

Como saber se o agente funciona? A pergunta se desdobra em três, com respostas técnicas diferentes:

1. **O harness funciona?**: testes de software clássicos sobre o código do harness (loop, tools, permissões).
2. **O agente se comporta bem?**: evals: o comportamento emergente (usa as tools certas? é frugal? respeita o plan mode? resiste a injection?) sob teste de regressão.
3. **O trabalho do agente está certo?**: verificação em runtime: sinais (LSP, testes, lint) realimentados ao modelo durante a tarefa.

A segunda é a mais difícil e a mais negligenciada: comportamento de agente é estocástico, caro de testar e muda silenciosamente a cada troca de modelo ou de prompt. E há uma quarta pergunta que a rodada 2 tornou incontornável: **o agente está trapaceando o verificador?**

## Fundamentos científicos

A ciência da verificação de agentes tem três mensagens duras, e todas empurram para o mesmo lugar: verificação **externa e ancorada**.

- **Grading por execução, não por aparência**: [SWE-bench, arXiv 2310.06770](https://arxiv.org/abs/2310.06770) (ICLR '24) verifica aplicando o patch do modelo e rodando os **testes reais e ocultos** do repositório (FAIL_TO_PASS + PASS_TO_PASS). Decisão: para código, o único sinal confiável é "os testes reais passaram", não similaridade de diff. E [SWE-agent, arXiv 2405.15793](https://arxiv.org/abs/2405.15793) mostra que a **ergonomia das tools** (a Agent-Computer Interface) dirige o sucesso tanto quanto o modelo.
- **A auto-correção intrínseca não basta**: [Large Language Models Cannot Self-Correct Reasoning Yet, arXiv 2310.01798](https://arxiv.org/abs/2310.01798) é o contra-resultado decisivo: sem feedback externo, pedir ao modelo que "revise" pode *degradar* respostas certas. Decisão: "pedir ao modelo para se conferir" **não é** estratégia de verificação, o harness precisa fornecer um verificador. [CRITIC, arXiv 2305.11738](https://arxiv.org/abs/2305.11738) mostra o caminho: auto-crítica **ancorada em tool** (o código roda? o fato confere?) supera introspecção; [Self-Consistency, arXiv 2203.11171](https://arxiv.org/abs/2203.11171) dá a versão barata (amostrar caminhos + voto) para respostas checáveis.
- **O juiz LLM funciona, com vieses**: [Judging LLM-as-a-Judge, arXiv 2306.05685](https://arxiv.org/abs/2306.05685) mede ~80% de acordo com humanos, mas documenta vieses de **posição, verbosidade e self-preference**. Decisão: randomize/troque a ordem das respostas e faça a média, dê rubrica e resposta-referência, e calibre contra um gold set humano ([survey, arXiv 2411.15594](https://arxiv.org/abs/2411.15594)), um único call de juiz não é ground truth. E verifique o **estado final do mundo**, não o transcript: [τ-bench, arXiv 2406.12045](https://arxiv.org/abs/2406.12045) mostra que `pass@1` esconde inconsistência brutal (`pass^8` < 25%).
- **O agente joga contra o verificador**: o tema novo e mais importante: com [recompensas verificáveis (RLVR / Tülu 3, arXiv 2411.15124](https://arxiv.org/abs/2411.15124)) um verificador determinístico é sinal e recompensa mais difícil de fraudar — *mas* [reward hacking, arXiv 2606.15385](https://arxiv.org/abs/2606.15385) e [testes randomizados contra trapaça, arXiv 2606.07379](https://arxiv.org/abs/2606.07379) mostram que agentes praticam *specification gaming* zero-shot: apagam asserts, dão `sys.exit(0)`, patcham o pytest. Decisão: mantenha uma métrica de ground-truth **held-out** que o agente nunca otimiza, e **testes imutáveis** que ele não pode tocar.

(Bibliografia completa e ponteiros: `livro/bibliografia.md`.)

## Fontes da indústria

- **O benchmark é o padrão. É contaminável**: [SWE-bench Verified (OpenAI)](https://openai.com/index/introducing-swe-bench-verified/) é o subconjunto de 500 tarefas *humanamente auditadas*, criado porque o SWE-bench cru tinha specs ambíguas e testes quebrados que reprovavam soluções corretas (audite o verificador antes de confiar nele). Mas o [OpenAI parou de reportar SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) por contaminação/memorização, o eval precisa de rotação e held-outs para seguir sendo sinal. O [Terminal-Bench](https://www.tbench.ai/) ([arXiv 2601.11868](https://arxiv.org/abs/2601.11868), repo `harbor-framework/terminal-bench`) leva o rigor ao terminal: cada tarefa embarca **Docker + solução humana + testes de verificação**, gradando o *estado final do ambiente*, não a plausibilidade do transcript.
- **Evals como disciplina de engenharia**: [Define success criteria and build evaluations (Claude)](https://docs.anthropic.com/en/docs/test-and-evaluate/develop-tests): defina critérios mensuráveis *antes*, force o juiz a emitir um veredito discreto e a raciocinar antes de pontuar. O [Demystifying evals for AI agents (Anthropic)](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) decompõe o eval em componentes (task · trial · agent harness · eval harness · trace · grader · suite) e insiste: **grade o estado final, não a última mensagem** (uma resposta pode "soar certa" e a tarefa ter falhado). E reporte o [erro-padrão da média](https://www.anthropic.com/research/statistical-approach-to-model-evals) para distinguir regressão real de ruído.
- **Verificação dentro do loop**: [Effective harnesses for long-running agents (Anthropic)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): cada sessão roda os testes, **verifica a feature end-to-end como um usuário faria** (automação de navegador), deixa um log de progresso e commita limpo. E o [Claude Code best practices](https://code.claude.com/docs/en/best-practices) eleva o TDD ao padrão agêntico mais forte: escreva os testes primeiro, confirme que falham, **commite-os como checkpoint. Implemente sem editá-los**, commitar os testes antes é a rede que revela quando o agente trapaceia alterando o teste em vez de corrigir o código.
- **Ferramental de eval versionado**: [OpenAI Evals](https://github.com/openai/evals), [Inspect (UK AISI)](https://github.com/UKGovernmentBEIS/inspect_ai) (Dataset + Solver + Scorer, com sandbox Docker/K8s, o eval e o sandbox são um só sistema), [promptfoo](https://www.promptfoo.dev/docs/intro/) (um `promptfooconfig.yaml` versionado como gate de CI), [Braintrust](https://www.braintrust.dev/docs/platform/functions/scorers) e [LangSmith](https://docs.langchain.com/langsmith/llm-as-judge) (rubrica como config, correções humanas viram few-shot). Decisão: os checks vivem no controle de versão e rodam no CI como qualquer teste.
- **Verificação virou adversarial**: [Natural emergent misalignment from reward hacking (Anthropic)](https://assets.anthropic.com/m/74342f2c96095771/original/Natural-emergent-misalignment-from-reward-hacking-paper.pdf): agentes aprendem a *gamear o verificador* (sair antes dos testes, patchar o pytest, apagar asserts) e o hábito **generaliza para sabotagem mais ampla**. Decisão: endureça o verificador (testes randomizados/held-out, arquivos de teste imutáveis) e não deixe o agente tocar no próprio grader, o [The Verification Horizon (arXiv 2606.26300)](https://arxiv.org/abs/2606.26300) adverte que, quando a capacidade do agente ultrapassa o verificador, o reward hacking ressurge. O verificador tem de *evoluir* (testes → rubrica → juízes interativos).
- **Consulte também**: a coleção viva [Awesome Harness Engineering: Verification & CI Integration](https://github.com/GHDaru/awesome-harness-engineering#verification--ci-integration) e [Awesome Harness Engineering — Evals & Verification](https://github.com/GHDaru/awesome-harness-engineering#evals--verification) reúne mais recursos consultáveis desta dimensão (padrões, artigos e implementações), curados por problema.

## Na prática: um eval determinístico, e depois um juiz que se mede

O primeiro instinto é avaliar o texto que o agente produz. É o instinto errado: texto varia entre execuções, e comparar strings transforma qualquer eval numa fonte de falso alarme.

O que se avalia é **comportamento**, e para isso a primeira peça é remover o não-determinismo:

```python
class ReplayAdapter:
    """LLMPort falso: devolve respostas GRAVADAS, na ordem. Zero rede,
    zero variação, zero custo. O eval passa a testar o HARNESS, não o modelo."""
    def __init__(self, respostas: list[Resposta]):
        self._fila = list(respostas)

    def completar(self, mensagens, tools):
        return self._fila.pop(0)
```

Com ele, um eval vira um teste comum, e testa exatamente o que o livro construiu:

```python
def test_politica_nega_caminho_sensivel():
    llm = ReplayAdapter([
        Resposta(tool_calls=[Chamada("read_file", {"path": "~/.ssh/id_rsa"})]),
        Resposta(texto="não consegui ler o arquivo"),
    ])
    fim = rodar_turno(sessao(llm, modo=Modo.EXECUTAR))

    assert fim.subtype == "sucesso"
    assert "recusado" in fim.trace[0].resultado        # a política agiu (cap. 07)
    assert not Path("~/.ssh/id_rsa").expanduser().read_calls   # e nada foi lido

def test_plan_mode_nega_escrita():
    llm = ReplayAdapter([Resposta(tool_calls=[Chamada("editar", {...})])])
    fim = rodar_turno(sessao(llm, modo=Modo.PLANEJAR))
    assert "planejamento" in fim.trace[0].resultado    # a recusa explica o modo (cap. 09)
```

Três coisas valem a atenção. As asserções são sobre **o que o harness fez**, não sobre o que o modelo disse. Os testes rodam sem rede, então cabem no CI de todo commit. E eles testam as garantias dos capítulos anteriores, política, plan mode, compactação, aprovação —, que é exatamente o que precisa continuar valendo quando alguém mexer no loop.

**Agora a parte que não é determinística.** Nem tudo é asserção: "esta explicação está boa?" não vira `assert`. Aí entra o juiz LLM, e ele precisa ser medido antes de ser usado:

```python
def julgar(pergunta, resposta_a, resposta_b, rubrica):
    """Chama o juiz DUAS vezes, com a ordem invertida. Se ele mudar de
    opinião ao trocar a ordem, o resultado é viés de posição, não veredito."""
    v1 = juiz.completar(PROMPT, pergunta, A=resposta_a, B=resposta_b, rubrica=rubrica)
    v2 = juiz.completar(PROMPT, pergunta, A=resposta_b, B=resposta_a, rubrica=rubrica)
    if v1.vencedor == inverter(v2.vencedor):
        return Veredito(vencedor=v1.vencedor, confianca="alta")
    return Veredito(vencedor=None, confianca="empate por inconsistência")

# LACUNA (etapa 10): o juiz precisa de taxa de erro conhecida. Escreva a
# calibração contra um conjunto anotado por humanos e devolva FNR e FPR.
def calibrar(juiz, gold_set) -> tuple[float, float]:
    ...
```

Rodar duas vezes com a ordem trocada custa o dobro e transforma um viés invisível em **número**. Sem isso, você tem um juiz que prefere a primeira opção e um relatório que parece rigoroso.

E o fecho, que amarra com a cena da abertura: **nenhum desses evals impede o `@pytest.mark.skip`**. O que impede é medir uma coisa que o agente não controla, a contagem de testes que rodaram. Um eval que verifica "a suíte tem 214 testes ativos" custa uma linha e fecha o caminho que três semanas de verde não fecharam.

## O estado da arte

### 1. Três perguntas, três campeões (e a lacuna que fechou)

A moldura da rodada 1 persiste: **OpenHarness** testa melhor *o harness* (121 arquivos por subsistema), **gemini-cli** testa melhor *o agente* (evals com juiz + baselines de regressão), **opencode** verifica melhor *o trabalho* (LSP em runtime → diagnósticos ao modelo no mesmo turno). Mas a lacuna reveladora da rodada 1 ("só um dos três testa comportamento sob ataque") **fechou** na rodada 2: IronClaw trata isolamento cross-tenant como cidadão de teste de primeira classe (com *parity de trace* contra o OpenClaw). Ohmo tem 96 testes adversariais (sessão não vaza para outro remetente, `/config` não vaza segredos).

### 2. A verificação certa é externa e ancorada, porque a interna falha

O achado científico central (a auto-correção intrínseca degrada. A ancorada em tool funciona) é exatamente o que o **LSP em runtime** do opencode faz: o agente descobre que quebrou a tipagem no turno seguinte, não no CI. É a mesma tese da **reflexão do Aider** (disparada por lint/testes falhando, não por introspecção) e do **verify-on-stop do Hermes**, o agente é *forçado* a verificar antes de parar, com `verification_evidence.py` rastreando a evidência. Verificar deixou de ser uma esperança e virou um **estágio imposto do loop**.

### 3. Eval comportamental virou table-stakes, e por categoria

Na rodada 1, só o gemini-cli tratava comportamento como superfície de regressão. Na rodada 2 isso virou norma: o **Goose** publica a **Harbor** (sobre o framework Terminal-Bench, 89 tasks, com **leaderboard real**: stock 50,6% / code-mode 57,3%). O **Codex** tem ~660 snapshots insta; o **Hermes** roda `mini_swe_runner` (estilo SWE-bench); o **n8n** transformou eval em *produto* (nós Evaluation + LLM-judge). E surgiu o eval **por categoria**: o **Personal Agent Benchmark Pack** do OpenClaw (10 cenários da categoria — `personal-redaction-no-secret-leak`, `personal-approval-denial-stop`, `personal-no-fake-progress`, `personal-memory-preference-recall`), o primeiro benchmark comportamental *da categoria agente pessoal*. Um harness sem evals não sabe o que perdeu no último ajuste de prompt.

### 4. O adversário é o próprio agente

A virada mais séria: a verificação virou **adversarial**. A literatura mostra agentes apagando asserts e patchando o pytest para "passar". A defesa da indústria é convergente — **testes imutáveis** (commite os testes primeiro, o agente não os edita), **held-out/randomizado** (o agente não pode overfittar o que não vê), **política anti-mock** (o `AGENTS.md` de teste do opencode proíbe mocks que mentem. O `http-recorder` grava chamadas reais), e **snapshots com drift-check** (OpenClaw) para determinismo onde o juiz é caro. A verificação não é mais só medir acerto, é impedir a trapaça.

> **Adendo (2026-07-31, texto integral verificado): como avaliar o próprio harness, três regras de um paper de método.** O preprint [*Rethinking the Evaluation of Harness Evolution for Agents*](https://arxiv.org/abs/2607.12227) (AI2/UW/indep., 14-jul-2026) testa a moda da "evolução automática de harness" e encontra um resultado incômodo: sob **orçamento equiparado** (K=5 para todos os métodos), ela "does not consistently outperform simple test-time scaling methods", no Terminal-Bench 2.1 (89 tarefas, 3 modelos), amostragem paralela pura levou a média de pass@1 de 68,2 a 72,3 (Tabela 1) enquanto a evolução chegou a **piorar** o GPT-5.4 (75,3→69,7); com testes unitários disponíveis, a amostragem paralela abre 86,0 contra 75,8 (Tabela 2); e em tarefas held-out o ganho médio da evolução é **+0,6** (Tabela 3) — "their gains largely stem from making multiple attempts" (§4.3), porque "most edits memorize fixes rather than distilling strategies" (§5.1), acumulando "context bloat that can offset the remaining gains". As três regras que ficam para quem avalia harness (incluindo este livro): (1) **orçamento equiparado**, todo ganho atribuído a design deve ser reportado contra um baseline de repetição de amostras com o mesmo compute; (2) **separação busca/avaliação**, held-out obrigatório, ou o ganho é overfitting ao conjunto; (3) **sensibilidade do instrumento**, os próprios autores suspeitam que "Terminal-Bench may simply not be very sensitive to harness design" (§5.2): benchmark bom para medir harness precisa de headroom E de desempenho que dependa do harness, senão o sinal é capacidade do modelo. Para o método deste livro (rubrica 0–3 por leitura de código), o paper refina sem contradizer: a rubrica mede a propriedade estrutural sem passar pelo canal contaminado por amostragem, mas herda o dever da **validade convergente** (notas altas deveriam prever desempenho held-out), o risco de overfitting se a régua for calibrada olhando os sistemas que se quer pontuar bem, e o alerta do §5.1: penalizar memorização e inchaço de contexto, não só ausência de recursos. Isso conversa com o cap. 16: se evoluir o harness automaticamente rende menos que re-amostrar, a auto-melhoria barata está no **conhecimento** (skills/memória), não na **estrutura**.

### 5. Verificar o harness que você **tem**, não só o que você escreveu

Tudo acima mede o agente trabalhando. Falta o degrau anterior. Ele é mensurável de forma barata: **o repositório está preparado para ser trabalhado por um agente?** Quando um agente entra num projeto, o harness efetivo não é só o CLI que você abriu, é ele **mais** o que o repositório oferece: instruções que orientam, testes que dão sinal, guarda-corpos que impedem estrago. Dois repositórios com o mesmo modelo e o mesmo CLI produzem resultados diferentes, e a diferença mora aí.

O [Harness Score](https://github.com/paladini/harness-score) (MIT) instrumenta essa pergunta: varre o sistema de arquivos e devolve nível **L0–L4** em seis dimensões que mapeiam quase limpo nos capítulos deste livro, contexto (03), skills (05/12), guarda-corpos (07), sensores e CI (11), higiene (07). O detalhe que interessa a **este** capítulo é a escolha de projeto: *"zero LLM calls, zero network access, and the same result every time you run it"*, cada resultado é *"a filesystem fact"*. É a tese da verificação externa e ancorada aplicada ao próprio ato de medir; o número é discutível, mas **reprodutível**, que é a única propriedade que uma medida precisa ter para sustentar uma discussão.

Duas armadilhas, aprendidas medindo o repositório deste livro (o relato completo, com os números antes e depois, está no [Apêndice — Meça o seu harness](../apendice-harness-score.md)):

- **Prosa não é sensor.** A medição deu 20/20 em contexto e **2/20 em sensores** num repositório com 81 testes: porque os testes existiam em três subdiretórios e nada na raiz os declarava. O `AGENTS.md` dizia onde rodar cada coisa; o agente lê e obedece, mas um hook, um CI ou o próximo colaborador não leem prosa. Documentação excelente **mascara** ausência de instrumento, e a medida sensível separa as duas.
- **Ponto ganho por ausência não é ponto.** A mesma medição aprovava a checagem de *lockfile* com a justificativa *"nothing to lock"*: e reprovou depois que o repositório ganhou um manifesto legítimo. Toda rubrica que pontua "não se aplica" como acerto infla quem faz menos, e faz o placar **não ser monótono sob melhoria honesta**. Vale para escadas de maturidade em geral, inclusive para a régua deste livro.

### Leitura executiva

O que está mais moderno: verificação externa ancorada (LSP/testes no loop, verify-on-stop). Eval comportamental como table-stakes e por categoria (Harbor, Personal Agent Benchmark Pack). O juiz LLM usado com controle de viés. A defesa contra reward hacking (testes imutáveis, held-out, anti-mock); as três regras do adendo para quem avalia o próprio harness (orçamento equiparado, held-out, instrumento sensível a design); e o degrau anterior a todos eles — **medir se o repositório é harnessável**, com instrumento determinístico e sem modelo no caminho. **O que roubar:** realimente sinal real ao modelo no mesmo turno (LSP/testes), não confie na auto-conferência. Commite os testes antes e não deixe o agente editá-los. Grade o estado final, não a última mensagem. Trate evals comportamentais como regressão de primeira classe; e meça o seu repositório antes de culpar o modelo — **prosa não é sensor**, e ponto ganho por ausência não é ponto.

## Mão na massa, harness-zero, etapa 10

A etapa 10 (`harness-zero/etapas/10-evals/`) dá ao harness-zero uma suíte de evals própria: **respostas de LLM gravadas** (replay determinístico em CI, barato e estável) para testar o loop e as tools sem chamar a API. Um **juiz LLM** mínimo que pontua se o comportamento do agente atende a critérios qualitativos (usou a tool certa? respeitou o plan mode?). Fiel à disciplina do capítulo: o juiz emite um veredito discreto e a suíte roda no CI como qualquer teste. Exercício de completude: você adiciona um caso de **teste imutável** (uma tarefa cujo teste o agente é proibido de editar) e observa a diferença entre "passou" e "trapaceou".

## Verificação

1. Seu agente diz "corrigi o bug e os testes passam". Por que isso, sozinho, não é verificação, e o que você faz em vez de confiar?
2. Depois de dar RLVR ao seu agente, o score sobe mas o produto piora. O que provavelmente aconteceu, e que duas defesas você aplica?
3. Você usa um juiz LLM para pontuar respostas abertas. Cite um viés conhecido e como mitigá-lo.
---

## Apêndice A — Como cada repositório trata verificação e evals

> Evidência por harness, com paths — complementação online, expandida a cada rodada.

### gemini-cli (rodada 1) — comportamento sob regressão contínua
Quatro suítes: (1) `evals/` — ~45 testes comportamentais com **juiz LLM** (`llm-judge.ts`) cobrindo frugalidade, memória hierárquica, plan mode, delegação, segurança de shell, **prompt injection via MCP (Model Context Protocol)** e recuperação de sandbox; (2) `integration-tests/` — E2E determinísticos com **respostas gravadas** (`.responses`); (3) `memory-tests/` — regressão contra `baselines.json`, nightly; (4) `perf-tests/` — CPU/startup, nightly. Comportamento como superfície de regressão de primeira classe.

### opencode (rodada 1) — verificação durante a tarefa
**LSP em runtime** (`packages/opencode/src/lsp/`): edições disparam diagnósticos realimentados ao modelo. **Política anti-mock** explícita (o `AGENTS.md` de `test/` proíbe mocks) + `http-recorder` (grava/replaya HTTP real com determinismo). Typecheck obrigatório (`bun typecheck`).

### OpenHarness (rodada 1) — E2E com modelo real
121 arquivos em `tests/`, ~31 subpastas espelhando cada subsistema. Suítes E2E com **chamadas reais de modelo** (`scripts/test_harness_features.py`) e testes contra artefatos reais do ecossistema (`test_real_skills_plugins.py` roda skills do anthropics/skills e plugins do claude-code). Skill `harness-eval` empacota a validação E2E.

### Goose (rodada 2) ⭐ — Harbor com leaderboard público
**Harbor** (`evals/harbor/`): benchmark sobre o framework Terminal-Bench (89 tasks) comparando harnesses/modelos/builds por pass-rate, custo, tokens e turns — com **leaderboard real no README** (stock ~50,6%, code-mode 57,3%) e LLM-judges de pós-processamento; `goose-self-test.yaml`; compactação com ~15 testes inline.

### Codex CLI (rodada 2) — snapshots em escala
~440 arquivos de teste + **~660 snapshots insta**; suíte E2E com turnos reais e backend mockado; testes de política de sandbox por plataforma; parity da compactação remota; CI multi-camada (nextest por plataforma, Bazel, postmerge).

### Hermes (rodada 2) ⭐ — verify-on-stop
32 subdiretórios de teste; **verify-on-stop nudge** (o agente é forçado a verificar antes de parar, com `verification_evidence.py` rastreando evidência); `batch_runner.py` (trajetórias em lote) e `mini_swe_runner.py` (avaliação estilo SWE-bench). Orientação a pesquisa.

### OpenClaw (rodada 2) ⭐ — benchmark da categoria
~8.649 arquivos de teste; **prompt snapshots com drift-check** em CI; stack QA com canal sintético e catálogo YAML de cenários; **Personal Agent Benchmark Pack** — 10 cenários da categoria (`personal-redaction-no-secret-leak`, `personal-approval-denial-stop`, `personal-no-fake-progress`, `personal-memory-preference-recall`…), rodáveis em mock. O primeiro benchmark comportamental *da categoria agente pessoal*.

### IronClaw (rodada 2) ⭐ — isolamento como cidadão de teste
~415 arquivos de teste; fuzzing; **testes de isolamento cross-tenant/agent/project/thread como primeira classe** (`reborn_*_scope_isolation_parity.rs`); **parity de trace gravado contra o OpenClaw**; testes de arquitetura mecanizados; regra que exige testes de denial/redaction/escape para qualquer mudança de sandbox.

### ohmo (rodada 2) — adversarial de canal
**96 testes adversariais** (75 no gateway): sessão não restaura mensagens de outro remetente, `/config show` não vaza segredos, histórico de `/group` sanitizado antes de virar contexto. Lacuna: sem teste de permissão/sandbox — exatamente a dimensão fraca.

### Aider (rodada 2) — reflexão ancorada + leaderboard de edit format
Reflexão (`reflected_message`, máx. 3) disparada quando o linter acha erros ou testes falham (sempre com confirmação humana) — auto-correção **reativa e ancorada**, não introspecção. Famoso por medir empiricamente o formato de edição por modelo (`percent_cases_well_formed`) num leaderboard próprio.

### n8n (rodada 2) — eval como produto
Feature **Evaluations** (nós Evaluation Trigger + Evaluation, UI enterprise) para rodar datasets contra workflows; suíte de evals com LLM-judge no AI Workflow Builder; testes de integração por workflow. Verificação empacotada como recurso vendável.

### OpenHands (rodada 2) — o eval que migrou
Eval de agente **ausente neste repo** (nota 0): o diretório `evaluation/` clássico (o harness SWE-bench pelo qual o OpenHands é histórico) migrou para o `software-agent-sdk`. Aqui há 115 arquivos de testes unitários do app-server, mas zero evals de agente — um lembrete de que a fronteira do que se avalia depende de onde o núcleo vive.

### Frameworks (rodada frameworks)
Os frameworks tratam eval como API: harnesses de eval versionados (OpenAI Evals), Solver+Scorer com sandbox (Inspect), scorers mistos código+juiz (Braintrust/autoevals), rubrica-como-config (LangSmith). O que os harnesses de código montam à mão, o ecossistema de frameworks expõe como ferramenta dedicada.

---

## Respostas da verificação

**1.** Porque o relato do agente e o trabalho do agente vêm da **mesma fonte**, e uma fonte não verifica a si mesma. "Os testes passam" é uma afirmação sobre o mundo feita por quem tem interesse no resultado, e a literatura de auto-correção mostra que modelos não detectam de forma confiável os próprios erros sem sinal externo. O que se faz em vez de confiar: rodar a verificação **fora** do turno do agente e ler o resultado bruto, não o resumo dele. Na prática são três coisas: um comando cuja saída você lê (não a paráfrase), asserções sobre comportamento com um adapter de replay, e pelo menos uma medida que o agente não controla, como o número de testes ativos. A cena da abertura é exatamente o caso em que o relato estava correto e a conclusão, falsa.

**2.** Aconteceu **reward hacking**: o agente encontrou um caminho barato para a recompensa que não passa pela qualidade. Marcar teste como pulado, afrouxar asserção, tratar exceção e seguir, escrever no arquivo de gabarito — todos sobem o score e nenhum melhora o produto. É a Lei de Goodhart, e não é má-fé: é otimização competente de uma métrica mal especificada.

Duas defesas. A primeira é **medir o que o agente não pode editar**: contagem de testes ativos, cobertura em relação a um baseline, resultado de uma suíte mantida fora do alcance dele. A segunda é **separar o conjunto de treino do conjunto de avaliação**, com um conjunto de retenção que o agente nunca vê e cuja queda denuncia a otimização. Some-se uma terceira, mais barata que as duas: **ler os transcripts das execuções que subiram o score**, porque o caminho barato quase sempre é visível na primeira leitura.

**3.** O viés mais bem documentado é o de **posição**: o juiz tende a preferir a primeira resposta apresentada, independentemente da qualidade. A mitigação é a do exemplo acima — chamar o juiz duas vezes com a ordem invertida e só aceitar o veredito quando ele se mantém; quando muda, o resultado não é empate, é **medida de viés**. Outros dois valem menção: **verbosidade**, com o juiz confundindo tamanho com qualidade, mitigado por rubrica explícita que nomeia critérios; e **auto-preferência**, com o juiz preferindo texto do próprio modelo, mitigado por usar como juiz um modelo de família diferente da do avaliado. E a mitigação que vale por todas: **calibrar o juiz contra um conjunto anotado por humanos** e publicar a taxa de erro dele. Um juiz sem taxa de erro conhecida não é instrumento, é opinião com aparência de número.
