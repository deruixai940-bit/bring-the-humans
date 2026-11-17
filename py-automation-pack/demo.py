# -*- coding: utf-8 -*-
"""demo.py — 一键演示：造样例数据、跑完 12 个脚本、打印全过程。

用法：python demo.py          在临时目录里跑，跑完自动清理
      python demo.py --keep   保留临时目录（想翻结果用）
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable or "python3"


def sh(args, stdin=None):
    print("$ " + " ".join(str(a) for a in args))
    r = subprocess.run(args, capture_output=True, text=True, input=stdin, timeout=120)
    out = (r.stdout or "").strip()
    err = (r.stderr or "").strip()
    if out:
        for line in out.splitlines()[:12]:
            print("  " + line)
        if len(out.splitlines()) > 12:
            print("  … (%d 行)" % len(out.splitlines()))
    if r.returncode != 0:
        print("  [rc=%d] %s" % (r.returncode, err.splitlines()[-1] if err else ""))
    print()
    return r


def main():
    keep = "--keep" in sys.argv
    root = Path(tempfile.mkdtemp(prefix="pya-demo-"))
    print("演示目录：%s\n" % root)
    try:
        # 1 造数据
        (root / "photos").mkdir()
        for n in ("IMG_0042.JPG", "IMG_0043.JPG", "IMG_0001.JPG"):
            (root / "photos" / n).write_bytes(b"x" * 10)
        for i in (1, 2):
            (root / ("reports_%d.csv" % i)).write_text(
                "sku,qty,price\nA-1,%d,19.9\nB-2,%d,5.0\n" % (i, i + 1), encoding="utf-8")
        (root / "big.csv").write_text(
            "sku,qty\n" + "\n".join("S%d,%d" % (i, i) for i in range(1, 26)), encoding="utf-8")
        (root / "notes.txt").write_text(
            "联系 a@b.com 或 https://example.com，备选 c@d.org\n", encoding="utf-8")
        (root / "events.jsonl").write_text(
            '{"t":"2026-11-01","user":{"id":1,"name":"a"},"n":3}\n'
            '{"t":"2026-11-02","user":{"id":2,"name":"b"},"n":5}\n', encoding="utf-8")
        (root / "app.log").write_text(
            "2026-11-01 10:00:01 ERROR timeout\n2026-11-01 10:00:41 INFO ok\n"
            "2026-11-01 10:01:02 ERROR refused\n", encoding="utf-8")
        (root / "dup").mkdir()
        (root / "dup" / "a.txt").write_bytes(b"same")
        (root / "dup" / "b.txt").write_bytes(b"same")

        # 2 逐个跑
        sh([PY, str(HERE / "01_rename_batch.py"), "--dir", str(root / "photos"), "--prefix", "trip"])
        sh([PY, str(HERE / "01_rename_batch.py"), "--dir", str(root / "photos"), "--prefix", "trip", "--apply"])
        sh([PY, str(HERE / "02_merge_csv.py"), "--dir", str(root), "--out", str(root / "all.csv")])
        sh([PY, str(HERE / "03_csv_to_md.py"), str(root / "all.csv")])
        sh([PY, str(HERE / "06_dedupe_files.py"), "--dir", str(root / "dup")])
        sh([PY, str(HERE / "07_extract_contacts.py"), str(root / "notes.txt")])
        sh([PY, str(HERE / "08_jsonl_to_csv.py"), str(root / "events.jsonl"), "--out", str(root / "ev.csv")])
        sh([PY, str(HERE / "09_split_csv.py"), str(root / "big.csv"), "--rows", "10", "--outdir", str(root / "parts")])
        sh([PY, str(HERE / "10_log_grep.py"), str(root / "app.log"), "--kw", "ERROR", "--by-minute"])
        sh([PY, str(HERE / "11_cron_builder.py"), "--at", "08:30", "--cmd", "python3 job.py"])
        sh([PY, str(HERE / "12_csv_daily_report.py"), str(root / "all.csv"), "--group", "sku"])

        # 3 产出清单
        print("产出文件：")
        for p in sorted(root.rglob("*")):
            if p.is_file():
                print("  %-46s %d B" % (p.relative_to(root), p.stat().st_size))
        print("\n演示完成。想自己试：把上面的命令换成你的目录即可。")
    finally:
        if keep:
            print("\n保留目录：%s" % root)
        else:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    main()
