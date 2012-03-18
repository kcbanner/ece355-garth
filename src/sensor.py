from event import *
from datetime import datetime
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
        raise NotImplementedError(
            "Generate sensor event called on base sensor class")

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
        return DoorSensorEvent(self.sensor_id, self.door_id, self.opened) 

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
        return WindowSensorEvent(self.sensor_id, self.window_id, self.opened)

class FloodSensor(Sensor):
    def __init__(self, sensor_id, status, current_water_height=0):
        Sensor.__init__(self, sensor_id, status)
        self.last_water_height = 0
        self.current_water_height = current_water_height

    def get_water_height(self):
        return self.current_water_height
    
    def get_delta(self):
        return self.current_water_height - self.last_water_height

    def set_water_height(self, water_height):
        self.last_water_height = self.current_water_height
        self.current_water_height = water_height

    def generate_sensor_event(self):
        return FloodSensorEvent(self.sensor_id,
                                self.current_water_height,
                                self.get_delta())

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, status, current_temperature=0):
        Sensor.__init__(self, sensor_id, status)
        self.last_temperature = 0
        self.current_temperature = current_temperature

    def get_temperature(self):
        return self.current_temperature

    def get_delta(self):
        return self.current_temperature - self.last_temperature

    def set_temperature(self, temperature):
        self.last_temperature = self.current_temperature
        self.current_temperature = temperature

    def generate_sensor_event(self):
        return TempSensorEvent(self.sensor_id, self.get_temperature(), self.get_delta())

class MotionSensor(Sensor):
    def __init__(self, sensor_id, status, motion_threshold):
        Sensor.__init__(self, sensor_id, status)
        self.motion_threshold = motion_threshold
        self.motion_started = 0
    
    def get_motion_threshold(self):
        return self.motion_threshold

    def set_motion_threshold(self, motion_threshold):
        self.motion_threshold = motion_threshold
   
    # This is for testing purposes...
    def set_motion_started_time(self, motion_started_time):
        self.motion_started = motion_started_time

    def motion_detected(self):
        self.motion_started = datetime.utcnow()
        
    def generate_sensor_event(self):
        return MotionSensorEvent(self.sensor_id,
                                 self.motion_threshold,
                                 self.motion_started)
        pass
