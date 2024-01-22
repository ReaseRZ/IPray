import requests
import sys
from datetime import date

today = date.today()
response = requests.get("http://api.aladhan.com/v1/calendar/{}/{}?latitude=-7.244&longitude=112.585&method=3".format(today.year,today.month))
data = response.json()

def pray_times():
    pray_times_data = []
    today_prayer_times = data["data"][today.day-1]["timings"]
    for name_time,time in today_prayer_times.items():
        pray_times_data.append("{} : {}".format(name_time,time))
    return pray_times_data

def hijri_date():
    hijri_date_data = []
    hijri = data["data"][today.day-1]["date"]["hijri"]
    hijri_date_data.append("Hijriyah Date : {}".format(hijri["date"]))
    hijri_date_data.append("Month           : {}".format(hijri["month"]["en"]))
    hijri_date_data.append("day               : {}".format(hijri["weekday"]["en"]))
    return hijri_date_data


def help():
    print("pt : showing the prayer times")
    print("hd : showing the hijriyah date")

