#!/usr/bin/env python3
"""合并目录下所有 CSV：表头相同才算同一种表，输出一个文件。

用法: python 02_merge_csv.py --dir reports --out all.csv [--keep-header-once]
"""
import argparse
import csv
import pathlib


def merge(paths, out_path):
    header = None
    rows = 0
    with open(out_path, "w", newline="", encoding="utf-8") as fh:
        w = None
        for p in paths:
            with open(p, newline="", encoding="utf-8") as src:
                r = csv.reader(src)
                try:
                    h = next(r)
                except StopIteration:
                    continue
                if header is None:
                    header = h
                    w = csv.writer(fh)
                    w.writerow(h)
                elif h != header:
                    print("skip (different header):", p.name)
                    continue
                for row in r:
                    w.writerow(row)
                    rows += 1
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    paths = sorted(pathlib.Path(a.dir).glob("*.csv"))
    n = merge(paths, a.out)
    print("files", len(paths), "rows", n, "->", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
