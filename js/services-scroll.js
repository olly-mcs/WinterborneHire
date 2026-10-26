// Our Services (dorset-wedding-styling.html): the pinned photo beside Full, Partial and Self Styling changes to the
// service whose text is in the middle of the screen. Built by scripts/build-services.py.
(function () {
  var scroller = document.querySelector("[data-sv-scroller]");
  if (!scroller || !("IntersectionObserver" in window)) return;
  var items = {};
  scroller.querySelectorAll("[data-sv-media]").forEach(function (el) { items[el.getAttribute("data-sv-media")] = el; });
  function show(slug) {
    Object.keys(items).forEach(function (k) { items[k].classList.toggle("is-active", k === slug); });
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) show(entry.target.getAttribute("data-sv-panel"));
    });
  }, { rootMargin: "-45% 0px -45% 0px" });
  scroller.querySelectorAll("[data-sv-panel]").forEach(function (panel) { observer.observe(panel); });
})();
