#!/bin/bash
set -eu

cd ~/sh7e/
docker compose -f compose.yaml -f compose.prod.yaml run --rm cert renew
docker compose -f compose.yaml -f compose.prod.yaml exec -T web nginx -s reload