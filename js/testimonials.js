// Testimonials page: photo slider (swipe, arrows, thumbnails, keyboard) and a full-screen viewer.
// Works for any number of <article class="tm"> blocks, each with its own [data-tm-gallery].
(function () {
  var lightbox = document.querySelector(".tm-lightbox");
  var lightboxImage = lightbox && lightbox.querySelector(".tm-lightbox-image");
  var lightboxGallery = null;

  function setupGallery(gallery) {
    var track = gallery.querySelector(".tm-track");
    var slides = Array.prototype.slice.call(track.querySelectorAll(".tm-slide"));
    var thumbs = Array.prototype.slice.call(gallery.querySelectorAll(".tm-thumb"));
    var prev = gallery.querySelector(".tm-prev");
    var next = gallery.querySelector(".tm-next");
    var counter = gallery.querySelector(".tm-current");
    var current = 0;

    function goTo(index) {
      index = Math.max(0, Math.min(slides.length - 1, index));
      track.scrollTo({ left: slides[index].offsetLeft - track.offsetLeft, behavior: "smooth" });
    }

    function update(index) {
      current = index;
      if (counter) counter.textContent = index + 1;
      if (prev) prev.disabled = index === 0;
      if (next) next.disabled = index === slides.length - 1;
      thumbs.forEach(function (thumb, i) {
        thumb.setAttribute("aria-current", i === index ? "true" : "false");
      });
    }

    var ticking = false;
    track.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        update(Math.round(track.scrollLeft / track.clientWidth));
        ticking = false;
      });
    });

    if (prev) prev.addEventListener("click", function () { goTo(current - 1); });
    if (next) next.addEventListener("click", function () { goTo(current + 1); });
    thumbs.forEach(function (thumb, i) {
      thumb.addEventListener("click", function () { goTo(i); });
    });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); goTo(current + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); goTo(current - 1); }
    });

    slides.forEach(function (slide, i) {
      var open = slide.querySelector(".tm-open");
      if (open) open.addEventListener("click", function () { openLightbox(api, i); });
    });

    var api = {
      count: slides.length,
      image: function (i) { return slides[i].querySelector("img"); },
      goTo: goTo,
    };
    update(0);
  }

  function showInLightbox(index) {
    var g = lightboxGallery;
    g.index = (index + g.count) % g.count;
    var img = g.image(g.index);
    lightboxImage.src = img.currentSrc || img.src;
    lightboxImage.alt = img.alt;
  }

  function openLightbox(gallery, index) {
    if (!lightbox || typeof lightbox.showModal !== "function") return;
    lightboxGallery = gallery;
    showInLightbox(index);
    lightbox.showModal();
  }

  if (lightbox) {
    lightbox.querySelector(".tm-lightbox-close").addEventListener("click", function () { lightbox.close(); });
    lightbox.querySelector(".tm-lightbox-prev").addEventListener("click", function () { showInLightbox(lightboxGallery.index - 1); });
    lightbox.querySelector(".tm-lightbox-next").addEventListener("click", function () { showInLightbox(lightboxGallery.index + 1); });
    lightbox.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") showInLightbox(lightboxGallery.index + 1);
      if (e.key === "ArrowLeft") showInLightbox(lightboxGallery.index - 1);
    });
    // Click on the dark background closes; keep the slider in step with the photo last viewed
    lightbox.addEventListener("click", function (e) {
      if (e.target === lightbox) lightbox.close();
    });
    lightbox.addEventListener("close", function () {
      if (lightboxGallery) lightboxGallery.goTo(lightboxGallery.index);
    });
  }

  Array.prototype.forEach.call(document.querySelectorAll("[data-tm-gallery]"), setupGallery);
})();
