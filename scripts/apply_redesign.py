#!/usr/bin/env python3
"""Write the redesigned files into the repository, once.

GitHub's web editor cannot replace a dozen files in one go, so the new
versions travelled here as one gzipped bundle split over two text files.
This script unpacks them. Once the redesign has landed you can delete
this script, the two _redesign_*.txt files and the apply-redesign
workflow; nothing else depends on them.
"""
import base64
import gzip
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent


def main():
    packed = "".join(
        (HERE / name).read_text().strip()
        for name in ("_redesign_a.txt", "_redesign_b.txt")
    )
    files = json.loads(gzip.decompress(base64.b64decode(packed)))

    written = []
    for rel, text in files.items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists() and p.read_text(encoding="utf-8") == text:
            continue
        p.write_text(text, encoding="utf-8")
        written.append(f"{rel} ({len(text)} chars)")

    print(f"{len(written)} of {len(files)} file(s) changed")
    for w in written:
        print("  " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
