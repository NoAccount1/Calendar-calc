import icalendar
from icalendar import Calendar, Event, prop
import requests
from requests import ConnectionError

from datetime import datetime, timedelta as td
import json
import os

from pprint import pprint

ical_urls = {
    "tp10_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=94072&projectId=11&calType=ical&nbWeeks=16",
    "tp11_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270585&projectId=11&calType=ical&nbWeeks=16",
}


def print_dir(obj):
    for i in dir(obj):
        print(i)


def main():
    ical_files = next(os.walk("cal"), (None, None, []))[2]  # List ICS files from urls

    # Refresh ICS files on disk
    try:
        for name, url in ical_urls.items():
            if not f"{name}.ics" in ical_files:
                urlfile = requests.get(url).content.decode()
                with open(f"cal/{name}.ics", "w+") as file:
                    file.write(urlfile)
                print(f"Getting file {name}")
    except ConnectionError as err:
        print(f"An error occured : \n{err}")

    ical_files = next(os.walk("cal"), (None, None, []))[2]  # Refresh local ics files
    calendars = {}
    for file in ical_files:
        with open(f"cal/{file}", "r") as ics_file:
            cal = Calendar.from_ical(ics_file.read())

            metadata = dict(cal.items())

            calendars[file] = cal.subcomponents
    test_date = datetime(2023, 12, 1, 14).astimezone()

    hours = [8, 10, 14, 16]

    merged = []

    date = datetime(2023, 11, 26, 8)
    while date < datetime(2024, 7, 1, 8):  # Checking every hour of class
        if hours.index(date.hour) == 3 or date.weekday() == 6:
            date += td(days=1)
        if date.weekday() == 5:
            date += td(days=2)
        date = date.replace(hour=hours[(hours.index(date.hour) + 1) % 4])

        event_tp11 = next(
            (
                i["dtstart"]
                for i in calendars["tp11_1a.ics"]
                if i["DTSTART"].dt.astimezone() == date.astimezone()
            ),
            None,
        )
        event_tp10 = next(
            (
                i["dtstart"]
                for i in calendars["tp10_1a.ics"]
                if i["DTSTART"].dt.astimezone() == date.astimezone()
            ),
            None,
        )

        if not event_tp10 and not event_tp11:
            merged.append(date.astimezone().ctime())

    pprint(merged)

    print(f"len = {len(merged)}")


if __name__ == "__main__":
    main()
