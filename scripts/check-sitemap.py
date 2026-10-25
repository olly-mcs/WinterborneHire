#!/usr/bin/env python3
"""List the old Webflow URLs (data/webflow-sitemap.xml) that have no page or redirect on the new site."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
urls = re.findall(r"<loc>https?://[^/<]+(/[^<]*)</loc>", open(os.path.join(ROOT, "data/webflow-sitemap.xml")).read())
toml = open(os.path.join(ROOT, "netlify.toml")).read()
redirects = set(re.findall(r'from = "([^"]+)"', toml))
# wildcard redirects such as /furniture-collection/* -> /furniture-rugs/:splat, which only count when the target exists
splats = re.findall(r'from = "([^"]+)/\*"\s*\n\s*to = "([^"]+)"', toml)


def exists(path):
    path = path.strip("/")
    return os.path.exists(os.path.join(ROOT, path + ".html")) or os.path.exists(os.path.join(ROOT, path, "index.html"))


def splat_ok(url):
    for prefix, to in splats:
        if url.startswith(prefix + "/"):
            target = to.replace(":splat", url[len(prefix) + 1:])
            return exists(target) or target.rstrip("/") in redirects
    return False


missing = {}
for url in urls:
    path = url.strip("/")
    if not path or url in redirects or exists(path) or splat_ok(url):
        continue
    missing.setdefault(path.split("/")[0], []).append(url)

covered = len(urls) - sum(len(v) for v in missing.values())
print(f"{covered} of {len(urls)} old URLs have a page or redirect.")
for group, items in sorted(missing.items()):
    print(f"\n{group} ({len(items)} missing)")
    for url in items:
        print("  " + url)
