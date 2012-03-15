from controller import Controller

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

    def get_input_devices(self):
        return self.input_devices
    
    def get_system_state(self):
        return self.system_state

    def get_user_list(self):
        return self.user_list

    def handle_event(self, event):
        pass

    def arm_system(self):
        pass

    def disarm_system(self):
        pass

    def log_event_to_server(self, event):
        pass
    
    def handle_nfc_input(self, nfc_event):
        pass
    
    def handle_keypad_input(self, keypad_event):
        pass
    
    def raise_alarm(self, alarm_event):
        pass
