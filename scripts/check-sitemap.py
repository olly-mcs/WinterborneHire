#!/usr/bin/env python3
"""List the old Webflow URLs (data/webflow-sitemap.xml) that have no page or redirect on the new site."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = re.findall(r"<loc>https?://[^/<]+(/[^<]*)</loc>", open(os.path.join(ROOT, "data/webflow-sitemap.xml")).read())
redirects = set(re.findall(r'from = "([^"]+)"', open(os.path.join(ROOT, "netlify.toml")).read()))

missing = {}
for url in urls:
    path = url.strip("/")
    if not path or url in redirects:
        continue
    if os.path.exists(os.path.join(ROOT, path + ".html")) or os.path.exists(os.path.join(ROOT, path, "index.html")):
        continue
    missing.setdefault(path.split("/")[0], []).append(url)

covered = len(urls) - sum(len(v) for v in missing.values())
print(f"{covered} of {len(urls)} old URLs have a page or redirect.")
for group, items in sorted(missing.items()):
    print(f"\n{group} ({len(items)} missing)")
    for url in items:
        print("  " + url)
