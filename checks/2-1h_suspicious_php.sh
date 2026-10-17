#!/bin/sh
# IPA 2-1：公開ディレクトリに、Webシェルのような不審なPHPが紛れていないか。
# 外から来た値をそのまま実行したり、コードを動的に組み立てたりする書き方を「候補」として挙げる。
# 見つかったら中身を人が確かめる前提。正規のアプリコードが引っかかること（誤検知）もある。
# その場合は、確認できたファイルを ALLOW に足して除外してよい。
ROOT=${1:-../legacy}
ALLOW=${2:-'/vendor/'}   # 誤検知を除外するパス（部分一致）。複数は | で区切る

# 動的にコードを実行する／外部コマンドを呼ぶ関数の呼び出しを探す
PATTERN='eval[[:space:]]*\(|assert[[:space:]]*\(|create_function[[:space:]]*\(|base64_decode[[:space:]]*\(|gzinflate[[:space:]]*\(|gzuncompress[[:space:]]*\(|str_rot13[[:space:]]*\(|system[[:space:]]*\(|shell_exec[[:space:]]*\(|passthru[[:space:]]*\(|popen[[:space:]]*\(|proc_open[[:space:]]*\('

hits=$(find "$ROOT" -type f -name '*.php' -print0 2>/dev/null \
  | xargs -0 grep -nEI "$PATTERN" 2>/dev/null \
  | grep -Ev "$ALLOW" \
  | sort)

if [ -n "$hits" ]; then
  printf '%s\n' "$hits"
else
  echo "(不審なPHPは見つかりませんでした)"
fi
