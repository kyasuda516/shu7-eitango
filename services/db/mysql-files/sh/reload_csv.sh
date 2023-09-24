#!/bin/bash

# 実行方法: $ <このスクリプトのパス> <テーブル名>
# なお、このスクリプトはどこに移動しても問題なく動きます。

# 引数チェック
if [ $# != 1 ]; then
  echo "Error! Valid usage: ${0} <table_name>"
  exit 1
fi

# メイン
sql_files=/var/lib/mysql-files/sql
rootpw=$(sed -n 1p $MYSQL_ROOT_PASSWORD_FILE)
mysql -u root -p$rootpw $MYSQL_DATABASE -e "$(sed s/%tableName%/${1}/g ${sql_files}/_update_base.sql)"
echo "Successfully reloaded csv!"