import json
import statistics
import paho.mqtt.client as mqtt
from collections import deque, defaultdict
import boto3

# --- Configuration ---
BROKER = "localhost"
PORT = 1883
TOPIC_SUBSCRIBE = "farm/#"  
WINDOW_SIZE = 30                 
Z_SCORE_THRESHOLD = 3.0          
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/447294930914/AquaAlerts"
REGION = "us-east-1"

class FogNode:
    def __init__(self):
        # Dictionary to hold a sliding window (deque) for each sensor
        self.sensor_history = defaultdict(lambda: deque(maxlen=WINDOW_SIZE))
        
        # Setup MQTT Client
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="fog_processor_node")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print(f"[FOG] Connected to Edge Broker with result code {rc}")
        # Subscribe to all pond sensors using wildcard
        self.client.subscribe(TOPIC_SUBSCRIBE)
        print(f"[FOG] Subscribed to {TOPIC_SUBSCRIBE}")

    def on_message(self, client, userdata, msg):
        """Callback triggered every time a sensor publishes data."""
        try:
            payload = json.loads(msg.payload.decode())
            sensor_id = payload["sensor_id"]
            current_value = payload["value"]
            
            # Process the data locally
            self.process_reading(sensor_id, payload, current_value)
            
        except Exception as e:
            print(f"[FOG] Error processing message: {e}")

    def process_reading(self, sensor_id, payload, current_value):
        history = self.sensor_history[sensor_id]
        
        # If we have enough data to calculate meaningful statistics
        if len(history) > 10:
            mean_val = statistics.mean(history)
            std_dev = statistics.stdev(history)
            
            # Prevent division by zero if all readings are identical
            if std_dev > 0:
                z_score = abs(current_value - mean_val) / std_dev
                
                if z_score > Z_SCORE_THRESHOLD:
                    self.trigger_alert(sensor_id, current_value, z_score, payload)
                else:
                    # Normal reading. In a full system, we'd add this to a batching queue here.
                    pass 

        # Append the new reading to the sliding window
        history.append(current_value)

    def trigger_alert(self, sensor_id, value, z_score, raw_payload):
            """Dispatch a high-priority alert to the Cloud SQS Queue."""
            print("\n" + "!"*50)
            print(f"[FOG ALERT] ANOMALY DETECTED on {sensor_id}!")
            # Removed the hardcoded °C so it makes sense for pH and Oxygen too
            print(f"Value: {value:.2f} | Z-Score: {z_score:.2f}")
            print(f"Action: Pushing payload to AWS SQS...")
            
            # Prepare the cloud payload
            cloud_payload = {
                "pond_id": raw_payload["pond_id"],
                "sensor_id": sensor_id,
                "timestamp": raw_payload["timestamp"],
                "value": round(value, 2),
                "z_score": round(z_score, 2),
                "alert_type": "z_score_anomaly" # Changed to a generic anomaly label
            }

            # Send to AWS SQS
            try:
                sqs = boto3.client('sqs', region_name=REGION)
                response = sqs.send_message(
                    QueueUrl=QUEUE_URL,
                    MessageBody=json.dumps(cloud_payload)
                )
                print(f"[AWS SUCCESS] Message ID: {response['MessageId']}")
            except Exception as e:
                print(f"[AWS ERROR] Failed to send to cloud: {e}")
            print("!"*50 + "\n")

    def start(self):
        print("[FOG] Starting Edge Processing Node...")
        # loop_forever() handles reconnections and blocks the main thread
        self.client.connect(BROKER, PORT)
        self.client.loop_forever()

if __name__ == "__main__":
    node = FogNode()
    try:
        node.start()
    except KeyboardInterrupt:
        print("\n[FOG] Shutting down.")