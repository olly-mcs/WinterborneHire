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
  function checkChoices() {
    var any = Array.prototype.some.call(checks, function (c) { return c.checked; });
    checks[0].setCustomValidity(any ? "" : "Please choose a bridal bouquet, buttonholes or both.");
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
