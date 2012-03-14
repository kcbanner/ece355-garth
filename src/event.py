import event_type
from datetime import datetime

class Event:
    def __init__(self, event_type):
        self.event_type = event_type
        self.timestamp = datetime.utcnow()
    
    def get_event_type(self):
        return self.event_type
    
    def get_timestamp(self):
        return self.timestamp


