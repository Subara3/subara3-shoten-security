#!/bin/sh
# 点検用SQLを手元のDBに流す。例: ./run_db.sh 2-2_accounts.sql
docker compose -f ../docker-compose.yml exec -T db \
  mysql --default-character-set=utf8mb4 -ushop -pshop-local-only shop -t < "$1" 2>/dev/null
