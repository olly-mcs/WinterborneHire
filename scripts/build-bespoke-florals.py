#!/usr/bin/env python3
"""Builds the Bespoke Florals pages and the Bespoke Florals menu on every page.

- bespoke-florals/index.html: the overview, one numbered strip per section
- bespoke-florals/<section>.html: one page per section, one numbered strip per type (with an #anchor)
- bespoke-florals/<section>/<type>.html: a product page per type (photo slider, details, questions, the section's
  other types and the other sections); its content is in scripts/bespoke_products.py
- the "Bespoke Florals" dropdown in every page's navigation: sections on the left, their types on the right

Edit SECTIONS below (and PRODUCTS in bespoke_products.py), then run:  python3 scripts/build-bespoke-florals.py
Types are listed alphabetically wherever they appear.
"""
import glob, html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bespoke_products import PRODUCTS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = "/images/testimonials/"
e = html.escape

SECTIONS = [
    dict(slug="the-ceremony", name="The Ceremony", tag="Frame the moment you say I do.",
         img=("/images/bespoke-florals/moongates/grand-hall-aisle", "Aisle in a grand hall lined with colourful meadow florals, leading to a floral moongate", "50% 50%"),
         body=["Statement florals for your ceremony, from pillars and moongates to grand urns and meadows along the aisle.",
               "Every piece is designed in your colours and can move to the reception afterwards, so it works hard all day."],
         perfect=["Ceremony backdrops", "Aisles", "Garden ceremonies", "Photo moments"],
         types=[
             dict(slug="aisle-meadows", name="Aisle Meadows", tag="Walk to each other through a garden of blooms.",
                  img=(T + "laura-alexandra/02-ceremony-aisle.jpg", "Outdoor ceremony aisle lined with guests and florals", "50% 60%"),
                  body=["Low meadow arrangements line the aisle, so the walk to your partner feels like a stroll through a wildflower garden.",
                        "They work indoors and out, and can be moved to the edges of the dance floor or the bar later on."],
                  perfect=["Aisles", "Outdoor ceremonies", "Barn ceremonies"]),
             dict(slug="moongates", name="Moongates", tag="A classic shape, completely your own.",
                  img=("/images/173MelDave-1-1.jpg", "Bride beneath a circular floral backdrop of rich jewel-toned blooms", "50% 30%"),
                  body=["Our moongates provide the perfect framework for a stunning floral backdrop. Keep the florals concentrated for a modern look, create an abundant crescent or go for a totally foliage-led design.",
                        "Choose a fully floral moongate, or our metal moongate dressed with florals and draping in your colours."],
                  perfect=["Ceremony backdrops", "Top table backdrops", "Photo moments"]),
             dict(slug="pillars", name="Pillars", tag="A statement backdrop without a traditional arch.",
                  img=(T + "laura-alexandra/01-floral-archway.jpg", "Floral pillars of burgundy, crimson and dusty pink framing a stone archway", "50% 45%"),
                  body=["Our floral pillars are one of our most versatile pieces, kept soft and romantic, filled with colour or styled with dramatic blooms for a contemporary look.",
                        "Two pillars of different heights can also be joined into a full floral arch."],
                  perfect=["Ceremony backdrops", "Venue entrances", "Top tables"]),
             dict(slug="urns-and-plinths", name="Urns & Plinths", tag="Elegant statement florals with a little more grandeur.",
                  img=(T + "sophie-ben/04-ceremony-kiss.jpg", "Couple kissing at the ceremony between tall pastel floral arrangements", "50% 40%"),
                  body=["Large urns and plinths make an impact in grand country houses, historic venues and formal ceremony spaces, or can be styled with softer blooms for a more relaxed look.",
                        "Placed in pairs to frame your ceremony, they move easily to the top table or entrance afterwards."],
                  perfect=["Grand and historic venues", "Ceremony backdrops", "Venue entrances"]),
         ]),
    dict(slug="the-reception", name="The Reception", tag="Florals for the tables you gather around.",
         img=("/images/bespoke-florals/the-reception/chandelier-reception", "Couple looking over a bright white reception room with chandeliers, blush and white table florals and a floral top table", "55% 55%"),
         body=["Table florals that set the mood for the meal, from clusters of bud vases to tall podium arrangements and a top table that carries on from your ceremony.",
               "We design them around your tables, your venue and your colours, so the whole room feels joined up."],
         perfect=["Long tables", "Round tables", "Top tables", "Marquees"],
         types=[
             dict(slug="bud-vases", name="Bud Vases", tag="Little pops of colour, all along the table.",
                  img=("/images/Table-Decor.webp", "Bud vases with bright stems along a wooden table", "50% 50%"),
                  body=["Clusters of glass bud vases with single stems, in clear, pink, green, orange or teal glass.",
                        "Mix them with candles down long tables, or group them around a larger centrepiece."],
                  perfect=["Long tables", "Relaxed receptions", "Colourful weddings"]),
             dict(slug="footed-bowls", name="Footed Bowls", tag="Low, abundant and easy to talk over.",
                  img=("/images/Winterborne-Hire-Styling-Table-Decor-Closeup.jpg", "Table setting with candles and soft florals", "50% 50%"),
                  body=["Low, generous arrangements in gold or white footed bowls, styled with candles for a soft glow.",
                        "They sit below eye level, so guests can see and chat across the table."],
                  perfect=["Round tables", "Long tables", "Candlelit receptions"]),
             dict(slug="podiums", name="Podiums", tag="Florals lifted above the table.",
                  img=("/images/bespoke-florals/the-reception/chandelier-reception", "Couple looking over a bright white reception room with chandeliers, blush and white table florals and a floral top table", "55% 55%"),
                  body=["Tall arrangements on gold, black or clear stands (70cm), lifting the florals above the table so they fill the room without blocking the view.",
                        "Perfect for high ceilings, marquees and grand rooms."],
                  perfect=["High ceilings", "Marquees", "Round tables"]),
             dict(slug="top-table", name="Top Table", tag="All eyes on the two of you.",
                  img=(T + "hannah-dave/02-reception-arch-and-tables.jpg", "Long reception tables with a floral arch at the top table", "50% 40%"),
                  body=["A statement centrepiece designed around your top table, from a long garland of blooms to a backdrop carried over from the ceremony.",
                        "Designed to look as good in the speeches photos as it does in the room."],
                  perfect=["Top tables", "Sweetheart tables", "Photo moments"]),
         ]),
    dict(slug="your-florals", name="Your Florals", tag="The florals you carry with you.",
         img=("/images/bespoke-florals/your-florals/bride-and-bridesmaids", "Bride walking with four bridesmaids in pale blue, all holding white, yellow and blue bouquets", "50% 45%"),
         body=["Bouquets and buttonholes designed for you and your wedding party, in the same colours and blooms as the rest of your day.",
               "Made with high-quality silk and real-touch flowers, they look fresh in every photo, whatever the weather."],
         perfect=["Brides and grooms", "Bridesmaids", "Groomsmen", "Family"],
         types=[
             dict(slug="bridal-bouquets", name="Bridal Bouquets", tag="Designed around you.",
                  img=(T + "hannah-dave/03-bridal-bouquet.jpg", "Bride holding a bright meadow bouquet", "50% 40%"),
                  body=["A bespoke bridal bouquet, from loose and wild to neat and classic, designed around your dress, your colours and your style.",
                        "Your faux bouquet won't wilt, so it looks as good at the end of the night as it did down the aisle."],
                  perfect=["Brides", "Grooms", "Elopements"]),
             dict(slug="bridesmaids-bouquets", name="Bridesmaids' Bouquets", tag="Your wedding party, all in bloom.",
                  img=(T + "hannah-dave/06-bridesmaids-bouquets.jpg", "Bridesmaids holding colourful bouquets", "50% 40%"),
                  body=["Smaller bouquets to match yours, designed to tie your wedding party together.",
                        "Choose matching designs or give each one its own colour."],
                  perfect=["Bridesmaids", "Flower girls", "Family"]),
             dict(slug="buttonholes", name="Buttonholes", tag="The finishing touch.",
                  img=(T + "hannah-dave/05-buttonhole.jpg", "Floral buttonhole on a suit lapel", "50% 40%"),
                  body=["Bespoke buttonholes made with the same blooms as your bouquet.",
                        "For the groom, the groomsmen, the parents and anyone else you'd like to include."],
                  perfect=["Grooms", "Groomsmen", "Parents"]),
         ]),
    dict(slug="installations", name="Installations", tag="Florals for every corner of your venue.",
         img=("/images/bespoke-florals/installations/autumn-arbor", "Outdoor ceremony with an oak arbor dressed in rust, burgundy and white florals, the aisle lined with meadow arrangements", "50% 50%"),
         body=["When a space calls for something different, we design it: florals hung above the tables, dressed ladders and chandeliers, and arbors made to measure.",
               "Each installation is made for your venue and installed by us, so the whole room feels considered from the ceiling down."],
         perfect=["Barns and marquees", "High ceilings", "Gazebos and pergolas", "Outdoor ceremonies"],
         types=[
             dict(slug="arbors", name="Arbors", tag="Made to measure for your venue.",
                  img=("/images/Abbotsbury-Subtropical-Gardens.webp", "Couple at a gazebo dressed with white florals", "50% 40%"),
                  body=["Florals made to measure for your venue's own arbor, pergola or gazebo.",
                        "We visit or work from photos, then design a piece that fits the structure exactly."],
                  perfect=["Garden ceremonies", "Gazebos and pergolas", "Venue arbors"]),
             dict(slug="chandeliers", name="Chandeliers", tag="Florals overhead.",
                  img=("/images/Styling.webp", "Hanging floral chandeliers above round tables in a marquee", "50% 25%"),
                  body=["3ft or 4ft hanging chandeliers dressed in foliage or custom florals, installed by us.",
                        "They fill tall spaces and draw the eye up, without taking any room on the tables."],
                  perfect=["Marquees", "Barns", "High ceilings"]),
             dict(slug="ladders", name="Ladders", tag="A canopy of blooms above the tables.",
                  img=("/images/Dorset-Wedding-Showroom.webp", "Hanging florals and foliage in the Winterborne showroom", "50% 40%"),
                  body=["3m or 4.5m ladders dressed with foliage or custom florals, hung above long tables.",
                        "A real statement in barns and marquees, and a lovely backdrop for the speeches."],
                  perfect=["Long tables", "Barns", "Marquees"]),
         ]),
]
for s in SECTIONS:
    s["types"].sort(key=lambda t: t["name"].lower())
    for t in s["types"]:
        t.update(PRODUCTS[t["slug"]])
        # the first slider photo is also the type's photo on the overview and section pages
        t["img"] = (t["gallery"][0][0], t["gallery"][0][1], t.get("focus", "50% 45%"))


def purl(s, t):
    return f'/bespoke-florals/{s["slug"]}/{t["slug"]}'


def img_src(spec, width=1200):
    """A photo as a src, plus a srcset when it has 600px and 1200px web copies: "wf:<collection>/<file>" (a Webflow
    product photo), or a path without an extension such as /images/bespoke-florals/pillars/minterne-house."""
    if spec.startswith("wf:") or not os.path.splitext(spec)[1]:
        base = "/images/webflow-sized/" + spec[3:] if spec.startswith("wf:") else spec
        for w in (600, 1200):
            if not os.path.exists(os.path.join(ROOT, base.lstrip("/") + f"-{w}.webp")):
                raise SystemExit(f"missing image {base}-{w}.webp")
        return f"{base}-{width}.webp", f"{base}-600.webp 600w, {base}-1200.webp 1200w"
    if not os.path.exists(os.path.join(ROOT, spec.lstrip("/"))):
        raise SystemExit(f"missing image {spec}")
    return spec, None


def img(spec, alt, sizes, width=1200, attrs=""):
    src, srcset = img_src(spec, width)
    ss = f' srcset="{srcset}" sizes="{sizes}"' if srcset else ""
    return f'<img src="{src}"{ss} alt="{e(alt)}"{attrs}>'

CHECK = ('<svg class="bf-check" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><circle cx="10" cy="10" r="8.5" '
         'fill="none" stroke="currentColor" stroke-width="1"/><path d="M6 10.3l2.6 2.6L14 7.6" fill="none" stroke="currentColor" '
         'stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def read(path):
    return open(os.path.join(ROOT, path), encoding="utf-8").read()


def write(path, text):
    open(os.path.join(ROOT, path), "w", encoding="utf-8").write(text)


# ---------- navigation (every page) ----------
def menu(current=None):
    groups = []
    for s in SECTIONS:
        types = "\n".join(
            f'                  <a href="{purl(s, t)}" class="dropdown-link-2 w-dropdown-link bf-menu-type">{e(t["name"])}</a>'
            for t in s["types"])
        groups.append(f'''              <div class="bf-menu-group">
                <a href="/bespoke-florals/{s["slug"]}" class="dropdown-link-2 w-dropdown-link bf-menu-section{" w--current" if s["slug"] == current else ""}">{e(s["name"])}</a>
                <div class="bf-menu-types">
{types}
                </div>
              </div>''')
    toggle_class = "mainnavstyling w-dropdown-toggle" + (" w--current" if current else "")
    return '''          <div data-hover="true" data-delay="0" class="dropdown-2 w-dropdown">
            <div class="''' + toggle_class + '''" data-nav-href="/bespoke-florals">
              <div class="w-icon-dropdown-toggle"></div>
              <div class="mainnavstyling">Bespoke Florals</div>
            </div>
            <nav class="dropdown-list-2 w-dropdown-list bf-menu">
              <a href="/bespoke-florals" class="dropdown-link-2 w-dropdown-link nav-overview-link">All bespoke florals</a>
''' + "\n".join(groups) + '''
            </nav>
          </div>'''


NAV_RE = re.compile(
    r'          <div data-hover="true" data-delay="0" class="dropdown-2 w-dropdown">\n'
    r'            <div class="mainnavstyling w-dropdown-toggle(?: w--current)?" data-nav-href="/bespoke-florals">.*?\n            </nav>\n          </div>',
    re.S)


def footer_column():
    links = "\n".join(f'              <a href="/bespoke-florals/{s["slug"]}" class="footer-link">{e(s["name"])}</a>' for s in SECTIONS)
    return f'''      <!-- bespoke-footer:start -->
      <ul role="list" class="w-list-unstyled footer-bespoke">
        <li>
          <div class="heading-3 footerheader"><a href="/bespoke-florals" class="footer-header-link">Bespoke Florals</a></div>
          <ul role="list" class="w-list-unstyled">
            <li>
{links}
            </li>
          </ul>
        </li>
      </ul>
      <!-- bespoke-footer:end -->
'''


FOOTER_RE = re.compile(r"      <!-- bespoke-footer:start -->.*?<!-- bespoke-footer:end -->\n", re.S)
FOOTER_AFTER = '      <ul id="w-node-d3e90d10-6a32-7334-83d7-bf6445119b7e-f9ed05b7"'


def update_footer(text):
    """The footer's Bespoke Florals column, first after the logo column (before "Contact us")."""
    if FOOTER_RE.search(text):
        return FOOTER_RE.sub(lambda m: footer_column(), text, count=1)
    if FOOTER_AFTER in text:
        return text.replace(FOOTER_AFTER, footer_column() + FOOTER_AFTER, 1)
    return text


def update_nav(text, current=None):
    """current: a section slug, or "overview", on the Bespoke Florals pages themselves.
    Also keeps the footer's Bespoke Florals column up to date."""
    return update_footer(NAV_RE.sub(lambda m: menu(current), text, count=1))


# ---------- page shell ----------
TPL = read("bespoke-florals/index.html")
HEAD = TPL[:TPL.index('  <section class="bf-hero"')]
FOOT = TPL[TPL.index('  <div class="badgesection">'):]


# The wish list panel (js/wishlist.js) on every Bespoke Florals page
WISHLIST_HEAD_AFTER = '<link href="/css/bespoke-florals.css" rel="stylesheet" type="text/css">'
WISHLIST_CSS = '\n  <link href="/css/wishlist.css" rel="stylesheet" type="text/css">'
WISHLIST_JS = ('  <script src="/js/quote-data.js" type="text/javascript"></script>\n'
               '  <script src="/js/wishlist.js" type="text/javascript"></script>\n')


def page(title, desc, canonical, body, current):
    s = HEAD
    s = re.sub(r"<title>.*?</title>", f"<title>{e(title)} | Winterborne Hire &amp; Styling</title>", s, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{e(desc)}" {attr}>', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{e(title)}" {attr}>', s, count=1)
    s = re.sub(r'<link href="https://www\.winterbornehireandstyling\.co\.uk[^"]*" rel="canonical">',
               f'<link href="https://www.winterbornehireandstyling.co.uk{canonical}" rel="canonical">', s, count=1)
    s = s.replace(WISHLIST_HEAD_AFTER, WISHLIST_HEAD_AFTER + WISHLIST_CSS, 1)
    foot = FOOT.replace("</body>", WISHLIST_JS + "</body>", 1)
    return update_nav(s + body + foot, current)


def subnav(current=None):
    items = "".join(
        f'<li><a href="/bespoke-florals/{s["slug"]}" class="bf-subnav-link{" is-current" if s["slug"] == current else ""}"'
        + (' aria-current="page"' if s["slug"] == current else "") + f'>{e(s["name"])}</a></li>'
        for s in SECTIONS)
    return f'''  <nav class="bf-subnav" aria-label="Bespoke florals">
    <ul class="bf-subnav-list" role="list">{items}</ul>
  </nav>
'''


def perfect(x):
    return ('<div class="bf-perfect"><p class="bf-perfect-title">Perfect for</p><ul role="list">'
            + "".join(f"<li>{CHECK}<span>{e(p)}</span></li>" for p in x["perfect"]) + "</ul></div>")


def strip(i, x, id_, title_id, title, button=None, extra=""):
    src, alt, pos = x["img"]
    btn = f'\n        <a href="{button[0]}" class="bf-button">{e(button[1])}</a>' if button else ""
    return f'''  <section class="bf-cat{" bf-cat-flip" if i % 2 else ""}" id="{id_}" aria-labelledby="{title_id}">
    <div class="bf-cat-main">
      {img(src, alt, "(max-width: 767px) 100vw, 40vw", attrs=f' class="bf-cat-image" style="object-position: {pos}" loading="lazy"')}
      <div class="bf-cat-text">
        <h2 id="{title_id}" class="bf-cat-title">{e(title)}</h2>
        <p class="bf-script">{e(x["tag"])}</p>
        {"".join(f'<p class="bf-body">{e(p)}</p>' for p in x["body"])}{btn}
      </div>
      {perfect(x)}
    </div>{extra}
  </section>'''


def types_row(s):
    cards = "".join(
        f'<li class="bf-look"><a href="{purl(s, t)}" class="bf-look-link">'
        + img(t["img"][0], t["img"][1], "(max-width: 991px) 50vw, 25vw", 600, f' style="object-position: {t["img"][2]}" loading="lazy"')
        + f'<p class="bf-look-venue">{e(t["name"])}</p><p class="bf-look-desc">{e(t["tag"])}</p></a></li>'
        for t in s["types"])
    return (f'\n    <div class="bf-looks"><h3 class="bf-looks-title">Our designs</h3>'
            f'<ul class="bf-looks-grid bf-looks-{len(s["types"])}" role="list">{cards}</ul></div>')


# The closing panel on every Bespoke Florals page (overview, sections and products): the same copy everywhere
CTA = '''  <section class="ff-cta" aria-labelledby="bf-cta-title">
    <h2 id="bf-cta-title" class="ff-heading">Let&#x27;s design your florals</h2>
    <p class="ff-body">Visit our Dorset showroom to see our statement pieces in person, talk through your colours and venue, and start designing something completely yours.</p>
    <a href="/showroom" class="ff-button ff-button-primary">Book a consultation</a>
  </section>
'''

# ---------- overview ----------
main_body = f'''  <section class="bf-hero" aria-labelledby="bf-hero-title">
    <img class="bf-hero-image" src="/images/bespoke-florals/hero/gazebo-lavender-kiss-1200.webp" srcset="/images/bespoke-florals/hero/gazebo-lavender-kiss-600.webp 600w, /images/bespoke-florals/hero/gazebo-lavender-kiss-1200.webp 1200w, /images/bespoke-florals/hero/originals/gazebo-lavender-kiss.jpg 2000w" sizes="(max-width: 991px) 100vw, 62vw" alt="Couple kissing beneath a wrought iron gazebo framed by lilac, white and green floral pillars, with lavender lining the aisle" fetchpriority="high">
    <div class="bf-hero-text">
      <h1 id="bf-hero-title" class="bf-hero-title">Bespoke wedding florals</h1>
      <p class="bf-script bf-hero-script">Designed in your colours, from the aisle to the last dance.</p>
      <p class="bf-body">From the ceremony backdrop to the reception tables, your bouquet and statement installations, every piece is designed with bespoke faux florals in your chosen colours, so it works perfectly with your venue and your wedding style.</p>
      <a href="#bf-collection" class="bf-button bf-button-dark">Explore the collection</a>
    </div>
  </section>
{subnav()}  <div class="bf-collection" id="bf-collection">
''' + "\n".join(
    strip(i, s, s["slug"], f'bf-{s["slug"]}-title', s["name"],
          button=(f'/bespoke-florals/{s["slug"]}', f'Explore {s["name"].lower()}'), extra=types_row(s))
    for i, s in enumerate(SECTIONS)) + '''
  </div>
''' + CTA

write("bespoke-florals/index.html", page(
    "Bespoke Florals", "Bespoke wedding florals for the ceremony, the reception, your bouquets and statement installations, "
    "designed with faux florals in your colours. Dorset wedding florals by Winterborne.", "/bespoke-florals", main_body, "overview"))

# ---------- section pages ----------
for s in SECTIONS:
    src, alt, pos = s["img"]
    body = f'''  <section class="bf-hero" aria-labelledby="bf-title">
    {img(src, alt, "(max-width: 991px) 100vw, 62vw", attrs=f' class="bf-hero-image" style="object-position: {pos}" fetchpriority="high"')}
    <div class="bf-hero-text">
      <p class="bf-crumb-line"><a href="/bespoke-florals" class="bf-crumb">Bespoke florals</a></p>
      <h1 id="bf-title" class="bf-hero-title">{e(s["name"])}</h1>
      <p class="bf-script bf-hero-script">{e(s["tag"])}</p>
      <p class="bf-body">{e(s["body"][0])}</p>
      <a href="#{s["types"][0]["slug"]}" class="bf-button bf-button-dark">See the designs</a>
    </div>
  </section>
{subnav(s["slug"])}  <div class="bf-collection">
''' + "\n".join(strip(i, t, t["slug"], f'bf-{t["slug"]}-title', t["name"], button=(purl(s, t), f'Discover {t["name"].lower()}'))
                for i, t in enumerate(s["types"])) + f'''
  </div>
''' + CTA
    write(f'bespoke-florals/{s["slug"]}.html', page(f'{s["name"]} | Bespoke Florals', s["body"][0], f'/bespoke-florals/{s["slug"]}', body, s["slug"]))

# ---------- product pages ----------
# Questions every product page shows, after the type's own (its "faq" in bespoke_products.py).
FAQ = [
    ("Are the flowers real?", "No. Every design is made with high-quality silk and real-touch faux blooms, so it looks fresh "
     "all day and in every photo, whatever the weather."),
    ("Can you match my colours?", "Yes. Every piece is designed around your colour palette, flower preferences, venue and style."),
    ("Can I see my florals before the wedding?", "Yes. Ahead of your wedding you'll be invited back to our showroom to see "
     "your arrangements mocked up, so you know everything is perfect."),
    ("How do I book?", "Start with a consultation at our Dorchester showroom, where we'll talk through your colours, venue "
     "and ideas, or add the florals you love to your wish list and send it to us for a quote."),
]


def more_title(s):
    n = s["name"]
    if n.startswith("The "):
        return f"More for {n.lower()}"
    if n.startswith("Your "):
        return f"More of {n.lower()}"
    return f"More {n.lower()}"


def gallery(t):
    shots = t["gallery"]
    slides = "".join(
        f'<li class="pd-slide" id="pd-slide-{i + 1}" aria-label="Photo {i + 1} of {len(shots)}">'
        + img(src, alt, "(max-width: 991px) 100vw, 50vw", attrs=' fetchpriority="high"' if i == 0 else ' loading="lazy"')
        + "</li>"
        for i, (src, alt) in enumerate(shots))
    if len(shots) == 1:  # one photo: no arrows, counter or thumbnails
        return f'<div class="pd-gallery"><div class="pd-stage"><ul class="pd-track" role="list">{slides}</ul></div></div>'
    current = ' aria-current="true"'
    thumbs = "".join(
        f'<li><button type="button" class="pd-thumb{" is-active" if i == 0 else ""}" data-slide="{i}" '
        f'aria-label="Show photo {i + 1}"{current if i == 0 else ""}>'
        + img(src, "", "120px", 600, ' loading="lazy"') + "</button></li>"
        for i, (src, alt) in enumerate(shots))
    return f'''<div class="pd-gallery" data-gallery>
      <div class="pd-stage">
        <ul class="pd-track" role="list" tabindex="0" aria-label="{e(t["name"])} photos">{slides}</ul>
        <button type="button" class="pd-arrow pd-prev" aria-label="Previous photo" data-prev>&#8249;</button>
        <button type="button" class="pd-arrow pd-next" aria-label="Next photo" data-next>&#8250;</button>
        <p class="pd-count" aria-hidden="true"><span data-count>1</span> / {len(shots)}</p>
      </div>
      <ul class="pd-thumbs" role="list">{thumbs}</ul>
    </div>'''


# Testimonial on every product page. Placeholder until real reviews are matched to each product: give a type its own
# with testimonial=dict(quote=..., names=..., venue=...) in bespoke_products.py.
TESTIMONIAL = dict(
    quote="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore "
          "magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi.",
    names="Emily & Tom",
    venue="Minterne House, Dorset",
)


def testimonial(t):
    q = t.get("testimonial", TESTIMONIAL)
    return f'''  <section class="pd-quote" aria-label="What our couples say">
    <figure class="pd-quote-inner">
      <span class="pd-quote-mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="pd-quote-text"><p>{e(q["quote"])}</p></blockquote>
      <figcaption class="pd-quote-by"><span class="pd-quote-names">{e(q["names"])}</span><span class="pd-quote-venue">{e(q["venue"])}</span></figcaption>
    </figure>
    <a href="/our-testimonials" class="pd-quote-link" target="_blank" rel="noopener">Read more kind words<span class="pd-visually-hidden"> (opens in a new tab)</span> &#8599;</a>
  </section>
'''


def product_body(s, t):
    # no prices: drop any detail that gives one
    details = "".join(f"<div class=\"pd-detail\"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>"
                      for k, v in t["details"] if "£" not in v and k != "Price")
    faqs = "".join(
        f'<details class="pd-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>'
        for q, a in t.get("faq", []) + FAQ)
    others = [o for o in s["types"] if o is not t]
    more = "".join(
        f'<li class="bf-look"><a href="{purl(s, o)}" class="bf-look-link">'
        + img(o["img"][0], o["img"][1], "(max-width: 991px) 50vw, 30vw", 600, f' style="object-position: {o["img"][2]}" loading="lazy"')
        + f'<p class="bf-look-venue">{e(o["name"])}</p><p class="bf-look-desc">{e(o["tag"])}</p></a></li>'
        for o in others)
    sections = "".join(
        f'<li><a href="/bespoke-florals/{o["slug"]}" class="pd-section">'
        + img(o["img"][0], o["img"][1], "(max-width: 767px) 100vw, 33vw", 1200, f' style="object-position: {o["img"][2]}" loading="lazy"')
        + f'<span class="pd-section-text"><span class="pd-section-name">{e(o["name"])}</span>'
        f'<span class="pd-section-types">{e(", ".join(x["name"] for x in o["types"]))}</span></span></a></li>'
        for o in SECTIONS if o is not s)
    know = ""
    if details or faqs:
        know = f'''  <section class="pd-know" aria-label="Good to know">
    <div class="pd-know-inner">
      {f'<div class="pd-know-col"><h2 class="pd-h2">Good to know</h2><dl class="pd-details">{details}</dl></div>' if details else ""}
      {f'<div class="pd-know-col"><h2 class="pd-h2">Questions</h2>{faqs}</div>' if faqs else ""}
    </div>
  </section>
'''
    more_section = f'''  <section class="pd-more" aria-labelledby="pd-more-title">
    <h2 id="pd-more-title" class="pd-h2 pd-center">{e(more_title(s))}</h2>
    <ul class="bf-looks-grid bf-looks-{len(others)} pd-more-grid" role="list">{more}</ul>
  </section>
''' if others else ""
    return f'''  <nav class="pd-crumbs" aria-label="Breadcrumb"><a href="/bespoke-florals">Bespoke Florals</a><span aria-hidden="true">/</span><a href="/bespoke-florals/{s["slug"]}">{e(s["name"])}</a><span aria-hidden="true">/</span><span aria-current="page">{e(t["name"])}</span></nav>
  <section class="pd-main" aria-labelledby="pd-title">
    {gallery(t)}
    <div class="pd-info">
      <h1 id="pd-title" class="pd-title">{e(t["name"])}</h1>
      <p class="bf-script pd-tag">{e(t["tag"])}</p>
      {"".join(f'<p class="pd-body">{e(p)}</p>' for p in t["about"])}
      <div class="pd-buttons">
        <button type="button" class="ff-button ff-button-primary" data-wish-add="{t["quote"]}">Add to your wish list</button>
        <a href="/showroom" class="ff-button ff-button-outline">Book a consultation</a>
      </div>
      {perfect(t)}
    </div>
  </section>
{testimonial(t)}{know}{more_section}  <section class="pd-sections" aria-labelledby="pd-sections-title">
    <h2 id="pd-sections-title" class="pd-h2 pd-center">Explore bespoke florals</h2>
    <ul class="pd-section-list" role="list">{sections}</ul>
  </section>
''' + CTA


PRODUCT_CSS = '<link href="/css/bespoke-florals.css" rel="stylesheet" type="text/css">'
built = 0
for s in SECTIONS:
    os.makedirs(os.path.join(ROOT, "bespoke-florals", s["slug"]), exist_ok=True)
    for t in s["types"]:
        html_ = page(f'{t["name"]} | {s["name"]} | Bespoke Florals', t["about"][0], purl(s, t), product_body(s, t), s["slug"])
        html_ = html_.replace(PRODUCT_CSS, PRODUCT_CSS + '\n  <link href="/css/bespoke-product.css" rel="stylesheet" type="text/css">', 1)
        html_ = html_.replace("</body>", '  <script src="/js/bespoke-gallery.js" type="text/javascript"></script>\n</body>', 1)
        write(f'bespoke-florals/{s["slug"]}/{t["slug"]}.html', html_)
        built += 1
print(f"built {built} product pages")

# ---------- the menu on every other page ----------
count = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if os.sep + "bespoke-florals" + os.sep in path:
        continue
    text = open(path, encoding="utf-8").read()
    new = update_nav(text)
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
        count += 1
print(f"built {len(SECTIONS) + 1} bespoke florals pages, updated the menu on {count} pages")
