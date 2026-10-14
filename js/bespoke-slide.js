// Direction for the slide between Bespoke Florals pages (css/bespoke-slide.css): moving right along the section strip
// (overview, The Ceremony, The Reception, Your Florals, Installations) slides forward, moving left slides back.
(function () {
  var ORDER = ["", "the-ceremony", "the-reception", "your-florals", "installations"];
  function index(url) {
    var m = new URL(url, location.href).pathname.replace(/\.html$/, "").replace(/\/$/, "").match(/^\/bespoke-florals(?:\/([^/]+))?$/);
    return m ? ORDER.indexOf(m[1] || "") : -1;
  }
  function direction(fromUrl, toUrl) {
    var a = index(fromUrl), b = index(toUrl);
    if (a < 0 || b < 0 || a === b) return null;
    return b > a ? "forward" : "back";
  }
  window.addEventListener("pageswap", function (e) {
    if (!e.viewTransition || !e.activation || !e.activation.entry) return;
    var dir = direction(location.href, e.activation.entry.url);
    if (dir) e.viewTransition.types.add(dir);
    else e.viewTransition.skipTransition();
  });
  window.addEventListener("pagereveal", function (e) {
    if (!e.viewTransition) return;
    var act = window.navigation && navigation.activation;
    var dir = act && act.from && act.entry ? direction(act.from.url, act.entry.url) : null;
    if (dir) e.viewTransition.types.add(dir);
    else e.viewTransition.skipTransition();
  });
})();
