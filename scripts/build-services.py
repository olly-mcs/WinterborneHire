#!/usr/bin/env python3
"""Builds the Our Services page, /dorset-wedding-styling ("Our Services" in the menu): the hero, a strip for each way
of working with us (Full, Partial and Self Styling), The Process (five steps) and the showroom/contact buttons.

Edit the copy below, then run:  python3 scripts/build-services.py
The page keeps its own <head>, menu and footer; this rewrites the content between the services markers.
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "dorset-wedding-styling.html")
e = html.escape

HERO = dict(
    title="Our Services",
    tag="Beautiful spaces, made simple.",
    body=["However you choose to style your wedding, we’re here to help.",
          "From full styling and setup, taking the stress away entirely, to hiring everything you need to style the venue "
          "yourself, or simply adding a few finishing touches, our services are designed to work around you.",
          "With a beautiful collection of hire items and bespoke florals, we help you create a cohesive, thoughtfully "
          "styled day from start to finish."],
    img="/images/services/castle-reception",
    alt="Round reception tables with white florals and tall candles in a grand stone hall with tall arched windows",
)

LOREM = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore "
         "magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.",
         "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
         "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]

# The small caption on photos from real weddings (the same as on the Bespoke Florals pages)
REAL_CAPTION = "Captured at a real Winterborne wedding"

# The three ways of working with us: the photo, then the title and copy (placeholder copy for now)
SERVICES = [
    dict(slug="full-styling", name="Full Styling", body=LOREM,
         img="/images/testimonials/hannah-dave/02-reception-arch-and-tables.jpg", pos="50% 50%",
         alt="Long reception tables styled with bright florals, candles and orange napkins beneath a floral arch"),
    dict(slug="partial-styling", name="Partial Styling", body=LOREM,
         img="/images/testimonials/laura-alexandra/02-ceremony-aisle.jpg", pos="50% 60%",
         alt="Outdoor ceremony aisle lined with guests and florals"),
    dict(slug="self-styling", name="Self Styling", body=LOREM,
         img="/images/hire-collection/minterne-reception-1200.webp", pos="50% 50%",
         alt="Reception tables with gold chairs and white florals, styled by the couple with hired pieces"),
]

PROCESS_INTRO = ("Every wedding is different, and that’s exactly how we like it. We’ll work with you to create a look that "
                 "feels personal, considered and completely yours.")

# Line icons for the five steps (drawn in a 48 x 48 box)
ICONS = {
    "notebook": '<rect x="13" y="8" width="24" height="32" rx="2"/><path d="M10 13h6M10 19h6M10 25h6M10 31h6"/>'
                '<path d="M19 14h12"/><path d="M25 31c-4-3-6-5-6-7.5a2.6 2.6 0 0 1 6-1.5 2.6 2.6 0 0 1 6 1.5c0 2.5-2 4.5-6 7.5z"/>',
    "sprig": '<path d="M24 42c0-10 1-20 4-30"/><path d="M25 30c-5-1-10-5-11-11 6 1 10 5 11 11z"/>'
             '<path d="M26 22c5-2 9-6 10-11-6 1-9 5-10 11z"/><circle cx="29" cy="9" r="3"/><circle cx="16" cy="14" r="2.5"/>'
             '<path d="M24 36c-4-1-8-3-10-7"/>',
    "arch": '<path d="M12 42V22a12 12 0 0 1 24 0v20"/><path d="M17 42V23a7 7 0 0 1 14 0v19"/><path d="M9 42h30"/>'
            '<circle cx="14" cy="17" r="2.5"/><circle cx="19" cy="11" r="2.5"/><circle cx="34" cy="17" r="2.5"/>'
            '<circle cx="12" cy="27" r="2"/><circle cx="36" cy="26" r="2"/>',
    "clipboard": '<rect x="12" y="10" width="24" height="31" rx="2"/><rect x="19" y="7" width="10" height="6" rx="1.5"/>'
                 '<path d="M16 20l2 2 3-4M16 27l2 2 3-4M16 34l2 2 3-4"/><path d="M24 20h8M24 27h8M24 34h8"/>',
    "glasses": '<path d="M9 14l9-3 3 9a5 5 0 0 1-9 3z"/><path d="M16 25l3 11M15 37l7-2"/>'
               '<path d="M39 14l-9-3-3 9a5 5 0 0 0 9 3z"/><path d="M32 25l-3 11M33 37l-7-2"/>'
               '<path d="M24 4v4M19 6l2 3M29 6l-2 3"/>',
}

STEPS = [
    ("notebook", "Tell us about your day", "Your venue, your plans, your colours and the look you’re dreaming of."),
    ("sprig", "Choose your style", "Explore our bespoke florals, hire collection and styling options, and decide what works for you."),
    ("arch", "Build your look", "We bring the pieces together, from statement ceremony florals and reception tables to signage and "
                                "finishing touches."),
    ("clipboard", "Finalise the details", "We refine the colours, quantities and practical details so everything is ready for "
                                          "your wedding day."),
    ("glasses", "Your wedding day", "Whether we style everything for you or you’re collecting and setting up yourself, we make "
                                    "the process simple from start to finish."),
]
# How far each step's number sits from the left on wider screens (px), so the line between them gently winds
STEP_OFFSETS = [0, 64, 24, 64, 8]

SPRIG = ('<svg class="sv-sprig" viewBox="0 0 48 48" aria-hidden="true" focusable="false">' + ICONS["sprig"] + "</svg>")
# A loose botanical line drawing for the corners of The Process
BOTANICAL = ('<svg class="sv-botanical {cls}" viewBox="0 0 200 320" aria-hidden="true" focusable="false">'
             '<path d="M110 318C104 240 96 170 70 96 60 66 46 40 30 18"/>'
             '<path d="M96 210c-28-6-50-24-60-52 30 4 52 22 60 52z"/><path d="M96 210c-20-14-36-28-46-44"/>'
             '<path d="M84 150c26-12 42-34 46-62-26 10-42 32-46 62z"/><path d="M84 150c14-18 28-36 36-52"/>'
             '<path d="M70 96c-22-2-40-14-50-32 22 0 40 12 50 32z"/>'
             '<path d="M104 262c26-4 48-20 60-44-28 2-50 18-60 44z"/><path d="M104 262c18-12 36-28 50-42"/>'
             '<g transform="translate(30 18)"><ellipse cx="0" cy="-12" rx="7" ry="12"/><ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(72)"/>'
             '<ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(144)"/><ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(216)"/>'
             '<ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(288)"/><circle r="4"/></g>'
             '<g transform="translate(130 88) scale(.7)"><ellipse cx="0" cy="-12" rx="7" ry="12"/><ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(72)"/>'
             '<ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(144)"/><ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(216)"/>'
             '<ellipse cx="0" cy="-12" rx="7" ry="12" transform="rotate(288)"/><circle r="4"/></g></svg>')


def hero():
    paras = "".join(f'<p class="bf-body">{e(p)}</p>' for p in HERO["body"])
    src = HERO["img"]
    return f'''  <section class="bf-hero sv-hero" aria-labelledby="sv-title">
    <img class="bf-hero-image" src="{src}-1200.webp" srcset="{src}-600.webp 600w, {src}-1200.webp 1200w" sizes="(max-width: 991px) 100vw, 62vw" alt="{e(HERO["alt"])}" style="object-position: 50% 72%" fetchpriority="high">
    <div class="bf-hero-text">
      <h1 id="sv-title" class="bf-hero-title">{e(HERO["title"])}</h1>
      <p class="bf-script bf-hero-script">{e(HERO["tag"])}</p>
      {paras}
      <a href="#{SERVICES[0]["slug"]}" class="bf-button bf-button-dark">Explore our services</a>
    </div>
  </section>
'''


def subnav():
    links = [(f'#{s["slug"]}', s["name"]) for s in SERVICES] + [("#the-process", "The Process")]
    items = "".join(f'<li><a href="{h}" class="bf-subnav-link">{e(n)}</a></li>' for h, n in links)
    return f'''  <nav class="bf-subnav" aria-label="Our services">
    <ul class="bf-subnav-list" role="list">{items}</ul>
  </nav>
'''


def services():
    out = []
    for s in SERVICES:
        paras = "".join(f'<p class="bf-body">{e(p)}</p>' for p in s["body"])
        out.append(f'''  <section class="bf-cat sv-cat" id="{s["slug"]}" aria-labelledby="sv-{s["slug"]}-title">
    <div class="bf-cat-main">
      <div class="bf-cat-image bf-real"><img src="{s["img"]}" alt="{e(s["alt"])}" class="bf-real-photo" style="object-position: {s["pos"]}" loading="lazy"><span class="real-caption">{REAL_CAPTION}</span></div>
      <div class="bf-cat-text">
        <h2 id="sv-{s["slug"]}-title" class="bf-cat-title">{e(s["name"])}</h2>
        {paras}
      </div>
    </div>
  </section>''')
    return '  <div class="bf-collection sv-services">\n' + "\n".join(out) + "\n  </div>\n"


def connector(a, b):
    """The gently curving line from one step's number down to the next."""
    left, width = min(a, b), max(abs(b - a), 2)
    x1, x2 = a - left, b - left
    return (f'<svg class="sv-link" style="--sv-link-left: {left}px; width: {width}px" viewBox="0 0 {width} 100" '
            f'preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<path d="M{x1} 0C{x1} 50 {x2} 50 {x2} 100" vector-effect="non-scaling-stroke"/></svg>')


def process():
    steps = []
    for n, ((icon, title, text), off) in enumerate(zip(STEPS, STEP_OFFSETS)):
        link = connector(off, STEP_OFFSETS[n + 1]) if n + 1 < len(STEPS) else ""
        steps.append(f'''      <li class="sv-step" style="--sv-offset: {off}px">
        <span class="sv-num" aria-hidden="true">{n + 1:02d}</span>{link}
        <span class="sv-icon" aria-hidden="true"><svg viewBox="0 0 48 48" focusable="false">{ICONS[icon]}</svg></span>
        <div class="sv-step-text">
          <h3 class="sv-step-title"><span class="pd-visually-hidden">Step {n + 1}: </span>{e(title)}</h3>
          <p class="sv-step-body">{e(text)}</p>
        </div>
      </li>''')
    links = '<span class="sv-dot" aria-hidden="true"></span>'.join(
        f'<a href="#{s["slug"]}" class="sv-process-link">{e(s["name"])}</a>' for s in SERVICES)
    return f'''  <section class="sv-process" id="the-process" aria-labelledby="sv-process-title">
    {BOTANICAL.format(cls="sv-botanical-top")}
    {BOTANICAL.format(cls="sv-botanical-bottom")}
    <div class="sv-process-inner">
      <div class="sv-process-head">
        <p class="sv-ornament" aria-hidden="true"><span></span>{SPRIG}<span></span></p>
        <h2 id="sv-process-title" class="sv-process-title">The Process</h2>
        <p class="sv-process-intro">{e(PROCESS_INTRO)}</p>
      </div>
      <ol class="sv-steps" role="list">
{chr(10).join(steps)}
      </ol>
      <p class="sv-process-links"><span class="sv-rule" aria-hidden="true"></span>{links}<span class="sv-rule" aria-hidden="true"></span></p>
      <div class="process-ctas sv-ctas">
        <a href="/showroom" class="ff-button ff-button-primary">Book your showroom visit</a>
        <span class="process-or">or</span>
        <a href="/contact-us" class="ff-button ff-button-outline">Tell us about your wedding</a>
      </div>
    </div>
  </section>
'''


START, END = "  <!-- services:start -->\n", "  <!-- services:end -->\n"
BF_CSS = '  <link href="/css/bespoke-florals.css" rel="stylesheet" type="text/css">\n'
CSS = ('  <link href="/css/site.css" rel="stylesheet" type="text/css">\n' + BF_CSS +
       '  <link href="/css/services.css" rel="stylesheet" type="text/css">\n')
TITLE = "Our Services: Wedding Styling &amp; Hire in Dorset | Winterborne Hire &amp; Styling"
DESC = ("Full styling and setup, styling support, or everything you need to style your venue yourself. Wedding styling, "
        "hire and bespoke florals in Dorset, designed around you.")

if __name__ == "__main__":
    s = open(PAGE, encoding="utf-8").read()
    body = START + hero() + subnav() + services() + process() + END
    if START in s:
        s = s[:s.index(START)] + body + s[s.index(END) + len(END):]
    else:  # first run: replace everything between the menu and the footer badges
        nav_end = s.index('  <div class="toplandingsection')
        s = s[:nav_end] + body + s[s.index('  <div class="badgesection">'):]
    s = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", s, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{e(DESC)}" {attr}>', s, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", f'<meta content="{TITLE}" {attr}>', s, count=1)
    # the old page's Instagram feed is gone
    s = s.replace('  <link href="/css/instagram-feed.css" rel="stylesheet" type="text/css">\n', "")
    s = s.replace('  <script src="/js/instagram-feed.js" type="text/javascript"></script>\n', "")
    if "/css/services.css" not in s:
        s = s.replace(BF_CSS, CSS, 1)
    open(PAGE, "w", encoding="utf-8").write(s)
    print("built the Our Services page")
