# Plano — spec 093

## Constitution Check

| Princípio | Conformidade |
|---|---|
| I — Evidência | O gatilho do convite saiu da telemetria do próprio livro, não de regra genérica de produto. |
| V — **Segurança** | Consentimento append-only (prova de quando e a que texto); exportação só com `ADMIN_TOKEN`, desligada por default; descadastro de um clique; revogar contato não toca continuidade. |
| VI — Neutralidade e acessibilidade | Nenhuma superfície bloqueia leitura; tudo funciona anônimo e sem backend; PT e EN. |
| VII — Spec-driven | Branch `093-progresso-e-contato`, merge `--no-ff`. ADR 0010 registra o porquê. |

## Arquitetura

**Progresso sem tabela nova.** `nav_events` já registra slug × sessão e já segue o leitor na
fusão da spec 080. Filtrar pelos slugs de capítulo do sumário dá "capítulos lidos" de graça. O
anônimo calcula pelo `localStorage`, sem backend — a mesma regra da spec 089: o local é a fonte
imediata, o servidor é o espelho que atravessa aparelhos.

**Consentimento append-only.** Cada "dei" e cada "revoguei" é uma linha; o estado é a última por
(e-mail, finalidade). Booleano perderia a história, e é justamente a história que a LGPD pede.

## Arquivos

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/store.py` | tabela `consentimentos`; `registrar_consentimento`, `consentimentos_de`, `emails_com_contato`, `capitulos_lidos` |
| `chat-companion/backend/app.py` | `POST`/`GET /consentimento`, `GET /progresso/detalhe`, `GET /leitores` (admin) |
| `publicar/build.mjs` | cartão "Sua leitura" no sumário (substitui `#ent-retomar`); bloco de fim de capítulo; total de capítulos exposto ao JS |
| `publicar/tema/app.js` | cálculo do progresso (local + remoto), pintura do cartão e do bloco |
| `publicar/tema/companion.js` | pergunta do consentimento de contato; estado e revogação no painel |
| `publicar/tema/entrar.js` | pergunta do consentimento na página de sucesso |
| `publicar/tema/estilo.css` | cartão, barra, bloco de fim de capítulo |
| `livro/HISTORICO.md` | entrada da edição |

## Ordem

1. Backend (store + rotas + testes) — contrato antes da tela.
2. Cartão "Sua leitura" e cálculo do progresso.
3. Bloco de fim de capítulo.
4. Consentimento de contato (painel + página de entrada).
5. Verificação em navegador nos dois idiomas; build 4 passos; checklist.

## Verificação

- `pytest` do backend: consentimento dado/revogado/regravado, exportação só com token, contato
  revogado não derruba continuidade.
- Playwright com backend stubado: cartão com barra e contagem; bloco a partir do 1º capítulo;
  dispensa lembrada; nada bloqueia leitura; PT e EN.
