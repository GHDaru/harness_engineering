# 0002 — Licenciamento duplo (CC BY 4.0 + MIT)

- **Status:** Aceito
- **Data:** 2026-07-27
- **Contexto (feature/spec):** `018-doi-citacao-zenodo`

## Contexto
O repositório mistura **texto do livro** (prosa, figuras) e **código** (harness-zero, motor, companion). O Zenodo exige uma licença para emitir o DOI. Licenças CC são feitas para conteúdo; licenças de software (MIT/Apache) para código.

## Decisão
**Licenciamento duplo**: `LICENSE` = **CC BY 4.0** para o conteúdo; `LICENSE-CODE` = **MIT** para o código; README diz o que cada uma cobre.

## Alternativas avaliadas
- **A — CC BY 4.0 para tudo**: simples. Contra: CC não é adequada a software (sem cláusulas de patente/garantia).
- **B — Dual CC BY 4.0 + MIT (escolhida)**: correto para livro+código; maximiza adoção acadêmica e industrial.
- **C — CC BY-SA / CC BY-NC**: copyleft/uso não-comercial. Contra: restringe adoção; o autor quer reuso amplo.

## Justificativa
B é o padrão para obras que juntam texto e software; separa sem ambiguidade e libera reuso com atribuição.

## Consequências
- Positivas: clareza jurídica; reuso amplo.
- Custos: dois arquivos + nota no README.
- Reversibilidade: média (mudar licença publicada exige cuidado).
