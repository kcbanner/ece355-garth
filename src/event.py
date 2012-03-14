import event_type
from datetime import datetime

class Event:
    def __init__(self, event_type, timestamp=None):
        self.event_type = event_type

        if timestamp:
            self.timestamp = timestamp
        else:        
            self.timestamp = datetime.utcnow()
    
    def get_event_type(self):
        return self.event_type
    
    def get_timestamp(self):
        return self.timestamp

#
# Sensor Event Base Class
#

class SensorEvent(Event):
    def __init__(self, event_type, sensor_id):
        Event.__init__(self, event_type)
        self.sensor_id = sensor_id

    def get_sensor_id():
        return self.sensor_id

#
# Sensor Events
# 

class DoorSensorEvent(SensorEvent):
    def __init__(self, event_type, sensor_id, door_id, opened):
        SensorEvent.__init__(self, event_type, sensor_id)
        self.door_id = door_id
        self.opened = opened

    def get_door_id():
        return self.door_id

    def get_opened():
        return self.opened

class WindowSensorEvent(SensorEvent):
    def __init__(self, event_type, sensor_id, window_id, opened):
        SensorEvent.__init__(self, event_type, sensor_id)
        self.window_id = window_id
        self.opened = opened

    def get_window_id():
        return self.window_id

    def get_opened():
        return self.opened

class TempSensorEvent(SensorEvent):
    def __init__(self, event_type, sensor_id, temperature, delta):
        SensorEvent.__init__(self, event_type, sensor_id)
        self.temperature = temperature
        self.delta = delta
    
    def get_temperature():
        return self.temperature

    def get_temp_delta():
        return self.delta

class FloodSensorEvent(SensorEvent):
    def __init__(self, event_type, sensor_id, water_height, delta):
        SensorEvent.__init__(self, event_type, sensor_id)
        self.water_height = water_height
        self.delta = delta

    def get_water_height():
        return self.water_height

    def get_height_delta():
        return self.delta

#
# Input Event Base Class
#

class InputEvent(Event):
    def __init__(self, event_type, input_device_id):
        Event.__init__(self, event_type)
        self.input_device_id = input_device_id

    def get_device_id():
        return self.input_device_id

#
# Input Events
#

class KeypadEvent(InputEvent):
    def __init__(self, event_type, input_device_id, input_char):
        InputEvent.__init__(self, event_type, input_device_id)
        self.input_char = input_char

    def get_input():
        return self.input_char

class NFCEvent(InputEvent):
    def __init__(self, event_type, input_device_id, data):
        InputEvent.__init__(self, event_type, input_device_id)
        self.data = data

    def get_NFC_string():
        return self.data
            
#
# Alarm Events
#

class AlarmSeverity:
    CRITICAL_ALARM  = 1
    MAJOR_ALARM     = 2
    MINOR_ALARM     = 3

class AlarmEvent(Event):
    def __init__(self, event_type, severity, description, speech_message):
        Event.__init__(self, event_type)
        self.severity = severity
        self.description = description
        self.speech_message = speech_message
    
    def get_severity():
        return self.severity

    def get_description():
        return self.description

    def get_speech_message():
        return self.speech_message

