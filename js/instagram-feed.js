// Instagram feed: loads the latest posts from /api/instagram (a Netlify Function, see
// netlify/functions/instagram.mjs) and shows them as a grid linking to each post.
// If the feed can't load, the placeholders are removed and only the follow link stays.
(function () {
  var grid = document.querySelector("[data-instagram-feed]");
  if (!grid) return;
  var count = parseInt(grid.getAttribute("data-count"), 10) || 8;

  function altText(caption) {
    var text = (caption || "").replace(/\s+/g, " ").trim();
    var firstSentence = text.split(/(?<=[.!?])\s/)[0];
    return firstSentence ? firstSentence.slice(0, 120) : "Instagram post by Winterborne Hire & Styling";
  }

  function render(posts) {
    var fragment = document.createDocumentFragment();
    posts.slice(0, count).forEach(function (post) {
      var link = document.createElement("a");
      link.className = "instagram-feed-item";
      link.href = post.permalink;
      link.target = "_blank";
      link.rel = "noopener";
      if (post.isVideo) link.classList.add("is-video");
      if (post.isCarousel) link.classList.add("is-carousel");

      var img = document.createElement("img");
      img.src = post.image;
      img.alt = altText(post.caption);
      img.loading = "lazy";
      img.decoding = "async";
      img.addEventListener("error", function () { link.remove(); });
      link.appendChild(img);

      if (post.caption) {
        var caption = document.createElement("span");
        caption.className = "instagram-feed-caption";
        caption.setAttribute("aria-hidden", "true");
        caption.textContent = post.caption.length > 140 ? post.caption.slice(0, 140).trim() + "…" : post.caption;
        link.appendChild(caption);
      }
      fragment.appendChild(link);
    });
    grid.innerHTML = "";
    grid.appendChild(fragment);
    grid.classList.remove("is-loading");
  }

  fetch("/api/instagram")
    .then(function (res) { return res.json(); })
    .then(function (data) {
      if (data && data.posts && data.posts.length) render(data.posts);
      else grid.remove();
    })
    .catch(function () { grid.remove(); });
})();
