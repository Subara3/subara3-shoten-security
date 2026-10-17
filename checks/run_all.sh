#!/bin/sh
# すべての点検を順に実行して、結果を1枚のMarkdown（out/REPORT.md）にまとめる。
# 使い方: cd checks && ./run_all.sh [ログ] [公開ディレクトリ]
#   ログのデフォルトは ../logs/access.log.sample、公開ディレクトリは ../legacy。
# SQLの点検（2-2, 2-3）は docker compose の db が起動している前提。
# 起動していない項目は「実行できませんでした」と記録して、残りは続ける。
LOG=${1:-../logs/access.log.sample}
ROOT=${2:-../legacy}
OUT=out/REPORT.md
mkdir -p out

sec() { printf '\n## %s\n' "$1" >> "$OUT"; }
sub() { printf '\n### %s\n' "$1" >> "$OUT"; }
run() {
  # run <コマンド...> : 出力をコードブロックにして追記。失敗したら注記を残す。
  printf '\n```\n' >> "$OUT"
  if "$@" >> "$OUT" 2>/dev/null; then :; else
    printf '(実行できませんでした。db の起動やログの有無を確かめてください)\n' >> "$OUT"
  fi
  printf '```\n' >> "$OUT"
}

{
  echo "# すばら３商店 点検レポート"
  echo
  echo "- 実行日時: $(date '+%Y-%m-%d %H:%M:%S')"
  echo "- 対象ログ: $LOG"
  echo "- 公開ディレクトリ: $ROOT"
  echo
  echo "IPAの項目に沿って点検した結果です。異常があれば、直す前に \`0_evidence.sh\` で控えを取ってください。"
} > "$OUT"

sec "2-1 外部公開アプリケーションの精査"
sub "ログの日ごとの件数（直近30日）"
run sh 2-1a_log_by_day.sh "$LOG" 30
sub "ログの日ごとの件数（直近90日）"
run sh 2-1a_log_by_day.sh "$LOG" 90
sub "許可リストにないのに200を返したURL"
run sh 2-1b_unexpected_200.sh "$LOG"
sub "そのURLを、いつ・どこから・何バイト返したか"
run sh 2-1c_who_got_it.sh "$LOG"
sub "公開ディレクトリに残っている非アプリのファイル"
run sh 2-1d_docroot_files.sh "$ROOT"
sub "不審なPHP（eval / base64_decode など）"
run sh 2-1h_suspicious_php.sh "$ROOT"

sec "2-2 アカウントと外部サービスの洗い出し"
sub "管理者アカウントの作成日・最終ログイン・接続元・ログイン失敗"
run sh run_db.sh 2-2_accounts.sql

sec "2-3 保有データの再点検"
sub "退会者・古い注文・昔のカード情報"
run sh run_db.sh 2-3_data_inventory.sql

echo "書き出しました: $OUT"
