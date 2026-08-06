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
      diz("ok", tx("Pronto" + quem, "You're in" + quem),
        meu && meu.slug
          ? tx("Seu progresso e suas conversas voltaram. Você parou em: " + (meu.titulo || meu.slug),
               "Your progress and conversations are back. You stopped at: " + (meu.titulo || meu.slug))
          : tx("Seu progresso e suas conversas passam a acompanhar você neste e nos outros aparelhos.",
               "Your progress and conversations now follow you across devices."),
        { href: (meu && meu.slug) ? meu.slug + ".html" : sumario,
          rotulo: (meu && meu.slug) ? tx("Continuar lendo", "Keep reading")
                                    : tx("Ir para o sumário", "Go to the contents") });
    })
    .catch(function () {
      diz("erro", tx("Não deu para entrar", "Could not sign you in"),
        tx("O serviço não respondeu. Tente de novo em instantes — o link continua valendo até expirar.",
           "The service did not respond. Try again shortly — the link stays valid until it expires."),
        { href: sumario, rotulo: tx("Ir para o sumário", "Go to the contents") });
    });
})();
