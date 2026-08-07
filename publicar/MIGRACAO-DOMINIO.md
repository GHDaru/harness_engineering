# Virar o site para o domínio próprio

> Estado: **preparado, não virado**. O código já lê o endereço de `SITE_URL` (spec 089); o
> default continua o endereço antigo, então nada mudou ainda.

Destino: **`https://harness.ghdaru.com.br`**, servido pelo Vercel, com o repositório fechando.
Decisão registrada na spec 089 — os endereços antigos **não** serão preservados (47 visitas na
telemetria; não há base de leitores a proteger).

## Ordem — cada passo é reversível até o último

> **Correção de ordem (a primeira versão deste guia estava errada).** O DNS não vem primeiro: o
> alvo do registro é o Vercel quem informa, ao adicionar o domínio. Projeto primeiro, DNS depois.

### 1. Projeto no Vercel (você) — **em branco, sem conectar o repositório**

Esta é a parte contraintuitiva, e a segunda correção: **não importe o repositório no Vercel.**

O motivo é concreto: `docs/` é **gerado** e está no `.gitignore` — não existe no repositório. Um
projeto conectado ao git tentaria construir a cada push, não acharia o `docs/`, e falharia. Pior:
falharia *toda vez*, virando ruído permanente.

O desenho certo é o inverso: o **GitHub Actions constrói** (é onde o Chromium dos PDFs já funciona
há meses) e **envia o resultado pronto** ao Vercel. O Vercel é rede de distribuição, não servidor
de build.

Então, no painel do Vercel:

1. Criar conta (o plano gratuito cobre isto de sobra).
2. **Add New → Project → não importe repositório nenhum.** Se a interface insistir em pedir um
   repositório, pule esta etapa: o projeto será criado sozinho no primeiro envio pela linha de
   comando, no passo 3. Nesse caso vá direto ao passo 3 e volte aqui depois para o domínio.
3. Em **Settings → Domains**, adicionar `harness.ghdaru.com.br`.
4. O Vercel exibe então o **alvo do CNAME** — é esse valor que vai para o DNS no passo 2.

### 2. DNS (você)

No painel do `ghdaru.com.br`, criar **um** registro. O apex (`ghdaru.com.br`) **não é tocado** —
sua aplicação atual continua intacta.

| Tipo | Nome | Valor |
|---|---|---|
| CNAME | `harness` | o alvo que o Vercel exibiu no passo 1 |

O certificado de segurança o Vercel emite sozinho assim que o DNS propagar (minutos a algumas
horas). Enquanto não propaga, nada quebra: o site antigo continua no ar.

### 3. Publicação pelo Actions (eu, quando você tiver a conta)

Você gera um **token de acesso** no Vercel (Account Settings → Tokens) e o guarda como *secret*
do repositório, com o nome `VERCEL_TOKEN`. Eu acrescento ao workflow o passo que envia o `docs/`
pronto (`vercel deploy --prebuilt --prod`), e o primeiro envio cria o projeto se ele ainda não
existir.

**O token é seu e fica só nos secrets do GitHub.** Não me mande por aqui — eu não preciso dele
para escrever o workflow, e segredo em chat é vazamento (foi a regra que valeu para a chave do
Resend hoje de manhã).

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
