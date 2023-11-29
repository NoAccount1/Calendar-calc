from datetime import datetime, timedelta as td

date = datetime(2023, 11, 29, 8)

hours = [8, 10, 14, 16]


while date < datetime(2024, 7, 1, 8):
    if hours.index(date.hour) == 3:
        date += td(days=1)
    date = date.replace(hour=hours[(hours.index(date.hour) + 1) % 4])
    print(date)


# for i in range(4):
#     for i in range(12 - month):
#         if month == 12:
#             month = 1
#             year += 1

#         for i in range(31 - day):
#             if day == 31:
#                 day = 0
#                 month += 1

#             for i in range(4):
#                 if hours.index(hour) == 3:
#                     day += 1
#                 hour = hours[(hours.index(hour) + 1) % 4]
#                 print(hour, day, month, year)
#     year += 1
