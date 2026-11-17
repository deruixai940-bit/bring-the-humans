#!/usr/bin/env python3
"""多文件日志按关键词过滤 + 按分钟统计：排查尖峰时比 grep 好用。

用法: python 10_log_grep.py logs/*.log --kw error --kw timeout [--by-minute]
"""
import argparse
import pathlib
import re
from collections import Counter

TS = re.compile(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2})")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--kw", action="append", default=[])
    ap.add_argument("--by-minute", action="store_true")
    ap.add_argument("--max", type=int, default=200)
    a = ap.parse_args(argv)
    hits, buckets = [], Counter()
    for p in a.paths:
        for line in pathlib.Path(p).read_text(encoding="utf-8", errors="replace").splitlines():
            if a.kw and not any(k.lower() in line.lower() for k in a.kw):
                continue
            hits.append((p, line))
            m = TS.search(line)
            if m:
                buckets[m.group(1)] += 1
    for p, line in hits[-a.max:]:
        print("%s: %s" % (pathlib.Path(p).name, line[:200]))
    print("total hits", len(hits))
    if a.by_minute:
        for k, v in sorted(buckets.items()):
            print("%s  %d" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
