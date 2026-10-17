# nginx で使う

`subara3-shoten.conf` は、点検後の `.htaccess`（Apache）と同じ狙いを nginx で書いたものです。
Apache ではなく nginx のサイトで、同じ点検結果を再現したいときに使います。

## 置きかた

1. `server_name`、`root`、`allow` のIP、`fastcgi_pass`（php-fpm の宛先）を自分のサイトに合わせる
2. `sites-available/` などに置いて有効化するか、既存の `server { ... }` に `location` を移植する
3. `nginx -t` で構文を確かめてから `nginx -s reload`

## 補足

- `fastcgi_hide_header X-Powered-By;` は、レスポンスヘッダから `X-Powered-By` を外します。合わせて php.ini で `expose_php = Off` にしておくと、PHP自身が付けるのをやめます。
- `server_tokens off;` は、nginx の版をヘッダやエラーページに出さない設定です。
- 管理画面を複数人・複数拠点から開く場合は、`allow` の行を増やします。固定IPがないなら、IP制限ではなくVPNやBasic認証、多要素認証に替える判断になります。
