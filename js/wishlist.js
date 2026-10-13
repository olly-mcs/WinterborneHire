// Bespoke Florals wish list: a panel that slides out from the right on the Bespoke Florals pages.
// "Add to your wish list" buttons (data-wish-add="<catalogue item id>") add a product; the panel lets the couple change
// quantities, and send the list with their details. It's sent to the Netlify form "quote"
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

  // the Bespoke Florals sections (js/bespoke-sections.js): page names for each item, and its section
  var sections = window.BESPOKE_SECTIONS || [];
  var pageItem = {};
  sections.forEach(function (sec) {
    sec.items.forEach(function (it) { pageItem[it.id] = { name: it.name, url: it.url, section: sec.name }; });
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
      var p = pageItem[id];
      return { id: id, item: items[id].item, name: p ? p.name : items[id].item.name,
        section: p ? p.section : items[id].section, url: p && p.url, qty: list[id] };
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
    '    <p class="wl-intro">Add the florals you love, then send us your list.</p>' +
    '    <p class="wl-promise"><strong>We&#x27;ll come back to you as soon as possible with your quote.</strong></p>' +
    '    <p class="wl-empty">Your wish list is empty. Add florals below, or use &ldquo;Add to your wish list&rdquo; on any of our florals.</p>' +
    '    <ul class="wl-lines" role="list"></ul>' +
    '    <h3 class="wl-more-title">Add more florals</h3>' +
    '    <div class="wl-more"></div>' +
    '    <form class="wl-form" name="quote" method="POST" data-netlify="true" netlify-honeypot="bot-field">' +
    '      <input type="hidden" name="form-name" value="quote">' +
    '      <p hidden><label>Leave this empty: <input name="bot-field"></label></p>' +
    '      <input type="hidden" name="subject" value="New floral wish list from the website">' +
    '      <textarea name="quote" hidden></textarea>' +
    '      <h3 class="wl-form-title">Send us your list</h3>' +
    '      <label class="wl-field"><span>Your name</span><input type="text" name="name" autocomplete="name" required></label>' +
    '      <label class="wl-field"><span>Email</span><input type="email" name="email" autocomplete="email" required></label>' +
    '      <label class="wl-field"><span>Phone number</span><input type="tel" name="phone" autocomplete="tel" required></label>' +
    '      <label class="wl-field"><span>Wedding date</span><input type="date" name="wedding-date" required></label>' +
    '      <label class="wl-field"><span>Venue</span><input type="text" name="venue" required></label>' +
    '      <label class="wl-field"><span>How did you hear about us?</span><select name="how-heard">' +
    '        <option value="">Choose one</option><option>Google</option><option>Instagram</option><option>Facebook</option>' +
    '        <option>Personal Recommendation</option><option>Wedding Fair</option><option>YouTube</option><option>Other</option>' +
    '        <option>Company Van</option></select></label>' +
    '      <details class="wl-showroom"><summary>Why not book a showroom appointment?</summary>' +
    '        <p>Come and see our florals in person at our Dorchester showroom. Choose a day and time and we&#x27;ll come back to you to confirm everything.</p>' +
    '        <label class="wl-field"><span>Day you&#x27;d like to visit</span><input type="date" name="showroom-date"></label>' +
    '        <label class="wl-field"><span>Time of day</span><select name="showroom-time">' +
    '          <option value="">Choose a time</option><option>Morning (9.30am - 11.59am)</option><option>Afternoon (12pm - 2.30pm)</option>' +
    '        </select></label></details>' +
    '      <button type="submit" class="wl-submit">Request my quote</button>' +
    '      <p class="wl-error" role="alert" hidden>Sorry, your list couldn&#x27;t be sent. Please try again, or email winterbornevintage@gmail.com.</p>' +
    '    </form>' +
    '    <div class="wl-done" hidden><h3 class="wl-form-title">Thank you!</h3>' +
    '      <p>Your wish list is on its way to us. We&#x27;ll come back to you as soon as possible with your quote, and to confirm your showroom visit if you asked for one.</p></div>' +
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
        '<div class="wl-line-text">' + (l.url ? '<a class="wl-line-name" href="' + esc(l.url) + '">' + esc(l.name) + '</a>'
          : '<span class="wl-line-name">' + esc(l.name) + '</span>') +
        '<span class="wl-line-section">' + esc(l.section) + '</span></div>' +
        '<div class="wl-qty" role="group" aria-label="Quantity of ' + esc(l.name) + '">' +
        '<button type="button" class="wl-minus" aria-label="One fewer">&minus;</button>' +
        '<span class="wl-qty-n" aria-live="polite">' + l.qty + '</span>' +
        '<button type="button" class="wl-plus" aria-label="One more">+</button></div>' +
        '<button type="button" class="wl-remove" aria-label="Remove ' + esc(l.name) + '">Remove</button></li>';
    }).join("");
    renderMore();
    panel.classList.toggle("has-items", ls.length > 0);
    var n = count();
    panel.querySelector(".wl-count").textContent = n;
    document.querySelectorAll("[data-wish-add]").forEach(function (btn) {
      var inList = list[btn.getAttribute("data-wish-add")] > 0;
      btn.classList.toggle("is-added", inList);
      btn.textContent = inList ? "In your wish list ✓" : "Add to your wish list";
    });
  }

  // All four sections, collapsed, each listing its products that aren't in the list yet, so the whole Bespoke
  // Florals range can be added from the panel
  var moreEl = panel.querySelector(".wl-more");
  var openMore = {};
  function renderMore() {
    moreEl.innerHTML = sections.map(function (sec, i) {
      var rest = sec.items.filter(function (it) { return items[it.id] && !(list[it.id] > 0); });
      if (!rest.length) return "";
      return '<details class="wl-add-more" data-sec="' + i + '"' + (openMore[i] ? " open" : "") + '>' +
        '<summary>' + esc(sec.name) + ' <span class="wl-add-count">' + rest.length + '</span></summary><ul role="list">' +
        rest.map(function (it) {
          return '<li><a href="' + esc(it.url) + '">' + esc(it.name) + '</a>' +
            '<button type="button" class="wl-add" data-id="' + esc(it.id) + '" aria-label="Add ' + esc(it.name) + ' to your wish list">+ Add</button></li>';
        }).join("") + '</ul></details>';
    }).join("");
    panel.querySelector(".wl-more-title").hidden = !moreEl.innerHTML;
  }
  moreEl.addEventListener("toggle", function (e) {
    var d = e.target.closest && e.target.closest(".wl-add-more");
    if (d) openMore[d.getAttribute("data-sec")] = d.open;
  }, true);
  moreEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".wl-add");
    if (!btn) return;
    var d = btn.closest(".wl-add-more");
    openMore[d.getAttribute("data-sec")] = true;
    setQty(btn.getAttribute("data-id"), 1);
  });

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
  function niceDate(value) {
    var d = value ? new Date(value + "T12:00:00") : null;
    return d && !isNaN(d) ? d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) : value;
  }
  function listText(details, est) {
    var out = ["Someone has sent their floral wish list from the website and would like a quote. Their details and list are below.", ""];
    out.push("Name: " + details.name, "Email: " + details.email, "Phone: " + details.phone,
      "Wedding date: " + details.date, "Venue: " + details.venue, "Heard about us: " + (details.heard || "Not given"), "");
    out.push("Showroom appointment: " + (details.showroom || "Not requested"), "");
    out.push("WISH LIST");
    lines().forEach(function (l) { out.push("  " + l.qty + " x " + l.name + " (" + l.section + ")"); });
    out.push("", "Guide total from the price list (not shown to them): " + money(est.low) + " - " + money(est.high));
    return out.join("\n");
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!lines().length) return;
    var data = new FormData(form);
    var est = estimate();
    var visitDay = data.get("showroom-date"), visitTime = data.get("showroom-time");
    var details = {
      name: data.get("name"), email: data.get("email"), phone: data.get("phone"), venue: data.get("venue"),
      date: niceDate(data.get("wedding-date")), heard: data.get("how-heard"),
      showroom: visitDay || visitTime ? [niceDate(visitDay), visitTime].filter(Boolean).join(", ") : "",
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
