from controller import Controller
from event_type import EventType
from event import *
from datetime import timedelta
import logging

STR_ALARM_DOOR_DESC = ""
STR_ALARM_DOOR_SPEECH = ""
STR_ALARM_WINDOW_DESC = ""
STR_ALARM_WINDOW_SPEECH = ""

STR_ALARM_FLOOD_MAJOR_DESC = ""
STR_ALARM_FLOOD_MAJOR_SPEECH = ""
STR_ALARM_FLOOD_CRIT_DESC = ""
STR_ALARM_FLOOD_CRIT_SPEECH = ""

STR_ALARM_TEMP_MINOR_DESC = ""
STR_ALARM_TEMP_MINOR_SPEECH = ""
STR_ALARM_TEMP_MAJOR_DESC = ""
STR_ALARM_TEMP_MAJOR_SPEECH = ""
STR_ALARM_TEMP_CRIT_DESC = ""
STR_ALARM_TEMP_CRIT_SPEECH = ""

STR_ALARM_MOTION_SPEECH = ""
STR_ALARM_MOTION_DESC = ""


FLOOD_DELTA_HEIGHT_CRIT = 3

ALARM_MOTION_DURATION = timedelta(0, 30)

class SystemState:
    ARMED           = 1
    DISARMED        = 2
    ERROR_ARMED     = 3
    ERROR_DISARMED  = 4
    UNKNOWN         = 5


class SystemController(Controller):
    def __init__(self, event_manager):
        Controller.__init__(self, event_manager)
        self.system_state = SystemState.ARMED
        self.user_list = []
        self.input_devices = []

        self.event_handling_functions = {
            EventType.DOOR_SENSOR_EVENT : self._handle_door_event,
            EventType.WINDOW_SENSOR_EVENT : self._handle_window_event,
            EventType.FLOOD_SENSOR_EVENT : self._handle_flood_event,
            EventType.TEMP_SENSOR_EVENT : self._handle_temp_event,
            EventType.MOTION_SENSOR_EVENT : self._handle_motion_event,
            EventType.ALARM_EVENT : self._handle_alarm_event,
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
        try:
            return self.event_handling_functions[event_type](event)  
        except Exception as e:
            logging.debug(e)
            return False

    def _handle_door_event(self, event):
        #if event.get_opened and self.system_state == SystemState.ARMED:
        pass   

    # Tested
    def _handle_window_event(self, event):
        if event.get_opened() and self.system_state == SystemState.ARMED:
            logging.debug("Window opened while system armed")
            description = STR_ALARM_WINDOW_DESC
            speech_message = STR_ALARM_WINDOW_SPEECH
            alarm = AlarmEvent(EventType.ALARM_EVENT, AlarmSeverity.MAJOR_ALARM,
                                description, speech_message) 
            self.raise_alarm(alarm)
            return True
        return False
    
    # Tested
    def _handle_flood_event(self, event):
        # TODO :: make this better
        description = ""
        message = ""
        severity = AlarmSeverity.MINOR_ALARM

        if event.get_height_delta() >= FLOOD_DELTA_HEIGHT_CRIT:
            description = STR_ALARM_FLOOD_CRIT_DESC
            message = STR_ALARM_FLOOD_CRIT_SPEECH
            severity = AlarmSeverity.CRITICAL_ALARM
        elif event.get_water_height() >= 1 or event.get_height_delta() >= 1:
            description = STR_ALARM_FLOOD_MAJOR_DESC
            message = STR_ALARM_FLOOD_MAJOR_SPEECH
            severity = AlarmSeverity.MAJOR_ALARM
        else: 
            return False
        alarm = AlarmEvent(severity, description, message)
        self.raise_alarm(alarm)
        return True
    
    # Tested
    def _handle_temp_event(self, event):
        # TODO :: make numbers less magic

        description = ""
        message = ""
        severity = AlarmSeverity.MINOR_ALARM
        
        temp = event.get_temperature()
        delta = event.get_temp_delta()
        if (temp >= 26 and temp < 30) or \
           (temp < 18 and temp >= 15) or \
           (abs(delta) <= 3 and abs(delta) > 2):  
            description = STR_ALARM_TEMP_MINOR_DESC
            message = STR_ALARM_TEMP_MINOR_SPEECH
            severity = AlarmSeverity.MINOR_ALARM
        elif (temp >= 30 and temp < 35) or \
           (temp < 15 and temp >= 12) or \
           (abs(delta) > 3  and abs(delta) <= 5):
            description = STR_ALARM_TEMP_MAJOR_DESC
            message = STR_ALARM_TEMP_MAJOR_SPEECH
            severity = AlarmSeverity.MAJOR_ALARM
        elif (temp >= 35) or (temp < 12) or (abs(delta) > 5):
            description = STR_ALARM_TEMP_CRIT_DESC
            message = STR_ALARM_TEMP_CRIT_SPEECH
            severity = AlarmSeverity.CRITICAL_ALARM
        else: 
            return False
        alarm = AlarmEvent(severity, description, message)
        self.raise_alarm(alarm)
        return True
    
    # Tested
    def _handle_motion_event(self, event):
        description = ""
        message = ""
        severity = AlarmSeverity.MINOR_ALARM
                
        duration = event.get_duration()
        if event.get_end_time() == None or \
           self.system_state == SystemState.DISARMED :
            return False
        elif (duration >= ALARM_MOTION_DURATION):
            message = STR_ALARM_MOTION_SPEECH
            description = STR_ALARM_MOTION_DESC
            severity = AlarmSeverity.MAJOR_ALARM
        else:
            return False
        
        alarm = AlarmEvent(severity, description, message)
        self.raise_alarm(alarm)
        return True

    def _handle_alarm_event(self, event):
        self.raise_alarm(event)
        return True
    
    # Tested
    def _arm_system(self):
        self.system_state = SystemState.ARMED

    # Tested
    def _disarm_system(self):
        self.system_state = SystemState.DISARMED

    def log_event_to_server(self, event):
        logging.debug("Sensor_controller::log_event_to_server %s" % str(event))
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

