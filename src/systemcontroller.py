from controller import Controller
from event_type import EventType
from event import *
import logging

class SystemState:
    ARMED           = 1
    DISARMED        = 2
    ERROR_ARMED     = 3
    ERROR_DISARMED  = 4
    UNKNOWN         = 5

class SystemController(Controller):
    def __init__(self, event_manager):
        Controller.__init__(self, event_manager)
        self.system_state = SystemState.UNKNOWN
        self.user_list = []
        self.input_devices = []

        self.event_handling_functions = {
            EventType.DOOR_SENSOR_EVENT : self.__handle_door_event,
            EventType.WINDOW_SENSOR_EVENT : self.__handle_window_event,
            EventType.FLOOD_SENSOR_EVENT : self.__handle_flood_event,
            EventType.TEMP_SENSOR_EVENT : self.__handle_temp_event,
            EventType.MOTION_SENSOR_EVENT : self.__handle_motion_event,
            EventType.ALARM_SENSOR_EVENT : self.__handle_alarm_event,
            EventType.KEYPAD_EVENT : self.__handle_keypad_event,
            EventType.NFC_EVENT : self.__handle_nfc_event
        }

    def get_input_devices(self):
        return self.input_devices
    
    def get_system_state(self):
        return self.system_state

    def get_user_list(self):
        return self.user_list

    def handle_event(self, event):
        event_type = event.get_event_type()
        self.log_event_to_server(event)
        self.event_handling_functions[event_type](event)  

    def __handle_door_event(self, event):
        pass

    def __handle_window_event(self, event):
        pass
    
    def __handle_flood_event(self, event):
        pass

    def __handle_temp_event(self, event):
        pass

    def __handle_motion_event(self, event):
        pass

    def __handle_alarm_event(self, event):
        pass
    
# Tested
    def __arm_system(self):
        self.system_state = SystemState.ARMED

# Tested
    def __disarm_system(self):
        self.system_state = SystemState.DISARMED

    def log_event_to_server(self, event):
        logging.debug(event.__str__())
        pass

    # 
    # Outside of implementation scope
    #

    def __handle_nfc_event(self, nfc_event):
        pass
    
    #
    # "a" or "A" => arm system
    # "d" or "D" => disarm system
    # "s" or "S" => stop alarms
    #
    def __handle_keypad_event(self, keypad_event):
        pass
    
    def raise_alarm(self, alarm_event):
        pass

