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
