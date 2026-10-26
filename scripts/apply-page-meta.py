#!/usr/bin/env python3
"""Sets every page's <title> and meta description (plus the matching og: and twitter: tags) from data/page-meta.json,
the titles and descriptions signed off for the site. Run last: the build scripts call it, so it wins over any
title or description a build script writes.

To change a page's title or description, edit data/page-meta.json (keys are page paths without .html, e.g.
"table-decor/coloured-napkins"), then run:  python3 scripts/apply-page-meta.py
A page that isn't listed keeps whatever its build script gives it.
"""
import html, json, os, re

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
