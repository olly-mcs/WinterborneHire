// Homepage: the "Faux florals" roundel in the hero opens a dialog about our faux florals.
(function () {
  var button = document.querySelector(".hero-roundel");
  var dialog = document.getElementById("faux-dialog");
  if (!button || !dialog || typeof dialog.showModal !== "function") return;
  button.addEventListener("click", function () { dialog.showModal(); });
  dialog.addEventListener("click", function (e) {
    // a click on the dimmed background (outside the box) or the close button closes it
    if (e.target === dialog || e.target.closest("[data-close]")) dialog.close();
  });
  dialog.addEventListener("close", function () { button.focus(); });
})();
