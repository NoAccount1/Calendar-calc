import icalendar
from icalendar import Calendar, Event, prop
import requests
from requests import ConnectionError

import datetime
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
    # Collecting ICS files
    ical_files = next(os.walk("cal"), (None, None, []))[2]

    try:
        for name, url in ical_urls.items():
            if not f"{name}.ics" in ical_files:
                urlfile = requests.get(url).content.decode()
                with open(f"cal/{name}.ics", "w+") as file:
                    file.write(urlfile)
                print(f"Getting file {name}")
    except ConnectionError as err:
        print(f"An error occured : \n{err}")

    ical_files = next(os.walk("cal"), (None, None, []))[2] # refresh file list
    calendars = []
    for file in ical_files:
        with open(f"cal/{file}", "r") as ics_file:
            cal = Calendar.from_ical(ics_file.read())

            metadata = dict(cal.items())

            calendars.append({file: cal.subcomponents})
    print(calendars)

if __name__ == "__main__":
    main()
