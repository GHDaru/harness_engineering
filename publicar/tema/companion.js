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

  var launcher = el("button", "cmp-launcher"); launcher.setAttribute("aria-label", "Abrir o companion do livro");
  launcher.innerHTML = "💬";

  var panel = el("section", "cmp-panel"); panel.setAttribute("role", "dialog");
  panel.setAttribute("aria-label", "Companion do livro");

  var head = el("div", "cmp-head");
  var title = el("div", "cmp-title"); title.appendChild(el("span", null, "Companion"));
  var capTag = el("span", "cmp-cap", CHAPTER ? ("cap. " + CHAPTER) : "capa"); title.appendChild(capTag);
  var actions = el("div", "cmp-actions");
  var modeSel = el("select", "cmp-mode"); modeSel.setAttribute("aria-label", "Modo do companion");
  [["progressivo", "Progressivo"], ["avancado", "Avançado"]].forEach(function (m) {
    var o = el("option", null, m[1]); o.value = m[0]; if (m[0] === MODE) o.selected = true; modeSel.appendChild(o);
  });
  var minBtn = el("button", "cmp-min", "–"); minBtn.setAttribute("aria-label", "Minimizar o companion");
  var sugBtn = el("button", "cmp-min", "💡"); sugBtn.setAttribute("aria-label", "Enviar sugestão ao autor"); sugBtn.title = "Enviar sugestão ao autor";
  var limparBtn = el("button", "cmp-min", "🗑"); limparBtn.setAttribute("aria-label", "Apagar a conversa"); limparBtn.title = "Apagar a conversa";
  actions.appendChild(modeSel); actions.appendChild(sugBtn); actions.appendChild(limparBtn); actions.appendChild(minBtn);
  head.appendChild(title); head.appendChild(actions);

  var capsBox = el("div", "cmp-caps");
  var capsT = el("p", "cmp-caps-t"); var chips = el("div", "cmp-chips");
  capsBox.appendChild(capsT); capsBox.appendChild(chips);

  var msgs = el("div", "cmp-msgs");

  var form = el("form", "cmp-form");
  var input = el("textarea", "cmp-input"); input.rows = 1; input.placeholder = "Pergunte sobre o livro…";
  input.setAttribute("aria-label", "Sua mensagem");
  var send = el("button", "cmp-send", "➤"); send.type = "submit"; send.setAttribute("aria-label", "Enviar");
  form.appendChild(input); form.appendChild(send);

  var sugForm = el("form", "cmp-sugform"); sugForm.hidden = true;
  var sugTxt = el("textarea", "cmp-input"); sugTxt.rows = 3; sugTxt.placeholder = "Sua sugestão para o livro… (vai para o autor)";
  sugTxt.setAttribute("aria-label", "Texto da sugestão");
  var sugSend = el("button", "cmp-send", "➤"); sugSend.type = "submit"; sugSend.setAttribute("aria-label", "Enviar sugestão");
  sugForm.appendChild(sugTxt); sugForm.appendChild(sugSend);
  panel.appendChild(head); panel.appendChild(capsBox); panel.appendChild(msgs); panel.appendChild(sugForm); panel.appendChild(form);
  root.appendChild(launcher); root.appendChild(panel);

  // --- render ---
  function renderCaps() {
    capTag.textContent = CHAPTER ? ("cap. " + CHAPTER) : "capa";
    capsT.textContent = "O que posso fazer agora" + (MODE === "avancado" ? " (avançado)" : (CHAPTER ? " (até o cap. " + CHAPTER + ")" : ""));
    chips.innerHTML = "";
    capsAtivas().forEach(function (c) {
      var ch = el("span", "cmp-chip", c.rotulo); ch.setAttribute("data-on", c.on ? "true" : "false"); chips.appendChild(ch);
    });
  }
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
    addMsg("sys", "Olá! Sou o companion deste livro vivo. Pergunte o que quiser — eu respondo com base no texto do livro.");
  }
  function sendMsg(text) {
    addMsg("user", text);
    send.disabled = true;
    var typing = el("div", "cmp-typing", "digitando…"); msgs.appendChild(typing); msgs.scrollTop = msgs.scrollHeight;
    api("/chat", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ session_id: SID, message: text, chapter: CHAPTER, mode: MODE })
    }).then(function (d) {
      typing.remove(); addMsg("bot", d.reply || "(sem resposta)", true);
    }).catch(function (err) {
      typing.remove();
      addMsg("sys", "⚠️ Não consegui falar com o companion agora (" + err.message + "). Tente de novo em instantes.");
    }).then(function () { send.disabled = false; input.focus(); });
  }

  // --- eventos ---
  function open() { root.setAttribute("data-open", "true"); renderCaps(); loadHistory(); setTimeout(function () { input.focus(); }, 30); }
  function close() { root.setAttribute("data-open", "false"); }
  launcher.addEventListener("click", open);
  minBtn.addEventListener("click", close);
  modeSel.addEventListener("change", function () { MODE = modeSel.value; set("cmp_mode", MODE); renderCaps(); });
  limparBtn.addEventListener("click", function () {
    if (!confirm("Apagar toda a conversa? (não dá para desfazer)")) return;
    api("/session/" + encodeURIComponent(SID), { method: "DELETE" })
      .catch(function () {})
      .then(function () { msgs.innerHTML = ""; greeted = false; histLoaded = true; greet(); });
  });
  sugBtn.addEventListener("click", function () {
    sugForm.hidden = !sugForm.hidden;
    if (!sugForm.hidden) sugTxt.focus();
  });
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
  form.addEventListener("submit", function (e) {
    e.preventDefault(); var t = input.value.trim(); if (!t) return; input.value = ""; input.style.height = "auto"; sendMsg(t);
  });
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
  });
  input.addEventListener("input", function () { input.style.height = "auto"; input.style.height = Math.min(input.scrollHeight, 120) + "px"; });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && root.getAttribute("data-open") === "true") close(); });

  renderCaps();
  document.addEventListener("DOMContentLoaded", function () { document.body.appendChild(root); });
  if (document.readyState !== "loading") document.body.appendChild(root);
})();
