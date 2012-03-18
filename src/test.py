#!/usr/bin/env python2

import new
import mox
import time
import select
import socket
import pickle
import logging
import unittest
import threading
from datetime import datetime
from datetime import timedelta

from event import *
from sensor import *
from event_type import EventType
from inputdevice import *
from eventmanager import EventManager

from communicationsinterface import CommunicationsInterface, ListenerThread
from controller import Controller
from sensorcontroller import SensorController
from systemcontroller import SystemController
from systemcontroller import SystemState

class TestController(unittest.TestCase):
    def test_handle_event(self):
        # This function should be a no-op, nothing should be called on
        # the EventManager
        mock_event_manager = mox.MockObject(EventManager)
        mox.Replay(mock_event_manager)

        controller = Controller(mock_event_manager)
        controller.handle_event('foo')

        mox.Verify(mock_event_manager)

    def test_stop(self):
        mock_event_manager = mox.MockObject(EventManager)
        mox.Replay(mock_event_manager)

        controller = Controller(mock_event_manager)
        controller.stop()
        controller.run()

        mox.Verify(mock_event_manager)


class TestCommunicationsInterface(unittest.TestCase):
    def test_listen(self):

        # listen should return a ListenerThread instance
        thread = CommunicationsInterface.listen(None, None)
        self.assertIsInstance(thread, ListenerThread)
        
    def test_broadcast_data(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setblocking(0)
        server_socket.bind(('localhost', 8001))
        server_socket.listen(1)

        test_message = 'test_message'

        # Verify that broadcast data is sent via socket
        CommunicationsInterface.broadcast_data(test_message, [('localhost', 8001)])

        readable, writable, exceptional = select.select(
            [server_socket], [], [], 1)
        
        self.assertEqual(len(readable), 1)
        
        (client_socket, address) = readable[0].accept()
        received_data = ''
        while True:
            data = client_socket.recv(1024)
            received_data += data
            if not data:
                break

        self.assertEqual(received_data, test_message)

    def test_broadcast_data_error(self):
        # No exception should be raised here
        CommunicationsInterface.broadcast_data('test_message',
                                               [('localhost', 8001)])
        



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

        event = DoorSensorEvent(sensor_id, door_id, opened )

        self.assertEqual(event.get_door_id(), door_id)
        self.assertEqual(event.get_opened(), opened)
    
    def test_window_sensor_event(self):
        event_type = EventType.WINDOW_SENSOR_EVENT
        sensor_id = 11 
        window_id = 2
        opened = True

        event = WindowSensorEvent(sensor_id, window_id, opened)

        self.assertEqual(event.get_window_id(), window_id)
        self.assertEqual(event.get_opened(), opened)
    
    def test_temp_sensor_event(self):
        event_type = EventType.TEMP_SENSOR_EVENT
        sensor_id = 13
        temperature = 25
        delta = 1

        event = TempSensorEvent(sensor_id, temperature, delta)

        self.assertEqual(event.get_temperature(), temperature)
        self.assertEqual(event.get_temp_delta(), delta)
        
    def test_flood_sensor_event(self):
        event_type = EventType.FLOOD_SENSOR_EVENT
        sensor_id = 15
        water_height = 1
        delta = 1

        event = FloodSensorEvent(sensor_id, water_height, delta)
        
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
        input_device_id = 20
        data_string = "asdfasdfasdf"

        event = NFCEvent(input_device_id, data_string)

        self.assertEqual(event.get_NFC_string(), data_string)
        self.assertEqual(event.get_event_type(), EventType.NFC_EVENT)

    def test_alarm_event(self):
        description = 'Test Alarm'
        speech_message = 'Test Speech Message'
        event = AlarmEvent(AlarmSeverity.MINOR_ALARM,
                           description,
                           speech_message)
        self.assertEqual(AlarmSeverity.MINOR_ALARM, event.get_severity())
        self.assertEqual(description, event.get_description())
        self.assertEqual(speech_message, event.get_speech_message())


class TestEventManager(unittest.TestCase):
    def test_broadcast_event(self):
        test_message = 'test_message'
        peers = []
        event_manager = EventManager(peers);

        m = mox.Mox()
        mock_broadcast_data = m.CreateMockAnything()
        event_manager._broadcast_data = new.instancemethod(mock_broadcast_data,
                                                           event_manager)
        mock_broadcast_data(event_manager,
                            EventManager.serialize_event(test_message),
                            peers)
        m.ReplayAll()

        event_manager.broadcast_event(test_message)

        m.VerifyAll()

    def test_listen(self):
        listen_port = 8000
        test_message = pickle.dumps('test_message')
        event_manager = EventManager([], listen_port);

        # Wait for thread to be ready
        while not event_manager.is_listening():
            time.sleep(0)

        # Mock the event_received method
        m = mox.Mox()
        mock_event_received = m.CreateMockAnything()
        event_manager.event_received = new.instancemethod(mock_event_received,
                                                          event_manager)
        mock_event_received(event_manager, 'test_message')
        m.ReplayAll()

        s = socket.create_connection((socket.gethostname(), listen_port))
        s.sendall(test_message)
        s.shutdown(socket.SHUT_RDWR)
        s.close()

        event_manager.shutdown()
        
        # Make sure event_received was called on the EventManager
        m.VerifyAll()

    def test_subscribe(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'

        event_manager = EventManager([]);
        event_manager.subscribe(event_type,
                                     controller)

        self.assertIsNotNone(event_manager.subscriptions[event_type])
        self.assertEqual(event_manager.subscriptions[event_type][0],
                         controller)
        self.assertEqual(len(event_manager.subscriptions[event_type]), 1)

    def test_subscribe_same(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'

        event_manager = EventManager([]);
        event_manager.subscribe(event_type, controller)
        event_manager.subscribe(event_type, controller)
        self.assertEqual(len(event_manager.subscriptions[event_type]), 1)

    def test_subscribe_multiple(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        other_controller = 'dummy_controller_other'
        
        event_manager = EventManager([]);
        event_manager.subscribe(event_type, controller)
        event_manager.subscribe(event_type, other_controller)
        self.assertEqual(len(event_manager.subscriptions[event_type]), 2)

    def test_serialize_deserialize_event(self):
        event_type = EventType.DOOR_SENSOR_EVENT
        timestamp = datetime.utcnow()
        event = Event(event_type, timestamp)
        
        event_manager = EventManager([]);
        serialized = event_manager.serialize_event(event)
        deserialized = event_manager.deserialize_event(serialized)

        self.assertIsInstance(deserialized, Event)
        self.assertEqual(deserialized.get_event_type(), event_type)
        self.assertEqual(deserialized.get_timestamp(), timestamp)

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

        event_manager = EventManager([]);
        event_manager.subscribe(event_type, controller)
        event_manager.event_received(event)
        event_manager.process_events()

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

        event_manager = EventManager([]);
        event_manager.subscribe(EventType.DOOR_SENSOR_EVENT, door_controller)
        event_manager.subscribe(EventType.WINDOW_SENSOR_EVENT, window_controller)

        # Send event
        event_manager.event_received(door_event)
        event_manager.process_events()

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

class TestSensorController(unittest.TestCase):
    def setUp(self):
        self.sensor_controller = SensorController(None)
        
    def test_handle_event(self):
        pass 
    
    def test_poll_sensor(self):
        pass
    
    def test_handle_sensor_input(self):
        pass 

    def test_check_sensor_status(self):
        pass

class TestSystemController(unittest.TestCase):
    def setUp(self):
        self.system_controller = SystemController(None)
    
    def test_handle_bad_events(self):
        event = Event(1000)
        ret_value = self.system_controller.handle_event(event)
        self.assertFalse(ret_value)

    def test_system_state(self):
        # Check controller's initial state
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED) 
        
        # Try to disarm with KEYPAD_EVENT
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'd')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(), 
                         SystemState.DISARMED)

        # Try to arm with KEYPAD_EVENT
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'a')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED)
        

    def test_system_state_caps(self):
        # Check controller's initial state
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED) 
        
        # Try to disarm with KEYPAD_EVENT
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'D')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(), 
                         SystemState.DISARMED)

        # Try to arm with KEYPAD_EVENT
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'A')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED)
        
    def test_window_event_handler(self):
        # Arm the system
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'A')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED)
        
        # Test an window opening with system armed
        event = WindowSensorEvent(1, 1, True)
        ret_value = self.system_controller.handle_event(event)
        self.assertTrue(ret_value)
        
        # Test a closed window...
        event = WindowSensorEvent(1,1,False)
        ret_value = self.system_controller.handle_event(event)
        self.assertFalse(ret_value)

        # Disarm the system
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'd')
        self.system_controller.handle_event(event)

         # Test an window opening with system disarmed
        event = WindowSensorEvent(1, 1, True)
        ret_value = self.system_controller.handle_event(event)
        self.assertFalse(ret_value)

        # Test a closed window...
        event = WindowSensorEvent(1,1,False)
        ret_value = self.system_controller.handle_event(event)
        self.assertFalse(ret_value)

    def test_flood_event_handler(self):
        # Arm the system
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'A')
        self.system_controller.handle_event(event)
        self.assertEqual(self.system_controller.get_system_state(),
                         SystemState.ARMED)
        test_vector = [
                        {'height' : 0 , 'delta' : 0, 'ret_value' : False},
                        {'height' : 1 , 'delta' : 0, 'ret_value' : True},
                        {'height' : 0 , 'delta' : 1, 'ret_value' : True},
                        {'height' : 3 , 'delta' : 0, 'ret_value' : True}
                      ]

        for test in test_vector:
            event = FloodSensorEvent(1,test['height'], test['delta'])
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, test['ret_value'])

        # Disarm the system -- Nothing should change in the test cases...
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'D')
        self.system_controller.handle_event(event)
        
        for test in test_vector:
            event = FloodSensorEvent(1,test['height'], test['delta'])
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, test['ret_value'])

    def test_temp_sensor_event(self):
        # TODO :: setup mox to get the alarm event severity...
        # Arm the system.
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'a')
        self.system_controller.handle_event(event)
        
        test_vector = [
                        {'temp' : 0, 'delta' : 0, 'ret_value' : True},
                        {'temp' : 18, 'delta' : 0, 'ret_value' : False},
                        {'temp' : 25, 'delta' : 0, 'ret_value' : False},
                        {'temp' : 27, 'delta' : 0, 'ret_value' : True},
                        {'temp' : 15, 'delta' : 0, 'ret_value' : True},
                        {'temp' : 33, 'delta' : 0, 'ret_value' : True},
                        {'temp' : 25, 'delta' : 2, 'ret_value' : False},
                        {'temp' : 25, 'delta' : 3, 'ret_value' : True},
                        {'temp' : 25, 'delta' : 5, 'ret_value' : True},
                        {'temp' : 25, 'delta' : 10, 'ret_value' : True}
                      ]
        
        for test in test_vector:
            event = TempSensorEvent(1, test['temp'], test['delta'], )
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, test['ret_value'])
        
        # Disarm the system, ensure that it is system state independent...
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, 'd')
        self.system_controller.handle_event(event)

        for test in test_vector:
            event = TempSensorEvent(1, test['temp'], test['delta'])
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, test['ret_value'])
        
    def test_motion_event(self):
        # Arm the system
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, "a")
        self.system_controller.handle_event(event)
        
        test_vector = [
                        # Start a motion event, but it doesn't have an end time
                        {'threshold' : 10, 'start_time' : datetime.utcnow(),
                        'end_time' : None, 'ret_value' : False}, 
                        # Motion event that will send an alarm
                        {'threshold' : 10, 'start_time' : datetime.utcnow(),
                        'end_time' : datetime.utcnow() + timedelta(0,3600),
                        'ret_value' : True},
                        # Motion event representing a glitch
                        {'threshold' : 10, 'start_time' : datetime.utcnow(),
                        'end_time' : datetime.utcnow() + timedelta(0,5), 
                        'ret_value' : False},
                        # Motion event in the past that will send an alarm
                        {'threshold' : 10, 
                        'start_time' : datetime(2012, 3, 15, 23, 33),
                        'end_time' : datetime(2012,3,15,23,35), 
                        'ret_value' : True},
                        # Motion event in the past that will not send an alarm
                        {'threshold' : 10, 
                        'start_time' : datetime(2012, 3, 15, 23, 33),
                        'end_time' : datetime(2012,3,15,23,33,5),
                        'ret_value' : False}
                      ]

        # Motion started
        for test in test_vector:
            event = MotionSensorEvent(1, test['threshold'], test['start_time'],
                                      test['end_time'])
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, test['ret_value']) 

        # Disarm the system
        event = KeypadEvent(EventType.KEYPAD_EVENT, 1, "d")
        self.system_controller.handle_event(event)
        
        # Everything should return False
        for test in test_vector:
            event = MotionSensorEvent(1, test['threshold'], test['start_time'],
                                      test['end_time'])
            ret_value = self.system_controller.handle_event(event)
            self.assertEqual(ret_value, False)

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
