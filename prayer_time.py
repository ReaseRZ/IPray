import requests
from datetime import date

today = date.today()
response = requests.get("http://api.aladhan.com/v1/calendar/{}/{}?latitude=-7.244&longitude=112.585&method=5".format(today.year,today.month))
data = response.json()

#get data API prayer time
def get_data_pray_time():
    today_prayer_times = data["data"][today.day-1]["timings"]
    return today_prayer_times.items()

#Temporary storr string to data array
def pray_times():
    pray_times_data = []
    for name_time,time in get_data_pray_time():
        pray_times_data.append([name_time,time])
    return pray_times_data

def hijri_date():
    hijri_date_data = []
    hijri = data["data"][today.day-1]["date"]["hijri"]
    hijri_date_data.append("Hijriyah Date : {}".format(hijri["date"]))
    hijri_date_data.append("Month           : {}".format(hijri["month"]["en"]))
    hijri_date_data.append("day               : {}".format(hijri["weekday"]["en"]))
    return hijri_date_data
