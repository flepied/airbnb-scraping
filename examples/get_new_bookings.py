#!/usr/bin/env python3

import json
import os
import re
import sys
from datetime import datetime

PROPERTY_REGEXP = re.compile(r"^[0-9]+\.json$")


def clean_up_dates(end, data):
    invalid_dates = []
    for key in data1:
        if datetime.strptime(key, "%Y-%m-%d") > end:
            invalid_dates.append(key)
    for key in invalid_dates:
        del data[key]


if len(sys.argv) != 4:
    print(
        f"Usage: {sys.argv[0]} <end date YYYY-mm-dd> <first directory> <second directory>",
        file=sys.stderr,
    )
    sys.exit(1)

end = datetime.strptime(sys.argv[1], "%Y-%m-%d")
dir1 = sys.argv[2]
dir2 = sys.argv[3]

for basename in os.listdir(dir1):
    if not PROPERTY_REGEXP.match(basename):
        continue
    if os.path.exists(os.path.join(dir2, basename)):
        with open(os.path.join(dir1, basename)) as json_file:
            try:
                data1 = json.load(json_file)
            except Exception:
                continue
        with open(os.path.join(dir2, basename)) as json_file:
            try:
                data2 = json.load(json_file)
            except Exception:
                continue
        clean_up_dates(end, data1)
        clean_up_dates(end, data2)
        for date in data1:
            if date in data2:
                if data1[date] != data2[date]:
                    print(
                        f"https://www.airbnb.com/rooms/{basename[:-5]} {'booked' if not data1[date] else 'not booked'} on {date}"
                    )

# get_new_bookings.py ends here
