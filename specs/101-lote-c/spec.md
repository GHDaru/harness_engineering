# Spec 101 — Lote C da cascata: 06, 09, 10, 11

> Branch: `101-lote-c` · 2026-08-12 · decisão: [ADR 0011](../../adr/0011-cascata-didatica.md)

## 1. Os quatro capítulos

**06 MCP** — cena: quatro agentes e seis sistemas dão 24 integrações sem protocolo e 10 com ele, e o que muda de dono importa mais que a aritmética. Exemplo: o `ClienteMCP` em três métodos sobre stdio, e o adapter de sete linhas que registra tools MCP na `ToolPort` do cap. 05 — com namespace por prefixo e a política do cap. 07 aplicada **do lado do cliente**.

**09 Planejamento** — cena: duzentas linhas de diff no controller errado, porque existiam três e o de produção era o terceiro. Exemplo: **plan mode como duas linhas na política do cap. 07**, com a recusa voltando ao modelo como dado que explica o modo, e aprovar sendo trocar o modo, não confiar numa frase.

**10 Subagentes** — cena: a resposta cabia em duas linhas e a leitura ocupou 80% da janela. Exemplo: a `task()` com a fronteira assimétrica (só a descrição na ida, só o resultado na volta), tools por **interseção**, orçamento fracionado, e o caso em que delegar **piora** — quando a subtarefa precisa negociar decisões de volta.

**11 Verificação** — cena: o agente que fazia os testes passarem com `@pytest.mark.skip`. Exemplo: evals determinísticos com `ReplayAdapter` asseverando **comportamento** e não texto, e o juiz LLM chamado **duas vezes com a ordem invertida**, que transforma viés de posição em número. Fecha com a linha que a cena pedia: medir o que o agente não controla, como a contagem de testes ativos.

## 2. O método de produção mudou no meio do lote, e o custo apareceu

A partir do cap. 09 a reescrita passou a ser feita por **transformação roteirizada** (cabeçalho, cena, seção "Na prática", gabarito, redução de travessão e quebra de frase longa) em vez de reescrita integral. Ganhou velocidade e **produziu degradação de prosa** que o portão não pega, porque o portão mede forma e não sentido.

Encontradas por leitura, não por medição:

- o próprio cabeçalho v4 estragado (`Camada didática v4, ver …`), em 9 arquivos;
- títulos de link partidos (`[Apêndice. Meça o seu harness]`);
- rótulos virando fragmento (`**O benchmark é o padrão. É contaminável**`);
- lista de infinitivos perdendo o dois-pontos (`**converge para um fato**, encontrar, medir…`).

Todas corrigidas. **A lição fica registrada porque ela é a do próprio cap. 11**: um portão sintático mede ausência de defeito de forma, e otimizar contra ele produz texto que passa e piora. A defesa é a que o ADR 0011 §5 já exigia — leitura humana por amostragem —, e ela precisou ser aplicada por mim mesmo, no meio da série, para pegar o estrago.

## 3. Medição

**26 capítulos v4** (13 PT + 13 EN) dentro dos limites.

## 4. Fila

Lote D (spec 102): **12 Extensibilidade**, **16 Auto-evolutivo**, **13 Interfaces**, **15 Embutido**, **14 Convergências** — com o 14 por último, sem exceção.
