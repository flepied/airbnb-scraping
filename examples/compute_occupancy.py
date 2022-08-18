#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime

if len(sys.argv) < 3:
    print(
        f"Usage: {sys.argv[0]} <end date YYYY-mm-dd> <json file>...",
        file=sys.stderr,
    )
    sys.exit(1)

end = datetime.strptime(sys.argv[1], "%Y-%m-%d")
files = sys.argv[2:]

for f in files:
    with open(f) as json_file:
        try:
            data = json.load(json_file)
        except:
            continue
    invalid_dates = []
    for key in data:
        if datetime.strptime(key, "%Y-%m-%d") > end:
            invalid_dates.append(key)
    for key in invalid_dates:
        del data[key]
    blocked = 0
    for key in data:
        if data[key]:
            blocked += 1
    print(
        f"{blocked/len(data)*100:#.2f}% for https://www.airbnb.com/rooms/{os.path.basename(f)[:-5]}"
    )

# compute_occupancy.py ends here
