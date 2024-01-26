import PySimpleGUI as sg
import prayer_time as pt

sg.theme("DarkAmber")
layout = [[sg.Table(pt.pray_times(),headings=['Name Time','Time'])]]

window = sg.Window('IPray',layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
window.close()
