# 0003 — Reescrita do cap. 01 (Fundamentos) com história + método

- **Status:** Aceito
- **Data:** 2026-07-28
- **Contexto (feature/spec):** `025-fundamentos-rigor`

## Contexto
O editor (autor) avaliou o cap. 01 como "bem fraco": sem rigor metodológico/científico, sem responder "de onde vieram os harnesses" e "o que tínhamos antes". O capítulo tinha 71 linhas e só definição+taxonomia.

## Decisão
Reescrever o cap. 01 em 9 seções: definição (com *scaffolding* traduzido) → **o que havia antes** (sistemas especialistas, RPA, chatbots, Copilot-autocomplete) → **linhagem técnica** (CoT → ReAct → function calling → AutoGPT/BabyAGI → CLIs → protocolos) com linha do tempo → definição constitutiva → **proveniência do corpus** (3 arquétipos + teste de inclusão) → **método do estudo** (casos múltiplos/Yin + MSR/Hassan + GQM + DESMET + DSR/Peffers + ameaças à validade) → taxonomia → cláusula de expiração → artefatos. Fontes verificadas por pesquisa dedicada; não-confirmadas marcadas ⏳ na Bibliografia.

## Alternativas avaliadas
- **A — Apenas expandir a definição existente**: barato, mas não responde às perguntas do editor (história/método).
- **B — Criar um capítulo separado "Método"**: rigoroso, porém fragmenta a abertura; o leitor precisa do método junto dos fundamentos.
- **C — Reescrita integral em 9 seções (escolhida)**: história + método no próprio cap. 01, com fontes verificadas.

## Justificativa
C atende diretamente a crítica do editor; o método fundamenta TODOS os capítulos seguintes, então pertence aos Fundamentos; a pesquisa em duas frentes (história; metodologia) produziu fontes confirmadas suficientes para escrever sem inventar.

## Consequências
- Positivas: o livro ganha lastro científico citável (MSR, Yin, DESMET, DSR); a cláusula de expiração vira mitigação declarada de validade externa.
- Custos: capítulo mais longo; itens ⏳ na Bibliografia ainda pedem verificação final.
- Reversibilidade: alta (Markdown).
