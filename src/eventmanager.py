import pickle
from communicationsinterface import CommunicationsInterface

class EventManager:
    def __init__(self):
        self.in_event_queue = []
        self.out_event_queue = []
        self.communications_interface = CommunicationsInterface(self)
        self.subscriptions = {}

    def serialize_event(self, event):        
        return pickle.dumps(event)

    def deserialize_event(self, event_string):
        return pickle.loads(event_string)
        
    def broadcast_event(self, event):
        pass

    def event_received(self, event):
        pass
        
    def subscribe(self, event_type, controller):
        if not event_type in self.subscriptions:
            self.subscriptions[event_type] = []
        
        if controller not in self.subscriptions[event_type]:
            self.subscriptions[event_type].append(controller)

    
