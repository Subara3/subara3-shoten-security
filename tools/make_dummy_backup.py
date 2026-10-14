"""legacy/backup/shop_20190401.sql（ダミー）を作る。中身は意味のない埋め草だけ。

アクセスログ（gen_logs.py）に合わせて 48,211,940 バイト、更新日時は 2019-04-01 にそろえる。
"""
import os
import sys
from datetime import datetime
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("legacy/backup/shop_20190401.sql")
SIZE = 48211940
head = ("-- すばら３商店 サーバ移行時のバックアップ（2019-04-01）\n"
        "-- 中身はダミー。点検の題材として「公開ディレクトリに残ったバックアップ」を再現するためのファイル\n").encode()
line = b"-- padding: dummy backup for the case study (no real data)\n"
body = head + line * ((SIZE - len(head)) // len(line))
body += b"-" * (SIZE - len(body) - 1) + b"\n"
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(body)
t = datetime(2019, 4, 1, 3, 12).timestamp()
os.utime(OUT, (t, t))
print(OUT, OUT.stat().st_size)
