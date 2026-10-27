// The "UK-wide delivery: Bouquets & buttonholes" tab opens a small enquiry form for made-to-order bouquets and
// buttonholes (bought, not hired), sent to the Netlify form "bouquet-order". Markup: scripts/build-bespoke-florals.py.
(function () {
  var tab = document.querySelector(".shop-tab .shop-pulltab");
  var dialog = document.getElementById("order-dialog");
  if (!tab || !dialog || typeof dialog.showModal !== "function") return;
  var form = dialog.querySelector(".order-form");
  var ask = dialog.querySelector(".order-ask");
  var done = dialog.querySelector(".order-done");

  tab.addEventListener("click", function (e) {
    e.preventDefault();
    ask.hidden = false;
    done.hidden = true;
    dialog.showModal();
  });
  dialog.addEventListener("click", function (e) {
    if (e.target === dialog || e.target.closest("[data-order-close]")) dialog.close();
  });
  dialog.addEventListener("close", function () { tab.focus(); });

  // Bridal bouquet and/or buttonholes: at least one must be ticked
  var checks = form.querySelectorAll(".order-check input");
  // ...and the "Your ideas" prompt follows what's ticked
  var ideas = form.querySelector("textarea[name=ideas]");
  var prompts = {
    none: "Have some ideas about the kind of bouquet or buttonholes you\u2019re after? Let us know here.",
    bouquet: "Have some ideas for your bridal bouquet? Colours, favourite flowers, size and shape\u2026 let us know here.",
    buttonholes: "Have some ideas for your buttonholes? Colours, flowers and how many you\u2019ll need\u2026 let us know here.",
    both: "Have some ideas for your bouquet and buttonholes? Colours, flowers, style and how many buttonholes\u2026 let us know here.",
  };
  function checkChoices() {
    var bouquet = form.querySelector("input[name=bridal-bouquet]").checked;
    var buttonholes = form.querySelector("input[name=buttonholes]").checked;
    checks[0].setCustomValidity(bouquet || buttonholes ? "" : "Please choose a bridal bouquet, buttonholes or both.");
    ideas.placeholder = prompts[bouquet && buttonholes ? "both" : bouquet ? "bouquet" : buttonholes ? "buttonholes" : "none"];
  }
  Array.prototype.forEach.call(checks, function (c) { c.addEventListener("change", checkChoices); });
  checkChoices();
  form.addEventListener("reset", function () { setTimeout(checkChoices); });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var button = form.querySelector(".order-submit");
    var error = form.querySelector(".order-error");
    var data = new FormData(form);
    data.set("subject", "Bouquet & buttonhole enquiry from " + data.get("name"));
    button.disabled = true;
    button.textContent = "Sending...";
    error.hidden = true;
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(data).toString(),
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.reset();
        ask.hidden = true;
        done.hidden = false;
        done.focus();
      })
      .catch(function () { error.hidden = false; })
      .finally(function () {
        button.disabled = false;
        button.textContent = "Request your custom order";
      });
  });
})();
