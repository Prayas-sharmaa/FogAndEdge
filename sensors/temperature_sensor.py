import random
from base_sensor import BaseSensor

class TemperatureSensor(BaseSensor):
    def __init__(self, sensor_id, pond_id, topic, frequency_sec, base_temp=20.0):
        super().__init__(sensor_id, pond_id, topic, frequency_sec)
        self.current_temp = base_temp
        self.noise_std_dev = 0.2  # Normal temperature fluctuation
        
    def generate_value(self):
            is_anomaly = False
            if random.random() < 0.02:
                self.current_temp += random.uniform(3.0, 5.0) 
                is_anomaly = True
            else:
                self.current_temp += random.gauss(0, self.noise_std_dev)
                # Make the reversion much stronger so it recovers instantly after a spike
                self.current_temp += (20.0 - self.current_temp) * 0.50 
                
            return round(self.current_temp, 2), is_anomaly