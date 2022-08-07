#!/bin/bash

set -eu

TOPDIR="$(cd $(dirname $0)/..; pwd)"
export PATH="$TOPDIR/utils:$PATH"

if [ ! -r "$TOPDIR/.tox/functional/bin/activate" ]; then
    tox -efunctional --notest
fi

. "$TOPDIR/.tox/functional/bin/activate"

scrap() {
    LOCATION="$1"
    OUTPUT="$2"
    START="$3"
    END="$4"
    URL="https://www.airbnb.fr/s/Casares-del-Sol--Casares/homes?flexible_trip_lengths%5B%5D=one_week&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&adults=6&source=structured_search_input_header&search_type=filter_change&pagination_search=true&l2_property_type_ids%5B%5D=3&room_types%5B%5D=Entire%20home%2Fapt&amenities%5B%5D=4&amenities%5B%5D=5&amenities%5B%5D=7&amenities%5B%5D=9&amenities%5B%5D=46&amenities%5B%5D=58&amenities%5B%5D=33&amenities%5B%5D=8&min_bedrooms=3&checkin=${START}&checkout=${END}"
    python "$TOPDIR/airbnb_listing_scraper.py" "$URL" > "${OUTPUT}-${START}.json"
    json2csv.py "${OUTPUT}-${START}"
}

datadir="data/$(date '+%Y-%m-%d')"
location="Casares-del-Sol--Casares"
output="$datadir/casares"

mkdir -p $datadir

# get all data for the next 3 months (12 weeks)
for week in $(seq 12); do
    saturday="$(next_weekday.py 5 $week)"
    next_saturday="$(next_weekday.py 5 $(($week + 1)))"
    scrap "$location" "$output" "$saturday" "$next_saturday"
done

for f in "$datadir"/*.json; do
    echo -n "$(basename $f .json) "
    "$TOPDIR/examples/analyze.py" "$f" 573780296900171962
done

# get.sh ends here
