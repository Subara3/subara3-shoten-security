# すばら３商店 セキュリティ点検

Zennの記事「お客さんからの「うちは大丈夫？」に答えるため、IPAの点検項目をレガシーPHPのECサイトで上から順にやってみた」で使った再現環境と点検スクリプトです。

https://zenn.dev/subara3/articles/b90ff538d87aa6

IPA「不正アクセスによる漏えい等の事案を踏まえ、速やかに実施すべき対策等について」（2026年10月9日）の項目に沿って、架空のECサイト「すばら３商店」を点検します。

## 注意

- `legacy/` は、わざと古くて危ない作りにしてあります。インターネットには公開せず、手元のDockerだけで動かしてください。`docker-compose.yml` は `127.0.0.1` にだけポートを開けています
- 会員・注文・ログはすべて生成したダミーです。IPアドレスは文書用の範囲（192.0.2.0/24、198.51.100.0/24、203.0.113.0/24）だけを使っています
- 攻撃のための道具は入っていません。中身は、守る側の点検と修正だけです

## 中身

```
docker-compose.yml        点検前の店（PHP 7.4 + MySQL 5.7）。http://127.0.0.1:8080/
docker-compose.fixed.yml  点検後の店（PHP 8.3）。http://127.0.0.1:8081/
legacy/                   点検前のソース
fixed/                    点検後のソース（public/ が公開ディレクトリ、app/ はその外）
tools/                    ダミーデータ・アクセスログ・バックアップを作るスクリプト
checks/                   IPAの項目ごとの点検スクリプト。out/ は記事に載せた出力
fixes/                    アカウントと保有データを直すSQL
lolipop/                  レンタルサーバで .htaccess の動きを確かめるためのダミーと手順
```

## 動かしかた

```sh
# ダミーデータを作る
python tools/gen_data.py db/01_schema_data.sql
python tools/gen_logs.py logs/access.log.sample
python tools/make_dummy_backup.py legacy/backup/shop_20190401.sql

# 点検前の店を起動する
docker compose up -d --build

# 古いライブラリを入れる（今のComposerは脆弱な版を入れないので、legacy/composer.json で止める設定を切っています）
docker run --rm -v "$PWD/legacy:/app" -w /app composer:2 install
```

## 点検

`checks/` で実行します。

| IPAの項目 | スクリプト | やること |
|---|---|---|
| 2-1 | `2-1a_log_by_day.sh [ログ] [日数]` | アクセスログを日ごとに数えて、4xxと5xxの増え方を見る |
| 2-1 | `2-1b_unexpected_200.sh [ログ]` | アプリのURLの一覧にないのに200を返したリクエストを数える |
| 2-1 | `2-1c_who_got_it.sh [ログ] [パターン]` | 上で出たURLを、いつ・どこから・何バイト返したか |
| 2-1 | `2-1d_docroot_files.sh [公開ディレクトリ]` | 控え・ダンプ・`phpinfo.php` が置かれていないか |
| 2-1 | `2-1f_dump_scope.sql` | 持ち出されたバックアップに入っていた範囲を数える |
| 2-2 | `2-2_accounts.sql` | 管理者アカウントの作成日・最終ログイン・接続元・ログイン失敗 |
| 2-3 | `2-3_data_inventory.sql` | 退会者・古い注文・昔のカード情報を数える |
| 異常があったら | `0_evidence.sh` | 直す前に控えを取り、ハッシュを残す |

SQLは `./run_db.sh 2-2_accounts.sql` のように流します。

自分のサイトで使うときは、`2-1b_unexpected_200.sh` の `ALLOW` を自分のアプリのURLに、ログの形式を自分のサーバに合わせてください。

## 直す

```sh
cd checks
./0_evidence.sh                        # 先に控えを取る
./run_db.sh ../fixes/2-2_accounts.sql  # アカウントを止め、作成・変更を記録するトリガーを入れる
./run_db.sh ../fixes/2-3_data.sql      # カード情報の表を消し、退会者の個人情報を消す
cd ..
docker run --rm -v "$PWD/fixed/app:/app" -w /app composer:2 install
docker compose -f docker-compose.fixed.yml up -d --build
```

## レンタルサーバで確かめる

`lolipop/before/` の中身（中身は「dummy」の文字だけ）をサーバの適当なディレクトリに置き、`lolipop/probe.sh https://example.com/そのディレクトリ` を実行します。そのあと `htaccess.root` を `.htaccess`、`htaccess.admin` を `admin/.htaccess` として置いて、もう一度実行します。ロリポップでの結果は `lolipop/RESULT.md` にあります。確かめ終わったら消してください。

## ライセンス

MIT
