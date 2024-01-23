import wx
import wx.adv
import prayer_time
import threading
from playsound import playsound


MAXWIDTH = 350
MAXHEIGTH = 500
    
class TT(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 

class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW, name=''):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_paint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def on_size(self, event):
        self.Refresh()
        event.Skip()

class HijriyahDate(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        for i in prayer_time.hijri_date():
            self.sample = TransparentText(self, label = i)
            self.sample.SetFont(wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
            self.sample.SetForegroundColour((255,255,255))
            self.sample.SetBackgroundColour((0,0,0,128))
            self.sizer.Add(self.sample,0,wx.EXPAND)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.sizer,0,wx.EXPAND)
        self.SetSizer(self.sizer2)
        self.SetAutoLayout(1)
        self.sizer2.Fit(self)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
                
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("david-billings-EwcvNe53bdM-unsplash1.jpg")
        dc.DrawBitmap(bmp, 0, 0)
        

class PrayerTime(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        for i in prayer_time.pray_times():
            self.sample = TransparentText(self, label = i)
            self.sample.SetFont(wx.Font(20,wx.FONTFAMILY_DEFAULT,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
            self.sample.SetForegroundColour((255,255,255))
            self.sizer.Add(self.sample,0,wx.EXPAND)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2.Add(self.sizer,0,wx.EXPAND)
        self.SetSizer(self.sizer2)
        self.SetAutoLayout(1)
        self.sizer2.Fit(self)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
    
    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        # yanked from ColourDB.py
        dc = evt.GetDC()
                
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("david-billings-EwcvNe53bdM-unsplash1.jpg")
        dc.DrawBitmap(bmp, 0, 0)

class MainFrame(wx.Frame):
    def __init__(self, parent=None,title="",size=wx.DefaultSize,style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent=parent,title=title,size=size,style=style)
        self.taskBarIcon = wx.adv.TaskBarIcon()
        if self.taskBarIcon.IsAvailable() is False:
            raise SystemExit("Cannot access system tray")
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_CMN_DIALOG, (32,32))
        self.taskBarIcon.SetIcon(wx.Icon(bitmap), "IPray")
        # Create timer and bind events
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnMinimize)
        self.taskBarIcon.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnShowFrame)

    def OnMinimize(self, event):
        if self.IsIconized() is True:
            self.Hide()

    def OnShowFrame(self, event):
        # Restore Frame if it is minimized.
        if self.IsIconized() is True:
            self.Restore()
        # Show MainFrame if it is not shown already.
        if self.IsShown() is True:
            # Frame is already visible. Flash it.
            self.RequestUserAttention()
            self.SetFocus()
        else:
            self.Show()

    def OnClose(self, event):
        # Frame closed. Destroy taskbar icon and stop timer.
        event.Skip(True)
        self.taskBarIcon.Destroy()
        if self.timer.IsRunning() is True:
            self.timer.Stop()


app = wx.App(False)
frame = MainFrame(None, title="IPRAY",size=(MAXWIDTH,MAXHEIGTH),style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX|wx.MINIMIZE_BOX)
frame.SetSizeHints((MAXWIDTH,MAXHEIGTH),maxSize=(MAXWIDTH,MAXHEIGTH))
nb = wx.Notebook(frame)
nb.AddPage(HijriyahDate(nb),"Hijriyah Time")
nb.AddPage(PrayerTime(nb),"Pray Time")
thread2 = TT(frame.Show(),2000)
thread = TT(playsound("assets/mecca_56_22.mp3",False),1000)
thread2.start()
app.MainLoop()
