import pathlib, sys
p = pathlib.Path("_includes/head.html")
t = p.read_text(encoding="utf-8")
old = "<link rel=\"stylesheet\" href=\"{{ '/assets/css/style.css' | relative_url }}\">"
new = "{%- comment -%}\n  The build time is stamped onto the stylesheet address so that a design\n  change always reaches readers immediately. Without it the page can update\n  while the old stylesheet is still cached, which shows the new layout\n  unstyled for anyone who visited recently.\n{%- endcomment -%}\n<link rel=\"stylesheet\" href=\"{{ '/assets/css/style.css' | relative_url }}?v={{ site.time | date: '%s' }}\">"
if old not in t:
    sys.exit("anchor missing")
p.write_text(t.replace(old, new, 1), encoding="utf-8")
print("stamped stylesheet url")
