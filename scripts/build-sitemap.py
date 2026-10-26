#!/usr/bin/env python3
"""Writes sitemap.xml and robots.txt for https://www.winterbornehireandstyling.co.uk.

The sitemap lists every published page except those in SKIP (hidden or prototype pages), using each page's
canonical address. Run it after adding or removing pages:  python3 scripts/build-sitemap.py

robots.txt allows everything: while the site is staged, pages are hidden from search by their noindex tag, which
crawlers can only see if robots.txt lets them in (see CLAUDE.md, "Staging").
"""
import glob, os, re, subprocess
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.winterbornehireandstyling.co.uk"

# Not in the sitemap: the error page, mock-ups and prototypes, and pages hidden from the menu
SKIP = {"404", "bridal-bouquets-delivery", "quote-builder", "large-props"}
SKIP_FOLDERS = ("large-prop-collection/",)


def lastmod(path):
    """The date the page last changed in git, or today."""
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path], cwd=ROOT, capture_output=True, text=True).stdout
    return out.strip() or date.today().isoformat()


def priority(url):
    if url == "/":
        return "1.0"
    depth = url.strip("/").count("/")
    return "0.8" if depth == 0 else "0.6"


if __name__ == "__main__":
    entries = []
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, ROOT)
        page = rel[:-5].replace(os.sep, "/")
        if rel.startswith(("node_modules", "netlify")) or page in SKIP or page.startswith(SKIP_FOLDERS):
            continue
        text = open(path, encoding="utf-8").read()
        m = re.search(r'<link href="(https://[^"]+)" rel="canonical">', text)
        url = m.group(1) if m else SITE + "/" + ("" if page == "index" else page.replace("/index", ""))
        path_part = url[len(SITE):] or "/"
        entries.append((path_part, url, lastmod(rel)))
    entries.sort(key=lambda e: (e[0] != "/", e[0].count("/"), e[0]))
    urls = "\n".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n    <priority>{priority(p)}</priority>\n  </url>"
                     for p, u, d in entries)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "# Winterborne Hire & Styling\nUser-agent: *\nAllow: /\n\nSitemap: " + SITE + "/sitemap.xml\n")
    print(f"sitemap.xml: {len(entries)} pages; robots.txt written")
