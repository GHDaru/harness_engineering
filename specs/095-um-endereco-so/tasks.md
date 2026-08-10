# Tarefas — spec 095

## Código
- [ ] T01 `build.mjs`: default de `SITE` passa a ser o endereço próprio (R5)
- [ ] T02 `build.mjs`: `rel="canonical"` nas quatro funções que emitem `<head>` (R1)
- [ ] T03 `build.mjs`: `sitemap.xml` da lista de páginas que o build já tem (R4)
- [ ] T04 `build.mjs`: `robots.txt` apontando o sitemap (R4)
- [ ] T05 `.github/workflows/publicar.yml`: sai a publicação no Pages; fica o Vercel (R3)
- [ ] T06 comentário do `build.mjs` corrigido: ele dizia que canonical já existia (R2)

## Verificação
- [ ] T07 teste: canonical de cada página aponta para si mesma, PT e EN
- [ ] T08 build 4 passos + 118 testes + alvos de repositório em 9
- [ ] T09 navegador: canonical, robots e sitemap servidos nos dois idiomas

## Fechamento
- [ ] T10 `HISTORICO.md`: edição nova, com a **correção datada** do registro da 0.76
- [ ] T11 `publicar/MIGRACAO-DOMINIO.md`: painel atualizado com o que sobrou para o editor
- [ ] T12 merge `--no-ff`, push, CI verde, e conferir o site no ar
