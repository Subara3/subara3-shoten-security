#!/bin/sh
# IPA 2-1：アプリが本来返すURLの一覧（許可リスト）にないのに、200 を返したリクエスト
LOG=${1:-../logs/access.log.sample}
ALLOW='^/(|index\.php|login\.php|favicon\.ico|admin/(login|index|members|export|admins)\.php)$'
awk '$9 == 200 { print $7 }' "$LOG" | sed 's/?.*//' | grep -Ev "$ALLOW" | sort | uniq -c | sort -rn
