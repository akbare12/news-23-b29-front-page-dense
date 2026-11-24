#!/usr/bin/env python3
"""news-23 b29 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MAX_BYTES = 1024 * 1024


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is empty", file=sys.stderr)
        return 1
    repo = os.path.dirname(os.path.abspath(__file__))
    if os.path.abspath(out_dir) == repo or os.path.abspath(out_dir).startswith(repo + os.sep):
        print("refusing to write inside the repo tree", file=sys.stderr)
        return 1
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        print("entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("bad PNG signature", file=sys.stderr)
        return 1
    if len(data) < 33:
        print("PNG too short", file=sys.stderr)
        return 1
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        print("bad IHDR", file=sys.stderr)
        return 1
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024) or depth != 8 or ctype not in (2, 6):
        print("unexpected PNG header", file=sys.stderr)
        return 1
    iend_len, iend_type = struct.unpack(">I4s", data[-12:-4])
    if (iend_len, iend_type) != (0, b"IEND"):
        print("missing IEND trailer", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    print("source %s (%d bytes, sha256 %s)" % (SRC, len(data), hashlib.sha256(data).hexdigest()))
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        print("output mismatch", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
