import gzip, base64, json, pathlib, sys, hashlib, os

blob = pathlib.Path("scripts/_d9.txt").read_text().strip()
if hashlib.sha256(blob.encode()).hexdigest() != "38b72fc26ed830866522490c2cb64942ed5fab929ec4486ae349fd28d3ac1110":
    sys.exit("checksum mismatch")
P = json.loads(gzip.decompress(base64.b64decode(blob)))

def must(c, m):
    if not c:
        sys.exit("FAILED: " + m)

for path, text in P["new"].items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path)

for path in P["delete"]:
    if os.path.exists(path):
        os.remove(path)
        print("removed", path)

c = pathlib.Path("assets/css/style.css")
t = c.read_text(encoding="utf-8")
must(".footer__follow {" in t, "css anchor missing")
old_start = t.find("/* --- Today: concept, word and thought")
must(old_start != -1, "old Today css block not found")
t = t[:old_start] + P["css"] + t[t.index(".footer__follow {"):]
must(".wordday__term {" in t, "new css did not land")
must(t.count("{") == t.count("}"), "css braces unbalanced")
c.write_text(t, encoding="utf-8")
print("patched assets/css/style.css")

cf = pathlib.Path("_config.yml")
t = cf.read_text(encoding="utf-8")
must("shop:" not in t, "shop keys already present")
a = "# Newsletter. Paste the form action URL"
must(a in t, "config anchor missing")
cf.write_text(t.replace(a, P["shop"] + a, 1), encoding="utf-8")
print("patched _config.yml")

ft = pathlib.Path("_includes/footer.html")
t = ft.read_text(encoding="utf-8")
if "site.shop" not in t:
    o1 = 'or site.email != "" %}{% assign has_social = true %}{% endif %}'
    must(o1 in t, "footer anchor 1 missing")
    t = t.replace(o1, 'or site.email != "" or site.shop != "" %}{% assign has_social = true %}{% endif %}', 1)
    o2 = '{% if site.email != "" %}<li><a href="mailto:{{ site.email }}">{{ site.email }}</a></li>{% endif %}'
    must(o2 in t, "footer anchor 2 missing")
    t = t.replace(o2, o2 + chr(10) + '      {% if site.shop != "" %}<li><a href="{{ site.shop }}" rel="noopener" target="_blank">{{ site.shop_label | default: "Books" }}</a></li>{% endif %}', 1)
    must(t.count("{% if") == t.count("{% endif"), "footer if/endif unbalanced")
    ft.write_text(t, encoding="utf-8")
    print("patched _includes/footer.html")

h = pathlib.Path("index.html")
t = h.read_text(encoding="utf-8")
must("{% include today.html %}" in t, "today include missing from index")
t = t.replace("{% include today.html %}" + chr(10) + chr(10), "", 1)
a = '<section class="band band--dark" id="how">'
must(a in t, "how band anchor missing")
t = t.replace(a, "{% include today.html %}" + chr(10) + chr(10) + '<section class="band" id="how">', 1)
must("{% include live-band.html %}" in t, "live-band include missing")
t = t.replace("{% include live-band.html %}" + chr(10) + chr(10), "", 1)
t = t.replace("{% include live-band.html %}" + chr(10), "", 1)
must("live-band" not in t, "live-band still referenced")
marker = '<h2 class="band__heading" data-reveal>Latest writing</h2>'
must(marker in t, "latest writing anchor missing")
i = t.index('<section class="band">', t.index(marker) - 400)
t = t[:i] + "{% include news-band.html %}" + chr(10) + chr(10) + t[i:]
t = t.replace('<h2 class="band__heading" data-reveal>Questions people ask</h2>', '<h2 class="band__heading" data-reveal>About this site</h2>', 1)
must(t.count("{% if") == t.count("{% endif"), "index if/endif unbalanced")
must(t.index("{% include today.html %}") < t.index('id="how"'), "today not above how band")
h.write_text(t, encoding="utf-8")
print("patched index.html")
print("ALL OK")
