# Apêndice — harness-um: a implementação de referência

> **Estado da arte capturado em 2026-07** · última revisão 2026-07-31 · [histórico e registro de expiração](HISTORICO.md)

Depois de dezoito capítulos descrevendo o que um harness tem, a pergunta honesta é: *e se juntássemos tudo?* Este apêndice responde com código. O **harness-um** é a implementação de referência do livro — as features dos capítulos 02–13 reunidas num sistema único, pequeno o bastante para ser lido numa tarde e completo o bastante para ser o ponto de partida do seu.

<figure class="figura">
  <img src="assets/harness-um.svg" alt="Figura oficial do harness-um: um numeral 1 âmbar luminoso no centro de um anel de 12 segmentos azuis — os capítulos 02 a 13 — sobre fundo azul-escuro de blueprint, ao lado do nome harness-um e do subtítulo 'a implementação de referência do livro Engenharia de Harness'.">
  <figcaption>A figura oficial: o núcleo (o agente) envolto pelos 12 segmentos do anel — os capítulos 02–13, um por feature. A identidade visual é a mesma da capa: o harness é o que está <em>em volta</em>.</figcaption>
</figure>

## Por que "harness-um" (e não "openharness")

O nome conta a progressão do livro: o **harness-zero** (Mão na massa) constrói uma feature por etapa, do zero; o **harness-um** é o destino — tudo junto e coeso. E há uma razão editorial: "OpenHarness" **já existe** — é um dos 16 sistemas do corpus deste estudo (HKUDS/OpenHarness, port open-source do Claude Code). Batizar a referência do livro com o nome de um sistema que o próprio livro avalia criaria a confusão que o Princípio I existe para evitar.

## A linguagem ubíqua

A decisão central do harness-um não é técnica, é **linguística**: o código fala a língua do livro. Cada termo que os capítulos definiram vira um nome de código idêntico — ler o código é reler o sumário. A tradução para o dialeto de cada API de modelo (hoje, Anthropic Messages) acontece numa única borda (`provedores.py`), a **camada anticorrupção**: se o provedor mudar, o domínio nem fica sabendo.

| Termo do livro | No código | Capítulo |
|---|---|---|
| Loop do agente | `LoopDoAgente.executar()` | 02 |
| Turno (com orçamento) | `max_turnos` | 02 |
| Montagem de contexto | `MontadorDeContexto` (camadas nomeadas) | 03 |
| Compactação | `Compactador` (resumo + cauda intacta) | 04 |
| Ferramenta | `Ferramenta`, `@ferramenta`, `CaixaDeFerramentas` | 05 |
| MCP | `ClienteMCP` (stateless, spec 2026-07-28) | 06 |
| Permissões | `Politica` → `PERMITIR / PERGUNTAR / NEGAR` | 07 |
| Memória durável | `Memoria` (`MEMORIA.md`) | 08 |
| Sessão | `Sessao` (JSONL, append-only) | 08 |
| Plano como artefato | `Plano` (persistido, re-injetado) | 09 |
| Subagente | `tarefa()` — contexto limpo, caixa só-leitura | 10 |
| Verificação | `Verificador` (pós-mutação, veredito ao modelo) | 11 |
| Gancho (hook) | `Gancho` (determinístico, pode vetar) | 12 |
| Habilidade (skill) | `Habilidade` (`SKILL.md`, divulgação progressiva) | 12 |
| Interface | REPL (`python -m harness_um`) | 13 |
| Provedor | `Provedor` → `ProvedorAnthropic`, `ProvedorEco` | 02, 11 |

## Como baixar e rodar

O código vive **neste repositório**, ao lado do livro — em [`harness-um/`](https://github.com/GHDaru/harness_engineering/tree/main/harness-um):

```bash
git clone https://github.com/GHDaru/harness_engineering.git
cd harness_engineering/harness-um
pip install -e .

# sem chave nenhuma (ProvedorEco, offline):
python -m harness_um --eco 'leia @usar ler_arquivo {"caminho": "README.md"}'

# com modelo real (chave SÓ no ambiente):
export ANTHROPIC_API_KEY=...
python -m harness_um     # REPL: /plano /memoria /contexto /sair
```

O `ProvedorEco` merece a nota: ele é determinístico e obedece diretivas `@usar ferramenta {...}` — o suficiente para exercitar o loop inteiro (tool-use, permissões, ganchos, verificação) **sem rede e sem custo**. É por isso que os testes do harness-um rodam no CI do livro a cada push: a referência não pode apodrecer em silêncio.

## harness-zero × harness-um

| | harness-zero | harness-um |
|---|---|---|
| Propósito | **ensinar a construir** (Backward Design) | **mostrar o conjunto pronto** |
| Forma | 13 etapas, cada uma um app completo | 1 pacote coeso (`harness_um/`) |
| Leitura | durante os capítulos | depois do livro |
| Análogo | caderno de exercícios | gabarito comentado |

## Expiração

Como tudo neste livro: o harness-um é a foto de **2026-07** — o cliente MCP já nasce na spec 2026-07-28, mas provedores, esquemas e convenções mudam em meses. A [cadência do livro vivo](HISTORICO.md) (ADR 0007) cobre também este apêndice; o código carrega a mesma cláusula no README.
