from controller import Controller

#
# Sensor controller handles the polling of events, not the handling of event
# data
# 

class SensorController(Controller):
    def __init__(self, event_manager):
        Controller.__init__(self, event_manager)
        self.sensor_list = []
    
    def add_sensor(self, sensor):
        self.sensor_list.append(sensor)
    
    def remove_sensor(self, sensor):
        self.sensor_list.remove(sensor)

    def handle_event(self, event):
        pass
    
    def poll_sensor(self, sensor_id):
        pass

    def handle_sensor_input(self, sensor_event):
        pass

    def check_sensor_status(self, sensor_id):
        pass
