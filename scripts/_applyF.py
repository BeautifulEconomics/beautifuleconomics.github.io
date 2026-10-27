import gzip, base64, json, pathlib, sys, hashlib

blob = pathlib.Path("scripts/_dF.txt").read_text().strip()
if hashlib.sha256(blob.encode()).hexdigest() != "1631d0013ab3c0735021da6e5d4ffe52fad54000875c0989a19e3b7fe788f300":
    sys.exit("checksum mismatch")
P = json.loads(gzip.decompress(base64.b64decode(blob)))

for path, text in P["new"].items():
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", path)

r = pathlib.Path("README.md").read_text(encoding="utf-8")
if "Running Beautiful Economics" not in r:
    sys.exit("README did not land")
if "185.199" in r:
    sys.exit("old DNS README still present")
print("ALL OK")
