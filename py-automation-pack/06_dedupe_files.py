#!/usr/bin/env python3
"""按内容哈希找重复文件：先报告，确认后再删。

用法: python 06_dedupe_files.py --dir downloads [--delete]
"""
import argparse
import hashlib
import pathlib


def digest(p, chunk=1 << 20):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def groups(d):
    table = {}
    for p in pathlib.Path(d).rglob("*"):
        if p.is_file():
            table.setdefault((digest(p), p.stat().st_size), []).append(p)
    return [v for v in table.values() if len(v) > 1]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--delete", action="store_true")
    a = ap.parse_args(argv)
    total = 0
    for g in groups(a.dir):
        keep = g[0]
        print("GROUP size=%d keep=%s" % (keep.stat().st_size, keep))
        for dup in g[1:]:
            print("  dup", dup)
            total += 1
            if a.delete:
                dup.unlink()
    print("duplicates", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
