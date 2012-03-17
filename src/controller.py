import threading
from eventmanager import EventManager

class Controller:
    def __init__(self, event_manager):
        self.event_manager = event_manager
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def handle_event(self, event):
        pass

    def run(self):
        while not self._stop.isSet():
            self.event_manager.process_events()
