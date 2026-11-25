#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261125 bounty.

Copies the pre-rendered entry.png (produced by draw_lead.py) into
$MAKEFUN_OUTPUT_DIR/entry.png, byte-for-byte.
"""
import hashlib
import os
import shutil
import sys

MAX_BYTES = 1 * 1024 * 1024  # competition cap: at most 1 MiB

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print("ERROR: %s is missing (run draw_lead.py first)"
              % SRC, file=sys.stderr)
        return 1
    src_size = os.path.getsize(SRC)
    if src_size > MAX_BYTES:
        print("ERROR: entry.png is %d bytes, over the 1 MiB cap"
              % src_size, file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            print("ERROR: entry.png is not a PNG file", file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("ERROR: cannot create output dir %s: %s"
              % (out_dir, exc), file=sys.stderr)
        return 1
    dst = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(SRC, dst)
    except OSError as exc:
        print("ERROR: copy failed: %s" % exc, file=sys.stderr)
        return 1
    if os.path.getsize(dst) != src_size or sha256(dst) != sha256(SRC):
        print("ERROR: incomplete copy: dst differs from src",
              file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, src_size, sha256(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
