import random
from base_sensor import BaseSensor

class OxygenSensor(BaseSensor):
    def __init__(self, sensor_id, pond_id, topic, frequency_sec=4.0, base_do=8.5):
        # Pass the core variables up to the BaseSensor
        super().__init__(sensor_id, pond_id, topic, frequency_sec)
        
        # Set the local variables
        self.current_do = base_do 
        self.noise_std_dev = 0.1

    def generate_value(self):
        is_anomaly = False
        # 2% chance of a sudden aerator failure (oxygen drops)
        if random.random() < 0.02:
            self.current_do -= random.uniform(2.0, 4.0) # Sudden drop
            is_anomaly = True
        else:
            self.current_do += random.gauss(0, self.noise_std_dev)
            self.current_do += (8.5 - self.current_do) * 0.05 # Revert to mean
            
        return round(self.current_do, 2), is_anomaly