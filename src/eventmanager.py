import pickle
from communicationsinterface import CommunicationsInterface

class EventManager:
    def __init__(self):
        self.in_event_queue = []
        self.out_event_queue = []
        self.communications_interface = CommunicationsInterface(self)
        self.subscriptions = {}

    @classmethod
    def serialize_event(cls, event):        
        return pickle.dumps(event)

    @classmethod
    def deserialize_event(cls, event_string):
        return pickle.loads(event_string)
        
    def broadcast_event(self, event):
        data = self.serialize_event(event)       
        self.communications_interface.broadcast_data(data)
        
    def event_received(self, event):
        if event.event_type in self.subscriptions:
            for controller in self.subscriptions[event.event_type]:
                controller.handle_event(event)
        
    def subscribe(self, event_type, controller):
        if not event_type in self.subscriptions:
            self.subscriptions[event_type] = []
        
        if controller not in self.subscriptions[event_type]:
            self.subscriptions[event_type].append(controller)
