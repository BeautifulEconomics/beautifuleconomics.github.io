import gzip, base64, pathlib, hashlib, sys
b = pathlib.Path("scripts/_p4.txt").read_text().strip()
if hashlib.sha256(b.encode()).hexdigest() != "0fb715f44a782d62d322a4ce4845bddd88d4663aea7dc1a6b3c5ce13b2c5a1ef":
    sys.exit("checksum mismatch")
pathlib.Path("scripts/_p4run.py").write_bytes(gzip.decompress(base64.b64decode(b)))
print("unpacked")
