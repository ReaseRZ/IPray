from email import message
import PySimpleGUI as sg
import prayer_time as pt
from psgtray import SystemTray

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
    #Update windows event(Interaction program and user)
    while True:
        event, values = window.read()

        if event == tray.key:
            event = values[event]

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event in (sg.WIN_CLOSE_ATTEMPTED_EVENT):
            window.hide()
            tray.show_icon()
            
        elif event in (sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
            window.un_hide()
            window.bring_to_front()

    tray.close()
    window.close()

if __name__ == '__main__':
    main()
