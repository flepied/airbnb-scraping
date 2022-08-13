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
            if "https://www.airbnb.fr/rooms/16584435" in listings:
                print(f"ERROR {file_path}")
            if file_name not in dates:
                dates[file_name] = {}
            dates[file_name][dir_name] = listings

# Process data
rented = {}
for d in sorted(dates):
    print(f"Analysing {d}")
    scraped_dates = sorted(dates[d])
    print("Evolution of the number of listings: ", end="")
    for f in scraped_dates:
        print(f"{len(dates[d][f])} ", end="")
    print()
    last = set(dates[d][scraped_dates[-1]])
    previous = set(dates[d][scraped_dates[0]])
    for f in scraped_dates[1:-1]:
        previous = previous.union(set(dates[d][f]))
    for removed in previous.difference(last):
        print(f"Listing {removed} removed")
        if removed in rented:
            rented[removed] += 1
        else:
            rented[removed] = 1
    for added in last.difference(previous):
        print(f"Listing {added} added")
print()
print("Ranking")
for url, number in sorted(rented.items(), key=operator.itemgetter(1), reverse=True):
    print(f"{url} rented {number} times")

# find_changes.py ends here
