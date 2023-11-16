#!/bin/bash
# secrets.jsonに書かれたシークレットファイルを書き出す。
# --overwriteオプションをつけることで、ファイルが存在しても書き換えられる。
set -eu

current_dir=$(cd $(dirname $0) && pwd)
prj_dir="${current_dir}/../.."
this_basename=$(basename -- $0)

# 引数の解析
overwrite=1  # 偽
while (( $# > 0 ))
do
  case $1 in
    --overwrite)
      overwrite=0  # 真にする
      ;;
    -h | --help)
      echo "usage: /to/path/${this_basename} [--overwrite]"
      exit 0
      ;;
    -*)
      echo "invalid option: ${1}"
      echo "usage: /to/path/${this_basename} [--overwrite]"
      exit 1
      ;;
    *)
      echo "unknown ${this_basename}'s command: '${1}'"
      echo "usage: /to/path/${this_basename} [--overwrite]"
      exit 1
      ;;
  esac
  shift
done

cat "${current_dir}/data/secrets.json" |
jq -c '.[]' |
while read -r array; do
  filestem=$(echo "${array}" | jq -r '.name')
  dummy_value=$(echo "${array}" | jq -r '.dummy_value')
  filepath="${prj_dir}/secrets/${filestem}.secret"
  if [ -f $filepath ]; then  # ファイルが存在する場合
    if [ $overwrite -ne 0 ]; then continue; fi   # overwriteが0（真）でないならスキップ
  fi
  echo -n $dummy_value > $filepath
done