# Virar o site para o domínio próprio

> Estado em **2026-08-10** (spec 095): o site vive em `harness.ghdaru.com.br`, o workflow publica
> num **canal só**, e cada página declara o próprio endereço canônico.
>
> | Etapa | Estado |
> |---|---|
> | 1. Token do Vercel | ✅ criado (escopo `Full Account`, provisório) |
> | 2. Secret `VERCEL_TOKEN` no GitHub | ✅ salvo |
> | 3. Primeiro envio (nasce o projeto) | ✅ `ghdarus-projects/harness-engineering` |
> | 4. Validar o endereço provisório | ✅ `harness-engineering-rho.vercel.app` |
> | 5. Domínio no projeto + `CNAME` no Cloudflare | ✅ `Valid Configuration`, proxy **desligado**, certificado válido |
> | 6. Virar `SITE_URL` no workflow | ✅ spec 091 |
> | 7. `SITE_URL` no Railway | ✅ feito pelo editor |
> | 8. Zenodo | ✅ identificador atualizado |
> | 9. Trocar por token de escopo restrito e revogar o provisório | ⏳ **editor** |
> | 10. Fechar o repositório | ⏳ **editor** (`private: false` em 2026-08-10) |
> | 11. `rel="canonical"`, `sitemap.xml`, `robots.txt` | ✅ spec 095 |
> | 12. Parar de publicar no GitHub Pages | ✅ spec 095 — saiu do workflow |
> | 13. Desligar o Pages em *Settings → Pages* | ⏳ **editor** — sem isto a última versão publicada continua servida |
> | 14. Limpar `ghdaru.github.io` do `ALLOWED_ORIGINS` no Railway | ⏳ **editor, só DEPOIS de 13** |
>
> **A ordem de 13 e 14 não é sugestão.** Limpar as origens antes de o endereço antigo sair do ar
> derruba o companion para quem ainda estiver lá — foi exatamente a falha da spec 092, e ela é
> silenciosa: o site abre, o texto aparece, e só o chat morre.

Destino: **`https://harness.ghdaru.com.br`**, servido pelo Vercel, com o repositório fechando.
Decisão registrada na spec 089 — os endereços antigos **não** serão preservados (47 visitas na
telemetria; não há base de leitores a proteger).

## Ordem — cada passo é reversível até o último

> **Correção de ordem (a primeira versão deste guia estava errada).** O DNS não vem primeiro: o
> alvo do registro é o Vercel quem informa, ao adicionar o domínio. Projeto primeiro, DNS depois.

### 1. Token primeiro — e ele nasce com escopo de conta, por força da ferramenta

> **Correção de 2026-08-11, do editor que executou os passos.** As duas versões anteriores deste
> guia mandavam criar um projeto **em branco** no painel do Vercel. **O Vercel não deixa** — a
> interface exige importar um repositório. O que aconteceu de verdade aqui foi o inverso: o projeto
> nasceu sozinho no primeiro `vercel link` da linha de comando, e a própria tabela de etapas no
> topo deste arquivo registra isso ("3. Primeiro envio (nasce o projeto)"). A realidade estava
> escrita duas linhas acima da instrução errada.

Em **Account Settings → Tokens**, criar o token.

Ele vai nascer com escopo de **conta inteira**, e não é descuido: escolher escopo de projeto faz a
interface **pedir um projeto**, que ainda não existe. É um ciclo — e a saída é aceitar o token
amplo agora e **trocá-lo depois do passo 2**, quando o projeto existir. Anote esta troca como
tarefa; aqui ela ficou pendente por dias justamente por não estar escrita.

Guardar como *secret* `VERCEL_TOKEN` no repositório do livro. **O token é seu e fica só nos
secrets do GitHub** — não mande por chat.

### 2. O projeto nasce do primeiro envio (eu)

O passo de publicação no workflow começa com `vercel link --yes --project <nome>`, que **cria o
projeto se ele não existir**. É assim que ele nasce, sem passar pela interface.

**E é por isso que não se importa o repositório**: `docs/` é **gerado** e está no `.gitignore` —
não existe no repositório. Um projeto conectado ao git tentaria construir a cada push, não acharia
o `docs/`, e falharia *toda vez*, virando ruído permanente. O desenho certo é o inverso: o **GitHub
Actions constrói** (é onde o Chromium dos PDFs já funciona) e **envia o resultado pronto**. O
Vercel é rede de distribuição, não servidor de build.

Depois do primeiro envio, o Vercel devolve um endereço provisório (`<projeto>-<hash>.vercel.app`).
Abrir e conferir que o livro está lá **antes** de mexer em DNS.

### 3. Domínio no projeto, e só então o DNS (você)

Agora o projeto existe, e o painel serve para o que ele é bom:

1. **Settings → Domains** → adicionar `harness.ghdaru.com.br`.
2. O Vercel exibe o **alvo do CNAME**. É esse valor que vai para o DNS — e é por isso que o
   domínio vem antes do registro, nunca depois.
3. No DNS, **um** registro. O apex (`ghdaru.com.br`) **não é tocado** — sua aplicação atual
   continua intacta.

| Tipo | Nome | Valor | Proxy |
|---|---|---|---|
| CNAME | `harness` | o alvo que o Vercel exibiu | **DNS only** (nuvem cinza) |

No Cloudflare o proxy tem de ficar **desligado**: com a nuvem laranja o Vercel não consegue emitir
o certificado e o domínio trava em *Invalid Configuration*. O certificado sai sozinho quando o DNS
propagar (minutos a algumas horas), e enquanto isso nada quebra.

4. **Volte ao passo 1** e troque o token por um de escopo do projeto, revogando o provisório.

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
