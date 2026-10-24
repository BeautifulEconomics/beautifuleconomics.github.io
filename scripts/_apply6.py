import gzip, base64, json, pathlib, sys, hashlib

blob = pathlib.Path("scripts/_d6.txt").read_text().strip()
if hashlib.sha256(blob.encode()).hexdigest() != "ebe07ede623eeb0494477b19a10aed1adabc6397b52e7f59718d5ff70c223d00":
    sys.exit("checksum mismatch")
P = json.loads(gzip.decompress(base64.b64decode(blob)))

def must(c, m):
    if not c:
        sys.exit("FAILED: " + m)

for path, text in P["files"].items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path)

c = pathlib.Path("assets/css/style.css")
t = c.read_text(encoding="utf-8")
must(".footer__follow {" in t, "css anchor missing")
must(".daily {" not in t, "css already applied")
c.write_text(t.replace(".footer__follow {", P["css"] + ".footer__follow {", 1), encoding="utf-8")
print("patched assets/css/style.css")

h = pathlib.Path("index.html")
t = h.read_text(encoding="utf-8")
must("Today's concept" in t, "index anchor missing")
start = t.index("{% if site.concepts.size > 0 %}")
marker = '<h2 class="band__heading" data-reveal>Browse the concepts</h2>'
bstart = t.index('<section class="band">', t.index(marker) - 400)
must("Today's concept" in t[start:bstart], "index slice wrong")
t = t[:start] + "{% include today.html %}" + chr(10) + chr(10) + "{% if site.concepts.size > 0 %}" + chr(10) + t[bstart:]
s = t.index("<script>")
e = t.index("</script>") + len("</script>")
t = t[:s] + P["script"] + t[e:]
ifs = t.count("{% if")
ends = t.count("{% endif")
must(ifs == ends, "index if/endif unbalanced: %d/%d" % (ifs, ends))
must("today-link" not in t, "stale id left in index")
h.write_text(t, encoding="utf-8")
print("patched index.html (if/endif %d/%d)" % (ifs, ends))
