import pathlib, sys
p = pathlib.Path("about.md")
t = p.read_text(encoding="utf-8")
old_reach = "Corrections are welcome and I would rather be told than left wrong. Write to [{{ site.email }}](mailto:{{ site.email }})."
new_reach = "{% if site.email != \"\" %}Corrections are welcome and I would rather be told than left wrong. Write to [{{ site.email }}](mailto:{{ site.email }}).\n{% elsif site.facebook != \"\" %}Corrections are welcome and I would rather be told than left wrong. Send a message on [Facebook]({{ site.facebook }}){% if site.instagram != \"\" %} or [Instagram]({{ site.instagram }}){% endif %}, and it gets fixed with the correction noted.\n{% else %}Corrections are welcome and I would rather be told than left wrong.{% endif %}"
old_list = "*Writing* — longer pieces, where an argument needs room."
new_list = "*Advanced* — the machinery underneath: models, proofs and methods, for readers who already have the basics.\n\n*Writing* — longer pieces, where an argument needs room."
if old_reach not in t:
    sys.exit("reach anchor missing")
if old_list not in t:
    sys.exit("list anchor missing")
t = t.replace(old_reach, new_reach, 1)
t = t.replace(old_list, new_list, 1)
if t.count("{% if") != t.count("{% endif"):
    sys.exit("unbalanced liquid")
p.write_text(t, encoding="utf-8")
print("about page repaired")
