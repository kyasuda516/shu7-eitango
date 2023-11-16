#!/bin/bash
# 引数で受け取ったURIが200を返すか確かめる。
# 実行方法: $ <このスクリプトのパス> <URI>
# URIは / /bunch /bunch/fri /admin/grafana など。省略するとルート（/）に。
set -eu

abs_url="https://localhost"

# 引数の数をチェックして適宜処理を実行
case $# in
  0)
    :  # 何もしない
    ;;
  1)
    if [[ $1 =~ ^/ ]]; then
      abs_url="${abs_url}${1}"
    else
      echo "Error: Invalid value: The first character of uri must be '/'"
      exit 1
    fi
    ;;
  *)
    echo "invalid usage"
    echo "usage: /to/path/${this_basename} [uri]"
    exit 1
    ;;
esac

# テスト
test $(curl -kLI $abs_url -o /dev/null -w '%{http_code}\n' -s) -eq 200