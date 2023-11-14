#!/bin/bash
# このスクリプトは、誤って運用中に実行してしまっても問題はおこらない。
set -eu
current_dir=$(cd $(dirname $0) && pwd)
prj_dir="${current_dir}/../.."

# secret_files.txt に書かれたシークレットファイルを作成。
while read line1
do
  filename=$(sed -r 's/^[[:space:]]*|[[:space:]]*$//g' <<< $line1)
  if [ "$filename" != "" ]; then
    touch "${prj_dir}/secrets/${filename}"
    echo $filename
  fi
done < "${current_dir}/data/secret_files.txt"

# external_volumes.txt に書かれたボリュームを作成。
# すでにあった場合、新しく作り直すわけではないことに注意。
while read line2
do
  volume=$(sed -r 's/^[[:space:]]*|[[:space:]]*$//g' <<< $line2)
  if [ "$volume" != "" ]; then
    docker volume create "${volume}"
  fi
done < "${current_dir}/data/external_volumes.txt"

# GeoLite2 (GeoIP2) データベースを取得。
docker compose -f compose.yaml -f compose.prod.yaml run --rm \
  -e GEOIPUPDATE_ACCOUNT_ID=$(sed -n 1p ./secrets/geoip_id.secret) \
  -e GEOIPUPDATE_LICENSE_KEY=$(sed -n 1p ./secrets/geoip_key.secret) \
  geoip geoipupdate
docker compose -f compose.yaml -f compose.prod.yaml rm -fsv geoip