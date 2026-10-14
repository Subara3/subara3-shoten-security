# ロリポップでの実測（2026-10-14、subara3.com/<TARGET_DIR>/、中身はダミーだけ）

| URL | .htaccess なし | .htaccess あり |
|---|---|---|
| / | 200 | 200 |
| /backup/（一覧） | 403 | 403 |
| /backup/shop_dummy.sql | **200** | 403 |
| /config.php.bak | 403 | 403 |
| /phpinfo.php | **200** | 403 |
| /admin/（Require ip で店舗回線だけ） | 200 | 403 |
| /.htaccess | 403 | 403 |

- サイト全体の .htaccess に一覧表示・.bak を止める規則は無い。/backup/ と .bak の 403 はロリポップ側の初期設定によるもの
- `.sql` と `phpinfo.php` は初期設定では素通しになる
- `X-Powered-By: PHP/8.3.35` は .htaccess の `Header unset` / `Header always unset` では消えなかった。PHP で `header_remove('X-Powered-By')` を呼ぶと消えた
