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

# The hire collection. "sources" lists the data/webflow-content.json collections a page combines (default: its own
# key). Florals & Foliage is no longer listed (Bespoke Florals covers it; its old URLs redirect in netlify.toml), and
# Furniture and Rugs & Runners are combined into Furniture & Rugs.
COLLECTIONS = {
    "signage": {"page": "signage.html", "title": "Signage", "label": "signage"},
    "furniture-rugs": {"page": "furniture-rugs.html", "title": "Furniture & Rugs", "label": "furniture & rugs",
                       "url": "furniture-rugs", "sources": ["furniture", "rugs-runners"]},
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
}


def collection_items(col):
    return [i for src in COLLECTIONS[col].get("sources", [col]) for i in DATA[src]]


def list_url(cfg):
    return "/" + cfg["page"][:-5]


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


# Product page scripts: the photo slider and the wish list (shared with Bespoke Florals; js/hire-items.js names the
# hire products for it)
HIRE_PAGE_JS = ('  <script src="/js/bespoke-gallery.js" type="text/javascript"></script>\n'
                '  <script src="/js/quote-data.js" type="text/javascript"></script>\n'
                '  <script src="/js/hire-items.js" type="text/javascript"></script>\n'
                '  <script src="/js/bespoke-sections.js" type="text/javascript"></script>\n'
                '  <script src="/js/wishlist.js" type="text/javascript"></script>\n')


def hire_id(col, item):
    return f"hire-{col}-{item['slug']}"


def slider(name, images):
    """The photo slider used on Bespoke Florals product pages: one shape (4:5, cropped to fill) for every photo."""
    slides = "".join(
        f'<li class="pd-slide" aria-label="Photo {n + 1} of {len(images)}"><img {sized(i, "(max-width: 991px) 100vw, 50vw", 1200)} '
        f'alt="{e(name)}{"" if n == 0 else " styled at a wedding"}" {"fetchpriority=" + chr(34) + "high" + chr(34) if n == 0 else "loading=" + chr(34) + "lazy" + chr(34)}></li>'
        for n, i in enumerate(images))
    if len(images) < 2:
        return f'<div class="pd-gallery"><div class="pd-stage"><ul class="pd-track" role="list">{slides}</ul></div></div>'
    thumbs = "".join(
        f'<li><button type="button" class="pd-thumb{" is-active" if n == 0 else ""}" data-slide="{n}" aria-label="Show photo {n + 1}"'
        f'{" aria-current=" + chr(34) + "true" + chr(34) if n == 0 else ""}><img {sized(i, "120px")} alt="" loading="lazy"></button></li>'
        for n, i in enumerate(images))
    return f'''<div class="pd-gallery" data-gallery>
        <div class="pd-stage">
          <ul class="pd-track" role="list" tabindex="0" aria-label="{e(name)} photos">{slides}</ul>
          <button type="button" class="pd-arrow pd-prev" aria-label="Previous photo" data-prev>&#8249;</button>
          <button type="button" class="pd-arrow pd-next" aria-label="Next photo" data-next>&#8250;</button>
          <p class="pd-count" aria-hidden="true"><span data-count>1</span> / {len(images)}</p>
        </div>
        <ul class="pd-thumbs" role="list">{thumbs}</ul>
      </div>'''


def write_hire_items():
    rows = [dict(id=hire_id(col, i), name=i["name"].strip(), section=cfg["title"], url=f"/{cfg.get('url', col)}/{i['slug']}")
            for col, cfg in COLLECTIONS.items() for i in collection_items(col)]
    write("js/hire-items.js", "// Written by scripts/build-webflow-content.py: the hire collection products, for the wish list\n"
          "// (js/wishlist.js). Don't edit by hand.\nwindow.HIRE_ITEMS = " + json.dumps(rows, indent=1, ensure_ascii=False) + ";\n")


def detail_page(col, cfg, item, items):
    s = read(cfg["page"])
    head = s[:s.index('<div class="section-14">')] if '<div class="section-14">' in s else None
    if head is None:
        raise ValueError("no section-14 in " + cfg["page"])
    foot = s[s.index('<div class="badgesection">'):]
    title = f'{item["name"]} | {cfg["title"]} Hire | Winterborne Hire &amp; Styling'
    head = re.sub(r"<title>.*?</title>", f"<title>{e(seo_title(item['name'], cfg['title']))}</title>", head, count=1)
    plain = seo_description(item["description"], item["name"])
    for pat in [r'(<meta content=")[^"]*(" name="description">)', r'(<meta content=")[^"]*(" property="og:description">)',
                r'(<meta content=")[^"]*(" name="twitter:description">)']:
        head = re.sub(pat, lambda m: m.group(1) + e(plain) + m.group(2), head, count=1)
    head = re.sub(r'(<meta content=")[^"]*(" property="og:title">)', lambda m: m.group(1) + e(item["name"]) + m.group(2), head, count=1)
    head = re.sub(r'(<meta content=")[^"]*(" name="twitter:title">)', lambda m: m.group(1) + e(item["name"]) + m.group(2), head, count=1)
    head = re.sub(r'(<link href="https://www\.winterbornehireandstyling\.co\.uk/)[^"]*(" rel="canonical">)',
                  lambda m: m.group(1) + f'{cfg.get("url", col)}/{item["slug"]}' + m.group(2), head, count=1)
    if "/css/products.css" not in head:
        head = head.replace(WF_CSS, WF_CSS + '\n  <link href="/css/products.css" rel="stylesheet" type="text/css">', 1)
    for css in ("/css/bespoke-product.css", "/css/wishlist.css"):
        if css not in head:
            head = head.replace('<link href="/css/products.css" rel="stylesheet" type="text/css">',
                                f'<link href="/css/products.css" rel="stylesheet" type="text/css">\n  <link href="{css}" rel="stylesheet" type="text/css">', 1)
    foot = re.sub(r'  <script src="/js/(?:quote-data|hire-items|bespoke-sections|wishlist|bespoke-gallery)\.js"[^>]*></script>\n', "", foot)
    foot = foot.replace("</body>", HIRE_PAGE_JS + "</body>", 1)
    images = [i for i in (item["image"], item["hover"]) if i]
    others = [i for i in items if i["slug"] != item["slug"]][:4]
    related = "".join("        " + card(col, i) + "\n" for i in others)
    body = f'''  <main class="product-page">
    <nav class="product-crumbs" aria-label="Breadcrumb"><a href="{list_url(cfg)}">{e(cfg["title"])}</a><span aria-hidden="true">/</span><span>{e(item["name"])}</span></nav>
    <div class="product-layout">
      {slider(item["name"], images)}
      <div class="product-info">
        <h1 class="product-title">{e(item["name"])}</h1>
        <div class="product-desc">{item["description"]}</div>
        <div class="product-actions">
          <button type="button" class="product-button product-button-primary" data-wish-add="{hire_id(col, item)}">Add to your wish list</button>
          <a href="/showroom" class="product-button">Book a showroom visit</a>
        </div>
      </div>
    </div>
    <section class="product-related" aria-labelledby="related-title">
      <h2 id="related-title" class="product-related-title">More {e(cfg["label"])}</h2>
      <div class="product-grid product-grid-4" role="list">
{related}      </div>
      <p class="product-related-more"><a href="{list_url(cfg)}">See all {e(cfg["label"])}</a></p>
    </section>
  </main>
'''
    write(f"{cfg.get('url', col)}/{item['slug']}.html", head + body + foot)


# Where each "More kind words" photo is cropped (its 4:3 card), as a CSS object-position, so no one's head is cut
# off. Photos not listed use TESTIMONIAL_FOCUS_DEFAULT, a little above the centre.
TESTIMONIAL_FOCUS_DEFAULT = "50% 35%"
TESTIMONIAL_FOCUS = {
    "amber-james": "50% 8%", "shakira-greg": "50% 0%", "rowanne-ben": "50% 0%", "annabelle-michael": "50% 0%",
    "jess-james": "50% 8%", "aklema": "50% 8%", "kayleigh-cj": "50% 0%", "emma-matt": "50% 5%", "helaina-jake": "50% 0%",
    "savannah-james": "50% 18%", "izzie-tom": "50% 18%", "sophie-jamie": "50% 18%", "emma-will": "50% 18%",
    "ian-aysa": "50% 18%", "aimee-adam": "50% 25%", "beth-jack": "50% 25%", "aida-phillip": "50% 25%",
    "becky-dan": "50% 45%",
}


def seo_title(name, collection):
    """Keep titles to about 60 characters so Google shows them in full."""
    for t in (f"{name} | {collection} Hire | Winterborne", f"{name} Hire | Winterborne", name):
        if len(t) <= 60:
            return t
    return name[:60].rsplit(" ", 1)[0]


def seo_description(description_html, name):
    """A 70-160 character meta description: the product text, cut at a word, or padded with where to hire it."""
    plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", description_html))).strip()
    if len(plain) > 155:
        cut = plain[:155]
        stop = max(cut.rfind(". "), cut.rfind("! "))
        plain = cut[:stop + 1] if stop >= 80 else cut.rsplit(" ", 1)[0].rstrip(",;:-") + "..."
    if not plain:
        plain = f"{name}, available to hire for weddings in Dorset."
    if len(plain) < 70:
        plain = plain.rstrip(".") + ". Available to hire for weddings and events in Dorset from Winterborne Hire & Styling."
    return plain


def testimonials():
    path = "our-testimonials.html"
    s = read(path)
    cards = []
    for t in DATA["testimonials"]:
        img = sized(t["image"], "(max-width: 767px) 100vw, 400px")
        # venue only: the dates aren't shown
        meta = f'\n            <p class="kw-meta">{e(t["venue"])}</p>' if t["venue"] else ""
        paras = "".join(f"<p>{e(p.strip())}</p>" for p in t["quote"].split("\n") if p.strip())
        cards.append(f'''        <li class="kw-card">
          <img {img} alt="{e(t["names"])}" loading="lazy" class="kw-photo" style="object-position: {TESTIMONIAL_FOCUS.get(t["slug"], TESTIMONIAL_FOCUS_DEFAULT)}">
          <div class="kw-text">
            <h3 class="kw-names">{e(t["names"])}</h3>{meta}
            <blockquote class="kw-quote">{paras}</blockquote>
          </div>
        </li>''')
    section = f'''<!-- kind-words:start -->
  <section class="kw" aria-labelledby="kw-title">
    <div class="kw-head">
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


# The reviews pop-up on the homepage (opened from "5.0 on Google"): a scrolling selection of reviews, then a link
# to all the Google reviews. Pick reviews by their slug in data/webflow-content.json.
HOME_REVIEWS = ["beth-jack", "katie-adam", "rhiannon-dan", "becky-dan", "pippa-james", "gen-james", "kayleigh-cj",
                "shakira-greg", "rowanne-ben", "joanna-ben"]
GOOGLE_REVIEWS_URL = "https://www.google.com/search?q=winterborne+hire+and+styling#lrd=0x487259dfa18baa05:0x82416b8c1fd52400,1,,,,"


def home_reviews():
    path = "index.html"
    s = read(path)
    by = {t["slug"]: t for t in DATA["testimonials"]}
    items = []
    for slug in HOME_REVIEWS:
        t = by[slug]
        paras = "".join(f"<p>{e(p.strip())}</p>" for p in t["quote"].split("\n") if p.strip())
        venue = f'<span class="rv-venue">{e(t["venue"])}</span>' if t["venue"] else ""
        items.append(f'''      <li class="rv-item"><span class="rv-stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
        <blockquote class="rv-quote">{paras}</blockquote>
        <p class="rv-by"><span class="rv-names">{e(t["names"])}</span>{venue}</p></li>''')
    block = f'''<!-- reviews-dialog:start -->
  <dialog class="faux-dialog rv-dialog" id="reviews-dialog" aria-labelledby="reviews-dialog-title">
    <button type="button" class="faux-dialog-close" aria-label="Close" data-close>&times;</button>
    <h2 id="reviews-dialog-title" class="rv-title"><picture class="g-rating"><source srcset="/images/google-rating-5.avif" type="image/avif"><img src="/images/google-rating-5.webp" width="258" height="70" alt="Google Rating 5.0, five stars"></picture></h2>
    <p class="rv-sub">From 101 five-star reviews. Here are a few of our favourites.</p>
    <ul class="rv-list" role="list">
{chr(10).join(items)}
    </ul>
    <a href="{GOOGLE_REVIEWS_URL}" class="hp-button" target="_blank" rel="noopener">Read all 101 on Google<span class="pd-visually-hidden"> (opens in a new tab)</span></a>
  </dialog>
  <!-- reviews-dialog:end -->'''
    if "<!-- reviews-dialog:start -->" in s:
        a = s.index("<!-- reviews-dialog:start -->")
        b = s.index("<!-- reviews-dialog:end -->") + len("<!-- reviews-dialog:end -->")
        s = s[:a] + block + s[b:]
    else:
        s = s.replace('  <dialog class="faux-dialog" id="faux-dialog"', "  " + block + "\n" + '  <dialog class="faux-dialog" id="faux-dialog"', 1)
    write(path, s)


if __name__ == "__main__":
    for col, cfg in COLLECTIONS.items():
        items = collection_items(col)
        fill_list_page(col, cfg, items)
        for item in items:
            detail_page(col, cfg, item, items)
        print(f"{col}: {len(items)} products")
    write_hire_items()
    testimonials()
    home_reviews()
    print(f"testimonials: {len(DATA['testimonials'])}")
    saved = sum(1 for k, v in DATA.items() for i in v for f in ("image", "hover")
                if i.get(f) and os.path.exists(os.path.join(ROOT, i[f]["file"])))
    total = sum(1 for k, v in DATA.items() for i in v for f in ("image", "hover") if i.get(f))
    print(f"images saved locally: {saved}/{total}")

# keep every page's social sharing image up to date
import subprocess  # noqa: E402
import sys  # noqa: E402
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo-images.py")], check=True)
