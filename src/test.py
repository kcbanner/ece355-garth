#!/usr/bin/env python2

import unittest
import pickle
import mox
from datetime import datetime

from event import Event
from event_type import EventType
from eventmanager import EventManager
from communicationsinterface import CommunicationsInterface

class TestEvent(unittest.TestCase):
    def test_event_init(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        timestamp = datetime.utcnow()

        event = Event(event_type, timestamp)

        self.assertEqual(event.get_event_type(), event_type)
        self.assertEqual(event.get_timestamp(), timestamp)

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager();
        
    def test_subscribe(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type,
                                     controller)

        self.assertIsNotNone(self.event_manager.subscriptions[event_type])
        self.assertEqual(self.event_manager.subscriptions[event_type][0],
                         controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

    def test_subscribe_multiple(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type, controller)
        self.event_manager.subscribe(event_type, controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

    def test_serialize_deserialize_event(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        timestamp = datetime.utcnow()

        event = Event(event_type, timestamp)
        
        serialized = self.event_manager.serialize_event(event)
        deserialized = self.event_manager.deserialize_event(serialized)

        self.assertIsInstance(deserialized, Event)
        self.assertEqual(deserialized.get_event_type(), event_type)
        self.assertEqual(deserialized.get_timestamp(), timestamp)

    def test_broadcast_event(self):
        comm_interface_mock = mox.MockObject(CommunicationsInterface)
    
        # Test Event
        event_type = EventType.DOOR_SENSOR_EVENT
        timestamp = datetime.utcnow()
        event = Event(event_type, timestamp)
        expected_data = EventManager.serialize_event(event)
        
        # Replace the comm interface with a mock
        self.event_manager.communications_interface = comm_interface_mock
        comm_interface_mock.broadcast_data(expected_data)
        mox.Replay(comm_interface_mock)

        # Broadcast the event
        self.event_manager.broadcast_event(event)

        # Verify that broadcasting uses communications interface
        mox.Verify(comm_interface_mock)

if __name__ == '__main__':
    unittest.main()
