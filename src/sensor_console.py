#!/usr/bin/env python2

import wx
import logging
import argparse

import event
from eventmanager import EventManager

class SensorFrame(wx.Frame):
    def __init__(self, parent, title, peers):
        wx.Frame.__init__(self, parent, title=title)

        self.event_manager = EventManager(peers)
        
        panel = wx.Panel(self)

        button_door_open = wx.Button(panel,
                                     wx.ID_ANY,
                                     'Send Door Open Event')
        button_door_closed = wx.Button(panel,
                                       wx.ID_ANY,
                                       'Send Door Closed Event')
        button_window_open = wx.Button(panel,
                                       wx.ID_ANY,
                                       'Send Window Open Event')
        button_window_closed = wx.Button(panel,
                                         wx.ID_ANY,
                                         'Send Window Closed Event')
        button_flood = wx.Button(panel,
                                 wx.ID_ANY,
                                 'Send Flood Sensor Event')

        
        self.Bind(wx.EVT_BUTTON, self.OnDoorOpen, button_door_open)
        self.Bind(wx.EVT_BUTTON, self.OnDoorClosed, button_door_closed)
        self.Bind(wx.EVT_BUTTON, self.OnWindowOpen, button_window_open)
        self.Bind(wx.EVT_BUTTON, self.OnWindowClosed, button_window_closed)
        self.Bind(wx.EVT_BUTTON, self.OnFlood, button_flood)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 0, wx.EXPAND)

        button_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer.Add(button_door_open, 0, wx.EXPAND)        
        button_sizer.Add(button_door_closed, 0, wx.EXPAND)
        button_sizer.Add(button_window_open, 0, wx.EXPAND)
        button_sizer.Add(button_window_closed, 0, wx.EXPAND)
        button_sizer.Add(button_flood, 0, wx.EXPAND)

        self.SetSizer(sizer)
        panel.SetSizer(button_sizer)

        self.Show(True)

    def OnDoorOpen(self, wx_event):
        e = event.DoorSensorEvent(0, 0, True)
        self.event_manager.broadcast_event(e)

    def OnDoorClosed(self, wx_event):
        e = event.DoorSensorEvent(0, 0, False)
        self.event_manager.broadcast_event(e)

    def OnWindowOpen(self, wx_event):
        e = event.WindowSensorEvent(1, 0, False)
        self.event_manager.broadcast_event(e)

    def OnWindowClosed(self, wx_event):
        e = event.WindowSensorEvent(1, 0, False)
        self.event_manager.broadcast_event(e)

    def OnFlood(self, wx_event):
        e = event.FloodSensorEvent(2, 2, 0, False)
        self.event_manager.broadcast_event(e)


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

    app = wx.App(False)
    frame = SensorFrame(None, 'GARTH Sensor Demo Console', peer_list)

    app.MainLoop()
