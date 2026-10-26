import pathlib, re, sys
files = ["index.html", "library.html", "concepts.html", "_layouts/concept.html", "_layouts/post.html"]
guard = "{% if site.newsletter_action != \"\" %}\n"
tail = "</section>\n{% endif %}"
for f in files:
    p = pathlib.Path(f)
    t = p.read_text(encoding="utf-8")
    if guard not in t:
        print("already ungated", f)
        continue
    i = t.index(guard)
    j = t.index(tail, i)
    t = t[:i] + t[i + len(guard):j + len("</section>")] + t[j + len(tail):]
    ifs = t.count("{% if") + t.count("{%- if")
    ends = t.count("{% endif") + t.count("{%- endif")
    if ifs != ends:
        sys.exit("unbalanced in " + f)
    if "newsletter_action" in t:
        sys.exit("guard left in " + f)
    p.write_text(t, encoding="utf-8")
    print("ungated", f)
print("ALL OK")
