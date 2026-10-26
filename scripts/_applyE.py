import gzip, base64, json, pathlib, sys, hashlib

blob = pathlib.Path("scripts/_dE.txt").read_text().strip()
if hashlib.sha256(blob.encode()).hexdigest() != "254e32c5ccbb5b61f60cec5d0be4630e93553c2175e1bde0f9cf4df1c91e8cc4":
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

c = pathlib.Path("assets/css/style.css")
t = c.read_text(encoding="utf-8")
for old, new in P["css"]:
    must(t.count(old) == 1, "css anchor not unique: " + old[:70])
    t = t.replace(old, new, 1)
must(t.count("{") == t.count("}"), "css braces unbalanced")
must("--grid:" in t and ".page-rules::before" in t, "grid rules missing")
must(".subscribe__kicker" in t, "kicker rule missing")
c.write_text(t, encoding="utf-8")
print("patched assets/css/style.css")

m = pathlib.Path("_includes/masthead.html").read_text(encoding="utf-8")
must(m.count("aria-current") == 5, "masthead should have 5 nav items")
cfg = pathlib.Path("_config.yml").read_text(encoding="utf-8")
must("advanced:" in cfg and "math: true" in cfg, "config missing advanced collection")
print("ALL OK")
