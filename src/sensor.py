import event

class SensorStatus():
    ONLINE      = 1
    OFFLINE     = 2
    BATTERY_LOW = 3
    ERROR       = 4


class Sensor():
    def __init__(self, sensor_id, status):
        self.sensor_id = sensor_id
        self.status = status

    def get_sensor_id(self):
        return self.sensor_id

    def get_sensor_status(self):
        return self.state

    def generate_sensor_event(self):
        raise "Generate sensor event called on base sensor class"


