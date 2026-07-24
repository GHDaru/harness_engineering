# Nota de pesquisa — A segunda corrida: agentes pessoais self-hosted

> Data: 2026-07-24 · Método: pesquisa web exploratória (fontes ao final). Status: panorama preliminar, a confrontar com código quando os repositórios entrarem no benchmark.

## A tese

A primeira rodada do benchmark cobriu a corrida dos **harnesses de código** (opencode, gemini-cli, Codex CLI...). A pesquisa desta nota confirma uma segunda corrida, paralela e igualmente quente: a dos **agentes pessoais self-hosted** — o assistente autônomo que roda no hardware do usuário e é acessado por mensageria (WhatsApp, Telegram, Slack, Discord). Mesmo scaffolding fundamental (loop, tools, memória, permissões), pesos completamente diferentes: aqui as dimensões dominantes são **superfícies de chat, memória/identidade de longo prazo, proatividade (agendamento/heartbeat), aprendizado de skills e — criticamente — segurança**, porque o agente roda com shell na máquina do dono, exposto à internet.

Já temos um representante da categoria dentro de casa sem perceber: o **ohmo** do OpenHarness (avaliado na rodada 1) é exatamente este arquétipo — Telegram/Slack/Discord/Feishu, workspace de identidade (`soul.md`, `identity.md`).

## Os dois líderes

### OpenClaw (ex-Moltbot, ex-Clawdbot)
- Node.js, MIT, criado por Peter Steinberger; hoje sob uma fundação sem fins lucrativos.
- ~329 mil estrelas em menos de quatro meses — um dos crescimentos mais rápidos da história do GitHub.
- Auto-hospedado; WhatsApp, Telegram, Discord e 12+ plataformas; executa shell, gerencia arquivos, automatiza navegador, agenda tarefas; multi-modelo (Claude, GPT, Gemini, DeepSeek); 100+ "AgentSkills" built-in.
- Posicionamento observado nos comparativos: vence em **alcance, multi-modelo e maturidade de features**.

### Hermes Agent (Nous Research)
- Python, MIT, lançado em fevereiro/2026; 200 mil+ estrelas até meados de 2026.
- CLI interativa com tools, memória e skills; conecta a Nous Portal, OpenRouter ou endpoint próprio.
- O diferencial conceitual da categoria: **loop de aprendizado auto-evolutivo** — ao resolver um problema difícil, o agente escreve um documento de skill reutilizável; workflows repetidos viram skills automaticamente. Skills pesquisáveis e compartilháveis, compatíveis com o padrão aberto **agentskills.io**.
- Posicionamento: vence em **personalização, aprendizado ao longo do tempo e custo**.

## O ecossistema em volta (a "família claw" e adjacentes)

A categoria já tem dinâmica de ecossistema — forks, reimplementações e derivados com nomes da mesma família:

- **IronClaw** (NEAR AI) — reimplementação **security-first em Rust** do OpenClaw, zero-trust, voltada a empresa. Relevante para nós: é a resposta da categoria ao seu próprio calcanhar de aquiles (agente com shell + exposição de rede), e candidata natural a referência da dimensão 6 (permissões/sandbox) nesta categoria.
- **TrustClaw, ZeroClaw, NanoClaw, Kimi Claw, Nemoclaw** — variantes/derivados citados nos comparativos (profundidade a verificar; possivelmente qualidade desigual).
- **metaharness** (ruvnet) — "meta-harness": gerador de harnesses focados/brandados com CLI própria, MCP server, memória e learning loop; declara interoperar com Claude Code, Codex, pi.dev, Hermes, OpenClaw. Sinal de maturidade: a categoria já tem ferramenta de *fabricar* harnesses.
- **Buzz** (Jack Dorsey, jul/2026) — workspace self-hostável com identidade compartilhada humano+agente (chat, Git, workflows); fronteira entre agente pessoal e organização.
- **awesome-openclaw** e **awesome-hermes-agent** — a categoria já tem suas listas curadas próprias.

## Implicações para o livro

1. **Nova categoria no benchmark**: "agentes pessoais" — mesmo template de 12 dimensões, mas com leitura própria (o que é "referência" em interfaces/memória/segurança aqui é diferente da categoria código). Candidatos à avaliação por código: **OpenClaw** e **Hermes Agent** (ambos MIT, código aberto de verdade); **IronClaw** como possível terceiro, pelo ângulo de segurança.
2. **O aprendizado de skills como dimensão emergente**: o loop auto-evolutivo do Hermes (skills escritas pelo próprio agente) não tem lugar limpo nas 12 dimensões atuais — hoje cairia entre extensibilidade (12) e memória (8). Se a segunda rodada confirmar o padrão, é candidata a **13ª dimensão** do template ("Aprendizado / auto-melhoria").
3. **Skills portáveis viram padrão**: agentskills.io + o formato SKILL.md do ecossistema Claude (que o OpenHarness já carrega) — a previsão do cap. 14 ("um MCP da extensibilidade está se formando") ganhou evidência.
4. **Segurança vira o capítulo mais importante da categoria**: agente pessoal = shell do dono + credenciais + exposição à internet + prompt injection via mensagens de terceiros. A existência do IronClaw é o mercado precificando esse risco. (A verificar quando avaliarmos o código: relatos de incidentes de instâncias OpenClaw expostas — não confirmado nesta pesquisa.)
5. **ohmo ganha contexto competitivo**: a avaliação do OpenHarness deve ser relida à luz desta categoria — o ohmo compete aqui, não com o gemini-cli.

## Fontes

- [Composio — 10 Best OpenClaw Alternatives 2026](https://composio.dev/content/openclaw-alternatives)
- [Vellum — Best OpenClaw Alternatives](https://www.vellum.ai/blog/best-openclaw-alternatives) · [Best Hermes Agent Alternatives](https://www.vellum.ai/blog/best-hermes-agent-alternatives) · [Best Personal AI Assistants for Developers](https://www.vellum.ai/blog/best-personal-ai-assistants-for-developers)
- [xCloud — Hermes Agent vs OpenClaw](https://xcloud.host/hermes-agent-vs-openclaw) · [Flowtivity — OpenClaw vs Hermes 2026](https://flowtivity.ai/blog/openclaw-vs-hermes-agent-comparison/)
- [Lushbinary — Hermes/OpenClaw/IronClaw compared](https://lushbinary.com/blog/best-self-hosted-ai-agents-hermes-openclaw-ironclaw-compared/)
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) · [hermes-agent.org](https://hermes-agent.org/)
- [SamurAIGPT/awesome-openclaw](https://github.com/SamurAIGPT/awesome-openclaw) · [0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent)
- [ruvnet/metaharness](https://github.com/ruvnet/metaharness)

> Ressalva metodológica: números de estrelas e datas vêm de fontes secundárias de qualidade desigual (blogs de hosting/comparativos comerciais, alguns com detalhes contraditórios entre si); confirmar tudo no repositório-fonte quando entrarem no benchmark.
