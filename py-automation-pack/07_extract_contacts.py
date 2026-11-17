#!/usr/bin/env python3
"""从一堆文本里抽出邮箱和链接，去重后按出现次数排序。

用法: python 07_extract_contacts.py notes/*.txt
"""
import argparse
import re
import pathlib
from collections import Counter

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
URL = re.compile(r"https?://[^\s\)\]\>,\"']+")


def collect(paths):
    mails, urls = Counter(), Counter()
    for p in paths:
        text = pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
        mails.update(EMAIL.findall(text))
        urls.update(u.rstrip(".,;") for u in URL.findall(text))
    return mails, urls


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    a = ap.parse_args(argv)
    mails, urls = collect(a.paths)
    print("emails", len(mails))
    for k, v in mails.most_common():
        print("  %s x%d" % (k, v))
    print("urls", len(urls))
    for k, v in urls.most_common(30):
        print("  %s x%d" % (k, v))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
