import base64, gzip, hashlib, io, re, tarfile
import xml.etree.ElementTree as ET

TAR_SHA = "81cf5d0a17c7a515b92c3744aee54b0808deeb3aa7764425a7861305041689bf"

raw = open("scripts/_dY.txt", encoding="utf-8").read()
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

def front_matter(path):
    s = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", s, re.S)
    assert m, "no front matter in %s" % path
    return m.group(1), s[m.end():]

for p in ["_advanced/phillips-curve.md", "_advanced/bellman-equation.md",
          "_advanced/envelope-theorem.md", "_advanced/instrumental-variables.md"]:
    fm, body = front_matter(p)
    assert re.search(r"^title:\s*\S", fm, re.M), p
    assert re.search(r"^math:\s*true\s*$", fm, re.M), "missing math: true in %s" % p
    assert "{%" not in body and "{{" not in body, "stray Liquid in %s" % p
    for line in body.split("\n"):
        if line.strip().startswith("$$"):
            continue
        assert len(re.findall(r"(?<!\$)\$(?!\$)", line)) % 2 == 0, \
            "unbalanced inline $ in %s: %s" % (p, line[:60])
    print("ok", p)

src = open("_advanced/phillips-curve.md", encoding="utf-8").read()
svg = re.search(r"<svg.*?</svg>", src, re.S)
assert svg, "svg missing"
ET.fromstring(svg.group(0))
print("svg parses")

lay = open("_layouts/concept.html", encoding="utf-8").read()
for a, b in [("if", "endif"), ("for", "endfor"), ("unless", "endunless")]:
    na = len(re.findall(r"\{%\s*" + a + r"\b", lay))
    nb = len(re.findall(r"\{%\s*" + b + r"\b", lay))
    assert na == nb, "layout tag imbalance %s %d/%d" % (a, na, nb)
assert "page.collection == 'advanced'" in lay, "layout patch missing"
print("layout OK")
print("ALL CHECKS PASSED")
