# Design System do livro — componentes de tela

> **O local da definição** (decisão registrada em [`adr/0006`](../adr/0006-design-system-componentes.md)): cada **entregável da metodologia** (esqueleto v3, Guia Editorial) corresponde a um **componente de tela nomeado**; a página de um capítulo é uma **composição** desses componentes. O motor (`build.mjs`) reconhece os entregáveis pelas convenções do Markdown (títulos de seção, blockquote de data, `sumario.json`) e aplica o componente — o **conteúdo nunca carrega HTML de apresentação**.

## Princípios

1. **Conteúdo ⟂ apresentação**: os `.md` declaram entregáveis (convenção); o motor aplica componentes (renderização). Trocar o visual de um componente muda o livro inteiro sem tocar um capítulo.
2. **Um entregável ↔ um componente**: se a metodologia cria um entregável novo, ele ganha componente (e entra aqui). Se um componente não corresponde a entregável, é infraestrutura (navegação) e é marcado como tal.
3. **Todo componente declara**: origem metodológica, anatomia, gatilho no motor, classes CSS, variantes e status.
4. **Theme-aware por herança**: componentes usam as `--vars` do tema; nunca cores fixas.

## Catálogo

### Componentes de entregável (metodologia → tela)

| # | Componente | Entregável de origem (metodologia) | Gatilho no motor | Classes | Status |
|---|---|---|---|---|---|
| C01 | **CabeçalhoDeCapítulo** | identidade do capítulo: número, título, teaser (Backward Design: o "para onde vamos") + datação (Princípio IV) + carga estimada (Sweller: expectativa de esforço) | item do `sumario.json` (capítulo numerado) + blockquote de data | `.cap-hero` | ✅ variante **B "faixa editorial"** (spec 043) |
| C02 | **SeloDeDatação** | cláusula de expiração — data de captura/revisão | 1º blockquote "Estado da arte capturado em" | `.selo-data` (integra-se ao C01 nos capítulos) | ✅ |
| C03 | **Objetivos** | Backward Design/Bloom: objetivos de aprendizagem | `## Objetivos de aprendizagem` | `h2[data-callout="callout-objetivos"]` | ✅ |
| C04 | **Verificação** | Backward Design: evidências de aprendizagem | `## Verificação` | `callout-verificacao` | ✅ |
| C05 | **MãoNaMassa** | 4C/ID: learning task (trilha harness-zero) | `## Mão na massa` | `callout-pratica` | ✅ |
| C06 | **OQueRoubar** | Diátaxis how-to: padrões transferíveis | `## O que roubar` | `callout-roubar` | ✅ |
| C07 | **ApêndiceA** | Princípio II: tratamento por repositório (evidência) | `## Apêndice A` | `callout-apendice` | ✅ |
| C08 | **LeituraExecutiva** | síntese acionável do estado da arte | `### Leitura executiva` | `.leitura-exec` | ✅ **V1 "painel âmbar"** (spec 043) |
| C09 | **Figura** | recurso visual com legenda (dual coding) | `<figure class="figura">` | `.figura` | ✅ (spec 027) |
| C10 | **IlhaDeVisualização** | dados vivos do benchmark (evidência interativa) | `<div data-viz="…">` | `.viz*` | ✅ (P2) |
| C11 | **SiglaAberta** | política de siglas (Guia): extenso na 1ª vez + hover sempre | mapa `SIGLAS` no motor | `abbr[title]` | ✅ (spec 023) |
| C12 | **Citação** | Princípio I: menção → Bibliografia → fonte | padrão `arXiv NNNN.NNNNN` | `.cita` | ✅ MVP (spec 028; ADR 0004) |

### Componentes de infraestrutura (navegação/site — sem entregável)

| # | Componente | Papel | Classes | Status |
|---|---|---|---|---|
| N01 | **Sidebar** | índice completo sempre visível | `.sidebar` | ✅ |
| N02 | **PaginaçãoEmCartões** | anterior/próximo na linguagem do cartão | `.pagcards` | ✅ **V2 "cartões com badge"** (spec 043) |
| N03 | **CartãoDeCapítulo** | entrada do livro (badge+título+teaser) | `.ent-card` | ✅ (spec 021) |
| N04 | **Trilha / Retomar / Pills** | onboarding e retomada na entrada | `.ent-*` | ✅ (spec 021) |
| N05 | **Companion** | tutor flutuante com gating por capítulo | `.cmp*` | ✅ (specs 016/017) |

## Regras de composição (página de capítulo)

```
CabeçalhoDeCapítulo (C01, absorve C02)
└─ corpo Markdown, onde o motor aplica:
   C03 Objetivos → prosa → C08 LeituraExecutiva → C05 MãoNaMassa →
   C04 Verificação → C06 OQueRoubar → C07 ApêndiceA
   (C09/C10/C11/C12 aparecem inline onde o conteúdo os declara)
└─ PaginaçãoEmCartões (N02)
```

Páginas do aparato (Glossário, Bibliografia, Histórico, Guia, Apêndice do estudo, Autor) **não** recebem C01 (não são capítulos numerados); mantêm C02+ quando aplicável.

## Como evoluir este catálogo

- Componente novo ou variante ⇒ **spec-kit** + linha aqui + (se houver alternativas de desenho) mockups no **gate humano** + ADR quando a decisão tiver alternativas relevantes.
- Validação de desenho: **página-espécime** (uma tela compondo o catálogo inteiro) para o conjunto + **3 modelos** por componente novo (método aprovado na spec 043).
- O gatilho no motor é **convenção de conteúdo** (título de seção, atributo) — nunca HTML de apresentação nos `.md`.
