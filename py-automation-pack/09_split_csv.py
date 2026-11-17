#!/usr/bin/env python3
"""大 CSV 按行数切片：给只能吃小文件的地方用。

用法: python 09_split_csv.py big.csv --rows 1000 --outdir parts
"""
import argparse
import csv
import pathlib


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--rows", type=int, default=1000)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args(argv)
    out = pathlib.Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    with open(a.csv, newline="", encoding="utf-8") as fh:
        r = csv.reader(fh)
        head = next(r, None)
        if head is None:
            print("empty")
            return 0
        n, idx, w, fh_out = 0, 0, None, None
        try:
            for row in r:
                if n % a.rows == 0:
                    if fh_out:
                        fh_out.close()
                    idx += 1
                    fh_out = open(out / ("part_%03d.csv" % idx), "w", newline="", encoding="utf-8")
                    w = csv.writer(fh_out)
                    w.writerow(head)
                w.writerow(row)
                n += 1
        finally:
            if fh_out:
                fh_out.close()
    print("rows", n, "parts", idx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
