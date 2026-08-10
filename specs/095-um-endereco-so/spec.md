# Feature Specification: um endereço só

**Feature Branch**: `095-um-endereco-so`

**Created**: 2026-08-10

**Status**: **Aprovada pelo editor** — *"já pode abrir a spec"*

## A origem

A verificação do estado da migração (2026-08-10, consulta direta aos endereços, ao `/health` do
backend e à API do GitHub) encontrou três coisas abertas que são de código. As duas restantes são
de painel e ficam com o editor.

O livro **está no ar e funcionando** — capa, sumário, inglês, PDFs, Radar, link mágico e
descadastro respondem 200 em `harness.ghdaru.com.br`, e o backend confirma
`site: https://harness.ghdaru.com.br/`. Nada aqui impede alguém de ler. É acabamento de migração —
mas um dos três itens é um **erro de documentação meu**, publicado, e esse não é acabamento.

## O que a verificação encontrou

### 1. Duas cópias vivas e idênticas do livro
`https://ghdaru.github.io/harness_engineering/` responde **200** e está **atualizado** — a cópia
lá tem o apêndice publicado hoje. Cada execução do CI publica **nos dois lugares**: o passo do
Vercel (spec 090) foi acrescentado e o do GitHub Pages nunca foi retirado.

A spec 089 decidiu, com dado (47 visitas na telemetria), **abandonar** os endereços antigos.
Decidiu e não executou: abandonar não é o mesmo que continuar publicando.

### 2. Não existe `rel="canonical"` — e a nossa documentação afirma que existe
O HTML gerado tem `<link rel="alternate" hreflang="…">` e `x-default`. Tem **zero** ocorrências de
`rel="canonical"`.

Só que o comentário do `publicar/build.mjs` diz que `SITE_URL` alimenta *"canonical, hreflang e
og:image: 428 ocorrências"*, e o registro da **edição 0.76** no `HISTORICO.md` repete: *"`SITE_URL`
passa a controlar canonical, hreflang, og:image e o rodapé dos PDFs"*. Fui eu quem escreveu as
duas. Alimenta dois dos três.

> Este é o item que justifica a spec sozinho. As outras duas coisas são configuração; esta é uma
> **afirmação falsa publicada** num livro cujo Princípio I é evidência acima de retórica. O
> conserto tem de ser duplo: pôr a tag **e** corrigir o texto que dizia que ela já estava lá.

E o defeito prático some junto: com duas cópias idênticas no ar e sem canonical, quem escolhe qual
endereço é o oficial é o buscador.

### 3. O default do endereço no build ainda é o antigo
`SITE` cai para `https://ghdaru.github.io/harness_engineering/` quando `SITE_URL` não existe — e
`SITE_URL` só existe no workflow. Quem constrói na própria máquina gera metadados apontando para o
endereço abandonado. Aconteceu nesta sessão.

## Requisitos

### R1 — `rel="canonical"` em toda página
Derivado de `SITE_URL`, como hreflang e og:image já são. Cada página aponta para **si mesma** no
endereço canônico; a página EN aponta para a EN, não para a PT (isso é papel do `hreflang`, que já
existe e continua).

### R2 — A documentação passa a dizer a verdade
- comentário do `build.mjs`: corrigido no mesmo commit que cria a tag;
- `HISTORICO.md`, edição 0.76: **não se reescreve o registro** — acrescenta-se a correção datada na
  entrada da edição nova. Livro vivo corrige em público, não apaga.

### R3 — Uma publicação só
Retirar do workflow os passos que publicam no GitHub Pages. O `docs/` continua sendo construído e
verificado — o que sai é a **distribuição** por dois canais.

**Ordem obrigatória**, e ela importa: R1 entra **antes** de R3. Enquanto as duas cópias coexistem,
o canonical é o que declara qual é a oficial; desligar a publicação antes disso deixaria uma cópia
**congelada e sem canonical** no ar, que é pior que uma cópia atualizada.

⚠️ **Depende de um passo de painel para completar.** Retirar o passo do workflow faz o Pages parar
de **receber atualização**; a última versão publicada **continua servida** até o editor desligar o
site em *Settings → Pages*. Fechar o repositório também resolve, porque Pages de repositório
privado exige plano pago. Fica registrado como pendência do editor, não como parte executável
desta spec.

### R4 — `robots.txt` e `sitemap.xml`
Ambos ausentes hoje, nos dois endereços. Entram porque a combinação de duas cópias + sem canonical
é precisamente o caso em que eles decidem o que é indexado — e porque o `sitemap.xml` sai de graça
da lista de páginas que o build já tem em memória.

### R5 — O default certo
`SITE` passa a cair para `https://harness.ghdaru.com.br/`. O workflow continua declarando
`SITE_URL` — redundância barata e desejável.

> Isto fecha a **armadilha nº 1** do guia de migração ("variável de ambiente antiga vence default
> novo"), que pegou este projeto quatro vezes. Desta vez o movimento é o contrário: alinhar o
> default com a realidade, para que não haja duas verdades.

## Não faz parte

- Desligar o GitHub Pages no painel (é do editor).
- Trocar o token do Vercel e fechar o repositório (são do editor).
- Limpar `ghdaru.github.io` do `ALLOWED_ORIGINS` no Railway — **só depois** que o endereço antigo
  sair do ar. Na ordem inversa o companion morre em silêncio, que foi a falha da spec 092.
- Redirecionar o endereço antigo para o novo: a spec 089 decidiu não preservar os links, com dado.
  Esta spec executa aquela decisão, não a revisa.

## Aceite

- [ ] `rel="canonical"` em toda página, apontando para si mesma no endereço canônico, PT e EN
- [ ] Comentário do `build.mjs` corrigido; correção datada registrada no `HISTORICO.md`
- [ ] Workflow publica **só** no Vercel
- [ ] `robots.txt` e `sitemap.xml` gerados e servidos
- [ ] Default de `SITE` é o endereço próprio; build local e build de CI produzem o mesmo metadado
- [ ] Build de 4 passos verde, 118 testes verdes, alvos de repositório em **9**
- [ ] Verificação em navegador nos dois idiomas; CI verde depois do push
