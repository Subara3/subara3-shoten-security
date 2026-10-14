"""すばら３商店のアクセスログ（Apache combined 形式）を直近90日ぶん作る。出力は logs/access.log.sample。

IPアドレスは文書用の範囲だけを使う。
  192.0.2.10        店舗（スタッフ）
  198.51.100.0/25   お客さん（IPv4）
  2001:db8::/32     お客さん（IPv6）
  198.51.100.200    support2 の接続元
  203.0.113.0/24    見覚えのない接続元
"""
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

random.seed(1014)
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("logs/access.log.sample")
NOW = datetime(2026, 10, 14, 9, 0)
START = NOW - timedelta(days=90)
UA = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36",
]
SCAN_UA = ["Mozilla/5.0 zgrab/0.x", "python-requests/2.32.3", "Go-http-client/1.1", "curl/8.5.0"]
lines = []


def add(t, ip, method, path, status, size, ua, ref="-"):
    lines.append((t, f'{ip} - - [{t.strftime("%d/%b/%Y:%H:%M:%S")} +0900] "{method} {path} HTTP/1.1" {status} {size} "{ref}" "{ua}"'))


def rnd(a, b):
    return a + timedelta(seconds=random.randint(0, int((b - a).total_seconds())))


def cust_ip():
    return f"198.51.100.{random.randint(2,126)}" if random.random() < 0.6 else f"2001:db8:{random.randint(1,0xffff):x}::{random.randint(1,0xffff):x}"


day = START
while day < NOW:
    d_end = min(day + timedelta(days=1), NOW)
    # ふだんのお客さん
    for _ in range(random.randint(380, 620)):
        t = rnd(day, d_end)
        ip, ua = cust_ip(), random.choice(UA)
        page = random.choices(["/", "/index.php", "/login.php", "/favicon.ico"], [5, 3, 1, 1])[0]
        add(t, ip, "GET", page, 200, random.randint(1800, 5200), ua)
        if page == "/login.php" and random.random() < 0.7:
            add(t + timedelta(seconds=9), ip, "POST", "/login.php", 302, 0, ua)
    # スタッフの管理画面
    for _ in range(random.randint(10, 30)):
        t = rnd(day.replace(hour=8), day.replace(hour=19))
        add(t, "192.0.2.10", "GET", random.choice(["/admin/index.php", "/admin/members.php"]), 200, random.randint(9000, 30000), UA[1])
    # 前から来ている、よくある探索（ずっと少量）
    for _ in range(random.randint(3, 12)):
        t = rnd(day, d_end)
        add(t, f"203.0.113.{random.randint(2,250)}", "GET",
            random.choice(["/wp-login.php", "/.env", "/xmlrpc.php", "/.git/config", "/phpmyadmin/", "/admin/.env"]), 404, 196, random.choice(SCAN_UA))
    day += timedelta(days=1)

# 9/29から探索が増える。見つかってはいけないものに200が返っている
wave_start = datetime(2026, 9, 29)
for _ in range(2600):
    t = rnd(wave_start, NOW)
    path, status, size = random.choices(
        [("/.env", 404, 196), ("/wp-login.php", 404, 196), ("/.git/config", 404, 196), ("/backup.zip", 404, 196),
         ("/old/", 404, 196), ("/admin/", 302, 0), ("/phpinfo.php", 200, 72310), ("/config.php.bak", 200, 512)],
        [30, 25, 15, 10, 8, 6, 4, 2])[0]
    add(t, f"203.0.113.{random.randint(2,250)}", "GET", path, status, size, random.choice(SCAN_UA))
add(datetime(2026, 10, 3, 4, 11, 7), "203.0.113.45", "GET", "/backup/", 200, 1043, SCAN_UA[1])
add(datetime(2026, 10, 3, 4, 11, 8), "203.0.113.45", "GET", "/backup/shop_20190401.sql", 200, 48211940, SCAN_UA[1])
# 10/3〜10/13 管理画面ログインの失敗（admin_login_log と同じ期間）
for _ in range(640):
    t = rnd(datetime(2026, 10, 3), datetime(2026, 10, 13))
    add(t, f"203.0.113.{random.randint(2,250)}", "POST", "/admin/login.php", 200, 512, random.choice(SCAN_UA))
# support2：深夜にログインして画面を見る
for d in [datetime(2026, 9, 18, 2, 14), datetime(2026, 9, 24, 3, 40), datetime(2026, 10, 2, 2, 55), datetime(2026, 10, 11, 3, 2)]:
    ua = UA[1]
    add(d, "198.51.100.200", "POST", "/admin/login.php", 302, 0, ua)
    add(d + timedelta(seconds=3), "198.51.100.200", "GET", "/admin/index.php", 200, 21877, ua)
    add(d + timedelta(seconds=40), "198.51.100.200", "GET", "/admin/admins.php", 200, 1342, ua)
add(datetime(2026, 10, 11, 3, 4, 31), "198.51.100.200", "GET", "/admin/export.php", 200, 611204, UA[1])

lines.sort()
OUT.write_text("\n".join(l for _, l in lines) + "\n", encoding="utf-8")
print(OUT, len(lines), "lines")
