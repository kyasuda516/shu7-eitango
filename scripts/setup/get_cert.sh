#!/bin/bash
# SSLサーバ証明書を取得。
set -eu

cd ~/sh7e/
docker compose -f compose.yaml -f compose.prod.yaml run --rm cert renew
docker compose -f compose.yaml -f compose.prod.yaml rm -fsv cert