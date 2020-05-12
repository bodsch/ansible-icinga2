#!/bin/bash

requester="${1:-local}"

lock_file=/run/icinga2/restart.lock

sleep $(shuf -i 5-30 -n 1)

exec 100>${lock_file} || exit 0
flock --timeout 10 --exclusive 100 || exit 0

trap 'rm -f ${lock_file}' EXIT

logger "external request to restart the icinga2 master (${requester})"

set -e

icinga2 daemon -C

systemctl reload icinga2

echo "Sleeping for 2 seconds…"

sleep 2
