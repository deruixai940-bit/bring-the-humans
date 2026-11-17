#!/usr/bin/env python3
"""带重试和超时的下载：接口偶尔抽风时用它，别手点刷新。

用法: python 05_retry_fetch.py https://example.com/api --out resp.json --retries 4
"""
import argparse
import time
import urllib.request


def fetch(url, timeout=15, retries=3, backoff=1.5, headers=None):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers or {"User-Agent": "py-pack/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read()
        except Exception as exc:  # noqa: BLE001
            last = exc
            if i + 1 < retries:
                time.sleep(backoff ** i)
    raise RuntimeError("give up after %d tries: %s" % (retries, last))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default="")
    ap.add_argument("--retries", type=int, default=4)
    ap.add_argument("--timeout", type=float, default=15)
    a = ap.parse_args(argv)
    code, body = fetch(a.url, timeout=a.timeout, retries=a.retries)
    print("status", code, "bytes", len(body))
    if a.out:
        open(a.out, "wb").write(body)
        print("saved", a.out)
    else:
        print(body[:400].decode("utf-8", "replace"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
