from event import *

from event_type import EventType

class SensorStatus():
    ONLINE      = 1
    OFFLINE     = 2
    BATTERY_LOW = 3
    ERROR       = 4


class Sensor():
    def __init__(self, sensor_id, status):
        self.sensor_id = sensor_id
        self.status = status

    def get_sensor_id(self):
        return self.sensor_id

    def get_sensor_status(self):
        return self.status

    def generate_sensor_event(self):
        raise "Generate sensor event called on base sensor class"

class DoorSensor(Sensor):
    def __init__(self, sensor_id, status, door_id, opened=False):
        Sensor.__init__(self, sensor_id, status)
        self.door_id = door_id
        self.opened = opened

    def get_door_id(self):
        return self.door_id
    
    def set_opened(self, opened):
        self.opened = opened
    
    def generate_sensor_event(self):
        return DoorSensorEvent(EventType.DOOR_SENSOR_EVENT, self.sensor_id,
        self.door_id, self.opened) 

class WindowSensor(Sensor):
    def __init__(self, sensor_id, status, window_id, opened=False):
        Sensor.__init__(self, sensor_id, status)
        self.window_id = window_id
        self.opened = opened
    
    def get_window_id(self):
        return self.window_id
    
    def set_opened(self, opened):
        self.opened = opened

    def generate_sensor_event(self):
        return WindowSensorEvent(EventType.WINDOW_SENSOR_EVENT, self.sensor_id,
                                self.window_id, self.opened)

class FloodSensor(Sensor):
    def __init__(self, sensor_id, status, last_water_height=None):
        Sensor.__init__(self, sensor_id, status)
        self.last_water_height = last_water_height

    def get_water_height(self):
        return self.current_water_height
    
    def set_water_height(self, water_height):
        pass     

    def generate_sensor_event(self):
        pass

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, status, last_temperature=None):
        Sensor.__init__(self, sensor_id, status)
        self.last_temperature = last_temperature

    def get_temperature(self):
        pass

    def generate_sensor_event(self):
        pass

class MotionSensor(Sensor):
    def __init__(self, sensor_id, status, motion_threshold):
        Sensor.__init__(self, sensor_id, status)
        self.motion_threshold = motion_threshold
    
    def get_motion_threshold(self):
        return self.motion_threshold

    def set_motion_threshold(self, motion_threshold):
        self.motion_threshold = motion_threshold

    def generate_sensor_event(self):
        pass
