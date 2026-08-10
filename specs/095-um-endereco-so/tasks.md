# Tarefas — spec 095

## Código
- [x] T01 `build.mjs`: default de `SITE` passa a ser o endereço próprio (R5)
- [x] T02 `build.mjs`: `rel="canonical"` nas quatro funções que emitem `<head>` (R1)
- [x] T03 `build.mjs`: `sitemap.xml` da lista de páginas que o build já tem (R4)
- [x] T04 `build.mjs`: `robots.txt` apontando o sitemap (R4)
- [x] T05 `.github/workflows/publicar.yml`: sai a publicação no Pages; fica o Vercel (R3)
- [x] T06 comentário do `build.mjs` corrigido: ele dizia que canonical já existia (R2)

## Verificação
- [x] T07 teste: canonical de cada página aponta para si mesma, PT e EN
- [x] T08 build 4 passos + 118 testes + alvos de repositório em 9
- [x] T09 navegador: canonical, robots e sitemap servidos nos dois idiomas

## Fechamento
- [x] T10 `HISTORICO.md`: edição nova, com a **correção datada** do registro da 0.76
- [x] T11 `publicar/MIGRACAO-DOMINIO.md`: painel atualizado com o que sobrou para o editor
- [ ] T12 merge `--no-ff`, push, CI verde, e conferir o site no ar
