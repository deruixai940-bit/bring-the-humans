#!/usr/bin/env python3
"""CSV 转 Markdown 表格：贴文档、贴 issue、贴周报用。

用法: python 03_csv_to_md.py data.csv > table.md
"""
import argparse
import csv


def to_md(rows, limit=200):
    rows = rows[:limit]
    if not rows:
        return ""
    head = rows[0]
    out = ["| " + " | ".join(head) + " |", "| " + " | ".join(["---"] * len(head)) + " |"]
    for r in rows[1:]:
        out.append("| " + " | ".join((c or "").replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--limit", type=int, default=200)
    a = ap.parse_args(argv)
    with open(a.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    print(to_md(rows, a.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
