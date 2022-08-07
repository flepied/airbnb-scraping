#!/usr/bin/env python

import json
import statistics
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <json file> <airnbnb id>", file=sys.stderr)
    sys.exit(1)

elts = json.load(open(sys.argv[1]))
prices = [e["price"] for e in elts]
median = statistics.median(prices)
mean = statistics.mean(prices)
stdev = statistics.stdev(prices)
page = [e["page"] for e in elts if e["url"].find(sys.argv[2]) >= 0]
page = page[0] if len(page) > 0 else None

print(
    f"listings={len(prices)} median={median:#.2f}€ mean={mean:#.2f}€ stdev={stdev:#.2f}€ min={min(prices)}€ max={max(prices)}€ page {page}"
)

# analyze.py ends here
