/* Widget do chat-companion — JS puro, sem dependências.
   Lê window.COMPANION = { backend, chapter, mode, capabilities:[{chave,rotulo,descricao,libera}] }.
   O backend (feature 016) é quem IMPÕE o gating no /chat; aqui o mapa é só exibição. */
(function () {
  "use strict";
  var CFG = window.COMPANION || {};
  var BACKEND = (CFG.backend || "").replace(/\/+$/, "");
  var CHAPTER = (typeof CFG.chapter === "number") ? CFG.chapter : 0;
  var CAPS = CFG.capabilities || [];

  // --- estado persistente (anônimo por navegador) ---
  var mem = {};
  function get(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return mem[k] || d; } }
  function set(k, v) { try { localStorage.setItem(k, v); } catch (e) { mem[k] = v; } }
  function uuid() {
    try { if (crypto && crypto.randomUUID) return crypto.randomUUID(); } catch (e) {}
    return "anon-" + Math.random().toString(36).slice(2) + Date.now().toString(36);
  }
  var SID = get("cmp_sid", ""); if (!SID) { SID = uuid(); set("cmp_sid", SID); }
  var MODE = get("cmp_mode", CFG.mode || "progressivo");
  var LANG_EN = (CFG.lang === "en"); // spec 067: superficie principal traduzida
  function tx(pt, en) { return LANG_EN ? en : pt; }
  // Estados de layout (spec 053): float (padrão) | dock (sidebar) | max (dock largo).
  var DOCK = get("cmp_dock", "float"); if (["float","dock","max"].indexOf(DOCK) < 0) DOCK = "float";
  // Consentimento (spec 054): versão do texto; mudou o texto => nova versão => novo aceite.
  var CONSENT_V = "v1";
  var CONSENT_TXT = tx("As conversas com o companion são usadas para o aprimoramento vivo deste livro. Nunca compartilhe dados pessoais (nome completo, email, documentos, senhas) no chat.", "Conversations with the companion feed the living improvement of this book. Never share personal data (full name, email, documents, passwords) in the chat.");
  function consentiu() { return get("cmp_consent", "").indexOf(CONSENT_V + ":") === 0; }
  function aceitarConsent() {
    set("cmp_consent", CONSENT_V + ":" + Date.now());
    if (BACKEND) fetch(BACKEND + "/consent", { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ session_id: SID, versao: CONSENT_V }) }).catch(function () {});
  }
  // BYOK (spec 048): a chave vive SÓ no localStorage deste navegador; é lida
  // no momento do envio e nunca aparece em texto claro na tela.
  function byok() { return (get("cmp_byok", "") || "").trim(); }
  function byokMask() { var k = byok(); return k ? "…" + k.slice(-4) : ""; }

  // --- helpers ---
  function el(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt != null) e.textContent = txt; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fmt(s) { // markdown mínimo e SEGURO (escapa antes)
    return esc(s)
      .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")            // **negrito**
      .replace(/(^|[^*])\*(?!\s)([^*\n]+?)\*/g, "$1<em>$2</em>")     // *itálico* (não toca no **; _snake_case_ preservado)
      .replace(/`([^`]+)`/g, "<code>$1</code>")                      // `código`
      .replace(/\[([^\]]+\.md[^\]]*)\]/g, '<span class="cmp-src">📖 $1</span>'); // citação do livro
  }
  function capsAtivas() {
    return CAPS.map(function (c) {
      return { rotulo: c.rotulo, on: MODE === "avancado" || c.libera <= CHAPTER };
    });
  }

  // --- DOM ---
  var root = el("div", "cmp"); root.id = "companion"; root.setAttribute("data-open", "false");

  var launcher = el("button", "cmp-launcher"); launcher.setAttribute("aria-label", tx("Abrir o companion do livro", "Open the book companion"));
  launcher.innerHTML = "💬";

  var panel = el("section", "cmp-panel"); panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "Companion do livro");

  var head = el("div", "cmp-head");
  var title = el("div", "cmp-title"); title.appendChild(el("span", null, "Companion"));
  var capTag = el("span", "cmp-cap", CHAPTER ? ("cap. " + CHAPTER) : "capa"); title.appendChild(capTag);
  var byokSelo = el("button", "cmp-byok-selo", "🔑"); byokSelo.hidden = true;
  byokSelo.setAttribute("aria-label", "Chave própria ativa — clique para remover");
  title.appendChild(byokSelo);
  var actions = el("div", "cmp-actions");
  var modeSel = el("select", "cmp-mode"); modeSel.setAttribute("aria-label", "Modo do companion");
  [["progressivo", "Progressivo"], ["avancado", "Avançado"]].forEach(function (m) {
    var o = el("option", null, m[1]); o.value = m[0]; if (m[0] === MODE) o.selected = true; modeSel.appendChild(o);
  });
  var minBtn = el("button", "cmp-min", "–"); minBtn.setAttribute("aria-label", "Minimizar o companion");
  var limparBtn = el("button", "cmp-min", "🗑"); limparBtn.setAttribute("aria-label", "Apagar a conversa"); limparBtn.title = "Apagar a conversa";
  var dockBtn = el("button", "cmp-min", "◧"); dockBtn.setAttribute("aria-label", "Ancorar como sidebar");
  var maxBtn = el("button", "cmp-min", "⤢"); maxBtn.setAttribute("aria-label", "Maximizar");
  actions.appendChild(modeSel); actions.appendChild(limparBtn); actions.appendChild(dockBtn); actions.appendChild(maxBtn); actions.appendChild(minBtn);
  head.appendChild(title); head.appendChild(actions);

  var capsBox = el("div", "cmp-caps");
  var capsT = el("p", "cmp-caps-t"); var chips = el("div", "cmp-chips");
  capsBox.appendChild(capsT); capsBox.appendChild(chips);

  var msgs = el("div", "cmp-msgs");

  var form = el("form", "cmp-form cmp-entrada");
  var pal = el("div", "cmp-pal"); pal.hidden = true; // paleta de comandos (/)
  var input = el("textarea", "cmp-input"); input.rows = 3; input.placeholder = tx("Pergunte sobre o livro…", "Ask about the book…");
  input.setAttribute("aria-label", "Sua mensagem");
  var linha = el("div", "cmp-ent-linha");
  var dica = el("span", "cmp-ent-dica", "Enter envia · Shift+Enter quebra linha · / comandos");
  var send = el("button", "cmp-send cmp-send-rot", tx("Enviar ➤", "Send ➤")); send.type = "submit"; send.setAttribute("aria-label", "Enviar");
  linha.appendChild(dica); linha.appendChild(send);
  form.appendChild(pal); form.appendChild(input); form.appendChild(linha);

  var sugForm = el("form", "cmp-sugform"); sugForm.hidden = true;
  var sugTxt = el("textarea", "cmp-input"); sugTxt.rows = 3; sugTxt.placeholder = "Sua sugestão para o livro… (vai para o autor)";
  sugTxt.setAttribute("aria-label", "Texto da sugestão");
  var sugSend = el("button", "cmp-send", "➤"); sugSend.type = "submit"; sugSend.setAttribute("aria-label", "Enviar sugestão");
  sugForm.appendChild(sugTxt); sugForm.appendChild(sugSend);

  var byokForm = el("form", "cmp-sugform cmp-byokform"); byokForm.hidden = true;
  var byokTxt = el("input", "cmp-input"); byokTxt.type = "password"; byokTxt.placeholder = "Cole sua chave de API… (fica só neste navegador)";
  byokTxt.setAttribute("aria-label", "Sua chave de API");
  var byokSave = el("button", "cmp-send", "✓"); byokSave.type = "submit"; byokSave.setAttribute("aria-label", "Salvar chave");
  byokForm.appendChild(byokTxt); byokForm.appendChild(byokSave);
  var consentCard = el("div", "cmp-consent"); consentCard.hidden = true;
  var status = el("div", "cmp-status"); status.setAttribute("role", "button"); status.tabIndex = 0;
  status.title = "Abrir os bastidores (contexto injetado, tokens, chamadas)";
  var aux = el("aside", "cmp-aux"); aux.hidden = true; aux.setAttribute("aria-label", "Bastidores do companion");
  panel.appendChild(head); panel.appendChild(capsBox); panel.appendChild(msgs); panel.appendChild(sugForm); panel.appendChild(byokForm); panel.appendChild(consentCard); panel.appendChild(form); panel.appendChild(status);
  root.appendChild(launcher); root.appendChild(aux); root.appendChild(panel);

  // --- render ---
  // Explicabilidade (spec 053): dados ricos do /capabilities (descrição + capítulo
  // que libera) alimentam tooltips nos chips; fallback ao espelho local (CFG).
  var capsRicas = null, tip = el("div", "cmp-tip"); tip.hidden = true;
  function carregarCaps() {
    api("/capabilities?chapter=" + CHAPTER + "&mode=" + MODE, {}).then(function (d) {
      capsRicas = d.capabilities || null; renderCaps();
    }).catch(function () {});
  }
  function mostrarTip(chip, c) {
    tip.innerHTML = "";
    var b1 = el("b", null, c.rotulo); tip.appendChild(b1);
    if (c.descricao) tip.appendChild(el("div", null, c.descricao));
    var lib = (c.libera_no_capitulo != null ? c.libera_no_capitulo : c.libera) || 0;
    tip.appendChild(el("div", "cmp-tip-st", c.on ? ("✓ liberado" + (lib ? " no cap. " + String(lib).padStart(2, "0") : "")) :
      ("🔒 libera no cap. " + String(lib).padStart(2, "0") + " — continue lendo")));
    chip.appendChild(tip); tip.hidden = false;
  }
  function esconderTip() { tip.hidden = true; if (tip.parentNode) tip.parentNode.removeChild(tip); }
  function renderCaps() {
    capTag.textContent = CHAPTER ? ("cap. " + CHAPTER) : "capa";
    byokSelo.hidden = !byok();
    byokSelo.title = byok() ? ("Usando sua chave (" + byokMask() + ") — clique para remover") : "";
    capsT.textContent = tx("O que posso fazer agora", "What I can do now") + (MODE === "avancado" ? " (avançado)" : (CHAPTER ? " (até o cap. " + CHAPTER + ")" : ""));
    chips.innerHTML = "";
    var lista = capsRicas
      ? capsRicas.map(function (c) { return { rotulo: c.rotulo, descricao: c.descricao, libera_no_capitulo: c.libera_no_capitulo, on: !!c.ativa }; })
      : CAPS.map(function (c) { return { rotulo: c.rotulo, libera: c.libera, on: MODE === "avancado" || c.libera <= CHAPTER }; });
    lista.forEach(function (c) {
      var ch = el("span", "cmp-chip", c.rotulo); ch.setAttribute("data-on", c.on ? "true" : "false"); ch.tabIndex = 0;
      ch.addEventListener("mouseenter", function () { mostrarTip(ch, c); });
      ch.addEventListener("mouseleave", esconderTip);
      ch.addEventListener("focus", function () { mostrarTip(ch, c); });
      ch.addEventListener("blur", esconderTip);
      ch.addEventListener("click", function (e) { e.stopPropagation(); tip.hidden || tip.parentNode !== ch ? mostrarTip(ch, c) : esconderTip(); });
      chips.appendChild(ch);
    });
  }
  // Bastidores (spec 053): contadores da sessão + debug do último turno.
  var stats = { chamadas: 0, tools: 0 }, lastDebug = null, health = null;
  function tokensFmt(t) { return t >= 1000 ? "~" + (t / 1000).toFixed(1).replace(".", ",") + "k" : "~" + t; }
  function renderStatus() {
    status.innerHTML = "";
    var d = lastDebug || {};
    status.appendChild(el("span", null, "🧠 " + (d.tokens_estimados ? tokensFmt(d.tokens_estimados) : "—") + " tokens"));
    status.appendChild(el("span", null, "🔁 " + stats.chamadas + " chamada" + (stats.chamadas === 1 ? "" : "s")));
    status.appendChild(el("span", null, "📎 " + ((d.trechos || []).length) + " trechos"));
    var abrir = el("span", "cmp-status-abrir", aux.hidden ? "𝍢 bastidores" : "𝍢 fechar");
    status.appendChild(abrir);
  }
  function renderAux() {
    aux.innerHTML = "";
    var tabs = el("div", "cmp-aux-tabs");
    var t1 = el("span", "on", "𝍢 Bastidores"), t2 = el("span", null, "📄 Documentos");
    var fechar = el("button", "cmp-aux-x", "×"); fechar.setAttribute("aria-label", "Fechar bastidores");
    fechar.addEventListener("click", function () { toggleAux(false); });
    tabs.appendChild(t1); tabs.appendChild(t2); tabs.appendChild(fechar); aux.appendChild(tabs);
    var corpo = el("div", "cmp-aux-corpo"); aux.appendChild(corpo);
    var d = lastDebug;
    function bloco(titulo) { var x = el("div", "cmp-bloco"); x.appendChild(el("div", "cmp-bloco-t", titulo)); corpo.appendChild(x); return x; }
    function kv(pai, k, v) { var l = el("div", "cmp-kv"); l.appendChild(el("span", null, k)); l.appendChild(el("b", null, v)); pai.appendChild(l); }
    function abaBastidores() {
      corpo.innerHTML = "";
      var b1 = bloco("Janela de contexto");
      if (d) {
        kv(b1, "Tokens estimados", tokensFmt(d.tokens_estimados) + " / " + tokensFmt(d.janela_tokens).replace("~", ""));
        var barra = el("div", "cmp-barra"); var fill = el("i");
        fill.style.width = Math.min(100, Math.round(100 * d.tokens_estimados / (d.janela_tokens || 1))) + "%";
        barra.appendChild(fill); b1.appendChild(barra);
        kv(b1, "Mensagens no histórico", d.historico_msgs + " (janela: 40)");
      } else { b1.appendChild(el("div", "cmp-aux-vazio", "Envie uma mensagem para ver os dados do turno.")); }
      kv(b1, "Chamadas ao modelo", String(stats.chamadas));
      kv(b1, "Tools executadas", String(stats.tools));
      var b2 = bloco("Injetado neste turno");
      if (d) {
        kv(b2, "Modo", d.modo === "avancado" ? "avançado" : "progressivo");
        kv(b2, "Capacidades ativas", String((d.capacidades_ativas || []).length));
        kv(b2, "Trechos do livro (RAG)", String((d.trechos || []).length));
        (d.trechos || []).forEach(function (t) {
          var l = el("div", "cmp-trecho"); l.appendChild(el("span", null, "📖 " + t.fonte + " · "));
          var i = el("i", null, "“" + (t.preview || t.titulo || "") + "…”"); l.appendChild(i); b2.appendChild(l);
        });
      } else { b2.appendChild(el("div", "cmp-aux-vazio", "Sem dados deste turno (backend sem debug ou nenhum turno ainda).")); }
      var b3 = bloco("Memória da sessão");
      kv(b3, "Sessão anônima", "…" + SID.slice(-4));
      kv(b3, "Persistência", health ? (health.store === "postgres" ? "Postgres (Neon)" : "memória") : "—");
      kv(b3, "Sua chave (BYOK)", byok() ? ("ativa (" + byokMask() + ")") : "não configurada");
      kv(b3, "Objetivo (/plano)", (d && d.objetivo) ? d.objetivo : "não declarado");
      t1.className = "on"; t2.className = "";
    }
    function abaDocs() {
      corpo.innerHTML = "";
      var slug = (document.body.getAttribute("data-slug") || "").trim();
      var b1 = bloco("Esta página");
      if (slug && slug !== "sumario" && slug !== "index") {
        var l1 = el("a", "cmp-doc", "⬇ " + slug + ".md — fonte Markdown"); l1.href = "md/" + slug + ".md"; l1.setAttribute("download", "");
        var l2 = el("a", "cmp-doc", "⬇ " + slug + ".pdf — PDF do capítulo"); l2.href = "pdf/" + slug + ".pdf";
        b1.appendChild(l1); b1.appendChild(l2);
      } else { b1.appendChild(el("div", "cmp-aux-vazio", "Abra um capítulo para ver os downloads dele.")); }
      var b2 = bloco("Fontes citadas na conversa");
      var fontes = {};
      ((lastDebug || {}).trechos || []).forEach(function (t) { if (t.fonte) fontes[t.fonte] = true; });
      var lista = Object.keys(fontes);
      if (lista.length) lista.forEach(function (f) {
        var a2 = el("a", "cmp-doc", "📖 " + f); a2.href = f.replace(/\.md$/i, ".html"); b2.appendChild(a2);
      });
      else b2.appendChild(el("div", "cmp-aux-vazio", "As fontes dos trechos usados aparecem aqui."));
      t2.className = "on"; t1.className = "";
    }
    t1.addEventListener("click", abaBastidores);
    t2.addEventListener("click", abaDocs);
    abaBastidores();
  }
  function toggleAux(abrirAux) {
    var novo = (typeof abrirAux === "boolean") ? abrirAux : aux.hidden;
    aux.hidden = !novo;
    if (novo) { if (!health) api("/health", {}).then(function (h) { health = h; renderAux(); }).catch(function () {}); renderAux(); }
    renderStatus();
  }
  status.addEventListener("click", function () { toggleAux(); });
  status.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleAux(); } });

  function addMsg(role, text, asHtml) {
    var m = el("div", "cmp-msg " + role);
    if (asHtml) m.innerHTML = fmt(text); else m.textContent = text;
    msgs.appendChild(m); msgs.scrollTop = msgs.scrollHeight; return m;
  }

  // --- backend ---
  var greeted = false, histLoaded = false;
  function api(path, opts) {
    if (!BACKEND) return Promise.reject(new Error("sem backend"));
    return fetch(BACKEND + path, opts).then(function (r) {
      if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { throw new Error(j.detail || ("HTTP " + r.status)); });
      return r.json();
    });
  }
  function loadHistory() {
    if (histLoaded) return; histLoaded = true;
    api("/history?session_id=" + encodeURIComponent(SID), {}).then(function (d) {
      (d.messages || []).forEach(function (m) { addMsg(m.role === "user" ? "user" : "bot", m.content, m.role !== "user"); });
      if (!(d.messages || []).length && !greeted) greet();
    }).catch(function () { if (!greeted) greet(); });
  }
  function greet() {
    greeted = true;
    addMsg("sys", "Olá! Sou o companion deste livro vivo. Pergunte o que quiser — eu respondo com base no texto do livro. Digite / para ver os comandos (sugestão ao autor, sua chave de API, bastidores…).");
  }
  // Streaming SSE (spec 047): consome POST /chat/stream via fetch+ReadableStream,
  // renderiza o texto conforme chega (textContent) e aplica markdown no final.
  // Qualquer falha cai no /chat clássico (compatível com backend antigo).
  function sendMsgStream(text, typing) {
    return fetch(BACKEND + "/chat/stream", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ session_id: SID, message: text, chapter: CHAPTER, mode: MODE, byok_key: byok() || undefined })
    }).then(function (r) {
      if (!r.ok || !r.body) throw new Error("HTTP " + r.status);
      typing.remove();
      var m = addMsg("bot", "");
      var reader = r.body.getReader(), dec = new TextDecoder(), buf = "", texto = "", houveErro = null;
      function trata(ev) {
        if (ev.delta) { texto += ev.delta; m.textContent = texto; msgs.scrollTop = msgs.scrollHeight; }
        if (ev.trace) { addMsg("sys", ev.trace); stats.tools++; }
        if (ev.erro) { houveErro = ev.erro; }
        if (ev.done) {
          m.innerHTML = fmt(ev.reply || texto || "(sem resposta)");
          if (ev.debug) { lastDebug = ev.debug; renderStatus(); if (!aux.hidden) renderAux(); }
        }
      }
      function pump() {
        return reader.read().then(function (x) {
          if (x.done) {
            if (houveErro) { m.remove(); var e2 = new Error(houveErro); e2.semFallback = true; throw e2; }
            if (!texto) { m.innerHTML = fmt("(sem resposta)"); }
            return;
          }
          buf += dec.decode(x.value, { stream: true });
          var blocos = buf.split("\n\n"); buf = blocos.pop();
          blocos.forEach(function (l) {
            if (l.indexOf("data: ") === 0) { try { trata(JSON.parse(l.slice(6))); } catch (e) {} }
          });
          return pump();
        });
      }
      return pump();
    });
  }

  function sendMsg(text) {
    addMsg("user", text);
    send.disabled = true; stats.chamadas++; renderStatus();
    var typing = el("div", "cmp-typing", "digitando…"); msgs.appendChild(typing); msgs.scrollTop = msgs.scrollHeight;
    var fallback = function () {
      return api("/chat", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ session_id: SID, message: text, chapter: CHAPTER, mode: MODE, byok_key: byok() || undefined })
      }).then(function (d) {
        typing.remove(); addMsg("bot", d.reply || "(sem resposta)", true);
        stats.tools += (d.trace || []).length;
        if (d.debug) { lastDebug = d.debug; renderStatus(); if (!aux.hidden) renderAux(); }
      });
    };
    (BACKEND ? sendMsgStream(text, typing).catch(function (err) {
      // erro do modelo no meio do stream: o turno já foi persistido — não
      // repetir via /chat (duplicaria o histórico); só transporte faz fallback.
      if (err && err.semFallback) throw err;
      return fallback();
    }) : fallback())
      .catch(function (err) {
        if (typing.parentNode) typing.remove();
        var dica = /limite|BYOK/i.test(err.message) ? " Dica: escreva /chave para usar sua própria chave de API (sem limite do projeto)." : "";
        addMsg("sys", "⚠️ Não consegui falar com o companion agora (" + err.message + ")." + dica);
      }).then(function () { send.disabled = false; input.focus(); });
  }

  // --- eventos ---
  // Dock (spec 053): aplica o estado no root + empurra o conteúdo via classe no <html>.
  function aplicarDock() {
    root.setAttribute("data-dock", DOCK);
    var aberto = root.getAttribute("data-open") === "true";
    var docked = aberto && (DOCK === "dock" || DOCK === "max") && window.innerWidth > 820;
    document.documentElement.classList.toggle("cmp-docked", docked);
    document.documentElement.style.setProperty("--cmp-dockw", DOCK === "max" ? "640px" : "430px");
    dockBtn.textContent = DOCK === "float" ? "◧" : "❐";
    dockBtn.setAttribute("aria-label", DOCK === "float" ? "Ancorar como sidebar" : "Voltar a flutuar");
    dockBtn.title = dockBtn.getAttribute("aria-label");
    maxBtn.hidden = DOCK === "float";
    maxBtn.textContent = DOCK === "max" ? "⤡" : "⤢";
    maxBtn.setAttribute("aria-label", DOCK === "max" ? "Restaurar largura" : "Maximizar");
    maxBtn.title = maxBtn.getAttribute("aria-label");
  }
  function setDock(d) { DOCK = d; set("cmp_dock", d); aplicarDock(); }
  dockBtn.addEventListener("click", function () { setDock(DOCK === "float" ? "dock" : "float"); });
  maxBtn.addEventListener("click", function () { setDock(DOCK === "max" ? "dock" : "max"); });
  window.addEventListener("resize", aplicarDock);
  function open() {
    root.setAttribute("data-open", "true"); aplicarDock(); renderCaps(); carregarCaps(); renderStatus(); loadHistory();
    if (banner) banner.style.display = "none"; // o cartão de aceite do chat assume
    setTimeout(function () { input.focus(); }, 30);
  }
  function close() {
    root.setAttribute("data-open", "false"); aux.hidden = true; aplicarDock();
    if (banner && !consentiu()) banner.style.display = "";
  }
  launcher.addEventListener("click", open);
  minBtn.addEventListener("click", close);
  modeSel.addEventListener("change", function () { MODE = modeSel.value; set("cmp_mode", MODE); renderCaps(); });
  function limparConversa() {
    if (!confirm("Apagar toda a conversa? (não dá para desfazer)")) return;
    api("/session/" + encodeURIComponent(SID), { method: "DELETE" })
      .catch(function () {})
      .then(function () { msgs.innerHTML = ""; greeted = false; histLoaded = true; greet(); });
  }
  limparBtn.addEventListener("click", limparConversa);
  // Sugestão sob demanda (spec 044): sem botão permanente — o formulário abre
  // quando o leitor pede no chat (comando /sugerir ou intenção explícita).
  function pedirSugestao() {
    sugForm.hidden = false;
    addMsg("sys", "💡 Escreva sua sugestão no campo destacado abaixo — ela vai por email ao autor. (Ela não passa pelo tutor.)");
    sugTxt.focus();
  }
  function pedirChave() {
    byokForm.hidden = false;
    addMsg("sys", "🔑 Cole sua chave de API no campo abaixo — ela fica só neste navegador (localStorage), nunca é enviada como mensagem nem persistida no servidor, e isenta do limite do projeto. Para remover depois: /chave limpar.");
    byokTxt.focus();
  }
  function ehPedidoDeChave(t) {
    if (/^\/chave\b|^\/byok\b/i.test(t)) return true;
    return /\b(byok|minha (própria )?chave)\b/i.test(t) && /\b(usar|colocar|configurar|cadastrar)\b/i.test(t);
  }
  function ehPedidoDeSugestao(t) {
    if (/^\/(sugerir|sugestao|sugestão)\b/i.test(t)) return true;
    return /sugest/i.test(t) && /\b(autor|enviar|mandar|deixar)\b/i.test(t);
  }
  sugForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = sugTxt.value.trim(); if (!t) return;
    sugSend.disabled = true;
    api("/suggestion", { method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ session_id: SID, texto: t, pagina: location.pathname.split("/").pop() || "index.html" }) })
      .then(function () { sugTxt.value = ""; sugForm.hidden = true; addMsg("sys", "💡 Sugestão enviada ao autor — obrigado!"); })
      .catch(function (err) { addMsg("sys", "⚠️ Não consegui enviar a sugestão (" + err.message + ")."); })
      .then(function () { sugSend.disabled = false; });
  });
  byokForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var k = byokTxt.value.trim(); if (!k) return;
    set("cmp_byok", k); byokTxt.value = ""; byokForm.hidden = true; renderCaps();
    addMsg("sys", "🔑 Chave salva neste navegador (" + byokMask() + "). Suas próximas mensagens usam a sua chave.");
  });
  byokSelo.addEventListener("click", function () {
    if (!confirm("Remover sua chave deste navegador?")) return;
    set("cmp_byok", ""); renderCaps(); addMsg("sys", "🔑 Chave removida.");
  });
  // Paleta de comandos (spec 053): digitar "/" lista, ↑↓ navega, Enter aplica, Esc fecha.
  var COMANDOS = [
    { c: "/sugerir", d: "enviar uma sugestão ao autor (por email)" },
    { c: "/chave", d: "usar sua própria chave de API (BYOK)" },
    { c: "/chave limpar", d: "remover sua chave deste navegador" },
    { c: "/limpar", d: "apagar a conversa" },
    { c: "/bastidores", d: "ver contexto injetado, tokens e chamadas" },
    { c: "/plano", d: "declarar seu objetivo e receber um plano de ensino" },
    { c: "/tour", d: "rever o tour das funcionalidades do livro" }
  ];
  var palSel = 0, palItens = [];
  function fecharPal() { pal.hidden = true; palItens = []; }
  function renderPal(filtro) {
    palItens = COMANDOS.filter(function (x) { return x.c.indexOf(filtro) === 0; });
    if (!palItens.length) { fecharPal(); return; }
    if (palSel >= palItens.length) palSel = 0;
    pal.innerHTML = "";
    palItens.forEach(function (x, i) {
      var l = el("div", "cmp-pal-item" + (i === palSel ? " sel" : ""));
      l.appendChild(el("b", null, x.c)); l.appendChild(el("span", null, x.d));
      l.addEventListener("mousedown", function (e) { e.preventDefault(); aplicarComando(x.c); });
      pal.appendChild(l);
    });
    pal.hidden = false;
  }
  function aplicarComando(c) {
    fecharPal(); input.value = c; form.requestSubmit();
  }
  input.addEventListener("input", function () {
    var v = input.value;
    if (v.charAt(0) === "/" && v.indexOf("\n") < 0) { renderPal(v.trim()); } else { fecharPal(); }
  });
  input.addEventListener("keydown", function (e) {
    if (pal.hidden) return;
    if (e.key === "ArrowDown") { e.preventDefault(); palSel = (palSel + 1) % palItens.length; renderPal(input.value.trim()); }
    else if (e.key === "ArrowUp") { e.preventDefault(); palSel = (palSel - 1 + palItens.length) % palItens.length; renderPal(input.value.trim()); }
    else if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); aplicarComando(palItens[palSel].c); }
    else if (e.key === "Escape") { e.stopPropagation(); fecharPal(); }
  }, true);

  form.addEventListener("submit", function (e) {
    e.preventDefault(); var t = input.value.trim(); if (!t) return; input.value = ""; input.style.height = "auto"; fecharPal();
    if (/^\/limpar\b/i.test(t)) { limparConversa(); return; }
    if (/^\/bastidores\b/i.test(t)) { toggleAux(); return; }
    if (/^\/tour\b/i.test(t)) { iniciarTour(); return; }
    var mPlano = t.match(/^\/plano\s*(.*)$/i);
    if (mPlano) {
      var objetivo = mPlano[1].trim();
      if (!objetivo) {
        api("/objetivo?session_id=" + encodeURIComponent(SID), {}).then(function (d) {
          addMsg("sys", d.objetivo
            ? ("🎯 Seu objetivo atual: “" + d.objetivo + "”. Para redefinir: /plano <novo objetivo>.")
            : "🎯 Declare seu objetivo assim: /plano quero construir um agente para meu produto — eu gravo e traço um plano de ensino pelos capítulos.");
        }).catch(function () {
          addMsg("sys", "🎯 Declare seu objetivo assim: /plano <seu objetivo> — eu gravo e traço um plano de ensino.");
        });
        return;
      }
      addMsg("user", "/plano " + objetivo);
      api("/objetivo", { method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ session_id: SID, texto: objetivo }) })
        .catch(function () {})
        .then(function () {
          addMsg("sys", "🎯 Objetivo gravado. Ele agora acompanha todas as suas conversas (veja nos Bastidores).");
          sendMsg("Meu objetivo é: " + objetivo + ". Trace um plano de ensino por este livro para mim (ordem de capítulos, o que praticar no harness-zero e por onde começar hoje).");
        });
      return;
    }
    if (/^\/(chave|byok)\s+(limpar|remover)\b/i.test(t)) {
      set("cmp_byok", ""); renderCaps(); addMsg("sys", "🔑 Chave removida deste navegador."); return;
    }
    if (ehPedidoDeChave(t)) { addMsg("user", t); pedirChave(); return; }
    if (ehPedidoDeSugestao(t)) { addMsg("user", t); pedirSugestao(); return; }
    sendMsg(t);
  });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener("input", function () { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 220) + "px"; });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.getAttribute("data-open") === "true") close(); });

  // Tour de onboarding (spec 054): overlay + spotlight; passos declarativos;
  // alvo ausente na página é pulado; roda 1x por navegador (cmp_tour), ou via /tour.
  var PASSOS_TOUR = [
    { alvo: ".sidebar", t: "Navegação", d: "O sumário completo fica sempre à esquerda. A entrada do livro tem trilha guiada e o botão Retomar leva onde você parou." },
    { alvo: ".cap-hero", t: "Cabeçalho do capítulo", d: "Cada capítulo mostra a data do estado da arte, o tempo de leitura e os downloads ⬇ md/pdf deste capítulo." },
    { alvo: ".cmp-launcher, .cmp-panel", t: "Companion", d: "Este é o tutor do livro. Digite / para ver os comandos; passe o mouse nos chips para saber o que cada capacidade faz e quando libera." },
    { alvo: ".cmp-status", t: "Bastidores", d: "Aqui o livro se demonstra: tokens, chamadas e o que foi injetado na conversa. Clique para abrir o painel." },
    { alvo: null, t: "Seu objetivo", d: "Conte seu objetivo com /plano (ex.: /plano quero construir um agente para meu produto) e eu traço um plano de ensino pelos capítulos. Reveja este tour quando quiser com /tour." }
  ];
  var tourOverlay = null, tourCard = null, tourIdx = 0;
  function fecharTour() {
    if (tourOverlay) tourOverlay.remove(); if (tourCard) tourCard.remove();
    tourOverlay = tourCard = null; set("cmp_tour", "1");
  }
  function passoTour() {
    var passos = PASSOS_TOUR.filter(function (px) { return !px.alvo || document.querySelector(px.alvo); });
    if (tourIdx >= passos.length) { fecharTour(); return; }
    var px = passos[tourIdx];
    var alvoEl = px.alvo ? document.querySelector(px.alvo) : null;
    if (!tourOverlay) { tourOverlay = el("div", "cmp-tour-ov"); document.body.appendChild(tourOverlay); }
    if (!tourCard) { tourCard = el("div", "cmp-tour-card"); document.body.appendChild(tourCard); }
    // spotlight
    tourOverlay.innerHTML = "";
    var foco = el("div", "cmp-tour-foco");
    if (alvoEl) {
      var r = alvoEl.getBoundingClientRect();
      foco.style.left = (r.left - 6) + "px"; foco.style.top = (r.top - 6) + "px";
      foco.style.width = (r.width + 12) + "px"; foco.style.height = (r.height + 12) + "px";
      tourOverlay.appendChild(foco);
    }
    // cartão
    tourCard.innerHTML = "";
    tourCard.appendChild(el("div", "cmp-tour-n", (tourIdx + 1) + " / " + passos.length));
    tourCard.appendChild(el("b", null, px.t));
    tourCard.appendChild(el("p", null, px.d));
    var linhaT = el("div", "cmp-tour-bts");
    var pular = el("button", "cmp-tour-skip", "pular tour");
    pular.addEventListener("click", fecharTour);
    var prox = el("button", "cmp-send cmp-send-rot", tourIdx + 1 >= passos.length ? "Concluir ✓" : "Próximo →");
    prox.addEventListener("click", function () { tourIdx++; passoTour(); });
    linhaT.appendChild(pular); linhaT.appendChild(prox); tourCard.appendChild(linhaT);
    if (alvoEl) {
      var rr = alvoEl.getBoundingClientRect();
      var top = Math.min(window.innerHeight - 190, Math.max(12, rr.top));
      var left = rr.right + 330 < window.innerWidth ? rr.right + 14 : Math.max(12, rr.left - 314);
      tourCard.style.top = top + "px"; tourCard.style.left = left + "px";
    } else {
      tourCard.style.top = "50%"; tourCard.style.left = "50%"; tourCard.style.transform = "translate(-50%,-50%)";
    }
  }
  function iniciarTour() { tourIdx = 0; passoTour(); }
  function oferecerTour() {
    if (get("cmp_tour", "")) return;
    setTimeout(iniciarTour, 350);
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && tourOverlay) fecharTour(); });

  // Gate de consentimento no chat (spec 054): sem aceite, o cartão substitui a entrada.
  function renderConsent() {
    var ok = consentiu();
    consentCard.hidden = ok; form.hidden = !ok; status.hidden = !ok;
    if (!ok && !consentCard.childNodes.length) {
      consentCard.appendChild(el("div", "cmp-consent-t", "Antes de conversar…"));
      consentCard.appendChild(el("p", null, CONSENT_TXT));
      var bt = el("button", "cmp-send cmp-send-rot", tx("Entendi e aceito", "Got it, I accept"));
      bt.addEventListener("click", function () { aceitarConsent(); renderConsent(); banner && banner.remove(); oferecerTour(); input.focus(); });
      consentCard.appendChild(bt);
    }
  }

  // Banner do site (todas as páginas, até aceitar) + telemetria pós-consent.
  var banner = null;
  function montarBanner() {
    if (consentiu()) return;
    banner = el("div", "cmp-banner");
    var texto = el("span", null, "💬 " + CONSENT_TXT);
    var bt = el("button", "cmp-banner-bt", tx("Entendi e aceito", "Got it, I accept"));
    bt.addEventListener("click", function () { aceitarConsent(); banner.remove(); banner = null; renderConsent(); oferecerTour(); });
    banner.appendChild(texto); banner.appendChild(bt);
    document.body.appendChild(banner);
  }
  function telemetria() {
    if (!BACKEND || !consentiu()) return;
    var slug = (document.body.getAttribute("data-slug") || "").trim() || (location.pathname.split("/").pop() || "index").replace(/\.html$/, "");
    var corpo = JSON.stringify({ session_id: SID, slug: slug });
    try {
      if (navigator.sendBeacon) { navigator.sendBeacon(BACKEND + "/telemetry", new Blob([corpo], { type: "application/json" })); return; }
    } catch (e) {}
    fetch(BACKEND + "/telemetry", { method: "POST", headers: { "content-type": "application/json" }, body: corpo, keepalive: true }).catch(function () {});
  }

  renderCaps(); root.setAttribute("data-dock", DOCK); renderConsent();
  var bootFeito = false;
  function bootstrap() {
    if (bootFeito) return; bootFeito = true;
    document.body.appendChild(root); montarBanner(); telemetria();
  }
  document.addEventListener("DOMContentLoaded", bootstrap);
  if (document.readyState !== "loading") bootstrap();
})();
