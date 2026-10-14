#!/bin/sh
# IPA 2-1：公開ディレクトリに、アプリ以外のファイルが置かれていないか
ROOT=${1:-../legacy}
cd "$ROOT" && find . -type f \( -name '*.bak' -o -name '*.sql' -o -name '*.zip' -o -name '*.gz' \
  -o -name '*.old' -o -name '*~' -o -name 'phpinfo.php' -o -name '.env' \) | sort
