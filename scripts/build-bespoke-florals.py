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
import glob, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bespoke_products import PRODUCTS  # noqa: E402
from hire_products import SECTIONS as HIRE_SECTIONS, OVERVIEW as HIRE_HOME, OLD_FOLDERS, OLD_LIST_PAGES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = "/images/testimonials/"
e = html.escape

SECTIONS = [
    dict(slug="the-ceremony", name="The Ceremony", tag="Make your ceremony the moment everyone remembers.",
         img=("/images/bespoke-florals/the-ceremony/garden-aisle", "Couple walking back down a garden aisle lined with blue and yellow meadow florals, beneath a floral arch", "50% 55%"),
         body=["Beautiful, statement ceremony florals designed to frame your vows, your first kiss and all those photographs "
               "you’ll treasure forever.",
               "From floral pillars and moongates to grand urns, meadow-style aisle flowers and ground arrangements, we create "
               "bespoke wedding ceremony flowers designed around your venue, your colour palette and your style.",
               "Based in Dorset, we create and style ceremony florals for weddings across Dorset and the surrounding areas."],
         perfect=["Ceremony backdrops", "Aisles", "Garden ceremonies", "Photo moments"],
         types=[
             dict(slug="aisle-meadows", name="Aisle Meadows", tag="Enter and leave your ceremony surrounded by flowers.",
                  img=(T + "laura-alexandra/02-ceremony-aisle.jpg", "Outdoor ceremony aisle lined with guests and florals", "50% 60%"),
                  body=["Beautiful low level floral arrangements create a flower filled aisle, with layers of blooms, colour and plenty of movement.",
                        "Designed in your chosen colours and style to complement your venue and the overall feel of your wedding, from soft and romantic to wild and abundant.",
                        "Our faux wedding flowers combine high quality silk, artificial and real touch flowers to create natural looking floral arrangements that photograph beautifully and look fresh throughout the day.",
                        "Perfect for indoor and outdoor ceremonies, our aisle meadows can be moved afterwards so you can continue the look throughout your day. Use them around the dance floor, bar or reception space for flowers that work a little harder."],
                  perfect=["Aisles", "Outdoor ceremonies", "Photo moments", "Reception styling"]),
             dict(slug="moongates", name="Moongates", tag="A classic shape, completely your own.",
                  img=("/images/173MelDave-1-1.jpg", "Bride beneath a circular floral backdrop of rich jewel-toned blooms", "50% 30%"),
                  body=["A beautiful wedding moongate creates an instant focal point for your ceremony, entrance or reception. Choose a modern design with florals concentrated in one area, an abundant crescent, a full circle of blooms or a more foliage led look.",
                        "Our faux floral moongates are designed using high quality silk, artificial and real touch flowers, giving you the look of fresh wedding flowers without the worry of wilting or seasonal availability.",
                        "Choose a fully floral moongate for maximum impact, or our metal moongate dressed with flowers and draping in your chosen colours and style.",
                        "Perfect for wedding ceremonies, statement backdrops and those all important photographs, with florals that can be repurposed throughout your day."],
                  perfect=["Ceremonies", "Photo booths", "Photo moments", "Indoor ceremonies", "Outdoor ceremonies", "Repurposing"]),
             dict(slug="pillars", name="Pillars", tag="A statement backdrop, beautifully in bloom.",
                  img=(T + "laura-alexandra/01-floral-archway.jpg", "Floral pillars of burgundy, crimson and dusty pink framing a stone archway", "50% 45%"),
                  body=["Our floral pillars create a show-stopping backdrop for your ceremony, with two different heights giving you the option to create a classic symmetrical look or our signature broken-arch design.",
                        "Both pillars are packed full of blooms, creating a lush, abundant display that feels incredibly special from every angle. They’re one of our most popular ceremony backdrops and work beautifully for indoor and outdoor weddings.",
                        "Perfect for framing your vows, creating a stunning setting for that all-important first kiss and providing a backdrop you’ll love in your photographs for years to come.",
                        "And when the ceremony is over, your pillars can be moved and reused elsewhere on your day, from your drinks reception and wedding breakfast to a photo backdrop, making them as versatile as they are beautiful."],
                  perfect=["Repurposing", "Indoor ceremonies", "Outdoor ceremonies", "Photo booths", "Top tables", "Backdrops", "Church doors", "Outdoor arbors", "Outdoor structures"]),
             dict(slug="urns-and-plinths", name="Urns & Plinths", tag="Elegant statement florals with a little more grandeur.",
                  img=(T + "sophie-ben/04-ceremony-kiss.jpg", "Couple kissing at the ceremony between tall pastel floral arrangements", "50% 40%"),
                  body=["Choose from elegant urns and plinths, with large or small urns to suit your venue and style. Or drape your plinths in beautiful fabric and add floral arrangements for the ultimate statement ceremony setup.",
                        "Style them in pairs or groups to create the look you’re after, from symmetrical and formal to something more relaxed and organic.",
                        "Perfect for grand country houses, historic venues and formal ceremony spaces, our designs can be styled with lush, statement blooms or softer florals for a more romantic feel.",
                        "And when the ceremony is over, they can be easily repurposed around your venue, from the entrance and drinks reception to the top table or evening backdrop."],
                  perfect=["Indoor ceremonies", "Outdoor ceremonies", "Church entrances", "Top tables", "Entrance styling", "Repurposing"]),
         ]),
    dict(slug="the-reception", name="The Reception", tag="Bring your reception to life with flowers.",
         img=("/images/bespoke-florals/the-reception/chandelier-reception", "Couple looking over a bright white reception room with chandeliers, blush and white table florals and a floral top table", "55% 55%"),
         body=["From beautiful centrepieces for your guests to a statement top table, our reception florals bring your "
               "wedding style into the heart of your celebration.",
               "Choose from delicate bud vase clusters, low floral arrangements or taller statement centrepieces, all designed "
               "in your chosen colours and floral style. Your top table can then carry those flowers through for a "
               "beautifully cohesive look.",
               "Designed to complement your ceremony flowers, our faux wedding florals create a reception that feels "
               "considered, stylish and completely yours."],
         perfect=["Long tables", "Round tables", "Top tables", "Marquees"],
         types=[
             dict(slug="bud-vases", name="Bud Vases", tag="Delicate details for beautifully styled tables.",
                  img=("/images/Table-Decor.webp", "Bud vases with bright stems along a wooden table", "50% 50%"),
                  body=["Our glass bud vases are perfect for adding colour, texture and little moments of florals throughout your reception. Each vase is filled with a single stem or small selection of blooms, creating a relaxed and effortlessly pretty table setting.",
                        "Choose from clear, pink, green, orange or teal glass to complement your wedding colours and floral style.",
                        "Perfect scattered along long tables with candles and other details, or grouped together to add extra interest around a larger centrepiece. They’re a simple way to bring your flowers right into the heart of your reception."],
                  perfect=["Long tables", "Round tables", "Top tables", "Drinks receptions", "Gift tables", "Card tables"]),
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


# The Hire Collection menu (second in the navigation, after Bespoke Florals), in the same two-column style: sections
# on the left, their products on the right. The sections and products are in scripts/hire_products.py.
HIRE_OVERVIEW = "/wedding-prop-hire-collection"


def hire_url(sec, prod=None):
    return f'/{sec["slug"]}' + (f'/{prod["slug"]}' if prod else "")


def hire_section(url):
    """The Hire Collection section a URL belongs to (its page, or one of its products), the overview, or None."""
    if not url:
        return None
    if url == HIRE_OVERVIEW:
        return HIRE_OVERVIEW
    for sec in HIRE_SECTIONS:
        if url == hire_url(sec) or url.startswith(hire_url(sec) + "/"):
            return hire_url(sec)
    return None


def hire_menu(url):
    here = hire_section(url)
    groups = []
    for sec in HIRE_SECTIONS:
        prods = "\n".join(
            f'                  <a href="{hire_url(sec, p)}" class="dropdown-link-2 w-dropdown-link bf-menu-type">{e(p["name"])}</a>'
            for p in sec["products"])
        groups.append(f'''              <div class="bf-menu-group">
                <a href="{hire_url(sec)}" class="dropdown-link-2 w-dropdown-link bf-menu-section{" w--current" if here == hire_url(sec) else ""}">{e(sec["name"])}</a>
                <div class="bf-menu-types">
{prods}
                </div>
              </div>''')
    return f'''          <div data-hover="true" data-delay="0" class="dropdown-2 w-dropdown">
            <div class="mainnavstyling w-dropdown-toggle{" w--current" if here else ""}" data-nav-href="{HIRE_OVERVIEW}">
              <div class="w-icon-dropdown-toggle"></div>
              <div class="mainnavstyling">Hire Collection</div>
            </div>
            <nav class="dropdown-list-2 w-dropdown-list bf-menu hire-menu">
              <a href="{HIRE_OVERVIEW}" class="dropdown-link-2 w-dropdown-link nav-overview-link">All hire collection</a>
''' + "\n".join(groups) + '''
            </nav>
          </div>'''


HIRE_RE = re.compile(
    r'          <div data-hover="true" data-delay="0" class="dropdown-2 w-dropdown">\n'
    r'            <div class="mainnavstyling w-dropdown-toggle(?: w--current)?"(?: data-nav-href="/wedding-prop-hire-collection")?>\n'
    r'              <div class="w-icon-dropdown-toggle"></div>\n'
    r'              <div class="mainnavstyling">(?:Hire )?Collection</div>.*?\n            </nav>\n          </div>', re.S)
FOOTER_HIRE_RE = re.compile(
    r'(<div class="heading-3 footerheader">Hire Collection</div>\n          <ul role="list" class="w-list-unstyled">\n'
    r'            <li>\n).*?(            </li>)', re.S)


def footer_hire(url):
    here = hire_section(url)
    return "".join(
        f'              <a href="{hire_url(sec)}"' + (' aria-current="page"' if url == hire_url(sec) else "")
        + f' class="footer-link{" w--current" if here == hire_url(sec) else ""}">{e(sec["name"])}</a>\n'
        for sec in HIRE_SECTIONS)


# The "UK-wide delivery: Bridal bouquets" pull tab hanging under the menu (a mock-up shop, scripts/build-shop.py).
# Set SHOP_TAB = False to take it off every page.
SHOP_TAB = True
# A little white delivery lorry drives on the left of the tab: its wheels turn as the road passes underneath
# (styles and animation in css/bespoke-florals.css)
SHOP_LORRY = ('<svg class="shop-lorry" viewBox="0 0 48 27" aria-hidden="true" focusable="false">'
              '<g class="shop-lorry-body"><rect x="2" y="3" width="26" height="14" rx="1.5"/>'
              '<path fill-rule="evenodd" d="M30 7h8.5l5 5.5V17H30z M32 9v4.5h8.6l-3.4-4.5z"/>'
              '<rect x="2" y="16.5" width="42" height="1.8" rx=".9"/></g>'
              '<g class="shop-lorry-wheel"><circle cx="10" cy="20.5" r="3.4"/><path d="M10 17.1v6.8M6.6 20.5h6.8"/></g>'
              '<g class="shop-lorry-wheel"><circle cx="36" cy="20.5" r="3.4"/><path d="M36 17.1v6.8M32.6 20.5h6.8"/></g>'
              '<path class="shop-lorry-road" d="M0 25.6h48"/></svg>')
SHOP_TAB_HTML = ('      <!-- shop-tab:start --><a href="/bridal-bouquets-delivery" class="shop-pulltab">' + SHOP_LORRY +
                 '<span class="shop-pulltab-small">UK-wide delivery</span>'
                 '<span class="shop-pulltab-big">Bridal bouquets</span></a><!-- shop-tab:end -->\n')
SHOP_TAB_RE = re.compile(r"      <!-- shop-tab:start -->.*?<!-- shop-tab:end -->\n", re.S)
SHOP_TAB_AFTER = 'class="navbar-3 w-nav">\n'


def update_shop_tab(text):
    text = SHOP_TAB_RE.sub("", text)
    if SHOP_TAB and SHOP_TAB_AFTER in text:
        text = text.replace(SHOP_TAB_AFTER, SHOP_TAB_AFTER + SHOP_TAB_HTML, 1)
    return text


def update_nav(text, current=None, url=None):
    """current: a section slug, or "overview", on the Bespoke Florals pages themselves; url: the page's address, to
    mark the current Hire Collection page. Puts Bespoke Florals first and Hire Collection second in the menu, and
    keeps the footer's Bespoke Florals column and Hire Collection list up to date."""
    b, h = NAV_RE.search(text), HIRE_RE.search(text)
    if b and h:
        pos = min(b.start(), h.start())
        spans = sorted([(b.start(), b.end()), (h.start(), h.end())], reverse=True)
        for a, z in spans:
            z = z + 1 if text[z:z + 1] == "\n" else z
            text = text[:a] + text[z:]
        text = text[:pos] + menu(current) + "\n" + hire_menu(url) + "\n" + text[pos:]
    elif b:
        text = NAV_RE.sub(lambda m: menu(current), text, count=1)
    text = FOOTER_HIRE_RE.sub(lambda m: m.group(1) + footer_hire(url) + m.group(2), text, count=1)
    return update_shop_tab(update_footer(text))


# ---------- page shell ----------
TPL = read("bespoke-florals/index.html")
HEAD = TPL[:TPL.index('  <section class="bf-hero"')]
FOOT = TPL[TPL.index('  <div class="badgesection">'):]


# The wish list panel (js/wishlist.js) on every Bespoke Florals page
WISHLIST_HEAD_AFTER = '<link href="/css/bespoke-florals.css" rel="stylesheet" type="text/css">'
WISHLIST_CSS = '\n  <link href="/css/wishlist.css" rel="stylesheet" type="text/css">'
WISHLIST_JS = ('  <script src="/js/quote-data.js" type="text/javascript"></script>\n'
               '  <script src="/js/hire-items.js" type="text/javascript"></script>\n'
               '  <script src="/js/bespoke-sections.js" type="text/javascript"></script>\n'
               '  <script src="/js/wishlist.js" type="text/javascript"></script>\n')


# The sideways slide between the overview and section pages (css/bespoke-slide.css, js/bespoke-slide.js)
# the script must be in <head> so its "pagereveal" listener is in place before the new page is first shown
SLIDE_CSS = ('\n  <link href="/css/bespoke-slide.css" rel="stylesheet" type="text/css">'
             '\n  <script src="/js/bespoke-slide.js" type="text/javascript"></script>')


def without_wishlist(text):
    """The template is the last-built overview page, so remove any wish list tags before adding them once."""
    text = re.sub(r'\n  <link href="/css/(?:wishlist|bespoke-slide)\.css"[^>]*>', "", text)
    text = text.replace('\n  <script src="/js/bespoke-slide.js" type="text/javascript"></script>', "")
    return re.sub(r'  <script src="/js/(?:quote-data|hire-items|bespoke-sections|wishlist|bespoke-slide)\.js"[^>]*></script>\n', "", text)


def meta_description(text):
    """Keep meta descriptions under about 155 characters, ending at a sentence or word."""
    if len(text) <= 155:
        return text
    cut = text[:155]
    stop = cut.rfind(". ")
    return cut[:stop + 1] if stop >= 80 else cut.rsplit(" ", 1)[0].rstrip(",;:-") + "..."


def page(title, desc, canonical, body, current, slide=False):
    s = without_wishlist(HEAD)
    s = re.sub(r"<title>.*?</title>", f"<title>{e(title)}</title>", s, count=1)
    desc = meta_description(desc)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{e(desc)}" {attr}>', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{e(title)}" {attr}>', s, count=1)
    s = re.sub(r'<link href="https://www\.winterbornehireandstyling\.co\.uk[^"]*" rel="canonical">',
               f'<link href="https://www.winterbornehireandstyling.co.uk{canonical}" rel="canonical">', s, count=1)
    s = s.replace(WISHLIST_HEAD_AFTER, WISHLIST_HEAD_AFTER + WISHLIST_CSS + (SLIDE_CSS if slide else ""), 1)
    foot = without_wishlist(FOOT).replace("</body>", WISHLIST_JS + "</body>", 1)
    return update_nav(s + body + foot, current, canonical)


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


# "Captured at a real Winterborne wedding" caption on photos with no overlay or hover effect.
# Pages (section slugs) that show it on their product block photos; add more as the test grows.
REAL_CAPTION = "Captured at a real Winterborne wedding"
# Shown on every Bespoke Florals page: section and type blocks, and product page slider photos. Not on photos with an
# overlay or hover effect (heroes, card rows, "More..." cards, section tiles), and not on photos that aren't from a
# real wedding (NOT_REAL_WEDDING: wedding fair shots).
REAL_CAPTION_PAGES = {"overview", "the-ceremony", "the-reception", "your-florals", "installations"}
NOT_REAL_WEDDING = {"urns-and-plinths/wedding-fair", "pillars/kingston-maurward", "aisle-meadows/kingston-maurward-detail"}


def is_real(src):
    return not any(src.rstrip("/").endswith("/" + n) for n in NOT_REAL_WEDDING)


def cat_image(x, src, alt, pos, real=False):
    """The block photo. fit="contain" (in bespoke_products.py) zooms out to show the whole photo, with a soft blurred
    copy of it filling the sides, for tall photos that would otherwise lose too much."""
    if real and is_real(src) and x.get("fit") != "contain":
        inner = img(src, alt, "(max-width: 767px) 100vw, 40vw", attrs=f' class="bf-real-photo" style="object-position: {pos}" loading="lazy"')
        return f'<div class="bf-cat-image bf-real">{inner}<span class="real-caption">{REAL_CAPTION}</span></div>'
    if x.get("fit") != "contain":
        return img(src, alt, "(max-width: 767px) 100vw, 40vw", attrs=f' class="bf-cat-image" style="object-position: {pos}" loading="lazy"')
    small = img_src(src, 600)[0]
    inner = img(src, alt, "(max-width: 767px) 100vw, 40vw", attrs=' class="bf-fit-photo" loading="lazy"')
    return f'<div class="bf-cat-image bf-fit" style="--bf-fit-bg: url(\'{small}\')">{inner}</div>'


def strip(i, x, id_, title_id, title, button=None, extra="", real=False):
    src, alt, pos = x["img"]
    btn = f'\n        <a href="{button[0]}" class="bf-button">{e(button[1])}</a>' if button else ""
    return f'''  <section class="bf-cat{" bf-cat-flip" if i % 2 else ""}" id="{id_}" aria-labelledby="{title_id}">
    <div class="bf-cat-main">
      {cat_image(x, src, alt, pos, real)}
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
          button=(f'/bespoke-florals/{s["slug"]}', f'Explore {s["name"].lower()}'), extra=types_row(s),
          real="overview" in REAL_CAPTION_PAGES)
    for i, s in enumerate(SECTIONS)) + '''
  </div>
''' + CTA

write("bespoke-florals/index.html", page(
    "Bespoke Wedding Florals in Dorset | Winterborne Hire & Styling",
    "Bespoke faux wedding florals in your colours: ceremony pillars and moongates, reception table florals, bouquets and "
    "installations. Designed in Dorset.", "/bespoke-florals", main_body, "overview", slide=True))

# ---------- section pages ----------
for s in SECTIONS:
    src, alt, pos = s["img"]
    body = f'''  <section class="bf-hero" aria-labelledby="bf-title">
    {img(src, alt, "(max-width: 991px) 100vw, 62vw", attrs=f' class="bf-hero-image" style="object-position: {pos}" fetchpriority="high"')}
    <div class="bf-hero-text">
      <p class="bf-crumb-line"><a href="/bespoke-florals" class="bf-crumb">Bespoke florals</a></p>
      <h1 id="bf-title" class="bf-hero-title">{e(s["name"])}</h1>
      <p class="bf-script bf-hero-script">{e(s["tag"])}</p>
      {"".join(f'<p class="bf-body">{e(p)}</p>' for p in s["body"])}
      <a href="#{s["types"][0]["slug"]}" class="bf-button bf-button-dark">See the designs</a>
    </div>
  </section>
{subnav(s["slug"])}  <div class="bf-collection">
''' + "\n".join(strip(i, t, t["slug"], f'bf-{t["slug"]}-title', t["name"], button=(purl(s, t), f'Discover {t["name"].lower()}'),
                      real=s["slug"] in REAL_CAPTION_PAGES)
                for i, t in enumerate(s["types"])) + f'''
  </div>
''' + CTA
    write(f'bespoke-florals/{s["slug"]}.html', page(f'{s["name"]} | Bespoke Wedding Florals | Winterborne', s["body"][0], f'/bespoke-florals/{s["slug"]}', body, s["slug"], slide=True))

# ---------- product pages ----------
# Questions every product page shows, after the type's own (its "faq" in bespoke_products.py).
FAQ = [
    ("Are the flowers real?", "No. Every design is made with high-quality silk and real-touch faux blooms, so it looks fresh "
     "all day and in every photo, whatever the weather."),
    ("Can you match my colours?", "Yes. Every piece is designed around your colour palette, flower preferences, venue and style."),
    ("Can I see my florals before the wedding?", "Yes. Ahead of your wedding you'll be invited back to our showroom to see "
     "your arrangements mocked up, so you know everything is perfect."),
    ("How do I book?", "Start with a consultation at our Dorchester {showroom}, where we'll talk through your colours, venue "
     "and ideas, or add the florals you love to your wish list and send it to us for a quote."),
]


# "{showroom}" in a question's answer becomes this link
SHOWROOM_LINK = ('<a href="/showroom" class="pd-faq-link" target="_blank" rel="noopener">showroom'
                 '<span class="pd-visually-hidden"> (opens in a new tab)</span></a>')


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
        + (f'<span class="real-caption">{REAL_CAPTION}</span>' if is_real(src) else "")
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


# Couples' photos for the review thumbnail: the older testimonials (data/webflow-content.json, by names) and the four
# featured couples on /our-testimonials. A review can also name its photo with photo="/images/...".
FEATURED_PHOTOS = {
    "laura & alexandra": "/images/testimonials/laura-alexandra/01-floral-archway.jpg",
    "hannah & dave": "/images/testimonials/hannah-dave/01-kiss-under-floral-arch.jpg",
    "sophie & ben": "/images/testimonials/sophie-ben/04-ceremony-kiss.jpg",
    "steph & karl": "/images/testimonials/steph-karl/04-confetti-walk.jpg",
}


def couple_photo(q):
    if q.get("photo"):
        return q["photo"]
    key = q["names"].lower().replace(" and ", " & ").strip()
    if key in FEATURED_PHOTOS:
        return FEATURED_PHOTOS[key]
    data = json.load(open(os.path.join(ROOT, "data", "webflow-content.json"), encoding="utf-8"))
    for item in data["testimonials"]:
        if item["names"].lower().replace(" and ", " & ").strip() == key and item.get("image", {}).get("file"):
            base = item["image"]["file"].replace("images/webflow/", "/images/webflow-sized/").rsplit(".", 1)[0]
            return base + "-600.webp"
    return None


def testimonial(t):
    q = t.get("testimonial", TESTIMONIAL)
    photo = None  # thumbnails switched off; couple_photo(q) finds one when wanted
    thumb = (f'<img class="pd-quote-photo" src="{photo}" alt="{e(q["names"])}" loading="lazy">' if photo else "")
    paras = "".join(f"<p>{e(p)}</p>" for p in (q["quote"] if isinstance(q["quote"], list) else [q["quote"]]))
    return f'''  <section class="pd-quote" aria-label="What our couples say">
    <figure class="pd-quote-inner">
      <span class="pd-quote-mark" aria-hidden="true">&ldquo;</span>
      <blockquote class="pd-quote-text">{paras}</blockquote>
      <figcaption class="pd-quote-by{" has-photo" if photo else ""}">{thumb}<span class="pd-quote-who"><span class="pd-quote-names">{e(q["names"])}</span><span class="pd-quote-venue">{e(q["venue"])}</span></span></figcaption>
    </figure>
    <a href="/our-testimonials" class="pd-quote-button" target="_blank" rel="noopener">View more testimonials<span class="pd-visually-hidden"> (opens in a new tab)</span></a>
  </section>
'''


def product_body(s, t):
    # no prices: drop any detail that gives one
    details = "".join(f"<div class=\"pd-detail\"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>"
                      for k, v in t["details"] if "£" not in v and k != "Price")
    faqs = "".join(
        f'<details class="pd-faq"><summary>{e(q)}</summary><p>{e(a).replace("{showroom}", SHOWROOM_LINK)}</p></details>'
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
      <p class="bf-script pd-tag">{e(t.get("page_tag", t["tag"]))}</p>
      {"".join(f'<h2 class="pd-subhead">{e(p[3:])}</h2>' if p.startswith("## ") else f'<p class="pd-body">{e(p)}</p>' for p in t["about"])}
      <div class="pd-buttons">
        <button type="button" class="ff-button ff-button-primary" data-wish-add="{t["quote"]}">Add to your wish list</button>
        <a href="/showroom" class="ff-button ff-button-outline">Book a consultation</a>
      </div>
      {perfect(dict(perfect=t.get("page_perfect", t["perfect"])))}
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
        html_ = page(f'{t["name"]} | Bespoke Wedding Florals | Winterborne', t["about"][0], purl(s, t), product_body(s, t), s["slug"])
        html_ = html_.replace(PRODUCT_CSS, PRODUCT_CSS + '\n  <link href="/css/bespoke-product.css" rel="stylesheet" type="text/css">', 1)
        html_ = html_.replace("</body>", '  <script src="/js/bespoke-gallery.js" type="text/javascript"></script>\n</body>', 1)
        write(f'bespoke-florals/{s["slug"]}/{t["slug"]}.html', html_)
        built += 1
print(f"built {built} product pages")

# ---------- hire collection ----------
# The overview (/wedding-prop-hire-collection), a page per section (/table-decor and so on) and a page per product
# (/table-decor/coloured-napkins), in the Bespoke Florals style. Data: scripts/hire_products.py.
def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("&", "and")).strip("-")


def hire_photos(spec):
    """A variant photo, plus the old product's second ("-hover") photo when there is one."""
    out = [spec]
    if spec.startswith("wf:") and not spec.endswith("-hover"):
        hover = spec + "-hover"
        if os.path.exists(os.path.join(ROOT, "images/webflow-sized", hover[3:] + "-600.webp")):
            out.append(hover)
    return out


for sec in HIRE_SECTIONS:
    for p in sec["products"]:
        p["id"] = f'hire-{sec["slug"]}-{p["slug"]}'
        p["slides"] = []
        for i, v in enumerate(p["variants"]):
            v["id"] = p["id"] if len(p["variants"]) == 1 else f'{p["id"]}--{slugify(v["name"])}'
            v["start"] = len(p["slides"]) if v["photos"] else None
            for spec in v["photos"]:
                for src in hire_photos(spec):
                    p["slides"].append((src, f'{p["name"]}: {v["name"]}' if len(p["variants"]) > 1 else p["name"], i))
        p["img"] = (p["slides"][0][0], p["slides"][0][1], "50% 50%") if p["slides"] else None

NO_PHOTO = '<div class="hc-nophoto"><span>Photos coming soon</span></div>'


def hire_card(sec, p, sizes="(max-width: 991px) 50vw, 25vw"):
    pic = (img(p["img"][0], p["img"][1], sizes, 600, f' style="object-position: {p["img"][2]}" loading="lazy"')
           if p["img"] else NO_PHOTO)
    return (f'<li class="bf-look"><a href="{hire_url(sec, p)}" class="bf-look-link">{pic}'
            f'<p class="bf-look-venue">{e(p["name"])}</p><p class="bf-look-desc">{e(p["tag"])}</p></a></li>')


def hire_subnav(current=None):
    items = "".join(
        f'<li><a href="{hire_url(s)}" class="bf-subnav-link{" is-current" if s is current else ""}"'
        + (' aria-current="page"' if s is current else "") + f'>{e(s["name"])}</a></li>'
        for s in HIRE_SECTIONS)
    return ('  <nav class="bf-subnav" aria-label="Hire collection">\n'
            f'    <ul class="bf-subnav-list" role="list">{items}</ul>\n  </nav>\n')


def hire_strip(i, x, id_, title, body, button, extra=""):
    if x["img"]:
        src, alt, pos = x["img"]
        pic = img(src, alt, "(max-width: 767px) 100vw, 50vw", attrs=f' class="bf-cat-image" style="object-position: {pos}" loading="lazy"')
    else:
        pic = NO_PHOTO.replace('class="hc-nophoto"', 'class="hc-nophoto bf-cat-image"')
    paras = "".join(f'<p class="bf-body">{e(t)}</p>' for t in body)
    return (f'  <section class="bf-cat hc-cat{" bf-cat-flip" if i % 2 else ""}" id="{id_}" aria-labelledby="{id_}-title">\n'
            f'    <div class="bf-cat-main">\n      {pic}\n      <div class="bf-cat-text">\n'
            f'        <h2 id="{id_}-title" class="bf-cat-title">{e(title)}</h2>\n'
            f'        <p class="bf-script">{e(x["tag"])}</p>\n        {paras}\n'
            f'        <a href="{button[0]}" class="bf-button">{e(button[1])}</a>\n      </div>\n    </div>{extra}\n  </section>')


def hire_hero(x, title, crumb, button):
    src, alt, pos = x["img"]
    pic = img(src, alt, "(max-width: 991px) 100vw, 62vw", attrs=f' class="bf-hero-image" style="object-position: {pos}" fetchpriority="high"')
    crumb_html = f'      <p class="bf-crumb-line"><a href="{HIRE_OVERVIEW}" class="bf-crumb">Hire collection</a></p>\n' if crumb else ""
    paras = "".join(f'<p class="bf-body">{e(t)}</p>' for t in x["body"])
    return (f'  <section class="bf-hero" aria-labelledby="bf-title">\n    {pic}\n    <div class="bf-hero-text">\n{crumb_html}'
            f'      <h1 id="bf-title" class="bf-hero-title">{e(title)}</h1>\n'
            f'      <p class="bf-script bf-hero-script">{e(x["tag"])}</p>\n      {paras}\n'
            f'      <a href="{button}" class="bf-button bf-button-dark">Explore the collection</a>\n    </div>\n  </section>\n')


HIRE_CTA = '''  <section class="ff-cta" aria-labelledby="hc-cta-title">
    <h2 id="hc-cta-title" class="ff-heading">Come and see the collection</h2>
    <p class="ff-body">Visit our Dorset showroom to see our hire pieces in person, try out ideas for your tables and venue, and put together everything you need for your day.</p>
    <a href="/showroom" class="ff-button ff-button-primary">Book a showroom visit</a>
  </section>
'''
HIRE_CSS = '\n  <link href="/css/hire-collection.css" rel="stylesheet" type="text/css">'


def hire_page(title, desc, canonical, body, product=False):
    html_ = page(title, desc, canonical, body, None).replace(WISHLIST_HEAD_AFTER, WISHLIST_HEAD_AFTER + HIRE_CSS, 1)
    if product:
        html_ = html_.replace(WISHLIST_HEAD_AFTER, WISHLIST_HEAD_AFTER + '\n  <link href="/css/bespoke-product.css" rel="stylesheet" type="text/css">', 1)
        html_ = html_.replace("</body>", '  <script src="/js/bespoke-gallery.js" type="text/javascript"></script>\n'
                              '  <script src="/js/hire-options.js" type="text/javascript"></script>\n</body>', 1)
    return html_


def hire_gallery(p):
    shots = p["slides"]
    if not shots:
        return f'<div class="pd-gallery"><div class="pd-stage">{NO_PHOTO}</div></div>'
    slides = "".join(
        f'<li class="pd-slide" aria-label="Photo {i + 1} of {len(shots)}" data-variant="{v}">'
        + img(src, alt, "(max-width: 991px) 100vw, 50vw", attrs=' fetchpriority="high"' if i == 0 else ' loading="lazy"') + "</li>"
        for i, (src, alt, v) in enumerate(shots))
    if len(shots) == 1:
        return f'<div class="pd-gallery"><div class="pd-stage"><ul class="pd-track" role="list">{slides}</ul></div></div>'
    thumbs = "".join(
        f'<li><button type="button" class="pd-thumb{" is-active" if i == 0 else ""}" data-slide="{i}" aria-label="Show photo {i + 1}"'
        + (' aria-current="true"' if i == 0 else "") + ">" + img(src, "", "120px", 600, ' loading="lazy"') + "</button></li>"
        for i, (src, alt, v) in enumerate(shots))
    return (f'<div class="pd-gallery" data-gallery>\n      <div class="pd-stage">\n'
            f'        <ul class="pd-track" role="list" tabindex="0" aria-label="{e(p["name"])} photos">{slides}</ul>\n'
            '        <button type="button" class="pd-arrow pd-prev" aria-label="Previous photo" data-prev>&#8249;</button>\n'
            '        <button type="button" class="pd-arrow pd-next" aria-label="Next photo" data-next>&#8250;</button>\n'
            f'        <p class="pd-count" aria-hidden="true"><span data-count>1</span> / {len(shots)}</p>\n      </div>\n'
            f'      <ul class="pd-thumbs" role="list">{thumbs}</ul>\n    </div>')


def hire_options(p):
    vs = p["variants"]
    if len(vs) < 2:
        return ""
    swatches = p.get("options") == "swatches"
    title = p.get("options_title", "Available styles")
    buttons = "".join(
        f'<li><button type="button" class="{"hc-swatch" if swatches else "hc-style"}" data-option data-name="{e(v["name"])}" '
        f'data-wish-id="{v["id"]}" data-slide="{"" if v["start"] is None else v["start"]}" aria-pressed="{"true" if i == 0 else "false"}">'
        + (f'<span class="hc-swatch-dot" style="background-color: {v["swatch"]}" aria-hidden="true"></span>'
           f'<span class="hc-swatch-name">{e(v["name"])}</span>' if swatches else e(v["name"]))
        + "</button></li>"
        for i, v in enumerate(vs))
    return (f'<div class="hc-options" data-options>\n'
            f'        <p class="hc-options-title">{e(title)}<span class="hc-options-current" data-option-current>{e(vs[0]["name"])}</span></p>\n'
            f'        <ul class="{"hc-swatches" if swatches else "hc-styles"}" role="list">{buttons}</ul>\n      </div>')


def hire_product_body(sec, p):
    others = [o for o in sec["products"] if o is not p]
    first = p["variants"][0]["id"]
    sections = "".join(
        f'<li><a href="{hire_url(o)}" class="pd-section">'
        + img(o["img"][0], o["img"][1], "(max-width: 767px) 100vw, 33vw", 1200, f' style="object-position: {o["img"][2]}" loading="lazy"')
        + f'<span class="pd-section-text"><span class="pd-section-name">{e(o["name"])}</span>'
        f'<span class="pd-section-types">{e(", ".join(x["name"] for x in o["products"]))}</span></span></a></li>'
        for o in HIRE_SECTIONS if o is not sec)
    paras = "".join(f'<p class="pd-body">{e(t)}</p>' for t in p["about"])
    more = ""
    if others:
        cards = "".join(hire_card(sec, o, "(max-width: 991px) 50vw, 30vw") for o in others)
        more = (f'  <section class="pd-more" aria-labelledby="pd-more-title">\n'
                f'    <h2 id="pd-more-title" class="pd-h2 pd-center">More {e(sec["name"].lower())}</h2>\n'
                f'    <ul class="bf-looks-grid bf-looks-{min(len(others), 4)} pd-more-grid" role="list">{cards}</ul>\n  </section>\n')
    return (f'  <nav class="pd-crumbs" aria-label="Breadcrumb"><a href="{HIRE_OVERVIEW}">Hire Collection</a><span aria-hidden="true">/</span>'
            f'<a href="{hire_url(sec)}">{e(sec["name"])}</a><span aria-hidden="true">/</span><span aria-current="page">{e(p["name"])}</span></nav>\n'
            f'  <section class="pd-main" aria-labelledby="pd-title">\n    {hire_gallery(p)}\n    <div class="pd-info">\n'
            f'      <h1 id="pd-title" class="pd-title">{e(p["name"])}</h1>\n'
            f'      <p class="bf-script pd-tag">{e(p["tag"])}</p>\n      {paras}\n      {hire_options(p)}\n'
            f'      <div class="pd-buttons">\n'
            f'        <button type="button" class="ff-button ff-button-primary" data-wish-add="{first}"'
            f'{" data-wish-options" if len(p["variants"]) > 1 else ""}>Add to your wish list</button>\n'
            f'        <a href="/showroom" class="ff-button ff-button-outline">Book a showroom visit</a>\n      </div>\n'
            f'    </div>\n  </section>\n' + more +
            f'  <section class="pd-sections" aria-labelledby="pd-sections-title">\n'
            f'    <h2 id="pd-sections-title" class="pd-h2 pd-center">Explore the hire collection</h2>\n'
            f'    <ul class="pd-section-list" role="list">{sections}</ul>\n  </section>\n' + HIRE_CTA)


def hire_row(sec):
    return (f'\n    <div class="bf-looks"><h3 class="bf-looks-title">In the collection</h3>'
            f'<ul class="bf-looks-grid bf-looks-{min(len(sec["products"]), 4)}" role="list">'
            + "".join(hire_card(sec, p) for p in sec["products"]) + "</ul></div>")


# overview
hire_body = hire_hero(HIRE_HOME, HIRE_HOME["title"], False, "#hc-collection") + hire_subnav() + \
    '  <div class="bf-collection" id="hc-collection">\n' + "\n".join(
        hire_strip(i, s, s["slug"], s["name"], s["body"], (hire_url(s), f'Explore {s["name"].lower()}'), extra=hire_row(s))
        for i, s in enumerate(HIRE_SECTIONS)) + "\n  </div>\n" + HIRE_CTA
write("wedding-prop-hire-collection.html", hire_page(
    "Wedding Hire Collection in Dorset | Winterborne Hire & Styling", HIRE_HOME["body"][0], HIRE_OVERVIEW, hire_body))

# sections and products
hire_built = 0
for s in HIRE_SECTIONS:
    body = hire_hero(s, s["name"], True, f'#{s["products"][0]["slug"]}') + hire_subnav(s) + \
        '  <div class="bf-collection">\n' + "\n".join(
            hire_strip(i, p, p["slug"], p["name"], p["about"][:2], (hire_url(s, p), f'Discover {p["name"].lower()}'))
            for i, p in enumerate(s["products"])) + "\n  </div>\n" + HIRE_CTA
    write(f'{s["slug"]}.html', hire_page(f'{s["name"]} Hire | Wedding Hire Collection | Winterborne', s["body"][0], hire_url(s), body))
    os.makedirs(os.path.join(ROOT, s["slug"]), exist_ok=True)
    for p in s["products"]:
        write(f'{s["slug"]}/{p["slug"]}.html', hire_page(f'{p["name"]} Hire | {s["name"]} | Winterborne', " ".join(p["about"][:2]),
                                                       hire_url(s, p), hire_product_body(s, p), product=True))
        hire_built += 1

# old product pages: removed here, and redirected (netlify.toml) to the product they were merged into, or their section
hire_redirects = []
for s in HIRE_SECTIONS:
    for p in s["products"]:
        for old in p["old"]:
            hire_redirects += [(f"{folder}/{old}", hire_url(s, p)) for folder in OLD_FOLDERS[s["slug"]]]
    for old in s.get("removed", []):
        hire_redirects += [(f"{folder}/{old}", hire_url(s)) for folder in OLD_FOLDERS[s["slug"]]]
removed_files = 0
for frm, to in hire_redirects:
    f = os.path.join(ROOT, frm.lstrip("/") + ".html")
    if os.path.exists(f):
        os.remove(f)
        removed_files += 1
for folder in ("table-decor-collection", "small-props-collection", "furniture-rugs"):
    full = os.path.join(ROOT, folder)
    if os.path.isdir(full):
        for left in glob.glob(os.path.join(full, "*.html")):  # anything left over is no longer hired
            os.remove(left)
            removed_files += 1
        os.rmdir(full)
if os.path.exists(os.path.join(ROOT, "furniture-rugs.html")):
    os.remove(os.path.join(ROOT, "furniture-rugs.html"))

REDIRECTS_START, REDIRECTS_END = "# hire-redirects:start", "# hire-redirects:end"
rules = ["# Written by scripts/build-bespoke-florals.py from scripts/hire_products.py. Don't edit by hand.\n"
         "# The hire section pages share their names with their folders of product pages, so say which file serves them."]
rules += [f'[[redirects]]\n  from = "{hire_url(s)}"\n  to = "{hire_url(s)}.html"\n  status = 200' for s in HIRE_SECTIONS]
rules += [f'[[redirects]]\n  from = "{a}"\n  to = "{b}"\n  status = 301' for a, b in OLD_LIST_PAGES.items()]
rules += [f'[[redirects]]\n  from = "{a}"\n  to = "{b}"\n  status = 301' for a, b in hire_redirects]
for folder, target in (("/table-decor-collection", "/table-decor"), ("/small-props-collection", "/small-props"),
                       ("/furniture-rugs", "/seating-areas"), ("/furniture-collection", "/seating-areas"),
                       ("/rugs-runners-collection", "/seating-areas")):
    rules.append(f'[[redirects]]\n  from = "{folder}/*"\n  to = "{target}"\n  status = 301')
toml = read("netlify.toml")
block = REDIRECTS_START + "\n" + "\n\n".join(rules) + "\n" + REDIRECTS_END
if REDIRECTS_START in toml:
    toml = toml[:toml.index(REDIRECTS_START)] + block + toml[toml.index(REDIRECTS_END) + len(REDIRECTS_END):]
else:
    toml = toml.rstrip("\n") + "\n\n" + block + "\n"
write("netlify.toml", toml)
print(f"built {len(HIRE_SECTIONS) + 1} hire collection pages and {hire_built} hire products; "
      f"{len(hire_redirects)} old product URLs redirect; removed {removed_files} old product pages")

# the hire products and their options, for the wish list (js/wishlist.js), plus the Large Props pages (hidden from
# the menu, built by scripts/build-webflow-content.py)
hire_items = []
for s in HIRE_SECTIONS:
    for p in s["products"]:
        for v in p["variants"]:
            hire_items.append(dict(id=v["id"], name=p["name"] + ("" if len(p["variants"]) == 1 else f': {v["name"]}'),
                                   section=s["name"], url=hire_url(s, p)))
_wf = json.load(open(os.path.join(ROOT, "data", "webflow-content.json"), encoding="utf-8"))
hire_items += [dict(id=f'hire-large-props-{i["slug"]}', name=i["name"].strip(), section="Large Props",
                    url=f'/large-prop-collection/{i["slug"]}') for i in _wf["large-props"]]
write("js/hire-items.js", "// Written by scripts/build-bespoke-florals.py: the hire collection products and their options, for the\n"
      "// wish list (js/wishlist.js). Don't edit by hand.\nwindow.HIRE_ITEMS = " + json.dumps(hire_items, indent=1, ensure_ascii=False) + ";\n")

# ---------- the sections and their products, for the wish list panel ----------
SECTIONS_JS = [dict(name=s["name"], url=f'/bespoke-florals/{s["slug"]}',
                    items=[dict(id=t["quote"], name=t["name"], url=purl(s, t)) for t in s["types"]]) for s in SECTIONS]
write("js/bespoke-sections.js", "// Written by scripts/build-bespoke-florals.py: the Bespoke Florals sections and their products,\n"
      "// used by js/wishlist.js (ids are the items in js/quote-data.js). Don't edit by hand.\n"
      "window.BESPOKE_SECTIONS = " + json.dumps(SECTIONS_JS, indent=2, ensure_ascii=False) + ";\n")

# ---------- the menu on every other page ----------
count = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if os.sep + "bespoke-florals" + os.sep in path:
        continue
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, ROOT)[:-5].replace(os.sep, "/")
    new = update_nav(text, url="/" + ("" if rel == "index" else rel))
    if new != text:
        open(path, "w", encoding="utf-8").write(new)
        count += 1
print(f"built {len(SECTIONS) + 1} bespoke florals pages, updated the menu on {count} pages")

# keep every page's social sharing image up to date
import subprocess  # noqa: E402
import sys  # noqa: E402
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "seo-images.py")], check=True)
