# Gumroad 商品页文案（直接抄）

## 商品名

12 Python Automation Scripts — rename, merge, dedupe, fetch, report

## 短描述（Gumroad 的 Subtitle，一行）

12 single-file Python scripts that do the boring parts: batch rename, merge CSVs, find duplicates, retry downloads, turn logs into reports. No dependencies.

## 价格

- 官方价 **$19**
- 勾选「允许客户多付」，最低价仍是 $19（有人会给 $25–$35）

## 长描述（粘贴到 Description）

**你不需要一个框架，你需要 12 个能马上跑的小脚本。**

每个脚本都是单文件、只用 Python 标准库、带 `--help`。拷到服务器、改两个参数就能用，不用 pip install 任何东西。

| # | 脚本 | 干什么 |
|---|---|---|
| 01 | rename_batch.py | 批量重命名，默认 dry-run 先看效果 |
| 02 | merge_csv.py | 合并同表头 CSV |
| 03 | csv_to_md.py | CSV 转 Markdown 表格 |
| 04 | folder_watch.py | 盯目录，来新文件就执行命令 |
| 05 | retry_fetch.py | 带重试与超时的下载 |
| 06 | dedupe_files.py | 按内容哈希找重复文件 |
| 07 | extract_contacts.py | 从文本抽邮箱与链接并计数 |
| 08 | jsonl_to_csv.py | JSONL 导出 CSV，自动摊平嵌套 |
| 09 | split_csv.py | 大 CSV 按行切片 |
| 10 | log_grep.py | 多日志按关键词过滤 + 按分钟统计 |
| 11 | cron_builder.py | 说人话生成 crontab 行 |
| 12 | csv_daily_report.py | CSV 汇总成 Markdown 日报 |

**为什么是它们**：这 12 件是「每周都要做一次、但写起来烦」的事。我把它们写成能读得懂的短代码（每个不到 90 行），你不想改也能直接用。

**安全的默认**：会动手脚的脚本（重命名、删重复、切片）默认都是 dry-run 或只读，加 `--apply` 才真的执行。第一次跑不会毁掉你的文件。

**跑在哪**：Windows、macOS、Linux 同一份代码（Python 3.9+）。`04_folder_watch.py` 在 Windows 下用 cmd.exe 执行 `--cmd`，其余行为一致。

**包里有什么**

- 12 个脚本（`01_*.py` … `12_*.py`）
- `README.md`：每个脚本的一行示例
- `verify.py`：给 12 个脚本各起临时目录跑真实小样，自检 12/12
- `SELL.md`：就是你正在读的这段

**不包含什么**：没有 GUI，没有云服务，没有「一键搞定所有事」。这是给会打开终端的人用的工具。

## 标签

`python` `automation` `scripts` `csv` `cli` `developer-tools` `productivity` `no-dependencies`

## FAQ

**Q：需要装什么吗？**
不用。Python 3.9 以上，标准库就够。

**Q：看不懂代码能用吗？**
能。README 里每个脚本都有一行示例命令，改路径就行。

**Q：会删我的文件吗？**
默认不会。重命名、删重复、切片都默认 dry-run，加 `--apply` 才真做。

**Q：能商用吗？**
用在你自己或你公司的项目里可以；不要把脚本本身再分发转卖。

**Q：更新吗？**
买了就是这份，后续我加了新脚本会免费补给你（用购买邮箱回信即可）。

## 退款政策

数字商品，售出不退。买之前不确定就先看上面的脚本清单——你大概能判断有没有用。
