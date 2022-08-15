#!/usr/bin/env python3

import json
import operator
import os
import sys

if len(sys.argv) < 3:
    print(
        f"Usage: {sys.argv[0]} <diretory1> <directory2>...",
        file=sys.stderr,
    )
    sys.exit(1)

# Load data
dirs = sys.argv[1:]
dates = {}
all_listings = set()
for d in dirs:
    dir_name = os.path.basename(d)
    for f in os.listdir(d):
        if f.endswith(".json"):
            file_name = os.path.basename(f)[:-5]
            file_path = os.path.join(d, f)
            print(f"Loading {file_path}")
            with open(file_path) as json_file:
                listings = [
                    data["url"]
                    for data in json.load(json_file)
                    if data["bedrooms"] >= 3
                ]
            if file_name not in dates:
                dates[file_name] = {}
            dates[file_name][dir_name] = listings
            all_listings = all_listings.union(set(listings))

# Process data
print(f"total number of listings: {len(all_listings)}")
rented = {}
sorted_dates = sorted(dates)
for d in sorted_dates:
    print(f"Analysing {d}")
    scraped_dates = sorted(dates[d])
    print("Evolution of the number of listings: ", end="")
    for f in scraped_dates:
        print(f"{len(dates[d][f])} ", end="")
    print()
    last = set(dates[d][scraped_dates[-1]])
    for removed in all_listings.difference(last):
        print(f"Listing {removed} removed")
        if removed in rented:
            rented[removed] += 1
        else:
            rented[removed] = 1
print()
print("Ranking")
for url, number in sorted(rented.items(), key=operator.itemgetter(1), reverse=True):
    print(f"{url} rented {number} times")

# find_changes.py ends here
