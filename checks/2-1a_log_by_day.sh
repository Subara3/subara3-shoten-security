#!/bin/sh
# IPA 2-1：外部公開アプリのログに異常がないか。直近1か月 → 3か月の順に見る
# 日ごとの件数と、そのうち 4xx / 5xx の件数を並べる
LOG=${1:-../logs/access.log.sample}
DAYS=${2:-30}
awk -v days="$DAYS" '
  {
    split($4, a, /[\[\/:]/); d = a[4] "-" a[3] "-" a[2]
    total[d]++; if ($9 ~ /^4/) c4[d]++; if ($9 ~ /^5/) c5[d]++
  }
  END { for (d in total) printf "%s %6d %6d %4d\n", d, total[d], c4[d], c5[d] }
' "$LOG" | sed 's/Jul/07/;s/Aug/08/;s/Sep/09/;s/Oct/10/' | sort | tail -n "$DAYS" \
  | awk 'BEGIN { print "日付          総数    4xx  5xx" } { print }'
