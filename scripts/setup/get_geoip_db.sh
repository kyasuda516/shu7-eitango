#!/bin/bash
# GeoLite2 (GeoIP2) データベースを取得。
set -eu

docker compose -f compose.yaml -f compose.prod.yaml run --rm \
  -e GEOIPUPDATE_ACCOUNT_ID=$(sed -n 1p ./secrets/geoip_id.secret) \
  -e GEOIPUPDATE_LICENSE_KEY=$(sed -n 1p ./secrets/geoip_key.secret) \
  geoip geoipupdate
docker compose -f compose.yaml -f compose.prod.yaml rm -fsv geoip