#!/usr/bin/env python2

import mox
import time
import socket
import pickle
import logging
import unittest
from datetime import datetime
from datetime import timedelta

from event import *
from sensor import *
from event_type import EventType
from inputdevice import *
from eventmanager import EventManager
from communicationsinterface import CommunicationsInterface
from controller import Controller

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
        self.event_manager = EventManager([]);
        
    def test_subscribe(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type,
                                     controller)

        self.assertIsNotNone(self.event_manager.subscriptions[event_type])
        self.assertEqual(self.event_manager.subscriptions[event_type][0],
                         controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

    def test_subscribe_same(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type, controller)
        self.event_manager.subscribe(event_type, controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

    def test_subscribe_multiple(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        other_controller = 'dummy_controller_other'
        
        self.event_manager.subscribe(event_type, controller)
        self.event_manager.subscribe(event_type, other_controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 2)

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
        comm_interface_mock.broadcast_data(expected_data, [])
        mox.Replay(comm_interface_mock)

        # Broadcast the event
        self.event_manager.broadcast_event(event)

        # Verify that broadcasting uses communications interface
        mox.Verify(comm_interface_mock)

    
    #
    # Verify events are sent to subscribed controllers
    #

    def test_event_received(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        event = Event(event_type)

        # Set up controller mock
        controller = mox.MockObject(Controller)
        controller.handle_event(event)
        mox.Replay(controller)

        self.event_manager.subscribe(event_type, controller)
        self.event_manager.event_received(event)
        self.event_manager.process_events()

        mox.Verify(controller)


    #
    # Verify that events are only sent to the appropriate controllers
    #

    def test_event_received_multiple_events(self):
        door_event = Event(EventType.DOOR_SENSOR_EVENT)
        window_event = Event(EventType.WINDOW_SENSOR_EVENT)

        # Set up controller mocks
        door_controller = mox.MockObject(Controller)
        door_controller.handle_event(door_event)
        mox.Replay(door_controller)

        window_controller = mox.MockObject(Controller)
        mox.Replay(window_controller)

        self.event_manager.subscribe(EventType.DOOR_SENSOR_EVENT,
                                     door_controller)
        self.event_manager.subscribe(EventType.WINDOW_SENSOR_EVENT, 
                                     window_controller)

        # Send event
        self.event_manager.event_received(door_event)
        self.event_manager.process_events()

        mox.Verify(door_controller)
        mox.Verify(window_controller)

class TestSensor(unittest.TestCase):
    def test_sensor_init(self):
        sensor_id = 1
        status = SensorStatus.ONLINE
        
        sensor = Sensor(sensor_id, status)

        self.assertEqual(sensor.get_sensor_id(), sensor_id)
        self.assertEqual(sensor.get_sensor_status(), status)
  
class TestDoorSensor(unittest.TestCase):
    def setUp(self):
        self.sensor_id = 2
        self.status = SensorStatus.ONLINE
        self.door_id = 1
        
        self.sensor = DoorSensor(self.sensor_id, self.status, self.door_id)

    def test_door_sensor_init(self):
        self.assertEqual(self.sensor.get_door_id(), self.door_id)

    def test_door_sensor_event(self):
        is_opened = False
        self.sensor.set_opened(is_opened)
        # Create an event from the sensor, assuming closed
        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.DOOR_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_door_id(), self.door_id)
        self.assertEqual(event.get_opened(), is_opened)
        
        # Checking if it is opened setter
        is_opened = True
        self.sensor.set_opened(is_opened)

        # Create another event...
        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.DOOR_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_door_id(), self.door_id)
        self.assertEqual(event.get_opened(), is_opened)

class TestWindowSensor(unittest.TestCase):
    def setUp(self):
        self.sensor_id = 3
        self.status = SensorStatus.ONLINE
        self.window_id = 1
        self.sensor = WindowSensor(self.sensor_id, self.status, self.window_id) 
    
    def test_window_sensor_init(self):
        self.assertEqual(self.sensor.get_window_id(), self.window_id)
    
    def test_window_sensor_event(self):
        is_opened = False
        self.sensor.set_opened(is_opened)
        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.WINDOW_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_window_id(), self.window_id)
        self.assertEqual(event.get_opened(), is_opened)
        
        # Checking if it is opened setter
        is_opened = True
        self.sensor.set_opened(is_opened)

        # Create another event...
        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.WINDOW_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_window_id(), self.window_id)
        self.assertEqual(event.get_opened(), is_opened)

class TestFloodSensor(unittest.TestCase):
    def setUp(self):
        self.sensor_id = 4
        self.status = SensorStatus.ONLINE
        self.sensor = FloodSensor(self.sensor_id, self.status)
   
    def test_flood_sensor_init(self):
        self.assertEqual(self.sensor.get_water_height(), 0)
        self.assertEqual(self.sensor.get_delta(), 0)

    def test_flood_sensor_event(self):
        # Check the base case
        old_height = 0
        new_height = 10 
        
        self.sensor.set_water_height(new_height)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.FLOOD_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_water_height(), new_height)
        self.assertEqual(event.get_water_height(), self.sensor.get_water_height())
        self.assertEqual(event.get_height_delta(), new_height - old_height)
        self.assertEqual(event.get_height_delta(), self.sensor.get_delta())
        
        # Ensure that the new water height values are stored correctly for the
        # delta
        old_height = new_height
        new_height = 20
       
        self.sensor.set_water_height(new_height)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.FLOOD_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_water_height(), new_height)
        self.assertEqual(event.get_water_height(), self.sensor.get_water_height())
        self.assertEqual(event.get_height_delta(), new_height - old_height)
        self.assertEqual(event.get_height_delta(), self.sensor.get_delta())
        
        # Case were the old_height > new_height, ensures that it isn't an
        # absolute value
        old_height = new_height
        new_height = 10
       
        self.sensor.set_water_height(new_height)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.FLOOD_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_water_height(), new_height)
        self.assertEqual(event.get_water_height(), self.sensor.get_water_height())
        self.assertEqual(event.get_height_delta(), new_height - old_height)
        self.assertEqual(event.get_height_delta(), self.sensor.get_delta())

class TestTemperatueSensor(unittest.TestCase):
    def setUp(self):
        self.sensor_id = 5
        self.status = SensorStatus.ONLINE
        self.sensor = TemperatureSensor(self.sensor_id, self.status)

    def test_temp_sensor_init(self):
        self.assertEqual(self.sensor.get_temperature(), 0)
        self.assertEqual(self.sensor.get_delta(), 0)

    def test_temp_sensor_event(self):
        old_temp = 0
        new_temp = 10

        self.sensor.set_temperature(new_temp)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.TEMP_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_temperature(), new_temp)
        self.assertEqual(event.get_temperature(), self.sensor.get_temperature())
        self.assertEqual(event.get_temp_delta(), new_temp - old_temp)
        self.assertEqual(event.get_temp_delta(), self.sensor.get_delta())

        old_temp = new_temp
        new_temp = 20
        self.sensor.set_temperature(new_temp)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.TEMP_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_temperature(), new_temp)
        self.assertEqual(event.get_temperature(), self.sensor.get_temperature())
        self.assertEqual(event.get_temp_delta(), new_temp - old_temp)
        self.assertEqual(event.get_temp_delta(), self.sensor.get_delta())
        
        old_temp = new_temp
        new_temp = 10
        self.sensor.set_temperature(new_temp)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.TEMP_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_temperature(), new_temp)
        self.assertEqual(event.get_temperature(), self.sensor.get_temperature())
        self.assertEqual(event.get_temp_delta(), new_temp - old_temp)
        self.assertEqual(event.get_temp_delta(), self.sensor.get_delta())

class TestMotionSensor(unittest.TestCase):
    def setUp(self):
        self.sensor_id = 6
        self.status = SensorStatus.ONLINE
        self.motion_threshold = 10
        self.sensor = MotionSensor(self.sensor_id, self.status, self.motion_threshold)
        
    def test_motion_sensor_init(self):
        self.assertEqual(self.sensor.get_motion_threshold(), self.motion_threshold)
        self.motion_threshold = 20
        self.sensor.set_motion_threshold(self.motion_threshold)
        self.assertEqual(self.sensor.get_motion_threshold(), self.motion_threshold)
    
    def test_motion_sensor_event(self):
        time = datetime.utcnow()        

        self.sensor.motion_detected()

        event = self.sensor.generate_sensor_event()
        
        self.assertEqual(event.get_event_type(), EventType.MOTION_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_threshold(), self.motion_threshold)
        self.assertTrue(event.get_duration() > timedelta(0))

        self.sensor.set_motion_started_time(time)

        event = self.sensor.generate_sensor_event()

        self.assertEqual(event.get_event_type(), EventType.MOTION_SENSOR_EVENT)
        self.assertEqual(event.get_sensor_id(), self.sensor_id)
        self.assertEqual(event.get_threshold(), self.motion_threshold)
        self.assertTrue(event.get_duration() <= datetime.utcnow() - time)
        
class TestInputDevice(unittest.TestCase):
    def setUp(self):
        return

    def test_input_device_init(self):
        device_id = 1
        device = InputDevice(device_id)

        self.assertEqual(device.get_device_id(), device_id)
         

class TestNFCReaderInputDevice(unittest.TestCase):
    def setUp(self):
        self.device_id = 2
        self.device = NFCReaderInputDevice(self.device_id)
    
    def test_nfc_reader_event(self):
        event = self.device.generate_NFC_event()
        self.assertEqual(event.get_device_id(), self.device_id)
        self.assertEqual(event.get_NFC_string(), None)
        self.assertEqual(event.get_event_type(), EventType.NFC_EVENT)

        data = "TEST STRING"
        self.device.set_data(data)

        event = self.device.generate_NFC_event()
        self.assertEqual(event.get_device_id(), self.device_id)
        self.assertEqual(event.get_NFC_string(), data)
        self.assertEqual(event.get_event_type(), EventType.NFC_EVENT)

class TestKeypadInputDevice(unittest.TestCase):
    def setUp(self):
        self.device_id = 3
        self.device = KeypadInputDevice(self.device_id)    

    def test_keypad_input_event(self):
        event = self.device.generate_keypad_event()
        self.assertEqual(event.get_device_id(), self.device_id)
        self.assertEqual(event.get_event_type(), EventType.KEYPAD_EVENT)
        self.assertEqual(event.get_input(), None)
        
        char = "b"
        self.device.set_input_char(char)

        event = self.device.generate_keypad_event()
        self.assertEqual(event.get_device_id(), self.device_id)
        self.assertEqual(event.get_event_type(), EventType.KEYPAD_EVENT)
        self.assertEqual(event.get_input(), char)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
