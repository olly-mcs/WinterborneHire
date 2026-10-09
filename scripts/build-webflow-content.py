#!/usr/bin/env python3
"""Rebuild the product lists, product pages and older testimonials from data/webflow-content.json
(converted from the Webflow CMS CSV exports).

Each image uses the copy saved in images/webflow/ when it exists, otherwise Webflow's original URL.
Run scripts/fetch-webflow-images.mjs to save the images, then run this again:

    python3 scripts/build-webflow-content.py
"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(ROOT, "data", "webflow-content.json"), encoding="utf-8"))
e = html.escape

COLLECTIONS = {
    "florals-foliage": {"page": "florals-foliage.html", "title": "Florals & Foliage", "label": "florals & foliage",
                        "tabs": {"All": None, "Centerpieces": "Centrepieces", "Top Table": "Top Table",
                                 "Runners": "Runners", "Other": "Other"}},
    "signage": {"page": "signage.html", "title": "Signage", "label": "signage"},
    "rugs-runners": {"page": "rugs-runners.html", "title": "Rugs & Runners", "label": "rugs & runners",
                     "url": "rugs-runners-collection"},
    "large-props": {"page": "large-props.html", "title": "Large Props", "label": "large props",
                    "url": "large-prop-collection",
                    "tabs": {"All": None, "Archways": "Archways", "Moongates": "Moongates", "Other Decor": "Other Decor"}},
    "small-props": {"page": "small-props.html", "title": "Small Props", "label": "small props",
                    "url": "small-props-collection",
                    "tabs": {"All": None, "Lanterns": "Lanterns", "Cake Stands": "Cake Stands", "Other Decor": "Other Decor"}},
    "table-decor": {"page": "table-decor.html", "title": "Table Decor", "label": "table decor",
                    "url": "table-decor-collection",
                    "tabs": {"All": None, "CandleHolders": "Candleholdes", "Vessels": "Vessels",
                             "Table Numbers": "Table Numbers", "Other": "Other"}},
    "furniture": {"page": "furniture.html", "title": "Furniture", "label": "furniture", "url": "furniture-collection"},
}


def img_url(img):
    if not img:
        return ""
    return "/" + img["file"] if os.path.exists(os.path.join(ROOT, img["file"])) else img["src"]


def sized(img, sizes, default=600):
    """src/srcset/sizes attributes, using the web-sized copies in images/webflow-sized/ when they exist."""
    if not img:
        return 'src=""'
    stem, _ = os.path.splitext(img["file"].replace("images/webflow/", "images/webflow-sized/", 1))
    small, large = f"{stem}-600.webp", f"{stem}-1200.webp"
    if os.path.exists(os.path.join(ROOT, small)) and os.path.exists(os.path.join(ROOT, large)):
        src = small if default == 600 else large
        return f'src="/{src}" srcset="/{small} 600w, /{large} 1200w" sizes="{sizes}"'
    return f'src="{img_url(img)}"'


CARD_SIZES = "(max-width: 767px) 50vw, (max-width: 991px) 33vw, 300px"


def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(text)


def block_end(s, start):
    """Index just after the </div> that closes the <div ...> opening at start."""
    depth, i = 0, start
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        depth += 1 if m.group(0) != "</div>" else -1
        if depth == 0:
            return start + m.end()
    raise ValueError("unbalanced div")


def card(col, item):
    prefix = COLLECTIONS[col].get("url", col)
    alt = e(item["name"])
    main = sized(item["image"], CARD_SIZES)
    hover_img = f'<img {sized(item["hover"], CARD_SIZES)} loading="lazy" alt="" class="smallpropplphover">' if item["hover"] else ""
    return (f'<div role="listitem" class="product-card">'
            f'<a href="/{prefix}/{item["slug"]}" class="product-card-link">'
            f'<span class="product-card-media"><img {main} loading="lazy" alt="{alt}">{hover_img}</span>'
            f'<span class="product-card-name">{alt}</span></a></div>')


def grid(col, items):
    if not items:
        return '<p class="product-empty">Nothing here at the moment. Ask us about this in the showroom.</p>'
    return ('<div class="product-grid" role="list">\n'
            + "\n".join("        " + card(col, i) for i in items) + "\n      </div>")


WF_CSS = '<link href="/css/winterborne-vintage.webflow.css" rel="stylesheet" type="text/css">'
MARK_START, MARK_END = "<!-- products:start -->", "<!-- products:end -->"


def fill_list_page(col, cfg, items):
    path = cfg["page"]
    s = read(path)
    tabs = cfg.get("tabs")
    if MARK_START in s:  # already built once: rebuild between markers
        a, b = s.index(MARK_START), s.index(MARK_END) + len(MARK_END)
        if tabs:
            # markers wrap each tab pane's list; rebuild each in order
            panes = list(tabs.items())
            out, pos, k = [], 0, 0
            for m in re.finditer(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), s, re.S):
                name, flt = panes[k]
                sel = [i for i in items if flt is None or i["filter"] == flt]
                out.append(s[pos:m.start()] + MARK_START + "\n      " + grid(col, sel) + "\n      " + MARK_END)
                pos, k = m.end(), k + 1
            s = "".join(out) + s[pos:]
        else:
            s = s[:a] + MARK_START + "\n      " + grid(col, items) + "\n      " + MARK_END + s[b:]
    else:  # first run: replace the empty Webflow CMS lists
        k = 0
        panes = list(tabs.items()) if tabs else [(None, None)]
        while True:
            m = re.search(r'<div class="[^"]*\bw-dyn-list"', s)
            if not m:
                break
            end = block_end(s, m.start())
            name, flt = panes[k]
            sel = [i for i in items if flt is None or i["filter"] == flt]
            s = s[:m.start()] + MARK_START + "\n      " + grid(col, sel) + "\n      " + MARK_END + s[end:]
            k += 1
    if "/css/products.css" not in s:
        s = s.replace(WF_CSS, WF_CSS + '\n  <link href="/css/products.css" rel="stylesheet" type="text/css">', 1)
    write(path, s)


def detail_page(col, cfg, item, items):
    s = read(cfg["page"])
    head = s[:s.index('<div class="section-14">')] if '<div class="section-14">' in s else None
    if head is None:
        raise ValueError("no section-14 in " + cfg["page"])
    foot = s[s.index('<div class="badgesection">'):]
    title = f'{item["name"]} | {cfg["title"]} Hire | Winterborne Hire &amp; Styling'
    head = re.sub(r"<title>.*?</title>", f"<title>{e(item['name'])} | {e(cfg['title'])} Hire | Winterborne Hire &amp; Styling</title>", head, count=1)
    plain = re.sub(r"<[^>]+>", " ", item["description"])
    plain = re.sub(r"\s+", " ", html.unescape(plain)).strip()[:155] or f"{item['name']}, available to hire for weddings in Dorset."
    for pat in [r'(<meta content=")[^"]*(" name="description">)', r'(<meta content=")[^"]*(" property="og:description">)',
                r'(<meta content=")[^"]*(" name="twitter:description">)']:
        head = re.sub(pat, lambda m: m.group(1) + e(plain) + m.group(2), head, count=1)
    head = re.sub(r'(<meta content=")[^"]*(" property="og:title">)', lambda m: m.group(1) + e(item["name"]) + m.group(2), head, count=1)
    head = re.sub(r'(<meta content=")[^"]*(" name="twitter:title">)', lambda m: m.group(1) + e(item["name"]) + m.group(2), head, count=1)
    head = re.sub(r'(<link href="https://www\.winterbornehireandstyling\.co\.uk/)[^"]*(" rel="canonical">)',
                  lambda m: m.group(1) + f'{cfg.get("url", col)}/{item["slug"]}' + m.group(2), head, count=1)
    if "/css/products.css" not in head:
        head = head.replace(WF_CSS, WF_CSS + '\n  <link href="/css/products.css" rel="stylesheet" type="text/css">', 1)
    images = [i for i in (item["image"], item["hover"]) if i]
    gallery = ""
    for n, i in enumerate(images):
        load = 'fetchpriority="high"' if n == 0 else 'loading="lazy"'
        extra = "" if n == 0 else " styled at a wedding"
        size = "(max-width: 991px) 100vw, 600px" if n == 0 or len(images) == 1 else "(max-width: 991px) 50vw, 300px"
        gallery += f'<img {sized(i, size, 1200 if n == 0 else 600)} alt="{e(item["name"])}{extra}" {load} class="product-photo">'
    qty = f'<p class="product-qty"><span>Available</span> {e(item["quantity"])}</p>' if item["quantity"] else ""
    others = [i for i in items if i["slug"] != item["slug"]][:4]
    related = "".join("        " + card(col, i) + "\n" for i in others)
    body = f'''  <main class="product-page">
    <nav class="product-crumbs" aria-label="Breadcrumb"><a href="/{col}">{e(cfg["title"])}</a><span aria-hidden="true">/</span><span>{e(item["name"])}</span></nav>
    <div class="product-layout">
      <div class="product-gallery product-gallery-{len(images)}">{gallery}</div>
      <div class="product-info">
        <p class="product-eyebrow">{e(cfg["title"])} to hire</p>
        <h1 class="product-title">{e(item["name"])}</h1>
        {qty}
        <div class="product-desc">{item["description"]}</div>
        <div class="product-actions">
          <a href="/showroom" class="product-button product-button-primary">Book a showroom visit</a>
          <a href="/contact-us" class="product-button">Ask about this piece</a>
        </div>
      </div>
    </div>
    <section class="product-related" aria-labelledby="related-title">
      <h2 id="related-title" class="product-related-title">More {e(cfg["label"])}</h2>
      <div class="product-grid product-grid-4" role="list">
{related}      </div>
      <p class="product-related-more"><a href="/{col}">See all {e(cfg["label"])}</a></p>
    </section>
  </main>
'''
    write(f"{cfg.get('url', col)}/{item['slug']}.html", head + body + foot)


def testimonials():
    path = "our-testimonials.html"
    s = read(path)
    cards = []
    for t in DATA["testimonials"]:
        img = sized(t["image"], "(max-width: 767px) 100vw, 400px")
        meta = " &middot; ".join(x for x in (e(t["venue"]), e(t["month"])) if x)
        paras = "".join(f"<p>{e(p.strip())}</p>" for p in t["quote"].split("\n") if p.strip())
        cards.append(f'''        <li class="kw-card">
          <img {img} alt="{e(t["names"])}" loading="lazy" class="kw-photo">
          <div class="kw-text">
            <h3 class="kw-names">{e(t["names"])}</h3>
            <p class="kw-meta">{meta}</p>
            <blockquote class="kw-quote">{paras}</blockquote>
          </div>
        </li>''')
    section = f'''<!-- kind-words:start -->
  <section class="kw" aria-labelledby="kw-title">
    <div class="kw-head">
      <p class="tm-eyebrow">Over the years</p>
      <h2 id="kw-title" class="kw-title">More kind words</h2>
    </div>
    <ul class="kw-grid" role="list">
{chr(10).join(cards)}
    </ul>
  </section>
  <!-- kind-words:end -->'''
    if "<!-- kind-words:start -->" in s:
        a = s.index("<!-- kind-words:start -->")
        b = s.index("<!-- kind-words:end -->") + len("<!-- kind-words:end -->")
        s = s[:a] + section + s[b:]
    else:
        anchor = '  <dialog class="tm-lightbox"'
        s = s.replace(anchor, "  " + section + "\n" + anchor, 1)
    if "/css/products.css" not in s:
        s = s.replace('<link href="/css/testimonials.css" rel="stylesheet" type="text/css">',
                      '<link href="/css/testimonials.css" rel="stylesheet" type="text/css">\n  <link href="/css/products.css" rel="stylesheet" type="text/css">', 1)
    write(path, s)


if __name__ == "__main__":
    for col, cfg in COLLECTIONS.items():
        items = DATA[col]
        fill_list_page(col, cfg, items)
        for item in items:
            detail_page(col, cfg, item, items)
        print(f"{col}: {len(items)} products")
    testimonials()
    print(f"testimonials: {len(DATA['testimonials'])}")
    saved = sum(1 for k, v in DATA.items() for i in v for f in ("image", "hover")
                if i.get(f) and os.path.exists(os.path.join(ROOT, i[f]["file"])))
    total = sum(1 for k, v in DATA.items() for i in v for f in ("image", "hover") if i.get(f))
    print(f"images saved locally: {saved}/{total}")
