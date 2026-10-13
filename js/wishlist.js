// Bespoke Florals wish list: a panel that slides out from the right on the Bespoke Florals pages.
// "Add to your wish list" buttons (data-wish-add="<catalogue item id>") add a product; the panel lets the couple change
// quantities, see an estimated range, and send the list with their details. It's sent to the Netlify form "quote"
// (the same form as /quote-builder, which emails winterbornevintage@gmail.com), and shares its saved list with the
// quote builder page. Product names and guide prices come from js/quote-data.js; no individual prices are shown.
(function () {
  var catalogue = window.QUOTE_CATALOGUE;
  if (!catalogue) return;
  var RANGE = 0.2; // 20% below to 20% above the guide total, like the quote builder
  var STORAGE_KEY = "winterborne-quote";

  var items = {};
  catalogue.forEach(function (section) {
    section.items.forEach(function (item) { items[item.id] = { item: item, section: section.title }; });
  });

  var list = {};
  try {
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    Object.keys(saved).forEach(function (id) { if (items[id] && saved[id] > 0) list[id] = saved[id]; });
  } catch (e) {}
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(list)); } catch (e) {}
  }

  var money = function (n) { return "£" + Math.round(n).toLocaleString("en-GB"); };
  var roundTo5 = function (n) { return Math.round(n / 5) * 5; };
  var esc = function (s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  };

  function lines() {
    return Object.keys(list).map(function (id) {
      return { id: id, item: items[id].item, section: items[id].section, qty: list[id] };
    });
  }
  function count() { return lines().reduce(function (n, l) { return n + l.qty; }, 0); }
  function estimate() {
    var total = lines().reduce(function (sum, l) { return sum + l.qty * l.item.price; }, 0);
    return { total: total, low: roundTo5(total * (1 - RANGE)), high: roundTo5(total * (1 + RANGE)) };
  }

  // ----- the panel -----
  var panel = document.createElement("div");
  panel.className = "wl";
  panel.innerHTML =
    '<button type="button" class="wl-tab" aria-expanded="false" aria-controls="wl-panel">Your wish list <span class="wl-count">0</span></button>' +
    '<div class="wl-overlay" hidden></div>' +
    '<aside class="wl-panel" id="wl-panel" role="dialog" aria-modal="true" aria-labelledby="wl-title" hidden>' +
    '  <div class="wl-head"><h2 id="wl-title" class="wl-title">Your wish list</h2>' +
    '    <button type="button" class="wl-close" aria-label="Close your wish list">&times;</button></div>' +
    '  <div class="wl-body">' +
    '    <p class="wl-intro">Add the florals you love, then send us your list. We&#x27;ll come back to you with a quote.</p>' +
    '    <ul class="wl-lines" role="list"></ul>' +
    '    <p class="wl-empty">Your wish list is empty. Use &ldquo;Add to your wish list&rdquo; on any of our florals.</p>' +
    '    <div class="wl-estimate"><span>Estimated range</span><strong class="wl-range"></strong>' +
    '      <small>A guide only, for the items above. We&#x27;ll confirm your quote once we know your design.</small></div>' +
    '    <form class="wl-form" name="quote" method="POST" data-netlify="true" netlify-honeypot="bot-field">' +
    '      <input type="hidden" name="form-name" value="quote">' +
    '      <p hidden><label>Leave this empty: <input name="bot-field"></label></p>' +
    '      <input type="hidden" name="subject" value="New floral wish list from the website">' +
    '      <input type="hidden" name="estimate"><textarea name="quote" hidden></textarea>' +
    '      <h3 class="wl-form-title">Send us your list</h3>' +
    '      <label class="wl-field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>' +
    '      <label class="wl-field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>' +
    '      <label class="wl-field"><span>Wedding date</span><input type="date" name="wedding-date" required></label>' +
    '      <label class="wl-field"><span>Venue</span><input type="text" name="venue" required></label>' +
    '      <button type="submit" class="wl-submit">Request my quote</button>' +
    '      <p class="wl-error" role="alert" hidden>Sorry, your list couldn&#x27;t be sent. Please try again, or email winterbornevintage@gmail.com.</p>' +
    '    </form>' +
    '    <div class="wl-done" hidden><h3 class="wl-form-title">Thank you!</h3>' +
    '      <p>Your wish list is on its way to us. We&#x27;ll be in touch with your quote soon.</p></div>' +
    '  </div>' +
    '</aside>';
  document.body.appendChild(panel);

  var tab = panel.querySelector(".wl-tab");
  var overlay = panel.querySelector(".wl-overlay");
  var aside = panel.querySelector(".wl-panel");
  var linesEl = panel.querySelector(".wl-lines");
  var form = panel.querySelector(".wl-form");
  var lastFocus = null;

  function open() {
    lastFocus = document.activeElement;
    aside.hidden = false;
    overlay.hidden = false;
    requestAnimationFrame(function () { panel.classList.add("is-open"); });
    tab.setAttribute("aria-expanded", "true");
    document.documentElement.classList.add("wl-locked");
    panel.querySelector(".wl-close").focus();
  }
  function close() {
    panel.classList.remove("is-open");
    tab.setAttribute("aria-expanded", "false");
    document.documentElement.classList.remove("wl-locked");
    setTimeout(function () { aside.hidden = true; overlay.hidden = true; }, 250);
    if (lastFocus) lastFocus.focus();
  }

  function setQty(id, qty) {
    if (qty > 0) list[id] = Math.min(qty, 99);
    else delete list[id];
    save();
    render();
  }

  function render() {
    var ls = lines();
    linesEl.innerHTML = ls.map(function (l) {
      return '<li class="wl-line" data-id="' + esc(l.id) + '">' +
        '<div class="wl-line-text"><span class="wl-line-name">' + esc(l.item.name) + '</span>' +
        '<span class="wl-line-section">' + esc(l.section) + '</span></div>' +
        '<div class="wl-qty" role="group" aria-label="Quantity of ' + esc(l.item.name) + '">' +
        '<button type="button" class="wl-minus" aria-label="One fewer">&minus;</button>' +
        '<span class="wl-qty-n" aria-live="polite">' + l.qty + '</span>' +
        '<button type="button" class="wl-plus" aria-label="One more">+</button></div>' +
        '<button type="button" class="wl-remove" aria-label="Remove ' + esc(l.item.name) + '">Remove</button></li>';
    }).join("");
    var est = estimate();
    panel.querySelector(".wl-range").textContent = ls.length ? money(est.low) + " – " + money(est.high) : "";
    panel.classList.toggle("has-items", ls.length > 0);
    var n = count();
    panel.querySelector(".wl-count").textContent = n;
    tab.hidden = n === 0 && !panel.classList.contains("is-open");
    document.querySelectorAll("[data-wish-add]").forEach(function (btn) {
      var inList = list[btn.getAttribute("data-wish-add")] > 0;
      btn.classList.toggle("is-added", inList);
      btn.textContent = inList ? "In your wish list ✓" : "Add to your wish list";
    });
  }

  linesEl.addEventListener("click", function (e) {
    var li = e.target.closest(".wl-line");
    if (!li) return;
    var id = li.getAttribute("data-id");
    if (e.target.closest(".wl-plus")) setQty(id, list[id] + 1);
    if (e.target.closest(".wl-minus")) setQty(id, list[id] - 1);
    if (e.target.closest(".wl-remove")) setQty(id, 0);
  });
  document.querySelectorAll("[data-wish-add]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-wish-add");
      if (!items[id]) return;
      if (!(list[id] > 0)) setQty(id, 1);
      open();
    });
  });
  tab.addEventListener("click", open);
  overlay.addEventListener("click", close);
  panel.querySelector(".wl-close").addEventListener("click", close);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && panel.classList.contains("is-open")) close();
  });

  // ----- send -----
  function listText(details, est) {
    var out = ["Someone has sent their floral wish list from the website. Their details and list are below.", ""];
    out.push("Name: " + details.name, "Email: " + details.email, "Wedding date: " + details.date, "Venue: " + details.venue, "");
    lines().forEach(function (l) { out.push("  " + l.qty + " x " + l.item.name + " (" + l.section + ")"); });
    out.push("", "Estimated range shown to them: " + money(est.low) + " - " + money(est.high));
    return out.join("\n");
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!lines().length) return;
    var data = new FormData(form);
    var est = estimate();
    var date = data.get("wedding-date");
    var d = date ? new Date(date + "T12:00:00") : null;
    var details = {
      name: data.get("name"), email: data.get("email"), venue: data.get("venue"),
      date: d && !isNaN(d) ? d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) : date,
    };
    data.set("estimate", money(est.low) + " - " + money(est.high));
    data.set("quote", listText(details, est));
    data.set("subject", "Floral wish list from " + details.name);
    var button = form.querySelector(".wl-submit");
    var error = form.querySelector(".wl-error");
    button.disabled = true;
    button.textContent = "Sending...";
    error.hidden = true;
    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(data).toString(),
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.hidden = true;
        panel.querySelector(".wl-done").hidden = false;
      })
      .catch(function () { error.hidden = false; })
      .finally(function () {
        button.disabled = false;
        button.textContent = "Request my quote";
      });
  });

  render();
})();
