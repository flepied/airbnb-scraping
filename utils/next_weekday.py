#!/usr/bin/env python

from datetime import datetime, timedelta


def get_next_weekday_from(startdate, weekday):
    """
    @startdate: given date
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    t = timedelta((7 + weekday - startdate.weekday()) % 7)
    return (startdate + t).strftime("%Y-%m-%d")


def get_next_weekday(weekday, weeks=0):
    start = datetime.now() + timedelta(7 * weeks)
    return get_next_weekday_from(start, weekday)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(
            f"Usage: {sys.argv[0]} <week day> <weeks>\n  weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)\n  weeks: number of weeks to compute as a positive integer",
            file=sys.stderr,
        )
        sys.exit(1)
    print(get_next_weekday(int(sys.argv[1]), int(sys.argv[2])))
