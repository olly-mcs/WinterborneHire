// Bespoke Florals product pages: the photo slider. The photos sit in a scroll-snapping strip, so swiping works on
// phones; the arrows, thumbnails and arrow keys move it, and the counter and thumbnails follow it.
(function () {
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-gallery]").forEach(function (gallery) {
    var track = gallery.querySelector(".pd-track");
    var total = track.children.length;
    var thumbs = gallery.querySelectorAll(".pd-thumb");
    var count = gallery.querySelector("[data-count]");
    var current = 0;

    function go(i) {
      i = (i + total) % total;
      track.scrollTo({ left: i * track.clientWidth, behavior: reduceMotion ? "auto" : "smooth" });
    }

    function mark(i) {
      current = i;
      count.textContent = i + 1;
      thumbs.forEach(function (thumb, j) {
        thumb.classList.toggle("is-active", j === i);
        if (j === i) thumb.setAttribute("aria-current", "true");
        else thumb.removeAttribute("aria-current");
      });
    }

    track.addEventListener("scroll", function () {
      var i = Math.round(track.scrollLeft / track.clientWidth);
      if (i !== current && i >= 0 && i < total) mark(i);
    }, { passive: true });

    gallery.querySelector("[data-prev]").addEventListener("click", function () { go(current - 1); });
    gallery.querySelector("[data-next]").addEventListener("click", function () { go(current + 1); });
    thumbs.forEach(function (thumb) {
      thumb.addEventListener("click", function () { go(Number(thumb.getAttribute("data-slide"))); });
    });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); go(current - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); go(current + 1); }
    });
  });
})();
