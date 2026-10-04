// Quote builder (/quote-builder): pick items, see a ranged estimate, then save it.
// Saving sends the quote to Winterborne through Netlify Forms (form "quote") and downloads a PDF for the couple.
// Prices live in js/quote-data.js.
(function () {
  var QUOTE_RANGE = 0.2; // the estimate runs 20% below to 20% above the catalogue total
  var catalogue = window.QUOTE_CATALOGUE || [];
  var root = document.querySelector("[data-quote-builder]");
  if (!root) return;

  var listEl = root.querySelector(".qb-sections");
  var summaryList = root.querySelector(".qb-summary-items");
  var emptyNote = root.querySelector(".qb-summary-empty");
  var rangeEls = root.querySelectorAll("[data-qb-range]");
  var countEls = root.querySelectorAll("[data-qb-count]");
  var form = root.querySelector(".qb-form");
  var saveButton = form.querySelector('[type="submit"]');
  var status = form.querySelector(".qb-status");
  var quantities = {};
  var STORAGE_KEY = "winterborne-quote";

  var money = function (n, exact) {
    return "£" + (exact
      ? n.toLocaleString("en-GB", { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 })
      : Math.round(n).toLocaleString("en-GB"));
  };
  var roundTo5 = function (n) { return Math.round(n / 5) * 5; };

  function allItems() {
    var out = [];
    catalogue.forEach(function (section) {
      section.items.forEach(function (item) { out.push({ section: section, item: item }); });
    });
    return out;
  }

  function selected() {
    return allItems()
      .filter(function (x) { return quantities[x.item.id] > 0; })
      .map(function (x) {
        var qty = quantities[x.item.id];
        return { section: x.section.title, item: x.item, qty: qty, total: qty * x.item.price };
      });
  }

  function estimate() {
    var total = selected().reduce(function (sum, line) { return sum + line.total; }, 0);
    return { total: total, low: roundTo5(total * (1 - QUOTE_RANGE)), high: roundTo5(total * (1 + QUOTE_RANGE)) };
  }

  function priceLabel(item) {
    return (item.from ? "from " : "") + money(item.price, true) + (item.unit ? " " + item.unit : "");
  }

  // ----- Build the item list -----
  catalogue.forEach(function (section) {
    var sec = document.createElement("section");
    sec.className = "qb-section";
    sec.innerHTML =
      '<h2 class="qb-section-title"></h2><p class="qb-section-intro"></p><ul class="qb-items" role="list"></ul>';
    sec.querySelector(".qb-section-title").textContent = section.title;
    sec.querySelector(".qb-section-intro").textContent = section.intro || "";
    var ul = sec.querySelector(".qb-items");

    section.items.forEach(function (item) {
      quantities[item.id] = 0;
      var li = document.createElement("li");
      li.className = "qb-item";
      li.dataset.id = item.id;
      li.innerHTML =
        '<div class="qb-item-text"><span class="qb-item-name"></span><span class="qb-item-note"></span>' +
        '<span class="qb-item-price"></span></div>' +
        '<div class="qb-stepper">' +
        '<button type="button" class="qb-step qb-minus" aria-label="">&minus;</button>' +
        '<output class="qb-qty" aria-live="polite">0</output>' +
        '<button type="button" class="qb-step qb-plus" aria-label="">+</button>' +
        "</div>";
      li.querySelector(".qb-item-name").textContent = item.name;
      li.querySelector(".qb-item-note").textContent = item.note || "";
      if (!item.note) li.querySelector(".qb-item-note").remove();
      li.querySelector(".qb-item-price").textContent = priceLabel(item);
      li.querySelector(".qb-minus").setAttribute("aria-label", "Remove one " + item.name);
      li.querySelector(".qb-plus").setAttribute("aria-label", "Add one " + item.name);
      li.querySelector(".qb-minus").addEventListener("click", function () { setQty(item, quantities[item.id] - 1); });
      li.querySelector(".qb-plus").addEventListener("click", function () { setQty(item, quantities[item.id] + 1); });
      ul.appendChild(li);
    });
    listEl.appendChild(sec);
  });

  function setQty(item, qty) {
    var max = item.max || 999;
    quantities[item.id] = Math.max(0, Math.min(max, qty));
    render();
    save();
  }

  // ----- Summary -----
  function render() {
    var lines = selected();
    var est = estimate();

    allItems().forEach(function (x) {
      var li = listEl.querySelector('[data-id="' + x.item.id + '"]');
      var qty = quantities[x.item.id];
      li.querySelector(".qb-qty").textContent = qty;
      li.classList.toggle("is-selected", qty > 0);
      li.querySelector(".qb-minus").disabled = qty === 0;
      li.querySelector(".qb-plus").disabled = qty >= (x.item.max || 999);
    });

    summaryList.innerHTML = "";
    lines.forEach(function (line) {
      var li = document.createElement("li");
      li.innerHTML = '<span class="qb-summary-name"></span><span class="qb-summary-total"></span>';
      li.querySelector(".qb-summary-name").textContent = line.qty + " × " + line.item.name;
      li.querySelector(".qb-summary-total").textContent = money(line.total, true);
      summaryList.appendChild(li);
    });
    emptyNote.hidden = lines.length > 0;

    var text = lines.length ? money(est.low) + " – " + money(est.high) : "£0";
    rangeEls.forEach(function (el) { el.textContent = text; });
    var count = lines.reduce(function (n, l) { return n + l.qty; }, 0);
    countEls.forEach(function (el) { el.textContent = count === 1 ? "1 item" : count + " items"; });
    saveButton.disabled = lines.length === 0;
    root.classList.toggle("has-items", lines.length > 0);
  }

  // Remember a half-built quote on this device
  function save() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(quantities)); } catch (e) {}
  }
  try {
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    Object.keys(saved).forEach(function (id) { if (id in quantities) quantities[id] = saved[id] || 0; });
  } catch (e) {}

  root.querySelector(".qb-clear").addEventListener("click", function () {
    Object.keys(quantities).forEach(function (id) { quantities[id] = 0; });
    render();
    save();
  });

  // ----- Save: send to Winterborne and download the PDF -----
  function quoteText(details, lines, est) {
    var out = [];
    out.push("Name: " + details.name, "Email: " + details.email, "Venue: " + details.venue, "Wedding date: " + details.date, "");
    var current = "";
    lines.forEach(function (l) {
      if (l.section !== current) { current = l.section; out.push(current.toUpperCase()); }
      out.push("  " + l.qty + " x " + l.item.name + " @ " + priceLabel(l.item) + " = " + money(l.total, true));
    });
    out.push("", "Catalogue total: " + money(est.total, true), "Estimated range: " + money(est.low) + " - " + money(est.high));
    return out.join("\n");
  }

  function formatDate(value) {
    if (!value) return "";
    var d = new Date(value + "T12:00:00");
    return isNaN(d) ? value : d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }

  function makePdf(details, lines, est) {
    var JsPDF = window.jspdf && window.jspdf.jsPDF;
    if (!JsPDF) return null;
    var doc = new JsPDF({ unit: "mm", format: "a4" });
    var W = 210, M = 18, y = 22;
    var ink = [58, 56, 53], soft = [110, 104, 98], peach = [229, 151, 117];

    doc.setFont("times", "normal");
    doc.setFontSize(24); doc.setTextColor.apply(doc, ink);
    doc.text("WINTERBORNE", W / 2, y, { align: "center" });
    doc.setFont("times", "italic"); doc.setFontSize(13); doc.setTextColor.apply(doc, peach);
    doc.text("Hire & Styling", W / 2, y + 7, { align: "center" });
    y += 20;
    doc.setDrawColor.apply(doc, peach); doc.setLineWidth(0.4); doc.line(M, y, W - M, y);
    y += 11;

    doc.setFont("times", "normal"); doc.setFontSize(18); doc.setTextColor.apply(doc, ink);
    doc.text("Your wedding styling estimate", M, y);
    y += 9;
    doc.setFont("helvetica", "normal"); doc.setFontSize(10); doc.setTextColor.apply(doc, soft);
    [["Name", details.name], ["Email", details.email], ["Venue", details.venue], ["Wedding date", details.date],
     ["Prepared", new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })]]
      .forEach(function (row) {
        doc.setTextColor.apply(doc, soft); doc.text(row[0], M, y);
        doc.setTextColor.apply(doc, ink); doc.text(String(row[1] || "-"), M + 32, y);
        y += 6;
      });
    y += 6;

    function header() {
      doc.setFont("helvetica", "bold"); doc.setFontSize(8.5); doc.setTextColor.apply(doc, soft);
      doc.text("ITEM", M, y); doc.text("QTY", 128, y, { align: "right" });
      doc.text("GUIDE PRICE", 160, y, { align: "right" }); doc.text("LINE", W - M, y, { align: "right" });
      y += 2.5; doc.setDrawColor(220, 212, 204); doc.setLineWidth(0.2); doc.line(M, y, W - M, y); y += 5.5;
    }
    header();
    var current = "";
    lines.forEach(function (l) {
      if (y > 262) { doc.addPage(); y = 22; header(); }
      if (l.section !== current) {
        current = l.section;
        doc.setFont("helvetica", "bold"); doc.setFontSize(9.5); doc.setTextColor.apply(doc, peach);
        doc.text(current.toUpperCase(), M, y); y += 6;
      }
      doc.setFont("helvetica", "normal"); doc.setFontSize(10); doc.setTextColor.apply(doc, ink);
      var name = doc.splitTextToSize(l.item.name, 100);
      doc.text(name, M, y);
      doc.text(String(l.qty), 128, y, { align: "right" });
      doc.setTextColor.apply(doc, soft);
      doc.text(priceLabel(l.item), 160, y, { align: "right" });
      doc.setTextColor.apply(doc, ink);
      doc.text(money(l.total, true), W - M, y, { align: "right" });
      y += 6 * name.length;
    });

    if (y > 235) { doc.addPage(); y = 22; }
    y += 4; doc.setDrawColor.apply(doc, peach); doc.setLineWidth(0.4); doc.line(M, y, W - M, y); y += 12;
    doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor.apply(doc, soft);
    doc.text("YOUR ESTIMATED RANGE", W / 2, y, { align: "center" }); y += 10;
    doc.setFont("times", "normal"); doc.setFontSize(26); doc.setTextColor.apply(doc, ink);
    doc.text(money(est.low) + "  –  " + money(est.high), W / 2, y, { align: "center" }); y += 10;
    doc.setFont("helvetica", "normal"); doc.setFontSize(9); doc.setTextColor.apply(doc, soft);
    var note = doc.splitTextToSize(
      "This is a guide based on our 2027/28 price list, shown as a range because every design is made to your " +
      "colours, venue and numbers. We'll confirm your final quote after a relaxed showroom consultation.", W - 2 * M - 20);
    doc.text(note, W / 2, y, { align: "center" });

    doc.setFontSize(9); doc.setTextColor.apply(doc, soft);
    doc.text("winterbornehireandstyling.co.uk  ·  Dawn 07869 136939  ·  winterbornevintage@gmail.com", W / 2, 285, { align: "center" });
    return doc;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var lines = selected();
    if (!lines.length) return;
    var est = estimate();
    var details = {
      name: form.elements["name"].value.trim(),
      email: form.elements["email"].value.trim(),
      venue: form.elements["venue"].value.trim(),
      date: formatDate(form.elements["wedding-date"].value),
    };
    form.elements["estimate"].value = money(est.low) + " - " + money(est.high);
    form.elements["quote"].value = quoteText(details, lines, est);

    var label = saveButton.textContent;
    saveButton.disabled = true;
    saveButton.textContent = "Saving…";
    status.hidden = true;

    var pdf = makePdf(details, lines, est);
    var filename = "Winterborne-estimate-" + (details.name || "wedding").replace(/[^a-z0-9]+/gi, "-") + ".pdf";

    fetch("/", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams(new FormData(form)).toString(),
    })
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        if (pdf) pdf.save(filename);
        status.className = "qb-status is-done";
        status.textContent = "Thank you! Your estimate has downloaded, and we’ve received your quote. We’ll be in touch soon.";
      })
      .catch(function () {
        if (pdf) pdf.save(filename);
        status.className = "qb-status is-error";
        status.textContent = "Your estimate has downloaded, but we couldn’t send it to us just now. Please email it to winterbornevintage@gmail.com.";
      })
      .finally(function () {
        status.hidden = false;
        saveButton.textContent = label;
        saveButton.disabled = false;
      });
  });

  render();
})();
