#!/usr/bin/env python3
"""把 12 个脚本各跑一遍（真实小样），全绿才算交付。"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
PY = sys.executable


def run(args, cwd=None):
    r = subprocess.run([PY] + args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError("%s -> rc=%d\n%s\n%s" % (" ".join(args), r.returncode, r.stdout[-500:], r.stderr[-500:]))
    return r.stdout


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pack-"))
    ok = []
    try:
        d = tmp / "photos"
        d.mkdir()
        for n in ("a.jpg", "b.jpg", "c.png"):
            (d / n).write_text("x")
        out = run([str(HERE / "01_rename_batch.py"), "--dir", str(d), "--prefix", "t", "--ext", ".jpg"])
        assert "2" in out.split()[-1], out
        ok.append("01")

        rd = tmp / "reports"
        rd.mkdir()
        for i in range(3):
            (rd / ("r%d.csv" % i)).write_text("a,b\n1,%d\n" % i)
        out = run([str(HERE / "02_merge_csv.py"), "--dir", str(rd), "--out", str(tmp / "all.csv")])
        assert "rows 3" in out, out
        ok.append("02")

        out = run([str(HERE / "03_csv_to_md.py"), str(tmp / "all.csv")])
        assert out.startswith("| a | b |"), out[:80]
        ok.append("03")

        out = run([str(HERE / "04_folder_watch.py"), "--dir", str(d), "--once", "--interval", "0.01"])
        assert "watching" in out
        ok.append("04")

        out = run([str(HERE / "05_retry_fetch.py"), "data:text/plain,hi", "--retries", "1"])
        assert "status" in out
        ok.append("05")

        dup = tmp / "dup"
        dup.mkdir()
        (dup / "1.txt").write_text("same")
        (dup / "2.txt").write_text("same")
        out = run([str(HERE / "06_dedupe_files.py"), "--dir", str(dup)])
        assert "duplicates 1" in out, out
        ok.append("06")

        f = tmp / "note.txt"
        f.write_text("mail me a@b.com or http://x.io/a")
        out = run([str(HERE / "07_extract_contacts.py"), str(f)])
        assert "a@b.com" in out
        ok.append("07")

        jl = tmp / "ev.jsonl"
        jl.write_text('{"id":1,"m":{"u":2}}\n{"id":2,"m":{"u":3}}\n')
        out = run([str(HERE / "08_jsonl_to_csv.py"), str(jl), "--out", str(tmp / "ev.csv")])
        assert "rows 2" in out
        ok.append("08")

        big = tmp / "big.csv"
        big.write_text("a\n" + "".join("%d\n" % i for i in range(25)))
        out = run([str(HERE / "09_split_csv.py"), str(big), "--rows", "10", "--outdir", str(tmp / "parts")])
        assert "parts 3" in out, out
        ok.append("09")

        lg = tmp / "app.log"
        lg.write_text("2026-11-12 10:00:01 error x\n2026-11-12 10:01:02 info y\n")
        out = run([str(HERE / "10_log_grep.py"), str(lg), "--kw", "error", "--by-minute"])
        assert "total hits 1" in out, out
        ok.append("10")

        out = run([str(HERE / "11_cron_builder.py"), "--at", "08:30", "--cmd", "python3 job.py"])
        assert out.strip().startswith("30 08"), out
        ok.append("11")

        out = run([str(HERE / "12_csv_daily_report.py"), str(tmp / "all.csv"), "--value", "b"])
        assert "合计" in out
        ok.append("12")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("passed %d/12: %s" % (len(ok), ",".join(ok)))
    return 0 if len(ok) == 12 else 1


if __name__ == "__main__":
    raise SystemExit(main())
