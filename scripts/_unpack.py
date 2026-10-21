import gzip, base64, json, hashlib, pathlib, sys
blob = pathlib.Path("scripts/_r31.txt").read_text().strip()
want = pathlib.Path("scripts/_sha.txt").read_text().strip()
got = hashlib.sha256(blob.encode()).hexdigest()
if got != want:
    sys.exit("checksum mismatch: %s != %s" % (got, want))
for path, text in json.loads(gzip.decompress(base64.b64decode(blob))).items():
    p = pathlib.Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8"); print("wrote", path)
