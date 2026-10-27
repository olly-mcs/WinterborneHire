#!/usr/bin/env python3
"""Adds the Google Analytics tag to every page, and sets every page's <title> and meta description (plus the matching og: and twitter: tags) from data/page-meta.json,
the titles and descriptions signed off for the site. Run last: the build scripts call it, so it wins over any
title or description a build script writes.

To change a page's title or description, edit data/page-meta.json (keys are page paths without .html, e.g.
"table-decor/coloured-napkins"), then run:  python3 scripts/apply-page-meta.py
A page that isn't listed keeps whatever its build script gives it.
"""
import html, json, os, re

# Google Analytics (GA4), first thing in every page's <head>; the old Universal Analytics tag (UA-) is removed
GA_ID = "G-962GWFVQZX"
GA_TAG = (f'  <!-- Google tag (gtag.js) -->\n'
          f'  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n'
          f'  <script>\n    window.dataLayer = window.dataLayer || [];\n    function gtag(){{dataLayer.push(arguments);}}\n'
          f"    gtag('js', new Date());\n\n    gtag('config', '{GA_ID}');\n  </script>\n")
OLD_UA = re.compile(r"[ \t]*<script type=\"text/javascript\">\(function\(i,s,o,g,r,a,m\).*?ga\('send', 'pageview'\);</script>\n")


# Keep the whole site out of search results (True) or let search engines index it (False). The matching
# X-Robots-Tag header in netlify.toml must agree: keep or remove its "Staging" block at the same time.
NOINDEX = True
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
    if GA_ID in text or "<head>" not in text:
        return text
    return text.replace("<head>\n", "<head>\n" + GA_TAG, 1)

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
        new = ensure_site_name(ensure_robots(ensure_analytics(old)))
        if new != old:
            open(path, "w", encoding="utf-8").write(new)
            tagged += 1
    if tagged:
        print(f"Google Analytics tag and robots setting (noindex {'on' if NOINDEX else 'off'}): updated {tagged} pages")
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
