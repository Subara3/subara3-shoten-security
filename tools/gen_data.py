"""すばら３商店のダミーデータを作る。出力は db/01_schema_data.sql。

人名・住所・メールは全部でたらめに組み合わせたもの。
カード番号は国際ブランドが公開しているテスト番号だけを使う。
"""
import hashlib
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

random.seed(20261014)
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("db/01_schema_data.sql")

SEI = "佐藤 鈴木 高橋 田中 伊藤 渡辺 山本 中村 小林 加藤 吉田 山田 佐々木 山口 松本 井上 木村 林 清水 斎藤".split()
MEI = "陽菜 結衣 葵 蓮 湊 大和 悠真 陽翔 美咲 さくら 健太 翔 拓海 七海 彩 優 誠 花子 太郎 舞".split()
PREF = "北海道 青森県 宮城県 東京都 神奈川県 埼玉県 千葉県 愛知県 大阪府 京都府 兵庫県 広島県 福岡県 沖縄県".split()
ITEMS = [
    ("手ぬぐい（すばら柄）", 1200), ("豆皿 5枚組", 2800), ("湯のみ", 1800), ("箸置き", 600),
    ("風呂敷 中判", 2400), ("和ろうそく", 900), ("干支の土鈴", 1500), ("がま口 小", 2200),
    ("お香 白檀", 1100), ("ぽち袋 10枚", 450),
]
TEST_CARDS = ["4111111111111111", "5555555555554444", "4012888888881881", "3530111333300000"]


def q(s):
    return "'" + str(s).replace("\\", "\\\\").replace("'", "''") + "'"


def ts(d):
    return q(d.strftime("%Y-%m-%d %H:%M:%S"))


def rand_dt(a, b):
    return a + timedelta(seconds=random.randint(0, int((b - a).total_seconds())))


out = ["SET NAMES utf8mb4;"]
out.append("""
CREATE TABLE products (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100), price INT);
CREATE TABLE members (
  id INT PRIMARY KEY AUTO_INCREMENT, email VARCHAR(200), password VARCHAR(64),
  name VARCHAR(100), zip VARCHAR(8), address VARCHAR(255), tel VARCHAR(20), birthday DATE,
  status VARCHAR(10), created_at DATETIME, withdrawn_at DATETIME NULL);
CREATE TABLE orders (
  id INT PRIMARY KEY AUTO_INCREMENT, member_id INT, ship_name VARCHAR(100), ship_address VARCHAR(255),
  ship_tel VARCHAR(20), total INT, ordered_at DATETIME);
-- 2018年の割賦販売法改正まで使っていた、自前のカード情報テーブル
CREATE TABLE order_cards_old (
  order_id INT, card_no VARCHAR(19), card_exp VARCHAR(5), card_name VARCHAR(100), created_at DATETIME);
CREATE TABLE admins (
  id INT PRIMARY KEY AUTO_INCREMENT, login VARCHAR(50), password VARCHAR(64), role VARCHAR(20),
  active TINYINT, note VARCHAR(255), created_at DATETIME, last_login DATETIME NULL);
CREATE TABLE admin_login_log (
  id INT PRIMARY KEY AUTO_INCREMENT, login VARCHAR(50), ip VARCHAR(45), success TINYINT, at DATETIME);
""")

for name, price in ITEMS:
    out.append(f"INSERT INTO products (name, price) VALUES ({q(name)}, {price});")

# 会員：2012年開店から。退会者も行は残ったまま（status だけ変える作り）
start, now = datetime(2012, 4, 1), datetime(2026, 10, 14, 9, 0)
members = []
rows = []
for i in range(1, 3201):
    created = rand_dt(start, now - timedelta(days=3))
    withdrawn = None
    if random.random() < 0.27:
        withdrawn = rand_dt(created + timedelta(days=30), now) if created + timedelta(days=30) < now else None
    name = random.choice(SEI) + " " + random.choice(MEI)
    pref = random.choice(PREF)
    addr = f"{pref}{random.choice(['中央区','北区','南区','緑区','青葉区'])}{random.randint(1,9)}-{random.randint(1,30)}-{random.randint(1,20)}"
    tel = f"0{random.randint(70,90)}-{random.randint(1000,9999)}-{random.randint(1000,9999)}"
    bday = datetime(random.randint(1950, 2004), random.randint(1, 12), random.randint(1, 28))
    pw = hashlib.md5(f"pass{i}".encode()).hexdigest()  # 旧仕様：塩なしMD5
    members.append((i, name, addr, tel, created, withdrawn))
    rows.append(f"({q(f'user{i:04d}@example.jp')},{q(pw)},{q(name)},{q(f'{random.randint(100,999)}-{random.randint(1000,9999)}')},"
                f"{q(addr)},{q(tel)},{q(bday.strftime('%Y-%m-%d'))},{q('withdrawn' if withdrawn else 'active')},{ts(created)},"
                f"{ts(withdrawn) if withdrawn else 'NULL'})")
for k in range(0, len(rows), 400):
    out.append("INSERT INTO members (email,password,name,zip,address,tel,birthday,status,created_at,withdrawn_at) VALUES\n"
               + ",\n".join(rows[k:k + 400]) + ";")

# 注文と、2018-05まで保存していたカード情報
orows, crows = [], []
oid = 0
for (mid, name, addr, tel, created, withdrawn) in members:
    end = withdrawn or now
    for _ in range(random.choice([0, 1, 1, 2, 3, 5, 8])):
        if created >= end:
            break
        oid += 1
        at = rand_dt(created, end)
        total = sum(random.choice(ITEMS)[1] for _ in range(random.randint(1, 4))) + 800
        orows.append(f"({mid},{q(name)},{q(addr)},{q(tel)},{total},{ts(at)})")
        if at < datetime(2018, 5, 31):
            crows.append(f"({oid},{q(random.choice(TEST_CARDS))},{q(f'{random.randint(1,12):02d}/{random.randint(19,24)}')},"
                         f"{q('TARO SUBARA')},{ts(at)})")
for k in range(0, len(orows), 500):
    out.append("INSERT INTO orders (member_id,ship_name,ship_address,ship_tel,total,ordered_at) VALUES\n" + ",\n".join(orows[k:k + 500]) + ";")
for k in range(0, len(crows), 500):
    out.append("INSERT INTO order_cards_old (order_id,card_no,card_exp,card_name,created_at) VALUES\n" + ",\n".join(crows[k:k + 500]) + ";")

# 管理者アカウント。パスワードは手元専用のダミー
md5 = lambda s: hashlib.md5(s.encode()).hexdigest()
admins = [
    ("tencho", "owner", 1, "店長", datetime(2012, 3, 20), datetime(2026, 10, 13, 18, 2)),
    ("admin", "owner", 1, "制作会社が初期設定で作ったもの", datetime(2012, 3, 15), datetime(2025, 2, 3, 11, 40)),
    ("yamada", "staff", 1, "出荷担当", datetime(2016, 6, 1), datetime(2023, 3, 30, 17, 55)),
    ("arbeit01", "staff", 1, "繁忙期アルバイト", datetime(2021, 11, 20), datetime(2022, 1, 8, 15, 10)),
    ("support2", "owner", 1, "", datetime(2026, 9, 18, 2, 14), datetime(2026, 10, 11, 3, 2)),
    ("kato", "staff", 1, "出荷担当", datetime(2024, 4, 1), datetime(2026, 10, 14, 8, 51)),
]
for login, role, active, note, created, last in admins:
    out.append(f"INSERT INTO admins (login,password,role,active,note,created_at,last_login) VALUES "
               f"({q(login)},{q(md5(login + '-local-only'))},{q(role)},{active},{q(note)},{ts(created)},{ts(last)});")

# 管理画面のログイン記録（直近90日）
lrows = []
d0 = now - timedelta(days=90)
day = d0
while day < now:
    for who in ("tencho", "kato"):
        if random.random() < 0.85:
            lrows.append(f"({q(who)},{q('192.0.2.10')},1,{ts(day.replace(hour=random.randint(8,18), minute=random.randint(0,59)))})")
    day += timedelta(days=1)
for d in [datetime(2026, 9, 18, 2, 14), datetime(2026, 9, 24, 3, 40), datetime(2026, 10, 2, 2, 55), datetime(2026, 10, 11, 3, 2)]:
    lrows.append(f"({q('support2')},{q('198.51.100.200')},1,{ts(d)})")
# 10月に入ってからの、よそからのログイン失敗
for _ in range(640):
    at = rand_dt(datetime(2026, 10, 3), datetime(2026, 10, 13))
    lrows.append(f"({q(random.choice(['admin','admin','tencho','root','shop','test']))},{q('203.0.113.' + str(random.randint(2,250)))},0,{ts(at)})")
lrows.sort(key=lambda r: r.split(",")[-1])
for k in range(0, len(lrows), 500):
    out.append("INSERT INTO admin_login_log (login,ip,success,at) VALUES\n" + ",\n".join(lrows[k:k + 500]) + ";")

OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(OUT, "members", len(members), "orders", oid, "cards", len(crows), "loginlog", len(lrows))
