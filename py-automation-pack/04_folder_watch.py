#!/usr/bin/env python3
"""盯一个目录：有新文件就打印/执行一条命令。适合配合 cron 或丢进 tmux。

用法: python 04_folder_watch.py --dir inbox --interval 5 [--cmd "echo {path}"]
"""
import argparse
import subprocess
import time
import pathlib


def scan(d):
    return {str(p): p.stat().st_mtime for p in pathlib.Path(d).iterdir() if p.is_file()}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--interval", type=float, default=5.0)
    ap.add_argument("--cmd", default="")
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args(argv)
    seen = scan(a.dir)
    print("watching", a.dir, "files:", len(seen))
    while True:
        time.sleep(a.interval)
        now = scan(a.dir)
        new = [p for p in now if p not in seen]
        for p in new:
            print("NEW", p)
            if a.cmd:
                subprocess.run(a.cmd.replace("{path}", p), shell=True, check=False)
        seen = now
        if a.once:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
