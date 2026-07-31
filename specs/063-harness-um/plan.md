# Plano — Spec 063 (harness-um)

## Arquitetura do pacote

`harness-um/` (diretório de topo, irmão do `harness-zero/`):

```
harness-um/
  README.md                  ← porta de entrada do repositório
  pyproject.toml             ← instalável: pip install -e .
  assets/harness-um.svg|png  ← figura oficial (fonte SVG + PNG)
  harness_um/
    __init__.py              ← exporta a fachada Harness
    __main__.py              ← python -m harness_um  → REPL (cap. 13)
    provedores.py            ← porta Provedor; ProvedorAnthropic, ProvedorEco (R2)
    ferramentas.py           ← Ferramenta, CaixaDeFerramentas, esquema por assinatura (cap. 05)
    permissoes.py            ← Politica, Decisao (PERMITIR/PERGUNTAR/NEGAR) (cap. 07)
    contexto.py              ← MontadorDeContexto: camadas sistema→memória→plano→história (cap. 03)
    compactacao.py           ← Compactador: resumo estrutural + cauda intacta (cap. 04)
    memoria.py               ← Memoria (MEMORIA.md), Sessao (JSONL em disco) (cap. 08)
    plano.py                 ← Plano como artefato: itens, estados, render (cap. 09)
    verificacao.py           ← Verificador pós-mutação; portão de qualidade (cap. 11)
    extensao.py              ← Gancho (hooks pré/pós-ferramenta), Habilidade (SKILL.md) (cap. 12)
    mcp.py                   ← ClienteMCP stateless (POST único, Mcp-Method; pós-2026-07-28) (cap. 06)
    subagentes.py            ← tool tarefa(): loop-filho com contexto limpo (cap. 10)
    loop.py                  ← LoopDoAgente: o coração — turnos, orçamento, eventos (cap. 02)
    harness.py               ← Harness: o agregado que monta tudo (composição, não herança)
  ferramentas_padrao.py?     → não: builtin em ferramentas.py (ler/escrever/listar/executar)
  tests/test_harness_um.py   ← pytest com ProvedorEco (R4)
```

Decisões:
- **Linguagem ubíqua em PT** nos nomes públicos; docstrings citam o capítulo (R1/R3).
- ProvedorEco entende diretivas simples (`@usar <ferramenta> {...}`) para exercitar o
  loop de tool-use em teste, offline e determinístico.
- Subagente reusa o MESMO LoopDoAgente com caixa restrita (só leitura) — a lição do
  cap. 10 em uma função.
- MCP: cliente mínimo da spec 2026-07-28 (sem initialize; `Mcp-Method` no header;
  `tools/list` + `tools/call`), marcado com nota de época.

## Site e apêndice

1. `livro/apendice-harness-um.md` — seções: por que existe · linguagem ubíqua
   (tabela termo/classe/capítulo) · figura oficial · arquitetura (árvore) · como
   baixar/rodar · harness-zero vs harness-um · expiração. Entra em
   `publicar/sumario.json` no "Aparato do livro" (antes da Bibliografia).
2. Figura oficial: SVG autoral (mesma família do favicon: núcleo âmbar, anel
   segmentado, marca "1") → PNG via Chromium (padrão da sessão: SVG inline +
   `locator('svg').screenshot()`). Copiada para `docs/assets/` no build.
3. CI (`publicar.yml`): passo "Testes do harness-um" (pip install -e + pytest) antes
   do build do site.
4. `HISTORICO.md`: edição 0.58. Corpus do companion regenerado (livro/ muda).

## Verificação

- pytest local verde; REPL fumaça com ProvedorEco.
- `npm run build` + portões; e2e Chromium do apêndice (figura, tabela, download).
- Merge `--no-ff`, push, CI verde (que agora inclui o pytest).

## Riscos

- Escopo do código crescer demais → alvo: ~1.200 linhas de pacote, recorte
  referência (não produto), cada módulo com uma responsabilidade de capítulo.
- Nome do pacote Python: `harness_um` (hífen não é identificador).
- `build.mjs` copia `assets/`: adicionar a figura ao build sem quebrar PDFs.
