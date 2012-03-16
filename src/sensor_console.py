#!/usr/bin/env python2

import wx

class SensorFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        
        button_door_open = wx.Button(self, wx.ID_ANY, 'Send Door Open Event')
        button_door_closed = wx.Button(self, wx.ID_ANY, 'Send Door Closed Event')
        
        self.Bind(wx.EVT_BUTTON, self.OnDoorOpen, button_door_open)
        self.Bind(wx.EVT_BUTTON, self.OnDoorClosed, button_door_closed)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button_door_open, 0, wx.EXPAND)        
        sizer.Add(button_door_closed, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Show(True)

    def OnDoorOpen(self, event):
        pass

    def OnDoorClosed(self, event):
        pass


app = wx.App(False)
frame = SensorFrame(None, 'GARTH Sensor Demo Console')

app.MainLoop()
