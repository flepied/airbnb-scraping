#!/usr/bin/env python

import csv
import json
import sys

if len(sys.argv) not in (1, 2):
    print(f"Usage: {sys.argv[0]} [<base name>]", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) == 1:
    data = json.load(sys.stdin)
    csv_file = sys.stdout
else:
    with open(sys.argv[1] + ".json") as json_file:
        data = json.load(json_file)
    csv_file = open(sys.argv[1] + ".csv", "w")

header = []
for elt in data:
    for key in elt.keys():
        if key not in header:
            header.append(key)

# create the csv writer object
csv_writer = csv.DictWriter(csv_file, fieldnames=header)

csv_writer.writeheader()
csv_writer.writerows(data)

csv_file.close()
