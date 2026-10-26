// Hire collection product pages: the colour swatches or style names under the description. Choosing one moves the
// photo slider to its photos and sets which option "Add to your wish list" adds; swiping the slider to another
// option's photos selects that option.
(function () {
  document.querySelectorAll("[data-options]").forEach(function (box) {
    var buttons = box.querySelectorAll("[data-option]");
    var current = box.querySelector("[data-option-current]");
    var wish = document.querySelector("[data-wish-options]");
    var track = document.querySelector(".pd-main .pd-track");

    function select(btn) {
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      if (current) current.textContent = btn.getAttribute("data-name");
      if (wish) {
        wish.setAttribute("data-wish-add", btn.getAttribute("data-wish-id"));
        document.dispatchEvent(new CustomEvent("wishlist:refresh"));
      }
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        select(btn);
        var slide = btn.getAttribute("data-slide");
        if (track && slide !== "") track.scrollTo({ left: Number(slide) * track.clientWidth, behavior: "smooth" });
      });
    });

    if (track) {
      var timer;
      track.addEventListener("scroll", function () {
        clearTimeout(timer);
        timer = setTimeout(function () {
          var slide = track.children[Math.round(track.scrollLeft / track.clientWidth)];
          var v = slide && slide.getAttribute("data-variant");
          if (v !== null && v !== undefined && buttons[v] && buttons[v].getAttribute("aria-pressed") !== "true") select(buttons[v]);
        }, 120);
      }, { passive: true });
    }
  });
})();
