import gzip, base64, json, pathlib, sys, hashlib, os

blob = pathlib.Path("scripts/_dB.txt").read_text().strip()
if hashlib.sha256(blob.encode()).hexdigest() != "318382dfe85ca39e3670db8b8e9c71c723483f8bac0d94b222ffb678868181cc":
    sys.exit("checksum mismatch")
P = json.loads(gzip.decompress(base64.b64decode(blob)))

def must(c, m):
    if not c:
        sys.exit("FAILED: " + m)

def edit(path, pairs):
    p = pathlib.Path(path)
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        must(old in t, path + ": anchor missing -> " + old[:60])
        t = t.replace(old, new, 1)
    p.write_text(t, encoding="utf-8")
    print("patched", path)

for path, text in P["new"].items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path)

for path in P["delete"]:
    if os.path.exists(path):
        os.remove(path)
        print("removed", path)

edit("assets/css/style.css", P["css"])
css = pathlib.Path("assets/css/style.css").read_text(encoding="utf-8")
must(css.count("{") == css.count("}"), "css braces unbalanced")
must(".papers__title" in css and ".page-rules" in css, "new css rules missing")

edit("_config.yml", P["config"])
edit("index.html", P["index"])
edit("_layouts/default.html", P["layout"])

idx = pathlib.Path("index.html").read_text(encoding="utf-8")
must(idx.count("{% if") == idx.count("{% endif"), "index if/endif unbalanced")
must("news-band" not in idx, "news-band still referenced")
print("ALL OK")
