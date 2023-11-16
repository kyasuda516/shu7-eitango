#!/bin/bash
# external_volumes.txt に書かれたボリュームを作成。
# すでにあった場合、新しく作り直すわけではないことに注意。
set -eu

current_dir=$(cd $(dirname $0) && pwd)

while read line2
do
  volume=$(sed -r 's/^[[:space:]]*|[[:space:]]*$//g' <<< $line2)
  if [ "$volume" != "" ]; then
    docker volume create "${volume}"
  fi
done < "${current_dir}/data/external_volumes.txt"