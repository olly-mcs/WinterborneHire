// Cookie banner. Google Analytics sets no cookies until a visitor accepts: each page's Google tag starts with
// consent denied (scripts/apply-page-meta.py) and re-applies a stored "accepted" before it loads. The choice is kept
// in this browser; "Cookie settings" in the footer brings the banner back to change it.
(function () {
  var KEY = "winterborne-cookies";
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // after a "Reject", remove any analytics cookies an earlier "Accept" left behind
  function clearAnalytics() {
    var host = location.hostname.replace(/^www\./, "");
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (!/^_ga/.test(name)) return;
      ["", "; domain=" + host, "; domain=." + host].forEach(function (d) {
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
      });
    });
  }

  var bar = null;
  function choose(v) {
    store(v);
    if (typeof window.gtag === "function") window.gtag("consent", "update", { analytics_storage: v === "accepted" ? "granted" : "denied" });
    if (v === "rejected") clearAnalytics();
    bar.hidden = true;
  }
  function show() {
    if (!bar) {
      bar = document.createElement("div");
      bar.className = "ck";
      bar.setAttribute("role", "region");
      bar.setAttribute("aria-label", "Cookies");
      bar.innerHTML =
        '<p class="ck-text">We use Google Analytics cookies to see how people use our site, so we can make it better. ' +
        "They're only set if you accept.</p>" +
        '<div class="ck-buttons"><button type="button" class="ck-btn" data-ck="accepted">Accept</button>' +
        '<button type="button" class="ck-btn" data-ck="rejected">Reject</button></div>';
      bar.addEventListener("click", function (e) {
        var b = e.target.closest("[data-ck]");
        if (b) choose(b.getAttribute("data-ck"));
      });
      document.body.appendChild(bar);
    }
    bar.hidden = false;
  }

  var after = document.querySelector('a.footer-link[href="/booking-cancellation-fees"]');
  if (after) {
    var link = document.createElement("button");
    link.type = "button";
    link.className = "footer-link ck-settings";
    link.textContent = "Cookie settings";
    link.addEventListener("click", function () { show(); bar.querySelector(".ck-btn").focus(); });
    after.insertAdjacentElement("afterend", link);
  }
  if (!stored()) show();
})();
