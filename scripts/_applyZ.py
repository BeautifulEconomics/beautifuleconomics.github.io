import base64, gzip, hashlib, io, json, os, re, tarfile

TAR_SHA = "9d2a83b101cafb43b02e92a585edb7adeb522749524e5aa448993f24b3ea104a"
CSS_SHA = "d6cd3f3e1ad981fb4759bf031d5ecc2b99aa0ff32ca0f28f6269939cb8556dad"

raw = open("scripts/_dZ.txt", encoding="utf-8").read()
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

# --- style.css: apply the recorded insertions, then prove the result ---
patches = json.load(open("_cssp.json", encoding="utf-8"))
css = open("assets/css/style.css", encoding="utf-8").read()
for i, p in enumerate(patches):
    assert css.count(p["old"]) == 1, "css anchor %d not unique/found" % i
    css = css.replace(p["old"], p["new"], 1)
open("assets/css/style.css", "w", encoding="utf-8").write(css)
after = hashlib.sha256(css.encode("utf-8")).hexdigest()
assert after == CSS_SHA, "css result sha mismatch: %s" % after
print("css patched and verified byte-for-byte")
os.remove("_cssp.json")

# --- validation ---
import yaml
g = yaml.safe_load(open("_data/guides.yml", encoding="utf-8"))
assert isinstance(g, list) and g, "guides.yml empty"
for e in g:
    assert e.get("title") and e.get("status"), e
    assert e["status"] in ("planned", "writing", "editing", "ready"), e["status"]
    if e["status"] == "ready":
        assert e.get("link"), "a ready guide needs a link: %s" % e["title"]
print("guides.yml OK:", len(g), "entries")

page = open("study-guides.html", encoding="utf-8").read()
fm = re.match(r"^---\n(.*?)\n---\n", page, re.S)
assert fm, "no front matter"
meta = yaml.safe_load(fm.group(1))
assert meta.get("permalink") == "/study-guides/" and meta.get("nav") == "guides", meta
for f in ["study-guides.html", "_includes/masthead.html", "_includes/icons.html"]:
    s = open(f, encoding="utf-8").read()
    for a, b in [("if", "endif"), ("for", "endfor"), ("case", "endcase"), ("unless", "endunless")]:
        na = len(re.findall(r"\{%-?\s*" + a + r"\b", s))
        nb = len(re.findall(r"\{%-?\s*" + b + r"\b", s))
        assert na == nb, "%s: %s %d/%d" % (f, a, na, nb)
    print("liquid balanced:", f)

mast = open("_includes/masthead.html", encoding="utf-8").read()
assert "/study-guides/" in mast and "name='guides'" in mast, "nav link missing"
assert "{% when 'guides' %}" in open("_includes/icons.html", encoding="utf-8").read(), "icon missing"
print("nav + icon OK")
print("ALL CHECKS PASSED")
