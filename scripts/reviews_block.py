"""The "Kind words from our couples" reviews block, in the homepage style, used on the homepage, Who we are and every
Bespoke Florals product page. Its quotes are the four featured couples' Google reviews on /our-testimonials, read
from our-testimonials.html, so editing a review there (then rebuilding) updates every block.

Each block holds all four quotes. One is shown when the page loads (a different one per page), and js/reviews.js
swaps in a random one on each visit, so a couple browsing the site sees different couples' words.
"""
import html, os, re, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

BLOCK_RE = re.compile(r'  <section class="hp-reviews"[^>]*>.*?\n  </section>\n', re.S)
SCRIPT = '  <script src="/js/reviews.js" type="text/javascript"></script>\n'


def featured():
    """The featured couples on /our-testimonials, in page order: names, venue and their review paragraphs."""
    s = open(os.path.join(ROOT, "our-testimonials.html"), encoding="utf-8").read()
    out = []
    for a in re.findall(r'<article class="tm" id="[^"]+".*?</article>', s, re.S):
        text = lambda frag: html.unescape(re.sub(r"<[^>]+>", "", frag)).strip()
        names = text(re.search(r'<h2[^>]*class="tm-names">(.*?)</h2>', a, re.S).group(1))
        venue = text(re.search(r'<p class="tm-meta"><span>(.*?)</span>', a).group(1))
        quote = re.search(r'<blockquote class="tm-quote">(.*?)</blockquote>', a, re.S).group(1)
        paras = [text(p) for p in re.findall(r"<p>(.*?)</p>", quote, re.S)]
        out.append(dict(names=" ".join(names.split()), venue=venue, paras=paras))
    return out


def block(key):
    """The block for a page; key (the page's path) picks which couple shows first, so pages differ without script."""
    reviews = featured()
    first = zlib.crc32(key.encode()) % len(reviews)
    figures = "\n".join(
        f'    <figure class="hp-quote" data-review{"" if i == first else " hidden"}>\n'
        f'      <blockquote>{"".join(f"<p>{e(p)}</p>" for p in r["paras"])}</blockquote>\n'
        f'      <figcaption><span class="hp-quote-names">{e(r["names"])}</span><span class="hp-quote-venue">{e(r["venue"])}</span></figcaption>\n'
        f'    </figure>'
        for i, r in enumerate(reviews))
    return f'''  <section class="hp-reviews" aria-labelledby="reviews-title" data-reviews>
    <h2 id="reviews-title" class="hp-heading">Kind words from our couples</h2>
    <p class="hp-rating"><span class="hp-stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span> 5.0 from over a hundred Google reviews</p>
{figures}
    <p class="hp-center"><a href="/our-testimonials" class="hp-button hp-button-outline">Read more reviews</a></p>
  </section>
'''


def update(text, key):
    """Rebuild a page's reviews block (if it has one) and make sure it loads js/reviews.js."""
    if not BLOCK_RE.search(text):
        return text
    text = BLOCK_RE.sub(lambda m: block(key), text, count=1)
    if SCRIPT not in text:
        text = text.replace("</body>", SCRIPT + "</body>", 1)
    return text
