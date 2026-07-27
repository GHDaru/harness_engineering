# Feature Specification: Widget do chat-companion no site

**Feature Branch**: `017-widget-chat-companion`

**Created**: 2026-07-27

**Status**: Draft

**Input**: O front-end do companion: um **chat flutuante** (launcher que **abre/minimiza** sobre um ícone) presente em **todas as páginas, inclusive a capa**. Ele **exibe claramente quais funcionalidades tem naquele momento** (dependendo do capítulo em que o leitor está) e conversa com o backend (feature 016) hospedado no Railway. Decisões do autor: aparece desde a capa; cabeçalho de capacidades por capítulo; identidade anônima por navegador; modos avançado × progressivo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - O leitor conversa com o companion desde a capa (Priority: P1)

Em qualquer página (capa incluída), há um **ícone flutuante**. Ao clicar, abre um **painel de chat**. No topo do painel, o leitor vê **o que o companion pode fazer naquele capítulo** (capacidades ativas). Ele digita, recebe resposta, e a conversa **continua** ao navegar (identidade anônima no navegador).

**Why this priority**: É o pedido central — dar ao leitor um ajudante presente desde o início, honesto sobre o que sabe fazer ali.

**Independent Test**: abrir qualquer página → ver o launcher → clicar → ver o cabeçalho de capacidades do capítulo + campo de conversa → enviar mensagem → receber resposta.

**Acceptance Scenarios**:

1. **Given** qualquer página do site, **When** carrego a página, **Then** vejo um **ícone flutuante** (launcher) no canto, inclusive na tela-capa.
2. **Given** o launcher, **When** clico, **Then** o painel **abre** (maximiza); clicando no minimizar/ícone ele **fecha** (minimiza) — o estado alterna.
3. **Given** o painel aberto numa página de capítulo N, **When** olho o topo, **Then** vejo **"o que posso fazer agora"** com as capacidades **ativas naquele capítulo** (e as bloqueadas indicadas), coerente com o modo.
4. **Given** o painel, **When** envio uma mensagem, **Then** aparece minha mensagem, um indicador de "digitando", e depois a resposta do companion.
5. **Given** que já conversei, **When** recarrego ou navego para outra página, **Then** o **histórico** continua (mesma identidade anônima do navegador).
6. **Given** o seletor de modo, **When** troco entre **Avançado** e **Progressivo**, **Then** o cabeçalho de capacidades e o comportamento se ajustam.

### Edge Cases

- **Backend indisponível**: o widget mostra um aviso amigável e não trava a página; o cabeçalho de capacidades ainda aparece (mapa embutido no build).
- **Mobile**: o painel ocupa quase a tela; não quebra a rolagem da página; o launcher não cobre conteúdo essencial.
- **Capa (fundo escuro)**: o widget é legível sobre a splash.
- **Acessibilidade**: launcher com `aria-label`; foco ao abrir; navegável por teclado; contraste adequado.
- **Sem `localStorage`**: cai para uma sessão em memória da aba (sem persistência), sem quebrar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: DEVE existir um **launcher flutuante** em todas as páginas geradas (capítulos, sumário, **splash/capa**, aparato, autor), que **abre e minimiza** um painel de chat.
- **FR-002**: O painel DEVE exibir um **cabeçalho de capacidades** — "o que posso fazer agora (cap. N)" — listando as capacidades **ativas** e sinalizando as **bloqueadas**, conforme o **capítulo da página** e o **modo**.
- **FR-003**: O **capítulo da página** DEVE ser determinado em build-time e injetado por página (capítulos numerados → seu número; capa/aparato → baseline 0).
- **FR-004**: O widget DEVE conversar com o backend via `POST /chat` (com `session_id`, `message`, `chapter`, `mode`) e renderizar a resposta; DEVE mostrar estado de "enviando".
- **FR-005**: A identidade DEVE ser **anônima por navegador** (`session_id` em `localStorage`); ao abrir, DEVE tentar carregar o **histórico** (`GET /history`).
- **FR-006**: DEVE haver um seletor de **modo** (Avançado × Progressivo), persistido no navegador, afetando o cabeçalho e o parâmetro enviado.
- **FR-007**: A **URL do backend** DEVE ser configurável em build-time (uma constante/config, não espalhada no código).
- **FR-008**: O widget DEVE **degradar com elegância** se o backend falhar (aviso amigável; página nunca trava; cabeçalho de capacidades ainda renderiza a partir de um mapa embutido no build).
- **FR-009**: DEVE ser **responsivo**, **theme-aware** e **acessível** (aria-label, foco, teclado, contraste), inclusive sobre a capa escura.
- **FR-010**: O portão de link-check do build DEVE continuar verde; sem identificador interno de modelo em qualquer artefato.

### Key Entities

- **Launcher**: botão flutuante fixo; alterna o painel.
- **Painel**: cabeçalho (título + modo + capacidades) + área de mensagens + input.
- **Config de página**: `{backend, chapter, capabilities[]}` injetada por página no build.

## Success Criteria *(mandatory)*

- **SC-001**: O launcher aparece em todas as páginas, incluindo a capa; abre/minimiza o painel.
- **SC-002**: Numa página de capítulo N, o cabeçalho mostra as capacidades ativas até N (progressivo) ou todas (avançado).
- **SC-003**: Enviar uma mensagem retorna resposta do backend e ela aparece no painel; o histórico sobrevive à navegação.
- **SC-004**: Trocar de modo muda o cabeçalho de capacidades.
- **SC-005**: Com o backend fora, a página não trava e o cabeçalho ainda renderiza (mapa embutido).
- **SC-006**: Responsivo (~375px sem overflow), theme-aware, launcher com `aria-label`; build verde; zero identificador interno de modelo.

## Assumptions

- Backend já no ar (feature 016) em `harnessengineering-production.up.railway.app`; CORS libera `https://ghdaru.github.io`.
- O mapa de capacidades para exibição é espelhado no build (rótulos estáveis); o **backend continua sendo quem impõe** o gating no `/chat` (segurança).
- Feature toca o motor `publicar/` → ciclo spec-kit (Princípio VII); merge dispara o deploy do site.
