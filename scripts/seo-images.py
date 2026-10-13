#!/usr/bin/env python3
"""Sets each page's social sharing image (og:image and twitter:image), so links shared on Facebook, WhatsApp,
iMessage and so on show a picture. Run after the build scripts (both run it themselves at the end).

The image is the page's main photo: the one marked fetchpriority="high" (heroes and product photos), else the
video poster (showroom), else the first content photo, else the homepage hero. URLs are made absolute with the
domain in the page's canonical link.
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = "/images/Garden-Ceremony-Floral-Arch.jpg"
NOT_CONTENT = re.compile(r"winterborne-centred|/2\.png|/2-p-|iconfinder|badge|cwm-featured|two-souls|favicon|webclip|profile")


def larger(src):
    """Prefer the 1200px web copy over the 600px one."""
    return src.replace("-600.webp", "-1200.webp")


def main_image(html):
    m = re.search(r'<img\b[^>]*\bfetchpriority="high"[^>]*>', html)
    if m:
        src = re.search(r'\bsrc="([^"]+)"', m.group(0))
        if src:
            return larger(src.group(1))
    m = re.search(r'data-poster-url="([^"]+)"', html)
    if m:
        return m.group(1)
    body = html[html.find("</nav>"):] if "</nav>" in html else html
    for src in re.findall(r'<img\b[^>]*\bsrc="(/[^"]+)"', body):
        if not NOT_CONTENT.search(src):
            return larger(src)
    return DEFAULT


def set_meta(html, attr, value):
    tag = f'<meta content="{value}" {attr}>'
    pattern = r'<meta content="[^"]*" ' + re.escape(attr) + ">"
    if re.search(pattern, html):
        return re.sub(pattern, lambda m: tag, html, count=1)
    return html.replace("</title>", "</title>\n  " + tag, 1)


# pages whose sharing image was chosen by hand
KEEP = {os.path.join(ROOT, "index.html")}

count = 0
for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
    if "node_modules" in path or path in KEEP:
        continue
    html = open(path, encoding="utf-8").read()
    canonical = re.search(r'<link href="(https://[^/"]+)[^"]*" rel="canonical">', html)
    host = canonical.group(1) if canonical else "https://www.winterbornehireandstyling.co.uk"
    src = main_image(html)
    url = src if src.startswith("http") else host + src
    new = set_meta(set_meta(html, 'property="og:image"', url), 'name="twitter:image"', url)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        count += 1
print(f"set the sharing image on {count} pages")
