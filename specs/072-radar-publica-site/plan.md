# Plano — spec 072

1 linha de mudança real + registro editorial. Sem impacto no motor nem no livro
(HISTORICO não é traduzido — regra da 067 não gera delta EN).

| Arquivo | Mudança |
|---|---|
| `.github/workflows/publicar.yml` | adicionar `- "radar/**"` aos paths do gatilho `push` |
| `livro/HISTORICO.md` | edição 0.66 (infraestrutura) com nota A3 |
| `radar/diario/2026-08-02.md` | nota de manutenção → "promovida (spec 072)" |

Validação: `python3 yaml.safe_load` no workflow; CI verde após o merge (o próprio push
toca `publicar.yml`, que já está nos paths — o run comprova o deploy; o gatilho por
`radar/**` fica comprovado na próxima execução agendada do Radar).
