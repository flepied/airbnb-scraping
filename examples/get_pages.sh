#!/bin/bash

set -eux

TOPDIR="$(cd $(dirname $0)/..; pwd)"
export PATH="$TOPDIR/utils:$PATH"

if [ ! -r "$TOPDIR/.tox/functional/bin/activate" ]; then
    tox -efunctional --notest
fi

. "$TOPDIR/.tox/functional/bin/activate"

datadir="data/$(date '+%Y-%m-%d')"

mkdir -p $datadir

for f in "$@"; do
    jq -r .[].url $f
done | sort -u | while read url; do
    output="${datadir}/$(basename $url).json"
    if [ ! -r "$output" ] || [ ! -s "$output" ]; then
        python3 "$TOPDIR"/airbnb_page_scraper.py "$url" > "${output}"
    else
        echo "Already processed $output"
    fi
done

# get_pages.sh ends here
