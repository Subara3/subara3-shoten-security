#!/bin/sh
# 2-1b で出たURLについて、いつ・どこから・何バイト持っていかれたか
LOG=${1:-../logs/access.log.sample}
PATTERN=${2:-'/backup/|\.bak|\.sql'}
awk '$9 == 200' "$LOG" | grep -E "\"GET [^ ]*($PATTERN)" | awk '{ print $4, $1, $7, $10 }' | tr -d '['
