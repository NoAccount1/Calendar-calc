import icalendar
from icalendar import Calendar, Event, prop, vDDDTypes
import requests
from requests import ConnectionError

# from calendar import *
from datetime import datetime, timedelta as td
import json
import time  # performance test
import os

from pprint import pprint

from gui import run_gui

ical_urls = {
    "tp1_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270574&projectId=11&calType=ical&nbWeeks=16",
    "tp2_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270575&projectId=11&calType=ical&nbWeeks=16",
    "tp3_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270576&projectId=11&calType=ical&nbWeeks=16",
    "tp4_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270577&projectId=11&calType=ical&nbWeeks=16",
    "tp5_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270578&projectId=11&calType=ical&nbWeeks=16",
    "tp6_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270579&projectId=11&calType=ical&nbWeeks=16",
    "tp7_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270580&projectId=11&calType=ical&nbWeeks=16",
    "tp8_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270581&projectId=11&calType=ical&nbWeeks=16",
    "tp9_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270582&projectId=11&calType=ical&nbWeeks=16",
    "tp10_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270583&projectId=11&calType=ical&nbWeeks=16",
    "tp11_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270585&projectId=11&calType=ical&nbWeeks=16",
    "tp12_1a": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270586&projectId=11&calType=ical&nbWeeks=16",
    "tp10_3a_ia2r": "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=94072&projectId=11&calType=ical&nbWeeks=16",
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
    calendars, metadata = {}, {}
    for file in ical_files:
        with open(f"cal/{file}", "r") as ics_file:
            cal = Calendar.from_ical(ics_file.read())

            metadata[file] = dict(cal.items())

            calendars[file] = cal.subcomponents

    for cal in calendars:
        for i in [
            x for x in calendars[cal] if x["DTEND"].dt.hour - x["DTSTART"].dt.hour == 4
        ]:
            date_start = i["DTSTART"]
            date_end = i["DTEND"]
            date_middle = vDDDTypes(i["DTSTART"].dt + td(hours=2))

            first = Event(i)
            second = Event(i)
            first["DTSTART"] = date_start
            second["DTEND"] = date_end
            first["DTEND"] = date_middle
            second["DTSTART"] = date_middle

            calendars[cal].append(first)
            calendars[cal].append(second)
        calendars[cal] = [
            i for i in calendars[cal] if i["DTEND"].dt.hour - i["DTSTART"].dt.hour != 4
        ]

    for cal in calendars:
        with open(f"tmp/{cal}", "w+") as file:
            calendar = Calendar()
            for i in calendars[cal]:
                calendar.add_component(i)
            file.write(calendar.to_ical().decode())

    hours = [8, 10, 14, 16]

    merged = []

    nbr = 0
    for i in calendars:
        nbr += 1
        print(f" {nbr} - {i}")
    names = [i for i in calendars]
    cal_first = names[int(input("first  > ")) - 1]
    cal_secnd = names[int(input("second > ")) - 1]

    date = datetime(2023, 11, 26, 8)
    while date < datetime(2024, 2, 1, 8):  # Checking every hour of class
        if hours.index(date.hour) == 3 or date.weekday() == 6:
            date += td(days=1)
        if date.weekday() == 5:
            date += td(days=2)
        date = date.replace(hour=hours[(hours.index(date.hour) + 1) % 4])

        event_tp11 = next(
            (
                i["dtstart"]
                for i in calendars[cal_first]
                if i["DTSTART"].dt.astimezone() == date.astimezone()
            ),
            None,
        )
        event_tp10 = next(
            (
                i["dtstart"]
                for i in calendars[cal_secnd]
                if i["DTSTART"].dt.astimezone() == date.astimezone()
            ),
            None,
        )

        if not (event_tp10 or event_tp11):
            # print(date.astimezone().ctime())
            merged.append(prop.vDDDTypes(date - td(hours=1)))

    free_time = Calendar(metadata["tp11_1a.ics"])
    for i in merged:
        free_time.add_component(
            Event(
                {
                    "DTSTART": i.to_ical(),
                    "DTEND": prop.vDDDTypes(i.dt + td(hours=2)).to_ical(),
                    "SUMMARY": "Temps libre",
                }
            )
        )
    with open("tmp/temps_libre.ics", "w+") as tmp:
        tmp.write(free_time.to_ical().decode())

    print(f"len = {len(merged)}")


if __name__ == "__main__":
    main()
