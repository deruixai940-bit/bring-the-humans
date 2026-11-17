#!/usr/bin/env python3
"""批量重命名：按规则改一个目录里的文件名。默认 dry-run，不改东西。

用法:
  python 01_rename_batch.py --dir photos --prefix trip --start 1 --pad 3 --dry-run
  python 01_rename_batch.py --dir photos --prefix trip --ext .jpg --apply
"""
import argparse
import pathlib


def plan(files, prefix, start, pad, ext):
    out = []
    for i, p in enumerate(files):
        if ext and p.suffix.lower() != ext.lower():
            continue
        name = "%s_%0*d%s" % (prefix, pad, start + i, p.suffix)
        out.append((p, p.with_name(name)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--prefix", default="file")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--pad", type=int, default=3)
    ap.add_argument("--ext", default="")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    d = pathlib.Path(a.dir)
    files = sorted([p for p in d.iterdir() if p.is_file()])
    pairs = plan(files, a.prefix, a.start, a.pad, a.ext)
    for src, dst in pairs:
        print(("RENAME " if a.apply else "DRY    ") + src.name + " -> " + dst.name)
        if a.apply:
            src.rename(dst)
    print("total", len(pairs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
