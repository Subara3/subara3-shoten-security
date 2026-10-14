#!/bin/sh
# 直す前に、消すものと記録を控えて、ハッシュを取っておく（インシデントとして扱うため）
D=../evidence/$(date +%Y%m%d-%H%M%S)
mkdir -p "$D"
cp ../logs/access.log.sample "$D/access.log"
cp ../legacy/backup/shop_20190401.sql ../legacy/config.php.bak ../legacy/phpinfo.php "$D/"
docker compose -f ../docker-compose.yml exec -T db \
  mysqldump --default-character-set=utf8mb4 -ushop -pshop-local-only --no-tablespaces shop admins admin_login_log 2>/dev/null > "$D/admins_and_loginlog.sql"
( cd "$D" && sha256sum * > SHA256SUMS )
chmod -R a-w "$D"
echo "$D"; cat "$D/SHA256SUMS"
