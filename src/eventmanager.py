import pickle
import threading
import Queue
from communicationsinterface import CommunicationsInterface

class EventManager:
    def __init__(self, peers, listen_port=None):
        self.peers = peers

        self.in_event_queue = Queue.Queue()
        self.subscriptions = {}

        # Start thread to listen for incoming events    
        if listen_port:
            self.peers.append(('localhost', listen_port))
            self.listener_thread = CommunicationsInterface.listen(self, listen_port)
            self.listener_thread.daemon = True
            self.listener_thread.start()

    def is_listening(self):
        return self.listener_thread.is_listening()

    def shutdown(self):
        self.listener_thread.stop()
        self.listener_thread.join()

    @classmethod
    def serialize_event(cls, event):
        return pickle.dumps(event)

    @classmethod
    def deserialize_event(cls, event_string):
        return pickle.loads(event_string)

    def event_received(self, event):
        self.in_event_queue.put(event)
        
    def broadcast_event(self, event):
        data = self.serialize_event(event)
        CommunicationsInterface.broadcast_data(data, self.peers)
   
    def subscribe(self, event_type, controller):
        if not event_type in self.subscriptions:
            self.subscriptions[event_type] = []
        
        if controller not in self.subscriptions[event_type]:
            self.subscriptions[event_type].append(controller)

    def process_events(self):

        # Get an event from the incoming queue and dispatch it to subscribers
        try:
            event = self.in_event_queue.get(timeout=1)
            if event.event_type in self.subscriptions:
                for controller in self.subscriptions[event.event_type]:
                    controller.handle_event(event)
        except Queue.Empty:
            pass
