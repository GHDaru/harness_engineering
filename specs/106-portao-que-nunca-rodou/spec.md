# Spec 106 — O portão que eu escrevi para pegar publicação silenciosa nunca rodou

> Branch: `106-portao-que-nunca-rodou` · 2026-08-22 · corrige a spec 104 · pedido do editor

## 1. O que eu afirmei, e o que o log diz

Na spec 104 escrevi um passo de conferência pós-deploy que compara o carimbo publicado com o
`GITHUB_SHA`. Em 20/ago, ao confirmar a publicação da edição 0.89, relatei ao editor que *"o passo de
verificação da spec 104 aprovou por mérito"*.

Conferindo o job da execução `32317355461` (commit `34a4fac`), passo 16:

```
"name": "Conferir que o site publicado e o que se construiu",
"conclusion": "skipped"
```

**Ele nunca rodou. Nem uma vez.** E a execução em que eu disse que ele aprovou é exatamente a execução
em que ele foi pulado.

## 2. Por que foi pulado

O passo carrega `if: env.VERCEL_TOKEN != ''`, copiado do passo de publicação. Mas `VERCEL_TOKEN` só
existe no bloco `env:` **do passo 15**. O `env:` do job define apenas `SITE_URL`, e o `env:` do passo
16 também.

Para o passo 15 a condição é verdadeira, porque um passo enxerga o próprio `env`. Para o passo 16 a
variável não existe no escopo, `env.VERCEL_TOKEN` é vazio, a condição dá falso, e o passo é pulado.
**Passo pulado não reprova job**, então o verde continuou verde.

A conferência precisa do endereço público e do `GITHUB_SHA`. Ela nunca precisou do token — eu copiei a
condição junto com o formato do passo, sem perguntar se ela fazia sentido ali.

## 3. Por que isto é pior que o defeito de 13/ago

A spec 104 nasceu porque um `tee` engoliu o código de saída do `vercel deploy` e uma falha de
publicação virou verde. O conserto tinha duas camadas: `pipefail` para a falha barulhenta, e o carimbo
para o deploy que "sucede" sem trocar conteúdo.

A segunda camada **nunca esteve ligada**. Durante nove dias o repositório carregou um portão que
existia no arquivo, aparecia na lista de passos, e não executava. Quem lesse o workflow concluiria que
a publicação é verificada. Quem lesse o log veria `skipped` e a mesma conclusão verde.

É o cap. **11** aplicado ao conserto do cap. 11: **um portão que não pode reprovar não é portão**, e a
forma mais silenciosa de não poder reprovar é não rodar. O portão anterior mentia por acidente de
shell; este mentia por acidente de escopo.

E há um agravante de método: eu **afirmei** que ele aprovou. O dado estava no mesmo objeto JSON que eu
já tinha consultado — bastava olhar a conclusão do passo 16 em vez de olhar só a conclusão do job.

## 4. O que muda

**A condição sai dos dois passos.**

- **Passo de publicação**: em vez de se ausentar quando o token falta, ele **falha e diz que falta**.
  Um repositório que perdeu o segredo de publicação precisa de um vermelho, não de um silêncio.
- **Passo de conferência**: perde a condição por completo. Ele não usa o token, nunca usou, e não tem
  motivo para depender dele.

Isso também remove a armadilha que o editor encontraria ao **revogar o token do Vercel**: hoje, tirar o
segredo faria os dois passos sumirem e o job continuar verde — a publicação pararia sem nenhum aviso.

**E o critério de parada ganha uma pergunta nova**, porque a antiga não teria pego isto: não basta o
job terminar verde, é preciso confirmar que **o passo de conferência executou**.

## 5. Critério de parada

| Critério | Como se verifica |
|---|---|
| Nenhum `if:` condicional em `publicar.yml` | `grep -n "if:" .github/workflows/*.yml` retorna vazio |
| YAML válido | `python3 -c "import yaml; yaml.safe_load(...)"` |
| Publicação sem token **falha** | leitura do passo: `[ -z "$VERCEL_TOKEN" ]` → `exit 1` |
| **O passo 16 executa** | conclusão do passo na API, e ela precisa ser `success`, **não `skipped`** |
| Carimbo publicado bate com o commit | o próprio passo 16, agora rodando |
| Build local verde | `npm run build` |

## 6. O que fica em aberto

- **O passo 16 só prova que funciona quando reprova.** Ele vai rodar e passar; o caminho triste
  continua sem teste de campo, como registrado na spec 104.
- **O acoplamento do Chromium** segue: a publicação espera um navegador que só serve para PDF, e em
  19/ago isso segurou o site por três horas. Proposto ao editor, sem decisão.
- **Nenhuma varredura encontraria este defeito.** Ele foi achado porque o editor mandou abrir a spec do
  `if:` e eu fui ler a semântica do escopo antes de escrever. Vale como método: quando for mexer numa
  condição, confira primeiro o que ela avalia hoje.
