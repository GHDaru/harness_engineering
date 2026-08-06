# Plano — spec 077

| Arquivo | Mudança |
|---|---|
| `chat-companion/backend/ragindex.py` | escopo das fontes; linha de tabela = bloco; score por termos distintos com penalidade de tamanho |
| `chat-companion/backend/build_corpus.py` | documentação do escopo novo e mensagem correta |
| `.github/workflows/publicar.yml` | `contents: write` + regenerar e commitar `corpus.json` quando mudar |
| `chat-companion/backend/corpus.json` | regenerado (1.406 blocos) |

Verificação: consultas reais contra o índice ao vivo (Grok Build, Microsoft, opencode×Anthropic),
inspeção do trecho enviado ao modelo, pytest do backend.
