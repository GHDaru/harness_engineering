# Plano — spec 095

## Constitution Check

| Princípio | Como esta spec o honra |
|---|---|
| **I — evidência acima de retórica** | a spec nasce de verificação direta (endereços, `/health`, API do GitHub), e o item 2 existe justamente porque uma afirmação nossa não resistiu a essa verificação |
| **III — o livro é vivo** | a correção do registro 0.76 entra **datada na edição nova**; não se reescreve história publicada |
| **VII — ciclo spec-kit** | esta spec |

Sem segredo. Sem identificador interno de modelo. Nenhuma mudança toca `radar/`.

## Ordem — e ela é obrigatória, não estilística

1. **`SITE` com o default certo** (R5). Primeiro porque tudo abaixo deriva dele, e porque com o
   default errado o teste local mede a coisa errada.
2. **`rel="canonical"`** (R1) + `robots.txt`/`sitemap.xml` (R4).
3. **Só então** retirar a publicação no Pages (R3). Inverter 2 e 3 deixaria no ar uma cópia
   **congelada e sem canonical** — pior que a cópia atualizada de hoje.
4. Documentação (R2), `HISTORICO`, verificação, merge.

## Decisões de projeto

### Onde a tag entra
Em `pagina()` e nas outras três funções que emitem `<head>` (`paginaEntrar`, `paginaSair`, splash).
O `hreflangs(slug)` já calcula o par de idioma e o caminho — o canonical sai do **mesmo** ponto,
para não haver duas noções de "endereço desta página".

Cada página aponta para **si mesma**. A EN não aponta para a PT: quem relaciona os idiomas é o
`hreflang`, que já existe. Confundir os dois papéis é o erro clássico de i18n, e produziria uma
edição inteira declarando-se cópia de outra.

### `sitemap.xml` sem lista nova
O build já conhece todas as páginas que escreve (`itens`, extras, jornal, apêndices). O sitemap sai
dessa lista, no fim do passe PT, com as URLs dos **dois** idiomas — uma lista nova seria uma
segunda verdade a divergir da primeira no primeiro apêndice que alguém acrescentasse.

### `robots.txt`
Permissivo, apontando o sitemap. Não é sobre bloquear ninguém: é sobre dizer onde está o mapa.

### O que NÃO se remove do workflow
Os passos de `configure-pages`/`upload-pages-artifact`/`deploy-pages` saem. O job `build` inteiro
**fica** — ele constrói, testa, gera PDFs, regenera o corpus e publica no Vercel. Sai a
distribuição por um canal, não a construção.

## Riscos

| Risco | Mitigação |
|---|---|
| canonical apontando para a página errada em EN | teste automatizado que confere `canonical == a própria URL` em amostra dos dois idiomas |
| retirar o job `deploy` e quebrar o workflow | o `deploy` depende de `build`; removê-lo inteiro é mais seguro que esvaziá-lo |
| a cópia velha ficar congelada no ar | previsto e registrado: R1 entra antes de R3, e o desligamento no painel fica com o editor |
| alvos de repositório crescerem | contagem no checklist (baseline 9), que já pegou duas regressões |
