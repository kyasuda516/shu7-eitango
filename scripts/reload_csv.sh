#!/bin/bash
# 実行方法: $ <このスクリプトのパス> <テーブル名>
# なお、このスクリプトはどこに移動しても問題なく動く。
set -eu

# 引数の数をチェック
if [ $# -ne 1 ]; then
  echo "ERROR: usage: ${0} [table]"
  exit 1
fi

# 引数の値をチェック
VALID_TABLES=('pool' 'pos_config')
if printf '%s\n' "${VALID_TABLES[@]}" | grep -qx $1; then
  :  # pass
else
  echo "ERROR: invalid value '${1}': No such table"
  exit 1
fi

docker compose -f compose.yaml -f compose.prod.yaml exec db /bin/bash /var/lib/mysql-files/sh/reload_csv.sh $1