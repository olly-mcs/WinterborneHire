#!/usr/bin/env python3
"""Adds the Google Analytics tag to every page, and sets every page's <title> and meta description (plus the matching og: and twitter: tags) from data/page-meta.json,
the titles and descriptions signed off for the site. Run last: the build scripts call it, so it wins over any
title or description a build script writes.

To change a page's title or description, edit data/page-meta.json (keys are page paths without .html, e.g.
"table-decor/coloured-napkins"), then run:  python3 scripts/apply-page-meta.py
A page that isn't listed keeps whatever its build script gives it.
"""
import html, json, os, re

# Google Analytics (GA4), first thing in every page's <head>; the old Universal Analytics tag (UA-) is removed.
# Google Consent Mode: analytics sets no cookies until a visitor accepts in the cookie banner (js/cookies.js), whose
# choice is kept in localStorage under COOKIE_KEY and re-applied here before the tag loads on later pages.
GA_ID = "G-962GWFVQZX"
COOKIE_KEY = "winterborne-cookies"
GA_TAG = (f'  <!-- Google tag (gtag.js): no analytics cookies until a visitor accepts (js/cookies.js) -->\n'
          f'  <script>\n    window.dataLayer = window.dataLayer || [];\n    function gtag(){{dataLayer.push(arguments);}}\n'
          f"    gtag('consent', 'default', {{analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'}});\n"
          f"    try {{ if (localStorage.getItem('{COOKIE_KEY}') === 'accepted') gtag('consent', 'update', {{analytics_storage: 'granted'}}); }} catch (e) {{}}\n"
          f"    gtag('js', new Date());\n    gtag('config', '{GA_ID}');\n  </script>\n"
          f'  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
          f'  <!-- /Google tag -->\n')
# the tag as it is now, as it was before the cookie banner, and any loader line left over, so a re-run replaces it
_GA = re.escape(GA_ID)
GA_BLOCKS = [
    re.compile(r"  <!-- Google tag \(gtag\.js\): .*?  <!-- /Google tag -->\n", re.S),
    re.compile(r"  <!-- Google tag \(gtag\.js\) -->\n  <script async src=[^\n]*</script>\n  <script>\n.*?gtag\('config', '" + _GA + r"'\);\n  </script>\n", re.S),
    re.compile(r'  <script async src="https://www\.googletagmanager\.com/gtag/js\?id=' + _GA + r'"></script>\n(  <!-- /Google tag -->\n)?'),
]
# the cookie banner's styles and script, on every page
COOKIE_CSS = '  <link href="/css/cookies.css" rel="stylesheet" type="text/css">\n'
COOKIE_JS = '  <script src="/js/cookies.js" defer></script>\n'
OLD_UA = re.compile(r"[ \t]*<script type=\"text/javascript\">\(function\(i,s,o,g,r,a,m\).*?ga\('send', 'pageview'\);</script>\n")


# Keep the whole site out of search results (True) or let search engines index it (False). The matching
# X-Robots-Tag header in netlify.toml must agree: keep or remove its "Staging" block at the same time.
NOINDEX = False
ROBOTS_TAG = '  <meta name="robots" content="noindex, nofollow">\n'


SITE_NAME_TAG = '  <meta property="og:site_name" content="Winterborne Hire &amp; Styling">\n'


def ensure_site_name(text):
    """The site's name for Google results and link previews, on every page (after the og:title tag)."""
    if 'property="og:site_name"' in text:
        return text
    m = re.search(r'[ \t]*<meta content="[^"]*" property="og:title">\n', text)
    return text[:m.end()] + SITE_NAME_TAG + text[m.end():] if m else text


def ensure_robots(text):
    text = text.replace(ROBOTS_TAG, "")
    if NOINDEX and "<head>\n" in text:
        text = text.replace("<head>\n", "<head>\n" + ROBOTS_TAG, 1)
    return text


def ensure_analytics(text):
    text = OLD_UA.sub("", text)
    if "<head>" not in text:
        return text
    for block in GA_BLOCKS:
        text = block.sub("", text)
    return text.replace("<head>\n", "<head>\n" + GA_TAG, 1)


def ensure_cookie_banner(text):
    if "</head>" not in text or "</body>" not in text:
        return text
    if COOKIE_CSS not in text:
        text = text.replace("</head>", COOKIE_CSS + "</head>", 1)
    if COOKIE_JS not in text:
        text = text.replace("</body>", COOKIE_JS + "</body>", 1)
    return text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = json.load(open(os.path.join(ROOT, "data", "page-meta.json"), encoding="utf-8"))


def apply(text, title, desc):
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    text = re.sub(r"<title>.*?</title>", lambda m: f"<title>{t}</title>", text, count=1, flags=re.S)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        text = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", lambda m: f'<meta content="{t}" {attr}>', text, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        text = re.sub(r'<meta content="[^"]*" ' + re.escape(attr) + ">", lambda m: f'<meta content="{d}" {attr}>', text, count=1)
    return text


if __name__ == "__main__":
    import glob
    tagged = 0
    for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if os.sep + "node_modules" + os.sep in path or os.sep + "netlify" + os.sep in path:
            continue
        old = open(path, encoding="utf-8").read()
        new = ensure_cookie_banner(ensure_site_name(ensure_robots(ensure_analytics(old))))
        if new != old:
            open(path, "w", encoding="utf-8").write(new)
            tagged += 1
    if tagged:
        print(f"Google Analytics tag, cookie banner and robots setting (noindex {'on' if NOINDEX else 'off'}): updated {tagged} pages")
    changed, missing = 0, []
    for page, m in META.items():
        path = os.path.join(ROOT, page + ".html")
        if not os.path.exists(path):
            missing.append(page)
            continue
        old = open(path, encoding="utf-8").read()
        new = apply(old, m["title"], m["description"])
        if new != old:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print(f"page titles and descriptions: updated {changed} pages" + (f"; not found: {', '.join(missing)}" if missing else ""))
