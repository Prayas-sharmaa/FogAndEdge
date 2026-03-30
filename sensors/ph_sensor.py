import random
from base_sensor import BaseSensor

class PHSensor(BaseSensor):
    def __init__(self, sensor_id, pond_id, topic, frequency_sec=3.0, base_ph=7.2):
        # Pass the core variables up to the BaseSensor
        super().__init__(sensor_id, pond_id, topic, frequency_sec)
        
        # Set the local variables
        self.current_ph = base_ph 
        self.noise_std_dev = 0.05

    def generate_value(self):
        is_anomaly = False
        # 2% chance of an acidic chemical runoff
        if random.random() < 0.02:
            self.current_ph -= random.uniform(0.5, 1.5) # Sudden drop in pH
            is_anomaly = True
        else:
            self.current_ph += random.gauss(0, self.noise_std_dev)
            self.current_ph += (7.2 - self.current_ph) * 0.05
            
        return round(self.current_ph, 2), is_anomaly