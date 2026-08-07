# Virar o site para o domínio próprio

> Estado: **preparado, não virado**. O código já lê o endereço de `SITE_URL` (spec 089); o
> default continua o endereço antigo, então nada mudou ainda.

Destino: **`https://harness.ghdaru.com.br`**, servido pelo Vercel, com o repositório fechando.
Decisão registrada na spec 089 — os endereços antigos **não** serão preservados (47 visitas na
telemetria; não há base de leitores a proteger).

## Ordem — cada passo é reversível até o último

### 1. DNS (você)
No painel do `ghdaru.com.br`, criar **um** registro. O apex (`ghdaru.com.br`) **não é tocado** —
sua aplicação atual continua intacta.

| Tipo | Nome | Valor |
|---|---|---|
| CNAME | `harness` | o alvo que o Vercel indicar ao adicionar o domínio |

### 2. Projeto no Vercel (você)
Importar o repositório e, em **Settings → Domains**, adicionar `harness.ghdaru.com.br`. O Vercel
mostra o alvo do CNAME e emite o certificado sozinho quando o DNS propagar.

**Não deixe o Vercel construir o site.** O build gera PDFs com Chromium, pesado demais para o
plano gratuito. O desenho é: o GitHub Actions constrói (onde o Chromium já funciona há meses) e o
Vercel só publica o `docs/` pronto. Em Settings → Build:

- Framework Preset: **Other**
- Build Command: *(vazio)*
- Output Directory: `docs`

### 3. Publicação pelo Actions (eu, quando o projeto existir)
O workflow passa a terminar com `vercel deploy --prebuilt`, usando `VERCEL_TOKEN`,
`VERCEL_ORG_ID` e `VERCEL_PROJECT_ID` como *secrets* do repositório. O Vercel vira CDN, não
servidor de build.

### 4. Virar o endereço (eu, 1 linha)
`SITE_URL=https://harness.ghdaru.com.br` no workflow. Isso reescreve canonical, hreflang,
og:image e o rodapé dos PDFs — 428 ocorrências, todas derivadas da mesma variável.

### 5. Backend (você, no Railway)
| Variável | Novo valor |
|---|---|
| `SITE_URL` | `https://harness.ghdaru.com.br/` |

O **CORS já está pronto**: `harness.ghdaru.com.br` entrou na lista padrão na spec 089. Só mexa em
`ALLOWED_ORIGINS` se quiser **remover** a origem antiga.

> Sem esta etapa o link mágico continua mandando o leitor para o endereço morto. É o único ponto
> em que esquecer produz um erro que o leitor vê.

### 6. Zenodo (você)
Atualizar o identificador para o endereço novo. É o link que sobrevive a qualquer troca de
hospedagem — o que se cita em artigo e em proposta editorial.

### 7. Só então: fechar o repositório
Com o site no ar sob o domínio próprio e o backend apontando para ele, o repositório pode virar
privado. **A partir daí `ghdaru.github.io/harness_engineering/` deixa de existir** — é a decisão
consciente da spec 089, não um efeito colateral.

## Por que isto não volta a acontecer

O endereço agora é variável, e o domínio é **seu**. Trocar de hospedagem outra vez — Vercel para
qualquer outro — passa a ser um registro de DNS e uma variável, sem tocar em código e sem quebrar
link nenhum. A dependência que existia era do endereço ser de outra pessoa.
