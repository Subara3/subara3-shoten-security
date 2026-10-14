#!/bin/sh
# レンタルサーバに置いたダミーの置き物へ外からリクエストして、状態コードを並べる
# 使い方: ./probe.sh https://example.com/置いたディレクトリ
BASE=${1:?usage: ./probe.sh BASE_URL}
for p in "" backup/ backup/shop_dummy.sql config.php.bak phpinfo.php admin/ .htaccess; do
  printf '%-24s %s\n' "/$p" "$(curl -s -o /dev/null -w '%{http_code}' "$BASE/$p")"
done
echo "--- X-Powered-By"
curl -sI "$BASE/" | grep -i 'x-powered-by' || echo "(なし)"
