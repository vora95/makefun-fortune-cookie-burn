#!/usr/bin/env python3
"""Fortune Cookie Wisdom for Developers — burn entry.

Writes one line of fortune-cookie wisdom to $MAKEFUN_OUTPUT_DIR/entry.txt.
Stdlib only. Deterministic.
"""
import hashlib
import os

ENTRY = "The estimate you give today will be quoted back to you as a promise tomorrow."


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    out_path = out_dir if out_dir.endswith("entry.txt") else os.path.join(out_dir, "entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    data = ENTRY.encode("utf-8")
    assert 1 <= len(ENTRY) <= 120, f"entry length {len(ENTRY)} out of range"
    assert ENTRY.strip() == ENTRY and "\n" not in ENTRY
    with open(out_path, "wb") as f:
        f.write(data)
    # Validation revision: read the file back and verify byte-identity,
    # single-line shape and the 1-120 char gate exactly as the scorer does.
    with open(out_path, "rb") as f:
        back = f.read()
    assert back == data, "written bytes differ from ENTRY"
    text = back.decode("utf-8")
    assert text.strip() != "", "entry is whitespace-only"
    assert "\n" not in text and "\r" not in text, "entry must be exactly one line"
    assert 1 <= len(text) <= 120, f"entry length {len(text)} out of range"
    print(f"wrote {out_path} ({len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()})")


if __name__ == "__main__":
    main()
