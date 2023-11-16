#!/bin/bash
# セットアップをおこなう。
# ※このスクリプトは、誤って運用中に実行してしまっても問題はおこらない。
set -eu

current_dir=$(cd $(dirname $0) && pwd)

source "${current_dir}/export_secrets.sh"
source "${current_dir}/create_volumes.sh"
source "${current_dir}/get_geoip_db.sh"
