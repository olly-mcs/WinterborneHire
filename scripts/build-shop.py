#!/usr/bin/env python3
"""Builds the mock-up shop page, /bridal-bouquets-delivery (bridal-bouquets-delivery.html): bridal bouquets and
buttonholes with UK-wide delivery. A design prototype: the products, prices and copy below are placeholders, and the
basket (js/shop.js) is kept in the visitor's browser; checkout isn't built.

Edit PRODUCTS, then run:  python3 scripts/build-shop.py
The "UK-wide delivery" pull tab under the menu (every page) is added by scripts/build-bespoke-florals.py.
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape
B = "/images/bespoke-florals/"

PRODUCTS = [
    dict(id="bouquet-autumn", group="Bridal bouquets", name="The Harvest Bouquet", price=145,
         desc="A loose, wild bouquet of burnt orange, peach and ivory blooms with dried grasses.",
         img=B + "bridal-bouquets/autumn-bouquet", pos="50% 30%"),
    dict(id="bouquet-meadow", group="Bridal bouquets", name="The Meadow Bouquet", price=135,
         desc="Bright, joyful meadow flowers in pinks, oranges and yellows, tied with ribbon.",
         img=B + "bridal-bouquets/bright-meadow-bouquet", pos="50% 45%"),
    dict(id="bouquet-pastel", group="Bridal bouquets", name="The Pastel Bouquet", price=140,
         desc="Soft blush, pale blue and ivory blooms for a romantic, timeless look.",
         img=B + "bridal-bouquets/sophie-and-ben-portrait", pos="50% 55%"),
    dict(id="bouquet-burgundy", group="Bridal bouquets", name="The Burgundy Bouquet", price=150,
         desc="Deep reds, burgundy and plum with trailing foliage, for an elegant, moody statement.",
         img=B + "bridal-bouquets/laura-and-alexandra-portrait", pos="50% 55%"),
    dict(id="bouquet-sunshine", group="Bridal bouquets", name="The Sunshine Bouquet", price=130,
         desc="White, buttercup yellow and pale blue blooms, fresh and light for a summer wedding.",
         img=B + "bridal-bouquets/alysha-and-chris", pos="50% 55%"),
    dict(id="bouquet-peony", group="Bridal bouquets", name="The Peony Bouquet", price=155,
         desc="Lush hot-pink and white peonies with soft greenery, full and abundant.",
         img=B + "bridal-bouquets/pink-peony-bouquet", pos="45% 55%"),
    dict(id="buttonhole-bright", group="Buttonholes", name="The Bright Buttonhole", price=15,
         desc="Pink, orange and yellow blooms with a sprig of fern, to match a colourful bouquet.",
         img=B + "buttonholes/buttonhole-close-up", pos="50% 30%"),
    dict(id="buttonhole-classic", group="Buttonholes", name="The Classic Buttonhole", price=12,
         desc="A single deep red bloom with ivory accents and foliage, simple and timeless.",
         img=B + "buttonholes/pinning-the-buttonhole", pos="50% 50%"),
]


def card(p):
    return f'''        <li class="shop-card">
          <img src="{p["img"]}-600.webp" srcset="{p["img"]}-600.webp 600w, {p["img"]}-1200.webp 1200w" sizes="(max-width: 767px) 50vw, 25vw" alt="{e(p["name"])}" style="object-position: {p["pos"]}" loading="lazy">
          <div class="shop-card-body">
            <h3 class="shop-card-name">{e(p["name"])}</h3>
            <p class="shop-card-desc">{e(p["desc"])}</p>
            <p class="shop-card-price">&pound;{p["price"]}</p>
            <button type="button" class="shop-add" data-shop-add="{p["id"]}" data-name="{e(p["name"])}" data-price="{p["price"]}">Add to basket</button>
          </div>
        </li>'''


def group(name, intro):
    items = [p for p in PRODUCTS if p["group"] == name]
    slug = name.lower().replace(" ", "-")
    return f'''  <section class="shop-group" aria-labelledby="shop-{slug}">
    <div class="shop-group-head">
      <h2 id="shop-{slug}" class="shop-group-title">{e(name)}</h2>
      <p class="shop-group-intro">{e(intro)}</p>
    </div>
    <ul class="shop-grid shop-grid-{len(items)}" role="list">
{chr(10).join(card(p) for p in items)}
    </ul>
  </section>
'''


BODY = f'''  <section class="shop-hero" aria-labelledby="shop-title">
    <h1 id="shop-title" class="shop-hero-title">Bridal bouquets</h1>
    <p class="shop-hero-sub">Delivered UK-wide.</p>
    <p class="shop-hero-lead">Ready-designed faux bridal bouquets and buttonholes in high-quality silk and real-touch flowers, made in our Dorset studio and delivered
      anywhere in the UK. They never wilt, so they look as fresh in your last photo as your first.</p>
    <p class="shop-mock-note">Design mock-up: products and prices are placeholders.</p>
  </section>
{group("Bridal bouquets", "Six signature designs, each made to order in our Dorset studio.")}{group("Buttonholes", "Made to match, for the groom, groomsmen and family.")}'''

SHOP_CSS = '<link href="/css/shop.css" rel="stylesheet" type="text/css">'
SHOP_JS = '  <script src="/js/shop.js" type="text/javascript"></script>\n'

if __name__ == "__main__":
    src = open(os.path.join(ROOT, "contact-us.html"), encoding="utf-8").read()
    head = src[:src.index('  <section class="sr-about ct-intro"')]
    foot = src[src.index('  <div class="badgesection">'):]
    title = "Bridal Bouquets with UK Delivery | Winterborne Hire &amp; Styling"
    desc = ("Faux bridal bouquets and buttonholes, made in our Dorset studio and delivered anywhere in the UK. "
            "They never wilt, so they look as fresh in your last photo as your first.")
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1)
    for a in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(r'<meta content="[^"]*" ' + re.escape(a) + ">", f'<meta content="{title}" {a}>', head, count=1)
    for a in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(r'<meta content="[^"]*" ' + re.escape(a) + ">", f'<meta content="{e(desc)}" {a}>', head, count=1)
    head = re.sub(r'<link href="https://www\.winterbornehireandstyling\.co\.uk[^"]*" rel="canonical">',
                  '<link href="https://www.winterbornehireandstyling.co.uk/bridal-bouquets-delivery" rel="canonical">', head, count=1)
    head = head.replace(' aria-current="page"', "").replace(" w--current", "")
    if SHOP_CSS not in head:
        head = head.replace("</head>", "  " + SHOP_CSS + "\n</head>", 1)
    foot = foot.replace(' aria-current="page"', "").replace(" w--current", "")
    if SHOP_JS not in foot:
        foot = foot.replace("</body>", SHOP_JS + "</body>", 1)
    open(os.path.join(ROOT, "bridal-bouquets-delivery.html"), "w", encoding="utf-8").write(head + BODY + foot)
    print(f"built the shop page with {len(PRODUCTS)} products")
    # the signed-off page title and description (data/page-meta.json) win over the ones above
    import subprocess, sys
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "apply-page-meta.py")], check=True)
