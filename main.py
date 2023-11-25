from icalendar import Calendar, Event, prop
import icalendar
import requests

import datetime
import json

from pprint import pprint

# TP 11
a1_t11 = "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=270585&projectId=11&calType=ical&nbWeeks=16"
# TP 9
a3_t10 = "https://planning.univ-lorraine.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=94072&projectId=11&calType=ical&nbWeeks=16"

urlfile = requests.get(a1_t11).content.decode()

with open("cal/270585.ics", "w+") as ics270585:
    ics270585.write(urlfile)

def print_dir(obj):
    for i in dir(obj):
        print(i)


with open("ADECal.ics", "r") as ics_file:
    cal = Calendar.from_ical(ics_file.read())

    metadata = dict(cal.items())

    cal = cal.walk()

    cal = [i for i in cal]
    # print(cal[0].items().mapping['DTSTART'])
    # events = []
    # for i in cal:
    #   events.append({})
