#!/bin/bash

set -eu

TOPDIR="$(cd "$(dirname "$0")/.." || exit 1; pwd)"
export PATH="$TOPDIR/examples:$HOME/bin:$PATH"

cd $TOPDIR

datadir="data/$(date '+%Y-%m-%d')"

mkdir -p "$datadir"

exec >> "$datadir/log" 2>&1

echo "=================================================="
date

if [ ! -f "$datadir/step1" ]; then
    get.sh
    touch "$datadir/step1"
fi

get_pages.sh casares data/*/casares-*.json

echo "Our occupancy rate:"
compute_occupancy.py 2022-12-31 $(ls "$TOPDIR"/data/$(date '+%Y-%m-%d')/casares/678080393507867259.json)

echo "All occupancy rates:"
compute_occupancy.py 2022-12-31 $(ls "$TOPDIR"/data/$(date '+%Y-%m-%d')/casares/*.json)|sort -n

# cron.sh ends here
