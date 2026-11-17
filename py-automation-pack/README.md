# 12 个零依赖 Python 自动化脚本

每个脚本都是单文件、只用标准库、带 `--help`。拿去改行名、改路径就能用。

| # | 脚本 | 干什么 | 一行示例 |
|---|---|---|---|
| 01 | rename_batch.py | 批量重命名，默认 dry-run | `python 01_rename_batch.py --dir photos --prefix trip --apply` |
| 02 | merge_csv.py | 合并同表头 CSV | `python 02_merge_csv.py --dir reports --out all.csv` |
| 03 | csv_to_md.py | CSV 转 Markdown 表格 | `python 03_csv_to_md.py data.csv > t.md` |
| 04 | folder_watch.py | 盯目录，有新文件就动手 | `python 04_folder_watch.py --dir inbox --cmd "echo {path}"` |
| 05 | retry_fetch.py | 带重试的超时下载 | `python 05_retry_fetch.py https://x/api --out r.json` |
| 06 | dedupe_files.py | 按内容哈希找重复文件 | `python 06_dedupe_files.py --dir downloads` |
| 07 | extract_contacts.py | 抽邮箱与链接并计数 | `python 07_extract_contacts.py notes/*.txt` |
| 08 | jsonl_to_csv.py | JSONL 导 CSV（自动摊平） | `python 08_jsonl_to_csv.py ev.jsonl --out ev.csv` |
| 09 | split_csv.py | 大 CSV 按行切片 | `python 09_split_csv.py big.csv --rows 1000 --outdir parts` |
| 10 | log_grep.py | 多日志按关键词过滤 + 按分钟统计 | `python 10_log_grep.py logs/*.log --kw error --by-minute` |
| 11 | cron_builder.py | 说人话生成 crontab 行 | `python 11_cron_builder.py --at 08:30 --cmd "python3 job.py"` |
| 12 | csv_daily_report.py | CSV 汇总成 Markdown 日报 | `python 12_csv_daily_report.py sales.csv --group sku` |

## 为什么值得买

- 不用装任何包（stdlib only），拷到服务器就能跑
- 每个都有 dry-run 或只读默认，不会一上手删你东西
- 代码短（每个 ≤90 行），看不懂可以改

## 许可

个人使用。可改、可用在你自己项目里；不要再分发转卖。

## 先看效果（30 秒）

```bash
python demo.py
```

它会在临时目录里造一批样例数据，把 12 个脚本逐个跑一遍，打印每一步的真实输出，跑完自动清理。想留着结果看就加 `--keep`。

## 自检

```bash
python verify.py
```

12 个脚本各自跑一遍真实小样，全绿才算交付。

## 运行环境

- Python **3.9+**，只用标准库，不需要 `pip install`
- Windows / macOS / Linux 同一份代码
- Windows 下 `04_folder_watch.py --cmd` 通过 `cmd.exe` 执行，其余脚本行为一致
- 会改文件的脚本（重命名 / 去重 / 切片）默认 dry-run，加 `--apply` 才真执行

## 包里有什么

| 文件 | 说明 |
|---|---|
| `01_*.py` … `12_*.py` | 12 个脚本 |
| `README.md` | 就是这份，每个脚本一行示例 |
| `verify.py` | 自检：给每个脚本起临时目录跑真实小样 |
| `demo.py` | 一键演示：造样例数据跑完 12 个脚本 |
| `SELL.md` | 商品页文案（买家用不到，可删） |
| `cover.png` | 商品封面（可删） |
