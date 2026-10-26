// "Kind words from our couples" (scripts/reviews_block.py): each block holds the four featured couples' reviews.
// Show a random one on each visit, never the same one twice in a row.
(function () {
  document.querySelectorAll("[data-reviews]").forEach(function (box) {
    var quotes = box.querySelectorAll("[data-review]");
    if (quotes.length < 2) return;
    var last = -1;
    try { last = Number(sessionStorage.getItem("winterborne-review")); } catch (e) {}
    var known = last >= 0 && last < quotes.length;
    var pick = Math.floor(Math.random() * (known ? quotes.length - 1 : quotes.length));
    if (known && pick >= last) pick += 1;
    quotes.forEach(function (q, i) { q.hidden = i !== pick; });
    try { sessionStorage.setItem("winterborne-review", String(pick)); } catch (e) {}
  });
})();
