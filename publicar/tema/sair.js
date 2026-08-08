/* Descadastro de um clique (spec 093 / ADR 0010, R4).

   O link que toda mensagem de contato vai levar termina aqui, com o sha256 do
   e-mail em `?e=`. O clique JÁ É a decisão: esta página não pede login, não pede
   confirmação e não pergunta por quê. Uma tela de "tem certeza?" no caminho de
   saída é atrito deliberado, e atrito para sair é a forma educada de não deixar
   sair — o contrário do que a ADR prometeu.

   O hash sai da URL assim que o POST parte, pelo mesmo motivo do link mágico:
   não precisa sobreviver ao histórico do navegador nem vazar por referer. */
(function () {
  "use strict";
  var CFG = window.COMPANION || {};
  var BACKEND = (CFG.backend || "").replace(/\/+$/, "");
  var EN = (CFG.lang === "en");
  function tx(pt, en) { return EN ? en : pt; }

  var caixa = document.getElementById("sair-estado");
  if (!caixa) return;
  var sumario = "sumario.html";

  function diz(classe, titulo, detalhe) {
    caixa.className = "entrar-estado " + classe;
    caixa.innerHTML = "";
    var h = document.createElement("h2"); h.textContent = titulo; caixa.appendChild(h);
    if (detalhe) { var p = document.createElement("p"); p.textContent = detalhe; caixa.appendChild(p); }
    var a = document.createElement("a");
    a.className = "btn btn-primario"; a.href = sumario;
    a.textContent = tx("Voltar ao livro", "Back to the book");
    caixa.appendChild(a);
  }

  var e = "";
  try { e = new URLSearchParams(location.search).get("e") || ""; } catch (err) {}
  try { history.replaceState(null, "", location.pathname); } catch (err) {}

  if (!e || !BACKEND) {
    diz("erro", tx("Link incompleto", "Incomplete link"),
      tx("Esta página só funciona a partir do link de descadastro que vai no rodapé do e-mail.",
         "This page only works from the unsubscribe link at the bottom of the e-mail."));
    return;
  }

  diz("carregando", tx("Cancelando…", "Unsubscribing…"), "");

  fetch(BACKEND + "/descadastrar", {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ e: e })
  })
    .then(function (r) { if (!r.ok) throw new Error("http"); })
    .then(function () {
      // Mensagem idêntica para quem saiu agora e para quem já tinha saído — a
      // rota responde igual nos dois casos de propósito, e a tela não pode
      // desfazer isso dizendo "você não estava na lista".
      diz("ok", tx("Pronto, você saiu", "Done, you're out"),
        tx("Você não receberá mais avisos de livro novo. Seu link de leitura e seu progresso continuam intactos — são coisas separadas.",
           "You won't get notices about new books anymore. Your reading link and your progress are untouched — they're separate things."));
    })
    .catch(function () {
      diz("erro", tx("Não deu para cancelar agora", "Could not unsubscribe right now"),
        tx("O serviço não respondeu. Tente abrir o link de novo em alguns minutos — ele não expira.",
           "The service did not respond. Try opening the link again in a few minutes — it does not expire."));
    });
})();
