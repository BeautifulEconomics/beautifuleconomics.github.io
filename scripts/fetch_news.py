#!/usr/bin/env python3
"""Collect economics headlines from the feeds listed in _data/sources.yml.

Only the headline, the publisher and the link are stored. No article text is
copied, and every link points back to the publisher.

Written to be impossible to break the site with: a feed that is unreachable,
slow or malformed is skipped, and if every feed fails the previous
_data/news.yml is left exactly as it was.
"""

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "_data", "sources.yml")
OUT = os.path.join(ROOT, "_data", "news.yml")

MAX_ITEMS = 6          # shown on the page
PER_FEED = 4           # considered from any single feed
MAX_AGE_DAYS = 21      # nothing staler than this
TIMEOUT = 20
UA = "BeautifulEconomics/1.0 (+https://beautifuleconomics.in)"


def read_sources():
    """Tiny reader for the flat '- name:/feed:' list, so no PyYAML is needed."""
    out, cur = [], {}
    if not os.path.exists(SOURCES):
        return out
    with open(SOURCES, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- "):
                if cur.get("name") and cur.get("feed"):
                    out.append(cur)
                cur = {}
                line = line[2:].strip()
            if ":" in line:
                k, _, v = line.partition(":")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k in ("name", "feed"):
                    cur[k] = v
    if cur.get("name") and cur.get("feed"):
        out.append(cur)
    return out


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def clean(text):
    text = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def parse_date(raw):
    raw = raw.strip()
    try:
        d = parsedate_to_datetime(raw)
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except Exception:
        pass
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", raw)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=timezone.utc)
    return None


def entries(xml):
    """Pull <item> (RSS) or <entry> (Atom) blocks out of a feed."""
    blocks = re.findall(r"<item[\s>].*?</item>", xml, flags=re.S | re.I)
    if not blocks:
        blocks = re.findall(r"<entry[\s>].*?</entry>", xml, flags=re.S | re.I)
    out = []
    for b in blocks:
        t = re.search(r"<title[^>]*>(.*?)</title>", b, flags=re.S | re.I)
        title = clean(t.group(1)) if t else ""

        link = ""
        l = re.search(r"<link[^>]*>([^<]+)</link>", b, flags=re.S | re.I)
        if l and l.group(1).strip():
            link = l.group(1).strip()
        else:
            l = re.search(r'<link[^>]*href=["\']([^"\']+)["\']', b, flags=re.I)
            if l:
                link = l.group(1).strip()

        date = None
        for tag in ("pubDate", "published", "updated", "dc:date"):
            d = re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), b, flags=re.S | re.I)
            if d:
                date = parse_date(clean(d.group(1)))
                if date:
                    break

        link = html.unescape(link).replace("//press/", "/press/")
        if title and link.startswith("http"):
            out.append({"title": title, "url": link, "date": date})
    return out


def main():
    sources = read_sources()
    if not sources:
        print("no sources listed; leaving news.yml alone")
        return 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    collected, ok, failed = [], [], []

    for s in sources:
        try:
            found = entries(fetch(s["feed"]))
        except Exception as exc:                      # noqa: BLE001 - any failure is skippable
            failed.append("%s (%s)" % (s["name"], type(exc).__name__))
            continue
        if not found:
            failed.append("%s (no items)" % s["name"])
            continue
        ok.append(s["name"])
        kept = 0
        for e in found:
            if kept >= PER_FEED:
                break
            if e["date"] and e["date"] < cutoff:
                continue
            e["source"] = s["name"]
            collected.append(e)
            kept += 1

    print("ok: %s" % (", ".join(ok) or "none"))
    if failed:
        print("skipped: %s" % ", ".join(failed))

    if not collected:
        print("nothing collected; previous news.yml kept")
        return 0

    seen, items = set(), []
    collected.sort(key=lambda e: e["date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    for e in collected:
        key = e["url"].split("?")[0]
        if key in seen:
            continue
        seen.add(key)
        title = e["title"]
        if len(title) > 150:
            title = title[:147].rstrip() + "..."
        items.append({
            "title": title,
            "url": e["url"],
            "source": e["source"],
            "date": e["date"].strftime("%Y-%m-%d") if e["date"] else "",
        })
        if len(items) >= MAX_ITEMS:
            break

    def q(v):
        return '"%s"' % v.replace("\\", "").replace('"', "'")

    lines = [
        "# Written automatically by scripts/fetch_news.py.",
        "# Do not edit by hand - the next scheduled run overwrites it.",
        "# Headlines and links only. Every link goes to the publisher.",
        "generated: %s" % q(datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        "items:",
    ]
    for it in items:
        lines.append("  - title: %s" % q(it["title"]))
        lines.append("    url: %s" % q(it["url"]))
        lines.append("    source: %s" % q(it["source"]))
        lines.append("    date: %s" % q(it["date"]))
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("wrote %d headlines from %d sources" % (len(items), len(set(i['source'] for i in items))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
