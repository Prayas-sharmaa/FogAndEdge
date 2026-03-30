import json
import time
import boto3
import sqlite3

# --- Configuration ---
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/447294930914/AquaAlerts"
REGION = "us-east-1"
DB_PATH = "/srv/iot_data/farm_data.db"

class CloudWorker:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name=REGION)
        self.init_db()
        print("[CLOUD] FaaS Worker Initialized.")
        print("[CLOUD] Long-polling AWS SQS for anomalies...\n")

    def init_db(self):
        """Creates a local database to feed Grafana."""
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pond_id TEXT,
                sensor_id TEXT,
                timestamp REAL,
                value REAL,
                z_score REAL,
                alert_type TEXT
            )
        ''')
        self.conn.commit()

    def poll_queue(self):
        while True:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=QUEUE_URL,
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=20  
                )

                messages = response.get('Messages', [])
                if messages:
                    print(f"[{time.strftime('%H:%M:%S')}] Pulled {len(messages)} alert(s) from AWS.")
                    for message in messages:
                        self.process_message(message)
                
            except Exception as e:
                print(f"[CLOUD ERROR] SQS Polling failed: {e}")
                time.sleep(5)

    def process_message(self, message):
        receipt_handle = message['ReceiptHandle']
        body = json.loads(message['Body'])

        # 1. Save the alert to the database
        self.cursor.execute('''
            INSERT INTO alerts (pond_id, sensor_id, timestamp, value, z_score, alert_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (body.get('pond_id'), body.get('sensor_id'), body.get('timestamp'), 
              body.get('value'), body.get('z_score'), body.get('alert_type')))
        self.conn.commit()
        
        print(f"☁️ [DB SAVED] Critical Alert on {body.get('sensor_id')} | Z-Score: {body.get('z_score')}")

        # 2. Delete the message from the queue
        self.sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)

if __name__ == "__main__":
    worker = CloudWorker()
    try:
        worker.poll_queue()
    except KeyboardInterrupt:
        print("\n[CLOUD] Worker shutting down.")
        worker.conn.close()