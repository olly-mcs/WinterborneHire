// Homepage pop-ups: "Find out more" under the Google rating ([data-open-dialog]) opens the reviews dialog. The faux florals
// roundel's pop-up is switched off for launch (the roundel is decoration only); this wires it again if it returns.
// Previously: "Find out more" under the Google
// rating ([data-open-dialog]) opens the reviews dialog.
(function () {
  function wire(button, dialog) {
    if (!button || !dialog || typeof dialog.showModal !== "function") return;
    button.addEventListener("click", function () { dialog.showModal(); });
    dialog.addEventListener("click", function (e) {
      // a click on the dimmed background (outside the box) or the close button closes it
      if (e.target === dialog || e.target.closest("[data-close]")) dialog.close();
    });
    dialog.addEventListener("close", function () { button.focus(); });
  }
  wire(document.querySelector(".hero-roundel"), document.getElementById("faux-dialog"));
  document.querySelectorAll("[data-open-dialog]").forEach(function (b) {
    wire(b, document.getElementById(b.getAttribute("data-open-dialog")));
  });
})();
