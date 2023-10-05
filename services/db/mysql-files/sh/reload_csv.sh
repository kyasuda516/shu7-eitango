#!/bin/bash
# 実行方法: $ <このスクリプトのパス> <テーブル名>
# なお、このスクリプトはどこに移動しても問題なく動きます。
set -eu

# 引数の数をチェック
if [ $# -ne 1 ]; then
  echo "ERROR: usage: ${0} [table]"
  exit 1
fi

# メイン
sql_files=/var/lib/mysql-files/sql
rootpw=$(sed -n 1p $MYSQL_ROOT_PASSWORD_FILE)
dbdb=$(sed -n 1p $MYSQL_DATABASE_FILE)
mysql -u root -p$rootpw $dbdb -e "$(sed s/%tableName%/${1}/g ${sql_files}/_update_base.sql)"
echo "Successfully reloaded csv!"