from socket import timeout
import PySimpleGUI as sg
import prayer_time as pt
from psgtray import SystemTray
from datetime import date, datetime
import wave
import pyaudio
import time
import re

def AdzanSoundThread(tray, adzan):
    prayerTime = pt.pray_times()
    for name_time,time in prayerTime:
        tempTime = time
        FinalizeTime = re.sub("[(WIB)]","",tempTime)
        SeparatorTime = FinalizeTime.split(':')
        if datetime.today().minute == SeparatorTime[1] and datetime.today().hour == SeparatorTime[0]:
            adzan[0] = False
            tray.show_message('Time for praying : {}'.format(name_time),'Lets go to pray, hurry up, Adzan has begun')
            wf = wave.open('assets/mecca_56_22.wav')
            pAudio = pyaudio.PyAudio()
            stream = pAudio.open(format=pAudio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            # Read data in chunks
            data = wf.readframes(1024)

            # Play the sound by writing the audio data to the stream
            while data != '':
                stream.write(data)
                data = wf.readframes(1024)
            adzan[0]=True
    


def main():
    sg.theme("DarkAmber")
    menu = ['',['Author','About','Exit']]
    tooltip = 'IPray'
    #Layout in Windows's Frame
    layout = [[sg.Table(pt.pray_times(),headings=['Name Time','Time'])]]
    #Window Class Instance
    window = sg.Window('IPray',layout,finalize=True,enable_close_attempted_event=True)
    window.hide()
    #Dekstop Tray Icon
    tray = SystemTray(menu,single_click_events=False,window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    tray.show_message('IPray','IPray is launching in the background')
    adzan = [True]
    #Update windows event(Interaction program and user)
    while True:
        event, values = window.read(timeout=1000)
    
        if event == tray.key:
            event = values[event]

        if event == sg.TIMEOUT_EVENT and adzan[0]:
            window.start_thread(lambda: AdzanSoundThread(tray,adzan), ('-THREAD-', '-THEAD ENDED-'))

        if event == 'Exit':
            break

        if event == sg.WIN_CLOSE_ATTEMPTED_EVENT:
            window.hide()
            tray.show_icon()

        elif event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
            window.un_hide()
            window.bring_to_front()
        window.refresh()

    tray.close()
    window.close()

if __name__ == '__main__':
    main()
