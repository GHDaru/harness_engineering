# Spec 104 — O deploy falhou e o CI reportou verde

> Branch: `104-deploy-mudo` · 2026-08-13 · achado pelo editor, não pelo processo

## 1. O sintoma, e quem o encontrou

O editor abriu o site e disse: *"não tinha nada de novidade hoje"*. Estava certo.

- `historico.html` tem a edição **0.87** ✓ (deploy das 02:53, spec 103)
- `radar-mesa.html` **não tem nenhuma linha de 2026-08-13** ✗
- `radar-2026-08.html` e `radar.html`, idem ✗

E o commit `b73be52` (`radar: 2026-08-13`) rodou às **11:15**, com os **15 passos verdes**, incluindo
o passo *"Publicar no Vercel"*.

Reproduzido localmente: o build gera o conteúdo certo — 11 ocorrências de `2026-08-13` em
`docs/radar-mesa.html`. O build não é o problema.

## 2. A causa, no log do próprio job

`logs_85979893722.zip`, linha 1673:

```
2026-08-13T11:16:55.4262313Z Error: Resource is limited - try again in 24 hours
                             (more than 100, code: "api-deployments-free-per-day").
```

O upload de 15 MB terminou; a criação do deployment foi **recusada por cota** — o plano gratuito do
Vercel permite 100 deployments por dia, e a conta passou desse número entre as 02:53 e as 11:16.

## 3. O defeito que importa não é a cota

A cota é uma condição do dia; ela passa em 24 horas. O defeito é o passo ter **reportado sucesso**:

```yaml
vercel deploy --prebuilt --prod --token="$VERCEL_TOKEN" | tee /tmp/vercel-url.txt
```

O shell padrão dos passos `run:` no GitHub Actions é `bash -e`, **sem `pipefail`**. O código de saída
de um *pipeline* é o do **último** comando — e o último é o `tee`, que gravou o texto do erro com
sucesso. O `vercel` saiu diferente de zero, o `tee` saiu zero, e o passo virou verde.

Pior: a linha seguinte escreve *"### Publicado no Vercel"* no resumo do job, com
`tail -1 /tmp/vercel-url.txt` — ou seja, o resumo **afirma publicação** e cola a mensagem de erro
como se fosse a URL.

O `tee` estava ali para exibir a URL no resumo. Ele acabou fazendo o oposto: **transformou uma falha
de publicação numa afirmação de publicação.**

Este é o cap. 11 aplicado ao nosso próprio CI. Um portão que não consegue reprovar não é portão — é
enfeite. E o item 9 do checklist de verificação (*"CI verde conferido depois do push — o merge é o
que publica"*) foi cumprido ao pé da letra hoje: eu conferi o verde. O verde é que mentia.

## 4. O que muda

**`pipefail` no passo, com diagnóstico legível.** A falha de publicação passa a reprovar o job, e a
mensagem diz o que fazer quando a causa é a cota — porque um vermelho que ninguém sabe ler vira
vermelho ignorado, que é o mesmo problema pelo outro lado.

```yaml
shell: bash
run: |
  set -o pipefail
  ...
  if ! vercel deploy --prebuilt --prod --token="$VERCEL_TOKEN" | tee /tmp/vercel-url.txt; then
    echo "::error::deploy recusado — ver /tmp/vercel-url.txt; se for api-deployments-free-per-day, a cota diária do plano gratuito estourou e o site segue na versão anterior"
    exit 1
  fi
```

**O resumo só afirma o que aconteceu.** *"Publicado no Vercel"* passa a ser escrito **depois** do
sucesso, nunca antes.

**Uma verificação de que a página publicada é a que se construiu.** O `pipefail` pega o deploy que
falha em voz alta; não pega o deploy que "sucede" sem trocar o conteúdo. Fica um passo final que
baixa uma página do endereço público e confere um **carimbo do build** — a edição corrente do
`HISTORICO.md` — contra o que subiu. É a diferença entre *"o comando não deu erro"* e *"a página
mudou"*, que é a mesma distinção do anti-checklist: **build verde ≠ página correta**.

## 5. Critério de parada

| Critério | Como se verifica |
|---|---|
| Um deploy recusado reprova o job | forçar a condição não é possível sem estourar a cota de novo; verificado por leitura + `bash -n` e por teste local do padrão `set -o pipefail` + `if !` |
| O resumo não afirma publicação antes do sucesso | leitura do workflow |
| A verificação pós-deploy compara o carimbo publicado com o construído | passo novo no workflow |
| Build local verde | `npm run build` em `publicar/` |
| CI verde depois do merge **e a página no ar com o conteúdo** | conferir `radar-mesa.html` com `2026-08-13` |

## 6. O que fica em aberto

- **A publicação de hoje segue represada.** Enquanto a cota não virar, nenhum push publica. O
  conteúdo (Radar de 13/ago) está na `main` e entra no site no primeiro deploy aceito.
- **A cota de 100/dia é do plano gratuito** e foi consumida por uma sequência de merges numa janela
  curta. Se a cadência de merge continuar assim, isto volta a acontecer — decisão do editor entre
  agrupar merges, mudar de plano, ou publicar por agendamento em vez de por push.
