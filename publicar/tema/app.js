// Interações mínimas do site: alternância de tema (persistida) e o "Retomar"
// da experiência de entrada (spec 021). Dependency-free.
(function () {
  var raiz = document.documentElement;
  var chave = "harness-tema";
  var salvo = localStorage.getItem(chave);
  if (salvo) raiz.setAttribute("data-tema", salvo);
  else if (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches)
    raiz.setAttribute("data-tema", "escuro");
  var btn = document.getElementById("alt-tema");
  if (btn)
    btn.addEventListener("click", function () {
      var atual = raiz.getAttribute("data-tema") === "escuro" ? "claro" : "escuro";
      raiz.setAttribute("data-tema", atual);
      localStorage.setItem(chave, atual);
    });

  // --- Progresso de leitura (spec 021 → 093) ---
  var corpo = document.body;
  var slug = corpo.getAttribute("data-slug");
  var titulo = corpo.getAttribute("data-titulo");
  var ehIndex = corpo.classList.contains("pagina-index");
  var LANG = corpo.getAttribute("data-lang") || "pt";
  var EN = LANG === "en";
  var CHAVE_ULT = "hz_ultimo" + (EN ? "_en" : "");
  var CHAVE_LIDOS = "hz_lidos" + (EN ? "_en" : "");
  var CHAVE_DISP = "hz_fimcap_dispensado";
  var CAPS = (window.LIVRO && window.LIVRO.caps) || [];

  // Não chamar de `tx`: o companion tem a sua própria `tx` e o checklist de
  // verificação proíbe o nome no tema desde a edição 0.64.
  function fala(pt, en) { return EN ? en : pt; }
  function ler(k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } }
  function gravar(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  // Ao abrir um capítulo (não o sumário), grava como "último lido".
  if (slug && !ehIndex && slug !== "sumario") {
    gravar(CHAVE_ULT, JSON.stringify({ slug: slug, titulo: titulo }));
  }

  // spec 093: o conjunto de capítulos já vistos vive no localStorage, e é o que
  // faz o leitor ANÔNIMO ver a própria barra. O servidor entra depois, como
  // reforço — não como pré-requisito. Pedir e-mail para mostrar progresso seria
  // cobrar antes de entregar, exatamente o que a spec diagnosticou como o erro
  // do convite anterior.
  function lidos() {
    var v = [];
    try { v = JSON.parse(ler(CHAVE_LIDOS, "[]")) || []; } catch (e) {}
    return v.filter(function (s) { return CAPS.indexOf(s) >= 0; });
  }

  function marcarLido(s) {
    if (CAPS.indexOf(s) < 0) return;
    var v = lidos();
    if (v.indexOf(s) >= 0) return;
    v.push(s);
    gravar(CHAVE_LIDOS, JSON.stringify(v));
  }

  function absorver(slugs) {
    var v = lidos(), mudou = false;
    for (var i = 0; i < slugs.length; i++)
      if (CAPS.indexOf(slugs[i]) >= 0 && v.indexOf(slugs[i]) < 0) { v.push(slugs[i]); mudou = true; }
    if (mudou) gravar(CHAVE_LIDOS, JSON.stringify(v));
    return mudou;
  }

  if (slug) marcarLido(slug);

  var local = null;
  try { local = JSON.parse(ler(CHAVE_ULT, "null")); } catch (e) {}

  function conectado() { return ler("cmp_email", ""); }

  // ---- A. o cartão "Sua leitura" no sumário ----
  function pintarLeitura() {
    var sec = document.getElementById("ent-leitura");
    if (!sec || !CAPS.length) return;
    var n = lidos().length;
    // Sem nenhum capítulo lido o cartão não existe: não há progresso para mostrar
    // nem para guardar, e um cartão vazio pedindo e-mail é só um anúncio.
    if (!n) { sec.hidden = true; return; }
    sec.hidden = false;

    var cont = document.getElementById("ent-leitura-cont");
    if (cont) cont.textContent = EN ? n + " of " + CAPS.length + " chapters"
                                    : n + " de " + CAPS.length + " capítulos";
    var barra = document.getElementById("ent-barra-i");
    if (barra) barra.style.width = Math.round((n / CAPS.length) * 100) + "%";

    var card = document.getElementById("ent-retomar");
    var cap = document.getElementById("ent-ret-cap");
    if (card && cap && local && local.slug) {
      card.setAttribute("href", local.slug + ".html");
      cap.textContent = local.titulo || local.slug;
      card.hidden = false;
    }
    pintarPe();
  }

  function pintarPe() {
    var pe = document.getElementById("ent-leitura-pe");
    if (!pe) return;
    pe.innerHTML = "";
    var email = conectado();
    if (email) {
      pe.appendChild(document.createTextNode("✉ " + fala("Sincronizado", "Synced") + " — " + email + " · "));
      pe.appendChild(botaoLink(fala("sair", "sign out"), sairDaqui));
      return;
    }
    pe.appendChild(document.createTextNode("ⓘ " + fala(
      "Este progresso vive só neste navegador. ",
      "This progress lives only in this browser. ")));
    if (!backend()) return;   // sem backend não há o que oferecer — e não se promete
    pe.appendChild(botaoLink("✉ " + fala("Guardar com um e-mail", "Save it with an e-mail"),
      function () { abrirForm(pe, "sumario"); }));
    pe.appendChild(document.createTextNode(" · "));
    pe.appendChild(botaoLink(fala("o que é isso?", "what is this?"), function () { explicar(pe); }));
  }

  function sairDaqui() {
    if (!confirm(fala("Desconectar este navegador? Nada é apagado — o mesmo e-mail traz tudo de volta.",
                    "Sign this browser out? Nothing is deleted — the same e-mail brings it all back."))) return;
    try { localStorage.removeItem("cmp_sid"); localStorage.removeItem("cmp_email"); } catch (e) {}
    location.reload();
  }

  // ---- B. o bloco de fim de capítulo ----
  // A partir do PRIMEIRO capítulo, não do terceiro. A regra genérica de produto
  // ("não peça antes de entregar valor") perdeu para o dado do próprio livro: a
  // telemetria mostra capa 17, sumário 9, introdução 7, capítulo 01 — 3. Um
  // convite no terceiro capítulo seria visto por ninguém, e quem lê um capítulo
  // e some é exatamente quem perde o progresso. O que se adapta é o tom.
  function pintarFimDeCapitulo() {
    var box = document.getElementById("fim-cap");
    if (!box || !backend() || conectado()) return;
    if (ler(CHAVE_DISP, "") === "1") return;
    var n = lidos().length;
    if (!n) return;

    box.innerHTML = "";
    var num = (String(titulo || "").match(/^\s*(\d+)/) || [])[1] || "";
    var cab = document.createElement("p");
    cab.className = "fim-cap-cab";
    cab.textContent = "✓ " + (num
      ? fala("Capítulo " + num + " concluído", "Chapter " + num + " done")
      : fala("Capítulo concluído", "Chapter done")) + " · " +
      (EN ? n + " of " + CAPS.length : n + " de " + CAPS.length);
    box.appendChild(cab);

    var p = document.createElement("p");
    p.className = "fim-cap-tx";
    p.appendChild(document.createTextNode(n < 3
      ? fala("Seu progresso está só neste navegador — não perca o fio. Guardar leva 10 segundos.",
           "Your progress lives only in this browser — don't lose the thread. Saving takes 10 seconds.")
      : fala("Você já andou " + n + " de " + CAPS.length + ", e isso está só neste navegador. Guardar leva 10 segundos.",
           "You're " + n + " of " + CAPS.length + " in, and that lives only in this browser. Saving takes 10 seconds.")));
    box.appendChild(p);
    abrirForm(box, "capitulo");

    var x = botaoLink(fala("agora não", "not now"), function () {
      gravar(CHAVE_DISP, "1");     // dispensou uma vez, não insiste de novo
      box.hidden = true;
    });
    x.className = "hz-link fim-cap-x";   // substituir a classe apagaria o estilo de link
    box.appendChild(x);
    box.hidden = false;
  }

  // ---- o formulário, compartilhado pelas duas superfícies ----
  function botaoLink(rotulo, aoClicar) {
    var b = document.createElement("button");
    b.type = "button"; b.className = "hz-link"; b.textContent = rotulo;
    b.addEventListener("click", aoClicar);
    return b;
  }

  function explicar(onde) {
    if (onde.querySelector(".hz-explica")) return;
    var p = document.createElement("p");
    p.className = "hz-explica";
    p.textContent = fala(
      "Você informa um e-mail e recebe um link. Ao abri-lo, sua leitura e suas conversas passam a acompanhar você em qualquer aparelho. Sem senha e sem cadastro — o e-mail serve para guardar a leitura. Depois de entrar, eu pergunto uma vez se você quer ser avisado quando sair um livro novo; dizer não não muda nada.",
      "You give an e-mail and get a link. Opening it makes your reading and conversations follow you on any device. No password, no account — the e-mail is there to keep your reading. Once you're in, I ask once whether you'd like to hear about a new book; saying no changes nothing.");
    onde.parentNode.insertBefore(p, onde.nextSibling);
  }

  function abrirForm(onde, origem) {
    var pai = origem === "capitulo" ? onde : onde.parentNode;
    if (pai.querySelector(".hz-assinar")) { pai.querySelector(".hz-assinar input").focus(); return; }
    var f = document.createElement("form");
    f.className = "hz-assinar";
    var i = document.createElement("input");
    i.type = "email"; i.required = true; i.autocomplete = "email";
    i.placeholder = fala("seu@email", "you@email");
    var b = document.createElement("button");
    b.type = "submit"; b.className = "ent-btn ent-btn-a"; b.textContent = fala("enviar", "send");
    var aviso = document.createElement("span");
    aviso.className = "hz-assinar-aviso";
    f.appendChild(i); f.appendChild(b); f.appendChild(aviso);
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      enviarLink(i.value, b, aviso);
    });
    if (origem === "capitulo") onde.appendChild(f);
    else pai.insertBefore(f, onde.nextSibling);
    i.focus();
  }

  function enviarLink(email, botao, aviso) {
    var mail = (email || "").trim();
    if (!mail) return;
    botao.disabled = true;
    aviso.className = "hz-assinar-aviso";
    aviso.textContent = fala("enviando…", "sending…");
    var corpo = { email: mail, lang: LANG };
    var sid = ler("cmp_sid", "");
    if (sid) corpo.session_id = sid;
    fetch(backend() + "/assinar", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify(corpo)
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        // Honestidade acima de conveniência (spec 084): sem link, dizer "enviado"
        // seria mentira — o leitor esperaria um e-mail que não vem.
        if (d && d.enviado) {
          aviso.textContent = "✓ " + fala(
            "Link enviado para " + mail + ". Vale uma vez e expira em " + (d.expira_min || 30) + " minutos.",
            "Link sent to " + mail + ". It works once and expires in " + (d.expira_min || 30) + " minutes.");
        } else {
          aviso.className = "hz-assinar-aviso erro";
          aviso.textContent = "⚠ " + fala(
            "Não consegui enviar agora. Seu progresso continua guardado neste navegador — tente daqui a pouco.",
            "I couldn't send it right now. Your progress is still kept in this browser — try again shortly.");
        }
      })
      .catch(function () {
        aviso.className = "hz-assinar-aviso erro";
        aviso.textContent = "⚠ " + fala("O serviço não respondeu.", "The service did not respond.");
      })
      .then(function () { botao.disabled = false; });
  }

  // --- Espelho do progresso no servidor (spec 080) ---
  // O localStorage continua sendo a fonte IMEDIATA: funciona offline, funciona
  // sem backend, e é o que pinta o cartão acima sem esperar rede. O servidor é o
  // espelho que atravessa aparelhos e entra em cena depois. `window.COMPANION`
  // é definido por um <script> inline DEPOIS deste arquivo — daí o DOMContentLoaded.
  var CFG = {};
  function backend() { return (CFG.backend || "").replace(/\/+$/, ""); }

  document.addEventListener("DOMContentLoaded", function () {
    CFG = window.COMPANION || {};
    if (ehIndex) pintarLeitura();
    else pintarFimDeCapitulo();

    var BACKEND = backend();
    if (!BACKEND) return;
    var sid = ler("cmp_sid", "");
    if (!sid) return;  // sessão ainda não criada pelo companion: nada a espelhar

    if (slug && !ehIndex && slug !== "sumario") {
      fetch(BACKEND + "/progresso", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ session_id: sid, lang: LANG, slug: slug, titulo: titulo || slug })
      }).catch(function () {});
      return;
    }
    if (!ehIndex) return;

    // spec 093: `/progresso/detalhe` traz também os slugs visitados. Quem leu num
    // aparelho e entrou noutro chega com a barra cheia, não zerada.
    fetch(BACKEND + "/progresso/detalhe?session_id=" + encodeURIComponent(sid))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var mudou = absorver((d && d.visitados) || []);
        var itens = (d && d.itens) || [];
        for (var i = 0; i < itens.length; i++) {
          if (itens[i].lang !== LANG || !itens[i].slug) continue;
          if (!local || local.slug !== itens[i].slug) {
            local = { slug: itens[i].slug, titulo: itens[i].titulo || itens[i].slug };
            gravar(CHAVE_ULT, JSON.stringify(local));
            mudou = true;
          }
          break;
        }
        if (mudou) pintarLeitura();
      })
      .catch(function () {});
  });
})();

// i18n (spec 067): preferência de idioma + convite discreto na capa.
(function () {
  var corpo = document.body;
  var lang = corpo.getAttribute("data-lang") || "pt";
  var pill = document.querySelector(".lang-pill a[data-lang-alvo]");
  if (pill) pill.addEventListener("click", function () {
    try { localStorage.setItem("hz_lang", pill.getAttribute("data-lang-alvo")); } catch (e) {}
  });
  try { localStorage.setItem("hz_lang_visto_" + lang, "1"); } catch (e) {}
  // Convite: só na capa PT, navegador em inglês, sem preferência gravada. Nunca redirect.
  if (!corpo.classList.contains("splash-body") || lang !== "pt") return;
  var pref = null; try { pref = localStorage.getItem("hz_lang"); } catch (e) {}
  var navEn = (navigator.language || "").toLowerCase().indexOf("en") === 0;
  if (pref || !navEn) return;
  var ctas = document.querySelector(".splash-ctas");
  if (!ctas) return;
  var p = document.createElement("p");
  p.className = "lang-sugestao";
  p.innerHTML = '\ud83c\udf10 This book is also available in <a href="en/index.html">English</a>.';
  ctas.parentNode.insertBefore(p, ctas.nextSibling);
})();
