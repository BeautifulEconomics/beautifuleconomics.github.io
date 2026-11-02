import base64, gzip, hashlib, io, re, tarfile, yaml

TAR_SHA = "9aa8f8d6ff30245ac2b9b791a00d784f78492e2c52951cc5e180cc457236f42e"

raw = open("scripts/_dB.txt", encoding="utf-8").read()
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

# shop.yml may legitimately be empty (comments only) -> the band hides itself
items = yaml.safe_load(open("_data/shop.yml", encoding="utf-8"))
assert items is None or isinstance(items, list), "shop.yml must be a list or empty"
if items:
    for e in items:
        assert e.get("title") and e.get("status"), e
        assert e["status"] in ("planned", "writing", "editing", "ready"), e["status"]
        if e["status"] == "ready":
            assert e.get("link"), "a ready item needs a link: %s" % e["title"]
print("shop.yml OK:", 0 if items is None else len(items), "items")

page = open("shop.html", encoding="utf-8").read()
meta = yaml.safe_load(re.match(r"^---\n(.*?)\n---\n", page, re.S).group(1))
assert meta.get("permalink") == "/shop/" and meta.get("nav") == "shop", meta
assert "Nothing listed yet" not in page, "empty-state text should be gone"
assert "{% if items and items.size > 0 %}" in page, "band must be guarded"
assert page.index("{% if items and items.size > 0 %}") < page.index('data-band="bronze"'), \
    "the guard must wrap the whole band, not sit inside it"
for a, b in [("if", "endif"), ("for", "endfor"), ("case", "endcase"), ("unless", "endunless")]:
    na = len(re.findall(r"\{%-?\s*" + a + r"\b", page))
    nb = len(re.findall(r"\{%-?\s*" + b + r"\b", page))
    assert na == nb, "shop.html: %s %d/%d" % (a, na, nb)
print("shop.html OK: band guarded, liquid balanced")
print("ALL CHECKS PASSED")
