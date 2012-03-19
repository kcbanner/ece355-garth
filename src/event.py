import json
import time
from event_type import EventType
from datetime import datetime

#
# JSON Encoder for Events
#

class EventEncoder(json.JSONEncoder):
    def default(self, obj):
        fields = {}

        # Event
        if isinstance(obj, Event):
            fields['timestamp'] = time.mktime(obj.timestamp.timetuple())
            fields['event_type'] = obj.event_type
        
            # SensorEvent
            if isinstance(obj, SensorEvent):
                fields['sensor_id'] = obj.sensor_id
                
                if isinstance(obj, DoorSensorEvent):
                    fields['door_id'] = obj.door_id
                    fields['opened'] = obj.opened
                elif isinstance(obj, WindowSensorEvent):
                    fields['window_id'] = obj.window_id
                    fields['opened'] = obj.opened
                elif isinstance(obj, TempSensorEvent):
                    fields['temperature'] = obj.temperature
                    fields['delta'] = obj.delta
                elif isinstance(obj, FloodSensorEvent):
                    fields['water_height'] = obj.water_height
                    fields['delta'] = obj.delta
                elif isinstance(obj, MotionSensorEvent):
                    fields['current_threshold'] = obj.current_threshold
                    fields['start_time'] = time.mktime(obj.start_time.timetuple())
                    fields['end_time'] = time.mktime(obj.end_time.timetuple())
                    fields['duration'] = obj.get_duration()
            # InputEvent
            elif isinstance(obj, InputEvent):
                fields['input_device_id'] = obj.input_device_id

                if isinstance(obj, KeypadEvent):
                    fields['input_char'] = obj.input_char
                elif isinstance(obj, NFCEvent):
                    fields['data'] = obj.data
            # AlarmEvent 
            elif isinstance(obj, AlarmEvent):
                fields['severity'] = obj.severity
                fields['description'] = obj.description
                fields['speech_message'] = obj.speech_message

            return fields
        else:
            raise TypeError('Provided object was not an Event')


class Event:
    def __init__(self, event_type, timestamp=None):
        self.event_type = event_type

        if timestamp:
            self.timestamp = timestamp
        else:        
            self.timestamp = datetime.utcnow()
   
    def __str__(self):
        return "Event: type = %s, timestamp = %s" % (self.event_type, self.timestamp)
        
    def get_event_type(self):
        return self.event_type
    
    def get_timestamp(self):
        return self.timestamp
    
#
# Sensor Event Base Class
#

class SensorEvent(Event):
    def __init__(self, event_type, sensor_id, timestamp=None):
        Event.__init__(self, event_type, timestamp)
        self.sensor_id = sensor_id
    
    def __str__(self):
        s = "SensorEvent: type = %s, timestamp = %s, sensor_id = %s" % (
            self.event_type, self.timestamp, self.sensor_id)
        return s

    def get_sensor_id(self):
        return self.sensor_id

#
# Sensor Events
# 

class DoorSensorEvent(SensorEvent):
    def __init__(self, sensor_id, door_id, opened, timestamp=None):
        SensorEvent.__init__(self, EventType.DOOR_SENSOR_EVENT, sensor_id, timestamp)
        self.door_id = door_id
        self.opened = opened

    def get_door_id(self):
        return self.door_id

    def get_opened(self):
        return self.opened

class WindowSensorEvent(SensorEvent):
    def __init__(self, sensor_id, window_id, opened, timestamp=None):
        SensorEvent.__init__(self,
                             EventType.WINDOW_SENSOR_EVENT,
                             sensor_id,
                             timestamp)
        self.window_id = window_id
        self.opened = opened

    def __str__(self):
        s = "WindowSensorEvent: type = %s, timestamp = %s, sensor_id = %s," \
            " opened = %s" % \
            (self.event_type, self.timestamp, self.sensor_id, self.opened)
        return s

    def get_window_id(self):
        return self.window_id

    def get_opened(self):
        return self.opened

class TempSensorEvent(SensorEvent):
    def __init__(self, sensor_id, temperature, delta, timestamp=None):
        SensorEvent.__init__(self, EventType.TEMP_SENSOR_EVENT, sensor_id, timestamp)
        self.temperature = temperature
        self.delta = delta
    
    def get_temperature(self):
        return self.temperature

    def get_temp_delta(self):
        return self.delta

class FloodSensorEvent(SensorEvent):
    def __init__(self, sensor_id, water_height, delta, timestamp=None):
        SensorEvent.__init__(self,
                             EventType.FLOOD_SENSOR_EVENT,
                             sensor_id,
                             timestamp)
        self.water_height = water_height
        self.delta = delta

    def get_water_height(self):
        return self.water_height

    def get_height_delta(self):
        return self.delta

class MotionSensorEvent(SensorEvent):
    def __init__(self,
                 sensor_id,
                 current_threshold,
                 start_time,
                 end_time=None,
                 timestamp=None):
        SensorEvent.__init__(self, EventType.MOTION_SENSOR_EVENT, sensor_id)
        self.current_threshold = current_threshold
        self.start_time = start_time
        self.end_time = end_time

    def get_threshold(self):
        return self.current_threshold
    
    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time

    def get_duration(self):
        if self.end_time != None:
            return self.end_time - self.start_time
        else:
            return datetime.utcnow() - self.start_time
        
#
# Input Event Base Class
#

class InputEvent(Event):
    def __init__(self, event_type, input_device_id, timestamp=None):
        Event.__init__(self, event_type, timestamp)
        self.input_device_id = input_device_id

    def get_device_id(self):
        return self.input_device_id

#
# Input Events
#

class KeypadEvent(InputEvent):
    def __init__(self, event_type, input_device_id, input_char, timestamp=None):
        InputEvent.__init__(self, event_type, input_device_id, timestamp)
        self.input_char = input_char

    def get_input(self):
        return self.input_char

class NFCEvent(InputEvent):
    def __init__(self, input_device_id, data, timestamp=None):
        InputEvent.__init__(self, EventType.NFC_EVENT, input_device_id, timestamp)
        self.data = data

    def get_NFC_string(self):
        return self.data
            
#
# Alarm Events
#

class AlarmSeverity:
    CRITICAL_ALARM  = 1
    MAJOR_ALARM     = 2
    MINOR_ALARM     = 3

class AlarmEvent(Event):
    def __init__(self,
                 severity,
                 description,
                 speech_message,
                 timestamp=None):
        Event.__init__(self, EventType.ALARM_EVENT, timestamp)
        self.severity = severity
        self.description = description
        self.speech_message = speech_message
    
    def __eq__(self, other):
        return (other.description == self.description and \
                other.speech_message == self.speech_message and \
                other.severity == self.severity)
    def get_severity(self):
        return self.severity

    def get_description(self):
        return self.description

    def get_speech_message(self):
        return self.speech_message

