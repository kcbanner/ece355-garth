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
            EventType.DOOR_SENSOR_EVENT : self._handle_door_event,
            EventType.WINDOW_SENSOR_EVENT : self._handle_window_event,
            EventType.FLOOD_SENSOR_EVENT : self._handle_flood_event,
            EventType.TEMP_SENSOR_EVENT : self._handle_temp_event,
            EventType.MOTION_SENSOR_EVENT : self._handle_motion_event,
            EventType.ALARM_SENSOR_EVENT : self._handle_alarm_event,
            EventType.KEYPAD_EVENT : self._handle_keypad_event,
            EventType.NFC_EVENT : self._handle_nfc_event
        }

        # Subscribe to events
        if self.event_manager != None:
            for event_type in self.event_handling_functions.keys():
                self.event_manager.subscribe(event_type, self)

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

    def _handle_door_event(self, event):
        pass

    def _handle_window_event(self, event):
        pass
    
    def _handle_flood_event(self, event):
        pass

    def _handle_temp_event(self, event):
        pass

    def _handle_motion_event(self, event):
        pass

    def _handle_alarm_event(self, event):
        pass
    
# Tested
    def _arm_system(self):
        self.system_state = SystemState.ARMED

# Tested
    def _disarm_system(self):
        self.system_state = SystemState.DISARMED

    def log_event_to_server(self, event):
        logging.debug(str(event))
        pass

    # 
    # Outside of implementation scope
    #

    def _handle_nfc_event(self, nfc_event):
        pass
    
    #
    # "a" or "A" => arm system
    # "d" or "D" => disarm system
    # "s" or "S" => stop alarms
    #
    def _handle_keypad_event(self, keypad_event):
        if keypad_event.input_char.lower() == 'a':
            self.system_state = SystemState.ARMED;
        elif keypad_event.input_char.lower() == 'd':
            self.system_state = SystemState.DISARMED;
        elif keypad_event.input_char.lower() == 's':
            pass
    
    def raise_alarm(self, alarm_event):
        pass

