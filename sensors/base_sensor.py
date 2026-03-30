import json
import time
import asyncio
import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod

class BaseSensor(ABC):
    def __init__(self, sensor_id, pond_id, topic, frequency_sec, broker="localhost", port=1883):
        self.sensor_id = sensor_id
        self.pond_id = pond_id
        self.topic = topic
        self.frequency = frequency_sec
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=f"{sensor_id}_client")
        
        # Connect to the MQTT Broker (We will use a local one like Eclipse Mosquitto for testing)
        try:
            self.client.connect(broker, port)
            self.client.loop_start()
            print(f"[{self.sensor_id}] Connected to MQTT broker at {broker}:{port}")
        except Exception as e:
            print(f"[{self.sensor_id}] Failed to connect: {e}")

    @abstractmethod
    def generate_value(self):
        """Override this method to generate specific sensor data."""
        pass

    async def run(self):
        """Asynchronous loop to generate and publish data."""
        while True:
            value, is_anomaly = self.generate_value()
            
            payload = {
                "sensor_id": self.sensor_id,
                "pond_id": self.pond_id,
                "timestamp": time.time(),
                "value": round(value, 2),
                "is_anomaly_injected": is_anomaly # Flagged for our testing purposes
            }
            
            # Publish to the MQTT topic
            self.client.publish(self.topic, json.dumps(payload))
            print(f"[{self.sensor_id}] Published: {payload['value']} to {self.topic}")
            
            # Wait asynchronously before the next reading
            await asyncio.sleep(self.frequency)