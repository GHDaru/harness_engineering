/* Página de entrada por link mágico (spec 080).

   Consome o `?t=` da URL, troca-o pela sessão canônica do leitor e devolve o
   leitor ao ponto em que parou. Não é login: nenhuma senha, nenhuma área
   restrita — o `session_id` adotado é a mesma chave que a navegação anônima
   já usava, só que agora atravessa dispositivos.

   O token sai da URL (history.replaceState) assim que o POST parte: link de uso
   único não precisa sobreviver ao histórico do navegador nem vazar por referer. */
(function () {
  "use strict";
  var CFG = window.COMPANION || {};
  var BACKEND = (CFG.backend || "").replace(/\/+$/, "");
  var EN = (CFG.lang === "en");
  function tx(pt, en) { return EN ? en : pt; }

  var caixa = document.getElementById("entrar-estado");
  if (!caixa) return;

  function diz(classe, titulo, detalhe, acao) {
    caixa.className = "entrar-estado " + classe;
    caixa.innerHTML = "";
    var h = document.createElement("h2"); h.textContent = titulo; caixa.appendChild(h);
    if (detalhe) { var p = document.createElement("p"); p.textContent = detalhe; caixa.appendChild(p); }
    if (acao) {
      var a = document.createElement("a");
      a.className = "btn btn-primario"; a.href = acao.href; a.textContent = acao.rotulo;
      caixa.appendChild(a);
    }
  }

  // A página EN vive em /en/, ao lado do seu próprio sumário: o relativo serve aos dois.
  var sumario = "sumario.html";

  /* Pergunta de contato (spec 093). Três regras que a ADR 0010 fixou e que este
     bloco existe para não deixar escorregar:
       1. desmarcada — aceitar é ato, não é omissão;
       2. sem bloqueio — a página já está utilizável, os botões já estão ali, e
          ir embora sem responder é uma resposta válida (vale não);
       3. só grava quando o leitor mexe — sair sem tocar não registra nada, e a
          pergunta volta uma outra hora em vez de virar um "não" fabricado. */
  function perguntarContato(sid) {
    var box = document.createElement("div");
    box.className = "entrar-avisos";

    var rot = document.createElement("label");
    var chk = document.createElement("input");
    chk.type = "checkbox";                       // nasce desmarcada
    rot.appendChild(chk);
    rot.appendChild(document.createTextNode(" " + tx(
      "Quer que eu avise quando sair um livro novo?",
      "Would you like me to tell you when a new book comes out?")));
    box.appendChild(rot);

    var nota = document.createElement("p");
    nota.className = "entrar-avisos-nota";
    nota.textContent = tx("Você cancela em qualquer e-mail, num clique. Nada além de aviso de publicação — sem patrocinador e sem repasse a terceiro.",
                          "You can opt out from any e-mail, in one click. Nothing but publication notices — no sponsors, no sharing with third parties.");
    box.appendChild(nota);

    chk.addEventListener("change", function () {
      chk.disabled = true;
      fetch(BACKEND + "/consentimento", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ session_id: sid, finalidade: "contato", aceito: chk.checked })
      })
        .then(function (r) { if (!r.ok) throw new Error("http"); })
        .then(function () {
          chk.disabled = false;   // continua sendo um interruptor, não um alçapão
          nota.textContent = chk.checked
            ? tx("Combinado — eu aviso quando sair um livro novo.",
                 "Done — I'll let you know when a new book comes out.")
            : tx("Sem avisos, então. Sua leitura continua igual.",
                 "No notices, then. Your reading is unchanged.");
        })
        .catch(function () {
          chk.disabled = false; chk.checked = !chk.checked;
          nota.textContent = tx("Não consegui registrar agora — tente de novo.",
                                "I couldn't record that right now — try again.");
        });
    });

    caixa.parentNode.insertBefore(box, caixa.nextSibling);
  }

  var token = "";
  try { token = new URLSearchParams(location.search).get("t") || ""; } catch (e) {}
  // Fora da URL antes de qualquer coisa: recarregar a página não reenvia o token,
  // e ele não fica no histórico nem no referer das requisições seguintes.
  try { history.replaceState(null, "", location.pathname); } catch (e) {}

  if (!token) {
    diz("erro", tx("Link ausente", "Missing link"),
      tx("Esta página só funciona a partir do link enviado por e-mail.",
         "This page only works from the link sent to your inbox."),
      { href: sumario, rotulo: tx("Ir para o sumário", "Go to the contents") });
    return;
  }
  if (!BACKEND) {
    diz("erro", tx("Serviço indisponível", "Service unavailable"),
      tx("O backend do companion não está configurado neste site.",
         "The companion backend is not configured on this site."),
      { href: sumario, rotulo: tx("Ir para o sumário", "Go to the contents") });
    return;
  }

  var sidLocal = "";
  try { sidLocal = localStorage.getItem("cmp_sid") || ""; } catch (e) {}

  diz("carregando", tx("Entrando…", "Signing you in…"),
      tx("Validando seu link de leitura.", "Validating your reading link."));

  fetch(BACKEND + "/entrar", {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ token: token, session_id: sidLocal || undefined })
  })
    .then(function (r) { return r.json().then(function (d) { return { ok: r.ok, d: d }; }); })
    .then(function (res) {
      if (!res.ok || !res.d || !res.d.session_id) {
        diz("erro", tx("Link inválido ou expirado", "Invalid or expired link"),
          tx("Links de leitura valem uma vez só e por poucos minutos. Peça um novo pelo companion.",
             "Reading links work once and only for a few minutes. Ask for a new one from the companion."),
          { href: sumario, rotulo: tx("Ir para o sumário", "Go to the contents") });
        return;
      }
      // Adotar o id canônico é o que faz histórico, objetivo e progresso seguirem.
      try {
        localStorage.setItem("cmp_sid", res.d.session_id);
        localStorage.setItem("cmp_email", res.d.email || "");
      } catch (e) {}

      var itens = res.d.progresso || [];
      var lang = EN ? "en" : "pt";
      var meu = null;
      for (var i = 0; i < itens.length; i++) if (itens[i].lang === lang) meu = itens[i];
      if (meu && meu.slug) {
        try {
          localStorage.setItem("hz_ultimo" + (EN ? "_en" : ""),
            JSON.stringify({ slug: meu.slug, titulo: meu.titulo || meu.slug }));
        } catch (e) {}
      }

      var quem = res.d.email ? " — " + res.d.email : "";
      var estado = res.d.consentimentos || {};
      diz("ok", tx("Pronto" + quem, "You're in" + quem),
        meu && meu.slug
          ? tx("Seu progresso e suas conversas voltaram. Você parou em: " + (meu.titulo || meu.slug),
               "Your progress and conversations are back. You stopped at: " + (meu.titulo || meu.slug))
          : tx("Seu progresso e suas conversas passam a acompanhar você neste e nos outros aparelhos.",
               "Your progress and conversations now follow you across devices."),
        { href: (meu && meu.slug) ? meu.slug + ".html" : sumario,
          rotulo: (meu && meu.slug) ? tx("Continuar lendo", "Keep reading")
                                    : tx("Ir para o sumário", "Go to the contents") });

      // spec 093 / ADR 0010: a SEGUNDA pergunta, e só depois de entrar. Nunca no
      // ato de assinar — um consentimento não pode carregar o outro de carona.
      if (!estado.contato) perguntarContato(res.d.session_id);
    })
    .catch(function () {
      diz("erro", tx("Não deu para entrar", "Could not sign you in"),
        tx("O serviço não respondeu. Tente de novo em instantes — o link continua valendo até expirar.",
           "The service did not respond. Try again shortly — the link stays valid until it expires."),
        { href: sumario, rotulo: tx("Ir para o sumário", "Go to the contents") });
    });
})();
