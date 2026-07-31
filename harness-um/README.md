# harness-um

<img src="assets/harness-um.png" alt="harness-um — a implementação de referência do livro Engenharia de Harness" width="640">

A **implementação de referência** do livro [Engenharia de Harness](https://ghdaru.github.io/harness_engineering/): as features dos capítulos 02–13 reunidas num harness completo, pequeno e legível. O `harness-zero` ensina a construir (uma feature por etapa); o **harness-um é o destino** — o código que se lê depois de ler o livro.

## A linguagem ubíqua

O código fala **a língua do livro** (DDD): `Harness`, `Turno`, `Ferramenta`, `Politica`, `Memoria`, `Plano`, `Subagente`, `Verificador`, `Gancho`, `Habilidade`, `Compactador`, `Provedor`. A tradução para o dialeto de cada API de modelo acontece só na borda (`provedores.py`) — a camada anticorrupção. A tabela completa termo → classe → capítulo está no [apêndice do livro](https://ghdaru.github.io/harness_engineering/apendice-harness-um.html).

## Baixar e rodar

```bash
git clone https://github.com/GHDaru/harness_engineering.git
cd harness_engineering/harness-um
pip install -e .

# offline, sem chave (ProvedorEco — diretivas @usar exercitam o loop):
python -m harness_um --eco 'leia @usar ler_arquivo {"caminho": "README.md"}'

# com modelo real (chave só no ambiente, nunca em arquivo):
export ANTHROPIC_API_KEY=...   # https://console.anthropic.com
python -m harness_um           # REPL: /plano /memoria /contexto /sair
```

## Testes

```bash
pip install -e ".[dev]"
python -m pytest tests/
```

Todos os testes rodam **offline** com o `ProvedorEco` — a lição do cap. 11 aplicada ao próprio harness: loop testável é loop com provedor falso.

## Mapa (cada módulo = um capítulo)

| Módulo | Capítulo | O que implementa |
|---|---|---|
| `loop.py` | 02 | o ciclo com orçamento de turnos |
| `contexto.py` | 03 | system prompt montado em camadas auditáveis |
| `compactacao.py` | 04 | resumo estrutural + cauda intacta |
| `ferramentas.py` | 05 | esquema pela assinatura; raiz como invariante |
| `mcp.py` | 06 | cliente stateless (spec 2026-07-28) |
| `permissoes.py` | 07 | permitir / perguntar / negar |
| `memoria.py` | 08 | MEMORIA.md + sessões JSONL |
| `plano.py` | 09 | o plano como artefato persistente |
| `subagentes.py` | 10 | tarefa() com contexto limpo e caixa só-leitura |
| `verificacao.py` | 11 | verificadores pós-mutação no loop |
| `extensao.py` | 12 | ganchos (vetáveis) + habilidades (SKILL.md) |
| `__main__.py` | 13 | o REPL com humano como aprovador |

> **Cláusula de expiração** (caps. 01 e 14): isto é uma referência didática de 2026-07, não um produto. Compare com o estado da arte antes de copiar.
