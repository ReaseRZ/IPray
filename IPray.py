import PySimpleGUI as sg
import prayer_time as pt
import location as loc
from psgtray import SystemTray
from datetime import datetime
import wave
import pyaudio

def Author(windows:sg.Window):
    layout = [[sg.Text("Github : ReaseRZ | CReszen")],
              [sg.Text("LinkedIn : Reggy Samius")],
              [sg.Text("Codewars : CReszen")],
              [sg.Text("Email me on : creszen.cpp@outlook.com")]]
    event,values = sg.Window('Author',layout,element_justification='center').read(close=True)

def AboutWindows(windows:sg.Window):
    layout = [[sg.Text("Remainder prayer for someone that got deep focus on the computer")],
              [sg.Text("Created with love By ResZ ©2024")]]
    event,values = sg.Window('About',layout,element_justification='center').read(close=True)

def Sync(window:sg.Window,values,ScannerPrayTime):
    city=str(values['city'])
    country=str(values['country'])
    ScannerPrayTime=pt.pray_times(city,country)
    window['-table-'].update(values=ScannerPrayTime)
    return (ScannerPrayTime,city,country)

#Pop Up for remind user every (@Parameter : cooldown<int>)
def WarningForPrayTimeIsNear(name_time,tray,flag,SeparatorTime,flag_number:int,cooldown:int):
    alarmMinuteToday = 0
    if flag[flag_number]:
        if datetime.today().minute > int(SeparatorTime[1]) and int(SeparatorTime[0])-datetime.today().hour == 1:
            alarmMinuteToday = int(SeparatorTime[1])+60-datetime.today().minute
        if datetime.today().minute < int(SeparatorTime[1]) and int(SeparatorTime[0])-datetime.today().hour == 1:
            alarmMinuteToday = int(SeparatorTime[1])+60-datetime.today().minute
        if datetime.today().minute < int(SeparatorTime[1]) and int(SeparatorTime[0])-datetime.today().hour == 0:
            alarmMinuteToday = int(SeparatorTime[1])-datetime.today().minute
    if int(alarmMinuteToday) <= int(cooldown) and alarmMinuteToday != 0 :
        tray.show_message('Time for {} is {} minute(s) more'.format(name_time,alarmMinuteToday),'I am coming for remind you')
        flag[flag_number]=False
    del alarmMinuteToday
    
#Play adzan sound when time is coming
def AdzanSoundThread(tray, flag ,name_time):
    flag[0] = False
    tray.show_message('Time for praying : {}'.format(name_time),'Lets go to pray, hurry up, Adzan has begun')
    wf = wave.open('assets/mecca_56_22.wav')
    pAudio = pyaudio.PyAudio()
    stream = pAudio.open(format=pAudio.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    # Read data in audio
    data = wf.readframes(512)
    # Play the sound by writing the audio data to the stream
    while data != '':
        stream.write(data)
        data = wf.readframes(512)
    stream.close()
    pAudio.terminate()
    flag[0]=True
    flag[1]=True
    flag[2]=True
    flag[3]=True

#Window for alert user
def WarningPage(text:str):
    LayoutWarning = [[sg.Text(text)]]
    warningWindow = sg.Window('Warning',LayoutWarning,finalize=True, icon='moon.ico')
    event, values = warningWindow.read(close=False)
    if event == sg.WINDOW_CLOSED:
        warningWindow.close()

#Function for confirm location Input
def ConfirmDefault():
    layoutOp = [[sg.Text("Confirm your default location",size=20)],
              [sg.Combo(loc.CountryList,enable_events=True,readonly=True,key='_country_'),sg.Combo(values=[],enable_events=True,readonly=True,key='_city_',disabled=True,expand_x=True,size=(15,10))],
              [sg.Button('Confirm',enable_events=True,key='Confirm')]]
    windowOp = sg.Window('IPray',layoutOp,finalize=True, icon='moon.ico')
    while True:
        event, values = windowOp.read(close=False)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event =='_country_':
            windowOp['_city_'].update(disabled=False)
            if values['_country_'] == 'Indonesia':
                windowOp['_city_'].update(values=loc.CityList[0])
            elif values['_country_'] == 'United Kingdom':
                windowOp['_city_'].update(values=loc.CityList[1])
            elif values['_country_'] == 'Germany':
                windowOp['_city_'].update(values=loc.CityList[2])
        if event == 'Confirm':
            if values['_city_'] == '' or values['_country_'] =='':
                WarningPage('Please enter format properly')
            else:
                windowOp.close()
                return [values['_country_'],values['_city_']]
    return []
def main():
    sg.theme("DarkAmber")
    menu = ['',['Author','About','Exit']]
    tooltip = 'IPray'
    country = None
    city=None
    #Create File for Default Location
    try:
        fileLocation = open('fileLoc.txt','x')
        country,city = ConfirmDefault()
        fileLocation.write('{}:{}'.format(city,country))
        fileLocation.close()
    except FileExistsError:
        fileLocation = open('fileLoc.txt','r')
        ResLocation = fileLocation.read()
        ResSplit = ResLocation.split(':')
        city = ResSplit[0]
        country = ResSplit[1]
        fileLocation.close()
    
    #Additional Object
    namePrayerTime = []
    timePrayer = []
    ScannerPrayTime=pt.pray_times(city,country)
    for name_time,time in ScannerPrayTime:
        if name_time == 'Fajr' or name_time == 'Dhuhr' or name_time == 'Asr' or name_time == 'Maghrib' or name_time =='Isha':
            namePrayerTime.append(name_time)
            timePrayer.append(time)
    for i in range (0,len(timePrayer)):
        timePrayer[i] = timePrayer[i][0:6]

    #Layout in Windows's Frame
    layout = [[sg.Text('Location : {}, {}'.format(city,country),key='location_tag')],
              [sg.Table(ScannerPrayTime,headings=['Name Time','Time'],key='-table-')],
              [sg.Combo(loc.CountryList,enable_events=True,readonly=True,key='country'),sg.Combo(values=[],enable_events=True,readonly=True,key='city',disabled=True,expand_x=True)],
              [sg.Button('Sync',enable_events=True,key='Sync')]]
    #Window Class Instance
    window = sg.Window('IPray',layout,finalize=True,enable_close_attempted_event=True,icon=r'moon.ico')
    window.hide()
    #Dekstop Tray Icon
    tray = SystemTray(menu,single_click_events=False,window=window, tooltip=tooltip, icon=r'moon.png')
    tray.show_message('IPray','IPray is launching in the background')
    flag = [True,True,True,True]
    #Update windows event(Interaction program and user)
    while True:
        event, values = window.read(timeout=3000)
        if event == tray.key:
            event = values[event]
        if event == sg.TIMEOUT_EVENT:
            for i in range (0,len(namePrayerTime)):
                SeparatorTime = timePrayer[i].split(':')
                WarningForPrayTimeIsNear(namePrayerTime[i],tray,flag,SeparatorTime,1,15)
                WarningForPrayTimeIsNear(namePrayerTime[i],tray,flag,SeparatorTime,2,60)
                if datetime.today().minute == int(SeparatorTime[1]) and datetime.today().hour == int(SeparatorTime[0]) and flag[0]:
                    window.start_thread(lambda: AdzanSoundThread(tray,flag,namePrayerTime[i]), ('-THREAD-', '-THEAD ENDED-'))
                SeparatorTime.clear()
        if event == 'Exit':
            break
        if event == 'Sync' :
            flag[1]=True
            flag[2]=True
            if values['city'] == '' or values['country'] =='':
                WarningPage('Take your time for filling up the location')
                continue
            namePrayerTime.clear()
            timePrayer.clear()
            ScannerPrayTime.clear()
            ScannerPrayTime, city, country=Sync(window,values, ScannerPrayTime)
            window['location_tag'].update('Location : {}, {}'.format(city,country))
            for name_time,time in ScannerPrayTime:
                if name_time == 'Fajr' or name_time == 'Dhuhr' or name_time == 'Asr' or name_time == 'Maghrib' or name_time =='Isha':
                    namePrayerTime.append(name_time)
                    timePrayer.append(time)
            for i in range (0,len(timePrayer)):
                timePrayer[i] = timePrayer[i][0:6]

        if event =='country':
            window['city'].update(disabled=False)
            if values['country'] == 'Indonesia':
                window['city'].update(values=loc.CityList[0])
            elif values['country'] == 'United Kingdom':
                window['city'].update(values=loc.CityList[1])
            elif values['country'] == 'Germany':
                window['city'].update(values=loc.CityList[2])
        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            window.hide()
            tray.show_message('IPray','IPray is launching in the background')
            tray.show_icon()
        if event == 'Author':
            Author(window)
        if event == 'About':
            AboutWindows(window)
        if event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
            window.un_hide()
            window.bring_to_front()
        window.refresh()
    tray.close()
    window.close()

if __name__ == '__main__':
    main()
