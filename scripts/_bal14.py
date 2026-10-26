import pathlib, sys
p = pathlib.Path("scripts/fetch_papers.py")
t = p.read_text(encoding="utf-8")
old = "    collected.sort(key=lambda p: p[\"when\"], reverse=True)\n\n    seen, items = set(), []\n    for p in collected:\n        if p[\"doi\"] in seen:\n            continue\n        seen.add(p[\"doi\"])\n        items.append(p)\n        if len(items) >= MAX_ITEMS:\n            break\n"
new = "    collected.sort(key=lambda p: p[\"when\"], reverse=True)\n\n    # Give every journal a share rather than letting the one that publishes\n    # most often fill the list. The AER appears monthly and Econometrica\n    # every other month, so a plain date sort would hide Econometrica for\n    # weeks at a time.\n    share = max(1, MAX_ITEMS // max(1, len(journals)))\n    seen, per, items = set(), {}, []\n    for p in collected:\n        if p[\"doi\"] in seen or per.get(p[\"journal\"], 0) >= share:\n            continue\n        seen.add(p[\"doi\"])\n        per[p[\"journal\"]] = per.get(p[\"journal\"], 0) + 1\n        items.append(p)\n    # If a journal had nothing to offer, fill the gap with the next newest.\n    for p in collected:\n        if len(items) >= MAX_ITEMS:\n            break\n        if p[\"doi\"] in seen:\n            continue\n        seen.add(p[\"doi\"])\n        items.append(p)\n    items.sort(key=lambda p: p[\"when\"], reverse=True)\n    items = items[:MAX_ITEMS]\n"
if old not in t:
    sys.exit("anchor missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("balanced journal shares")
