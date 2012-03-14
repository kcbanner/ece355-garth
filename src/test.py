#!/usr/bin/env python2

import unittest
import pickle
import mox
from datetime import datetime

from event import *
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

    def test_sensor_event(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        sensor_id = 12 

        event = SensorEvent(event_type, sensor_id)

        self.assertEqual(event.get_sensor_id(), sensor_id)

    def test_door_sensor_event(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        sensor_id = 12 
        door_id = 1
        opened = True

        event = DoorSensorEvent(event_type, sensor_id, door_id, opened )

        self.assertEqual(event.get_door_id(), door_id)
        self.assertEqual(event.get_opened(), opened)
    
    def test_window_sensor_event(self):
        event_type = EventType.WINDOW_SENSOR_EVENT
        sensor_id = 11 
        window_id = 2
        opened = True

        event = WindowSensorEvent(event_type, sensor_id, window_id, opened)

        self.assertEqual(event.get_window_id(), window_id)
        self.assertEqual(event.get_opened(), opened)
    
    def test_temp_sensor_event(self):
        event_type = EventType.TEMP_SENSOR_EVENT
        sensor_id = 13
        temperature = 25
        delta = 1

        event = TempSensorEvent(event_type, sensor_id, temperature, delta)

        self.assertEqual(event.get_temperature(), temperature)
        self.assertEqual(event.get_temp_delta(), delta)
        
    def test_flood_sensor_event(self):
        event_type = EventType.FLOOD_SENSOR_EVENT
        sensor_id = 15
        water_height = 1
        delta = 1

        event = FloodSensorEvent(event_type, sensor_id, water_height, delta)
        
        self.assertEqual(event.get_water_height(), water_height)
        self.assertEqual(event.get_height_delta(), delta)

    def test_input_event(self):
        event_type = EventType.KEYPAD_EVENT
        input_device_id = 18
        
        event = InputEvent(event_type, input_device_id)

        self.assertEqual(event.get_device_id(), input_device_id)
    
    def test_keypad_input_event(self):
        event_type = EventType.KEYPAD_EVENT
        input_device_id = 19
        input_char = "a"

        event = KeypadEvent(event_type, input_device_id, input_char)

        self.assertEqual(event.get_input(), input_char)
    
    def test_NFC_input_event(self):
        event_type = EventType.NFC_EVENT
        input_device_id = 20
        data_string = "asdfasdfasdf"

        event = NFCEvent(event_type, input_device_id, data_string)

        self.assertEqual(event.get_NFC_string(), data_string)

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
