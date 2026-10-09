// Navigation: on devices with a mouse, clicking the "Bespoke Florals" menu item opens the overview page
// (hovering still shows the dropdown). On touch screens a tap opens the dropdown, which has an overview link.
(function () {
  var canHover = window.matchMedia && window.matchMedia("(hover: hover) and (min-width: 992px)").matches;
  document.querySelectorAll("[data-nav-href]").forEach(function (toggle) {
    toggle.addEventListener("click", function (e) {
      if (!canHover) return;
      e.preventDefault();
      e.stopPropagation();
      window.location.href = toggle.getAttribute("data-nav-href");
    }, true);
  });
})();
