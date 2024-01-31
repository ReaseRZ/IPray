import requests
import IPray as IP
from datetime import date

today = date.today()
#get data API prayer time
def refresh_data_api(city:str,country:str):
    today = date.today()
    response = requests.get("https://api.aladhan.com/v1/calendarByCity/{}/{}?city={}&country={}&method=5".format(today.year,today.month,city,country))
    data = response.json()
    #print("status code :{}".format(response.status_code))
    if response.status_code == 200:
        return data
    else:
        IP.WarningPage('Required good internet connection')
        return
        

def get_data_pray_time(city:str,country:str):
    data = refresh_data_api(city,country)
    today_prayer_times = data["data"][today.day-1]["timings"]
    return today_prayer_times.items()

#Temporary storr string to data array
def pray_times(city:str,country:str):
    pray_times_data = []
    for name_time,time in get_data_pray_time(city,country):
        #print(name_time+"   "+time)
        pray_times_data.append([name_time,time])
    return pray_times_data
''''
def hijri_date():
    hijri_date_data = []
    hijri = data["data"][today.day-1]["date"]["hijri"]
    hijri_date_data.append("Hijriyah Date : {}".format(hijri["date"]))
    hijri_date_data.append("Month           : {}".format(hijri["month"]["en"]))
    hijri_date_data.append("day               : {}".format(hijri["weekday"]["en"]))
    return hijri_date_data
'''