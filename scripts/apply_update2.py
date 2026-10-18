#!/usr/bin/env python3
"""Write the updated site files into the repository, once.

The new versions travel here as a gzipped bundle split over two text files.
The bundle's SHA-256 is checked before anything is written, so a single
corrupted character stops the run instead of silently producing broken
files. Deleted by the workflow once the update has landed.
"""
import base64
import gzip
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = "303f7b170fd5d8f03ab046de536fd0ec9bc611339962c87af9c550442c353521"


def main():
    packed = "".join(
        (HERE / name).read_text().strip()
        for name in ("_r2a2.txt", "_r2b.txt")
    )

    digest = hashlib.sha256(packed.encode()).hexdigest()
    if digest != EXPECTED:
        print("Bundle checksum mismatch - refusing to write anything.", file=sys.stderr)
        print(f"  expected {EXPECTED}", file=sys.stderr)
        print(f"  got      {digest}  ({len(packed)} chars)", file=sys.stderr)
        return 1

    files = json.loads(gzip.decompress(base64.b64decode(packed)))

    written = []
    for rel, text in files.items():
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists() and p.read_text(encoding="utf-8") == text:
            continue
        p.write_text(text, encoding="utf-8")
        written.append(f"{rel} ({len(text)} chars)")

    print(f"Checksum verified. {len(written)} of {len(files)} file(s) changed")
    for w in written:
        print("  " + w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
