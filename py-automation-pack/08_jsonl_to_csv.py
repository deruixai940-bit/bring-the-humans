#!/usr/bin/env python3
"""JSONL 转 CSV：日志、事件、审计记录批量导表。

用法: python 08_jsonl_to_csv.py events.jsonl --out events.csv --fields a,b,c
"""
import argparse
import csv
import json


def read(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def flatten(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = prefix + k
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("jsonl")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fields", default="")
    a = ap.parse_args(argv)
    rows = [flatten(r) for r in read(a.jsonl)]
    if not rows:
        print("no rows")
        return 0
    fields = [f for f in a.fields.split(",") if f] or sorted({k for r in rows for k in r})
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("rows", len(rows), "cols", len(fields), "->", a.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
