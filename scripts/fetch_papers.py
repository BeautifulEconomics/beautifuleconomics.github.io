#!/usr/bin/env python3
"""Newly published papers from the journals listed in _data/journals.yml.

Looked up through Crossref, which is free, open and needs no key. Only the
title, the authors and the DOI link are stored, and the link always opens at
the publisher's own page.

Built so it cannot break the site: a journal that fails is skipped, and if
every journal fails the previous _data/papers.yml is left untouched.
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNALS = os.path.join(ROOT, "_data", "journals.yml")
OUT = os.path.join(ROOT, "_data", "papers.yml")

ROWS = 40          # asked of each journal before filtering
MAX_ITEMS = 6      # shown on the page
TIMEOUT = 25
UA = "BeautifulEconomics/1.0 (https://beautifuleconomics.in)"

# Front matter, back matter, indexes and notices are deposited as articles but
# are not papers. They carry no authors, which is the reliable test; the title
# patterns catch the few that do.
NOT_A_PAPER = re.compile(
    r"\b(front\s*matter|back\s*matter|frontmatter|backmatter|editorial|erratum"
    r"|corrigendum|retraction|submission of manuscripts|report of the editor"
    r"|acknowledg\w* of referees|index to volume|table of contents"
    r"|announcements?|list of referees|notes? from the editor)\b",
    re.I,
)


def read_journals():
    out, cur = [], {}
    if not os.path.exists(JOURNALS):
        return out
    with open(JOURNALS, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- "):
                if cur.get("issn"):
                    out.append(cur)
                cur = {}
                line = line[2:].strip()
            if ":" in line:
                k, _, v = line.partition(":")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k in ("name", "short", "issn"):
                    cur[k] = v
    if cur.get("issn"):
        out.append(cur)
    return out


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def date_key(item):
    """A sortable date, from the finest-grained field the record offers."""
    for field in ("published", "published-online", "published-print", "issued", "created"):
        parts = (item.get(field) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            p = list(parts[0]) + [1, 1]
            try:
                return datetime(int(p[0]), int(p[1]), int(p[2]), tzinfo=timezone.utc)
            except (ValueError, TypeError):
                continue
    return None


def names(item):
    people = [a for a in (item.get("author") or []) if a.get("family")]
    if not people:
        return ""
    surnames = [a["family"].strip() for a in people]
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return "%s and %s" % (surnames[0], surnames[1])
    if len(surnames) == 3:
        return "%s, %s and %s" % tuple(surnames)
    return "%s and %d others" % (surnames[0], len(surnames) - 1)


def clean_title(raw):
    t = re.sub(r"<[^>]+>", "", raw)
    t = t.replace("&amp;", "&").replace("&quot;", '"').replace("&#39;", "'")
    return re.sub(r"\s+", " ", t).strip()


def main():
    journals = read_journals()
    if not journals:
        print("no journals listed; leaving papers.yml alone")
        return 0

    collected, ok, failed = [], [], []
    for j in journals:
        url = ("https://api.crossref.org/journals/%s/works?sort=published&order=desc&rows=%d"
               "&select=title,author,DOI,issued,published,created,type"
               % (urllib.parse.quote(j["issn"]), ROWS))
        try:
            data = fetch(url)
            items = data["message"]["items"]
        except Exception as exc:                      # noqa: BLE001 - any failure is skippable
            failed.append("%s (%s)" % (j.get("name", j["issn"]), type(exc).__name__))
            continue

        kept = 0
        for it in items:
            if it.get("type") != "journal-article":
                continue
            titles = it.get("title") or []
            if not titles:
                continue
            title = clean_title(titles[0])
            who = names(it)
            # No author means front matter, an index or a notice, not a paper.
            if not title or not who or NOT_A_PAPER.search(title):
                continue
            d = date_key(it)
            if not d:
                continue
            collected.append({
                "title": title,
                "authors": who,
                "doi": it.get("DOI", ""),
                "journal": j.get("short") or j.get("name", ""),
                "when": d,
            })
            kept += 1
        if kept:
            ok.append("%s (%d)" % (j.get("name"), kept))
        else:
            failed.append("%s (no usable records)" % j.get("name"))

    print("ok: %s" % (", ".join(ok) or "none"))
    if failed:
        print("skipped: %s" % ", ".join(failed))

    if not collected:
        print("nothing collected; previous papers.yml kept")
        return 0

    collected.sort(key=lambda p: p["when"], reverse=True)

    seen, items = set(), []
    for p in collected:
        if p["doi"] in seen:
            continue
        seen.add(p["doi"])
        items.append(p)
        if len(items) >= MAX_ITEMS:
            break

    def q(v):
        return '"%s"' % str(v).replace("\\", "").replace('"', "'")

    lines = [
        "# Written automatically by scripts/fetch_papers.py.",
        "# Do not edit by hand - the next scheduled run overwrites it.",
        "# Title, authors and DOI link only. Every link opens at the publisher.",
        "generated: %s" % q(datetime.now(timezone.utc).strftime("%Y-%m-%d")),
        "items:",
    ]
    for p in items:
        lines.append("  - title: %s" % q(p["title"]))
        lines.append("    authors: %s" % q(p["authors"]))
        lines.append("    journal: %s" % q(p["journal"]))
        lines.append("    url: %s" % q("https://doi.org/" + p["doi"]))
        lines.append("    date: %s" % q(p["when"].strftime("%Y-%m-%d")))
    lines.append("")

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("wrote %d papers" % len(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
