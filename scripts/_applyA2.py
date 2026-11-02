import base64, gzip, hashlib, io, json, os, re, tarfile

TAR_SHA = "cd2036319c4feaf9b1783aefdb261b9d4d9b2c89c22bcafcb02110d5c4673527"

raw = open("scripts/_dA2.txt", encoding="utf-8").read()
blob = gzip.decompress(base64.b64decode(re.sub(r"\s", "", raw)))
got = hashlib.sha256(blob).hexdigest()
assert got == TAR_SHA, "bundle sha mismatch: %s" % got
print("bundle sha OK")

tf = tarfile.open(fileobj=io.BytesIO(blob))
names = tf.getnames()
print("files:", names)
for n in names:
    assert not n.startswith("/") and ".." not in n, n
tf.extractall(".")

# the Guides page is replaced by the Shop page; its data file moves too
if os.path.exists("_data/guides.yml"):
    os.remove("_data/guides.yml")
    print("removed _data/guides.yml")

# --- patch style.css and _config.yml, then prove each result ---
patches = json.load(open("_p2.json", encoding="utf-8"))
for key, path in [("css", "assets/css/style.css"), ("cfg", "_config.yml")]:
    spec = patches[key]
    text = open(path, encoding="utf-8").read()
    for i, p in enumerate(spec["patches"]):
        assert text.count(p["old"]) == 1, "%s anchor %d not unique/found" % (path, i)
        text = text.replace(p["old"], p["new"], 1)
    open(path, "w", encoding="utf-8").write(text)
    after = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert after == spec["sha"], "%s result sha mismatch: %s" % (path, after)
    print("patched and verified byte-for-byte:", path)
os.remove("_p2.json")

# --- validation ---
import yaml
items = yaml.safe_load(open("_data/shop.yml", encoding="utf-8"))
assert isinstance(items, list) and items, "shop.yml empty"
for e in items:
    assert e.get("title") and e.get("status"), e
    assert e["status"] in ("planned", "writing", "editing", "ready"), e["status"]
    if e["status"] == "ready":
        assert e.get("link"), "a ready item needs a link: %s" % e["title"]
print("shop.yml OK:", len(items), "items")

meta = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n",
        open("shop.html", encoding="utf-8").read(), re.S).group(1))
assert meta.get("permalink") == "/shop/" and meta.get("nav") == "shop", meta
red = open("study-guides.html", encoding="utf-8").read()
assert "/shop/" in red and "noindex" in red, "redirect page wrong"

for f in ["shop.html", "study-guides.html", "_includes/masthead.html", "_includes/icons.html"]:
    s = open(f, encoding="utf-8").read()
    for a, b in [("if", "endif"), ("for", "endfor"), ("case", "endcase"), ("unless", "endunless")]:
        na = len(re.findall(r"\{%-?\s*" + a + r"\b", s))
        nb = len(re.findall(r"\{%-?\s*" + b + r"\b", s))
        assert na == nb, "%s: %s %d/%d" % (f, a, na, nb)
    print("liquid balanced:", f)

mast = open("_includes/masthead.html", encoding="utf-8").read()
assert "/shop/" in mast and "name='shop'" in mast and "guides" not in mast, "nav wrong"
icons = open("_includes/icons.html", encoding="utf-8").read()
assert "{% when 'shop' %}" in icons and "'guides'" not in icons, "icon wrong"
css = open("assets/css/style.css", encoding="utf-8").read()
assert 'data-section="shop"' in css and 'data-section="guides"' not in css, "css section wrong"
cfg = open("_config.yml", encoding="utf-8").read()
assert 'shop_label: "Shop"' in cfg, "config label wrong"
print("nav + icon + css + config OK")
print("ALL CHECKS PASSED")
