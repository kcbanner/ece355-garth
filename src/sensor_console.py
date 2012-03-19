#!/usr/bin/env python2

import wx
import logging
import argparse

import event
from eventmanager import EventManager

class DoorWindowPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        button_door_open = wx.Button(self, wx.ID_ANY, 'Send Door Open Event')
        button_door_closed = wx.Button(self, wx.ID_ANY, 'Send Door Closed Event')
        button_window_open = wx.Button(self, wx.ID_ANY, 'Send Window Open Event')
        button_window_closed = wx.Button(self, wx.ID_ANY, 'Send Window Closed Event')

        self.Bind(wx.EVT_BUTTON, self.OnDoorOpen, button_door_open)
        self.Bind(wx.EVT_BUTTON, self.OnDoorClosed, button_door_closed)
        self.Bind(wx.EVT_BUTTON, self.OnWindowOpen, button_window_open)
        self.Bind(wx.EVT_BUTTON, self.OnWindowClosed, button_window_closed)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button_door_open, 0, wx.EXPAND)        
        sizer.Add(button_door_closed, 0, wx.EXPAND)
        sizer.Add(button_window_open, 0, wx.EXPAND)        
        sizer.Add(button_window_closed, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def OnDoorOpen(self, wx_event):
        e = event.DoorSensorEvent(0, 0, True)
        g_event_manager.broadcast_event(e)

    def OnDoorClosed(self, wx_event):
        e = event.DoorSensorEvent(0, 0, False)
        g_event_manager.broadcast_event(e)

    def OnWindowOpen(self, wx_event):
        e = event.WindowSensorEvent(1, 0, True)
        g_event_manager.broadcast_event(e)

    def OnWindowClosed(self, wx_event):
        e = event.WindowSensorEvent(1, 0, False)
        g_event_manager.broadcast_event(e)


class FloodPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        button_flood = wx.Button(self, wx.ID_ANY, 'Send Flood Sensor Event')
        
        self.Bind(wx.EVT_BUTTON, self.OnFlood, button_flood)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button_flood, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def OnFlood(self, wx_event):
        e = event.FloodSensorEvent(2, 2, 0, False)
        g_event_manager.broadcast_event(e)
        
        
class SensorFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        notebook.AddPage(DoorWindowPage(notebook), "Door and Window Events")
        notebook.AddPage(FloodPage(notebook), "Flood Events")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 0, wx.EXPAND)
        panel.SetSizer(sizer)

        self.Show(True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--peers',
                        help='comma seperated list of peers to connect to. eg: \'localhost:8001,localhost:8002\'',
                        required=True,
                        dest='peers')
    parser.add_argument('-v',
                        '--verbose',
                        default=False,
                        action='store_true',
                        dest='verbose',
                        help='show debug logging')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    peer_list = []
    for peer in args.peers.split(','):
        peer_list.append(tuple(peer.split(':')))

    g_event_manager = EventManager(peer_list)

    app = wx.App(False)
    frame = SensorFrame(None, 'GARTH Sensor Demo Console')

    app.MainLoop()
