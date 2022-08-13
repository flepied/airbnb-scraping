#!/usr/bin/env python

import json
import statistics
import sys

if len(sys.argv) < 3:
    print(
        f"Usage: {sys.argv[0]} <json file> <name>:<airnbnb id> [<name>:<airnbnb id>]",
        file=sys.stderr,
    )
    sys.exit(1)

airbnb = {}
for arg in sys.argv[2:]:
    name, id = arg.split(":")
    airbnb[id] = name
elts = json.load(open(sys.argv[1]))
prices = [e["price"] for e in elts]
mean = statistics.mean(prices)
stdev = statistics.stdev(prices)
# filter prices that are outside of the standard deviation
min_price = mean - stdev
max_price = mean + stdev
filtered_prices = [p for p in prices if p <= max_price and p >= min_price]
# compute the median of this filtered prices
median = statistics.median(filtered_prices)

extra = ""
for id in airbnb:
    listing = [e for e in elts if e["url"].find(id) >= 0]
    page = listing[0]["page"] if len(listing) > 0 else None
    price = listing[0]["price"] if len(listing) > 0 else 0
    extra += f" {airbnb[id]}={price}€ page {page}"

print(f"listings={len(prices)} median={median:#.2f}€{extra}")

# analyze.py ends here
