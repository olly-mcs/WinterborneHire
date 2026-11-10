#!/usr/bin/env python3
"""Sets every page's social sharing image (og:image, twitter:image), so a link shared on WhatsApp, Facebook,
iMessage, LinkedIn and so on shows the same picture: the garden ceremony floral arch (Olly, 2026-11-10).
Run after the build scripts (both run it themselves at the end). URLs are made absolute with the domain in the
page's canonical link.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE = "/images/Garden-Ceremony-Floral-Arch.jpg"
WIDTH, HEIGHT = 1536, 1024
ALT = "Garden wedding ceremony with a bespoke faux floral arch by Winterborne Hire &amp; Styling"


def set_meta(html, attr, value, after):
    """Set <meta content="value" attr>, adding it after the tag `after` (or the title) if missing."""
    tag = f'<meta content="{value}" {attr}>'
    pattern = r'<meta content="[^"]*" ' + re.escape(attr) + ">"
    if re.search(pattern, html):
        return re.sub(pattern, lambda m: tag, html, count=1)
    anchor = re.search(r'<meta content="[^"]*" ' + re.escape(after) + ">", html)
    if anchor:
        return html[:anchor.end()] + "\n  " + tag + html[anchor.end():]
    return html.replace("</title>", "</title>\n  " + tag, 1)


count = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if "node_modules" in path:
        continue
    html = open(path, encoding="utf-8").read()
    if "<head>" not in html:
        continue
    canonical = re.search(r'<link href="(https://[^/"]+)[^"]*" rel="canonical">', html)
    host = canonical.group(1) if canonical else "https://www.winterbornehireandstyling.co.uk"
    url = host + IMAGE
    new = set_meta(html, 'property="og:image"', url, 'property="og:description"')
    new = set_meta(new, 'property="og:image:width"', WIDTH, 'property="og:image"')
    new = set_meta(new, 'property="og:image:height"', HEIGHT, 'property="og:image:width"')
    new = set_meta(new, 'property="og:image:alt"', ALT, 'property="og:image:height"')
    new = set_meta(new, 'name="twitter:image"', url, 'name="twitter:description"')
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        count += 1
print(f"set the sharing image on {count} pages")
