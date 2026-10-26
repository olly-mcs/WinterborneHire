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

// Links to a section on the same page (e.g. "Full Styling" on Our Services): scroll there straight away with the
// browser's own smooth scroll. Webflow's built-in version waits and then eases in slowly, taking over two seconds.
(function () {
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.addEventListener("click", function (e) {
    var link = e.target.closest && e.target.closest('a[href^="#"]');
    if (!link || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var id = decodeURIComponent(link.getAttribute("href").slice(1));
    var target = id && document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    e.stopPropagation();
    target.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    if (history.replaceState) history.replaceState(null, "", "#" + id);
  }, true);
})();
