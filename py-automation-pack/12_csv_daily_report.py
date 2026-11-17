#!/usr/bin/env python3
"""把一份 CSV 汇总成每日 Markdown 报告：总和、均值、最大项、Top N。

用法: python 12_csv_daily_report.py sales.csv --value amount --group sku --top 5
"""
import argparse
import csv
from collections import defaultdict


def num(x):
    try:
        return float(str(x).replace(",", "").replace("¥", "").strip())
    except (TypeError, ValueError):
        return 0.0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--value", default="")
    ap.add_argument("--group", default="")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--title", default="日报")
    a = ap.parse_args(argv)
    with open(a.csv, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print("# %s\n\n没有数据" % a.title)
        return 0
    cols = list(rows[0].keys())
    vcol = a.value or cols[-1]
    vals = [num(r.get(vcol)) for r in rows]
    total = sum(vals)
    print("# %s" % a.title)
    print("")
    print("- 行数：%d" % len(rows))
    print("- %s 合计：%.2f" % (vcol, total))
    print("- 平均：%.2f" % (total / len(vals) if vals else 0))
    if vals:
        imax = vals.index(max(vals))
        print("- 最大：%.2f（第 %d 行）" % (max(vals), imax + 2))
    if a.group and a.group in cols:
        agg = defaultdict(float)
        for r, v in zip(rows, vals):
            agg[r.get(a.group, "")] += v
        print("")
        print("## 按 %s 汇总（Top %d）" % (a.group, a.top))
        print("")
        print("| %s | 合计 |" % a.group)
        print("| --- | --- |")
        for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:a.top]:
            print("| %s | %.2f |" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
