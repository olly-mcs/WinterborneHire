// Mock-up shop (bridal-bouquets-delivery.html): "Add to basket" buttons and a basket panel that slides out from the
// right. A design prototype only: the basket is kept in the visitor's browser and checkout isn't built.
(function () {
  var KEY = "winterborne-shop-basket";
  var basket = {};
  try { basket = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(basket)); } catch (e) {} }
  var esc = function (s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  };
  var money = function (n) { return "£" + n.toFixed(2).replace(/\.00$/, ""); };

  var el = document.createElement("div");
  el.className = "sb";
  el.innerHTML =
    '<button type="button" class="sb-tab" aria-controls="sb-panel" aria-expanded="false">Basket <span class="sb-count">0</span></button>' +
    '<div class="sb-overlay" hidden></div>' +
    '<aside class="sb-panel" id="sb-panel" role="dialog" aria-modal="true" aria-labelledby="sb-title" hidden>' +
    '  <div class="sb-head"><h2 id="sb-title" class="sb-title">Your basket</h2>' +
    '    <button type="button" class="sb-close" aria-label="Close your basket">&times;</button></div>' +
    '  <div class="sb-body"><ul class="sb-lines" role="list"></ul>' +
    '    <p class="sb-empty">Your basket is empty.</p>' +
    '    <div class="sb-total"><span>Total</span><strong class="sb-sum"></strong></div>' +
    '    <p class="sb-delivery">Delivered anywhere in the UK.</p>' +
    '    <button type="button" class="sb-checkout" disabled>Checkout (coming soon)</button>' +
    '    <p class="sb-note">Design mock-up: checkout isn&#x27;t built yet.</p></div>' +
    '</aside>';
  document.body.appendChild(el);
  var panel = el.querySelector(".sb-panel"), overlay = el.querySelector(".sb-overlay"), tab = el.querySelector(".sb-tab");

  function open() {
    panel.hidden = false; overlay.hidden = false;
    requestAnimationFrame(function () { el.classList.add("is-open"); });
    tab.setAttribute("aria-expanded", "true");
    el.querySelector(".sb-close").focus();
  }
  function close() {
    el.classList.remove("is-open");
    tab.setAttribute("aria-expanded", "false");
    setTimeout(function () { panel.hidden = true; overlay.hidden = true; }, 250);
    tab.focus();
  }
  function render() {
    var ids = Object.keys(basket), n = 0, sum = 0;
    el.querySelector(".sb-lines").innerHTML = ids.map(function (id) {
      var l = basket[id]; n += l.qty; sum += l.qty * l.price;
      return '<li class="sb-line" data-id="' + esc(id) + '"><div><span class="sb-name">' + esc(l.name) + '</span>' +
        '<span class="sb-price">' + money(l.price) + ' each</span></div>' +
        '<div class="sb-qty"><button type="button" class="sb-minus" aria-label="One fewer">&minus;</button>' +
        '<span aria-live="polite">' + l.qty + '</span>' +
        '<button type="button" class="sb-plus" aria-label="One more">+</button></div></li>';
    }).join("");
    el.querySelector(".sb-count").textContent = n;
    el.querySelector(".sb-sum").textContent = money(sum);
    el.classList.toggle("has-items", ids.length > 0);
    tab.hidden = n === 0 && !el.classList.contains("is-open");
  }
  function setQty(id, qty) {
    if (qty > 0) basket[id].qty = Math.min(qty, 99); else delete basket[id];
    save(); render();
  }
  document.querySelectorAll("[data-shop-add]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var id = btn.getAttribute("data-shop-add");
      if (basket[id]) basket[id].qty += 1;
      else basket[id] = { name: btn.getAttribute("data-name"), price: Number(btn.getAttribute("data-price")), qty: 1 };
      save(); render();
      btn.textContent = "Added ✓";
      setTimeout(function () { btn.textContent = "Add to basket"; }, 1400);
      open();
    });
  });
  el.querySelector(".sb-lines").addEventListener("click", function (e) {
    var li = e.target.closest(".sb-line"); if (!li) return;
    var id = li.getAttribute("data-id");
    if (e.target.closest(".sb-plus")) setQty(id, basket[id].qty + 1);
    if (e.target.closest(".sb-minus")) setQty(id, basket[id].qty - 1);
  });
  tab.addEventListener("click", open);
  overlay.addEventListener("click", close);
  el.querySelector(".sb-close").addEventListener("click", close);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && el.classList.contains("is-open")) close(); });
  render();
})();
