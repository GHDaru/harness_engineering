# decisor-zero — a construção prática

Uma etapa executável por capítulo do [livro](../livro/SUMARIO.md). **O diff entre etapas
consecutivas é a lição do capítulo.** Cada etapa é autocontida: roda sozinha, sem banco,
sem build de frontend, a custo zero (Princípio VI da constituição).

## As 4 regras da construção (constituição, "Restrições")

1. **Uma etapa por capítulo, autocontida** — `etapas/NN-tema/` roda com
   `uvicorn app:app --reload`; frontend em HTML+JS puro, sem build.
2. **Motor de cálculo puro** — algoritmos MCDA são funções/classes sem I/O em `motor/`,
   testáveis sem servidor; FastAPI é casca.
3. **Stack congelada** — Python + FastAPI; nada novo sem ADR.
4. **Worked example = teste** — os números de cada capítulo vivem em `tests/` da etapa
   correspondente; se o exemplo não fecha no código, a prosa está errada (Princípio I).

## Como rodar qualquer etapa

```bash
pip install -r requirements.txt      # na raiz do decisor-zero
cd etapas/NN-tema
uvicorn app:app --reload             # abra http://localhost:8000
pytest                               # os números do capítulo, verificados
```

## Mapa das etapas

| Etapa | Capítulo | O que nasce | Estado |
|---|---|---|---|
| `00-esqueleto` | 00 | Chassi FastAPI + página com o caso âncora | ✅ |
| `01-matriz` | 01 | `MatrizDecisao` (validação de dimensões, direções, pesos) + API genérica | ✅ |
| `02-dominancia` | 02 | Filtro de dominadas / fronteira de Pareto | ⬜ |
| `03-normalizacao-pesos` | 03 | Normalizações (min-max, vetorial) + pesos (direto, ROC, swing, entropia) | ⬜ |
| `04-saw` | 04 | Primeiro ranking completo (SAW/WSM) | ⬜ |
| `05-ahp` | 05 | Comparações par a par, autovetor, razão de consistência | ⬜ |
| `06-topsis` | 06 | Distância ao ideal/anti-ideal | ⬜ |
| `07-funcoes-de-valor` | 07 | Funções de valor por critério (MAVT) + even swaps | ⬜ |
| `08-promethee` | 08 | Funções de preferência e fluxos | ⬜ |
| `09-electre` | 09 | Concordância, discordância, veto | ⬜ |
| `10-vikor-bwm` | 10 | Solução de compromisso + pesos best-worst | ⬜ |
| `11-sensibilidade` | 11 | Análise de sensibilidade e comparação entre métodos | ⬜ |
| `12-grupo` | 12 | Agregação de julgamentos e rankings | ⬜ |
| `13-persistencia` | 13 | Postgres (Neon) atrás de repositório — a ponte para o `app/` | ⬜ |
