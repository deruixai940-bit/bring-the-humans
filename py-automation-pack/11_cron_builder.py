#!/usr/bin/env python3
"""把「每天几点干什么」翻成 crontab 行，省得数星号。

用法: python 11_cron_builder.py --at 08:30 --cmd "/usr/bin/python3 job.py"
"""
import argparse


def build(at, cmd, days="*", month="*", dom="*"):
    hh, mm = at.split(":")
    return "%02d %02d %s %s %s %s" % (int(mm), int(hh), dom, month, days, cmd)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--at", default="08:30", help="HH:MM")
    ap.add_argument("--cmd", required=True)
    ap.add_argument("--days", default="*", help="0-6, * = 每天")
    ap.add_argument("--once-daily-note", action="store_true")
    a = ap.parse_args(argv)
    line = build(a.at, a.cmd, a.days)
    print(line)
    if a.once_daily_note:
        print("# 装法: crontab -e 后粘一行；系统级放 /etc/cron.d/ 并加用户名")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
