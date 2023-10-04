#!/bin/bash
set -eu

cd ~/sh7e/
docker compose -f compose.yaml -f compose.prod.yaml run --rm \
  -e GEOIPUPDATE_ACCOUNT_ID=$(sed -n 1p ./secrets/geoip_id.secret) \
  -e GEOIPUPDATE_LICENSE_KEY=$(sed -n 1p ./secrets/geoip_key.secret) \
  geoip geoipupdate