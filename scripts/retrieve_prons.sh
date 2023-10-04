#!/bin/bash
set -eu

cd ~/sh7e/
docker compose -f compose.yaml -f compose.prod.yaml exec -T app python set_pron_caches.py 5:49:50