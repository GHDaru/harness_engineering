# Spec 054: Experiência educacional — consentimento, onboarding, telemetria e plano de ensino

**Feature Branch**: `054-experiencia-educacional` · **Criada em**: 2026-07-29

## Requisitos funcionais

### 1. Consentimento (disclaimer com aceite gravado)
- FR-101: ao entrar no site pela primeira vez, um **banner discreto** (rodapé, todas as páginas) avisa: as conversas com o companion são usadas para o **aprimoramento vivo do livro**; **nunca compartilhe dados pessoais** no chat. Botão "Entendi e aceito".
- FR-102: o aceite é gravado **no navegador** (`cmp_consent` = versão + timestamp) e **no backend** (`POST /consent` → tabela `consents`: session_id anônima, versão do texto, timestamp) — auditável e versionado (mudou o texto ⇒ nova versão ⇒ novo aceite).
- FR-103: o chat **exige o aceite**: sem consentimento, o painel mostra o cartão do disclaimer com o botão de aceite no lugar da entrada; aceitar libera na hora (e dispara FR-201).

### 2. Onboarding (tour das funcionalidades)
- FR-201: após o aceite (ou via comando **`/tour`**), um **tour de ~5 passos** com destaque visual (spotlight) apresenta: navegação/sumário · cabeçalho do capítulo com downloads e tempo de leitura · o companion (paleta `/`, capacidades com tooltip) · os Bastidores · o convite a declarar um objetivo (`/plano`). Passos cujo alvo não existe na página são pulados; "pular tour" sempre visível; roda 1× por navegador (`cmp_tour`).

### 3. Telemetria de navegação
- FR-301: **somente após o aceite**, cada carregamento de página envia `POST /telemetry` (sendBeacon/keepalive) com `{session_id, slug}`; backend persiste em `nav_events` (session anônima, slug, timestamp) nos dois stores.
- FR-302: `GET /telemetry?token=ADMIN_TOKEN` devolve o resumo (páginas × visitas, últimos N eventos) — insumo do livro vivo (que capítulos recebem atenção).
- FR-303: privacidade: sem IP/UA persistidos, sessão anônima, `delete_session` continua apagando tudo da sessão (LGPD).

### 4. Objetivo do leitor + plano de ensino (via chat)
- FR-401: comando **`/plano <objetivo>`**: grava o objetivo (`POST /objetivo` → por sessão, nos dois stores) e pede ao tutor um **plano de ensino personalizado** (ordem de capítulos + trilha harness-zero) conectado ao objetivo.
- FR-402: com objetivo gravado, **toda conversa** ganha a camada de contexto "Objetivo declarado do leitor" no system prompt (o livro demonstrando a entrega de contexto do cap. 03) — o tutor conecta as respostas ao objetivo e sugere o próximo passo.
- FR-403: `/plano` sem argumento mostra o objetivo atual e ensina a redefinir; os Bastidores (bloco Memória da sessão) exibem o objetivo; `GET /objetivo?session_id=` para o widget.

## Não-funcionais
- NFR-001: tudo em JS puro no widget; nenhum dado pessoal solicitado; textos do disclaimer em PT claro e curto.
- NFR-002: compat: backend antigo → banner/tour funcionam (aceite só local, com re-tentativa silenciosa); telemetria/objetivo falham silenciosos.

## Verificação
- Suíte backend: consent gravado; telemetry persiste e resumo com token; objetivo gravado aparece no system prompt (via debug/resposta) e no GET.
- E2E: banner aparece 1×; aceite libera o chat e grava; tour navega e pula alvos ausentes; beacon disparado após aceite; /plano grava e o tutor recebe a camada; bastidores mostram o objetivo.
