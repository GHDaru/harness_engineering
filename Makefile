# Ponto de entrada do repositório (spec 094).
#
# Este arquivo existe porque a medição de 2026-08-10 mostrou que quem chega na
# raiz não tinha como rodar nada sem antes ler o `CLAUDE.md`. Aqui cada alvo é a
# forma executável de uma frase que antes só existia em prosa.
#
# `make` sozinho mostra os alvos.

.DEFAULT_GOAL := help
.PHONY: help test test-backend test-harness-um test-hooks lint fmt build score

help:  ## mostra os alvos disponíveis
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[1m%-16s\033[0m %s\n", $$1, $$2}'

test: test-harness-um test-backend test-hooks  ## roda as três suítes Python

test-harness-um:  ## testes da implementação de referência
	cd harness-um && python3 -m pytest tests/ -q

test-backend:  ## testes do chat-companion
	cd chat-companion/backend && python3 -m pytest tests/ -q

test-hooks:  ## testes dos guarda-corpos (.claude/hooks)
	python3 -m pytest .claude/hooks/tests/ -q

lint:  ## Ruff nos dois projetos Python (não bloqueia; ver spec 094 R4)
	@python3 -m ruff check . || echo "  (ruff indisponível ou apontou achados — ver spec 094, R4)"

fmt:  ## formata com Ruff
	python3 -m ruff format .

build:  ## site completo: build PT, build EN, verifica PT, verifica EN
	cd publicar && npm run build

score:  ## mede o harness deste repositório (spec 094)
	npx --yes harness-score@latest .
