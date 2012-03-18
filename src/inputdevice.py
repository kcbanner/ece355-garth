from event import *
from event_type import EventType

class InputDevice():
    def __init__(self, device_id):
        self.device_id = device_id

    def get_device_id(self):
        return self.device_id

class NFCReaderInputDevice(InputDevice):
    def __init__(self, device_id):
        InputDevice.__init__(self, device_id)
        self.data = None
    
    def set_data(self, data):
        self.data = data
        
    def generate_NFC_event(self):
        return NFCEvent(self.device_id, self.data)

class KeypadInputDevice(InputDevice):
    def __init__(self, device_id):
        InputDevice.__init__(self, device_id)
        self.input_char = None

    def set_input_char(self, char):
        self.input_char = char

    def generate_keypad_event(self):
        return KeypadEvent(EventType.KEYPAD_EVENT, self.device_id,
                            self.input_char)
