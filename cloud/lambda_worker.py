import json
import time
import boto3

# --- Configuration ---
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/447294930914/AquaAlerts"
REGION = "us-east-1"

class CloudWorker:
    def __init__(self):
        self.sqs = boto3.client('sqs', region_name=REGION)
        print("[CLOUD] FaaS Worker Initialized.")
        print("[CLOUD] Long-polling AWS SQS for anomalies...\n")

    def poll_queue(self):
        while True:
            try:
                # Long polling (WaitTimeSeconds=20) to save API requests/costs
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

        print("-" * 40)
        print(f"☁️ CLOUD PROCESSING: CRITICAL ALERT ☁️")
        print(f"Pond ID:   {body.get('pond_id')}")
        print(f"Sensor:    {body.get('sensor_id')}")
        print(f"Z-Score:   {body.get('z_score')} (Severe Anomaly)")
        print("-" * 40)

        # Delete the message so it doesn't get processed twice
        self.sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        print(f"[CLOUD] Alert processed and deleted from queue.\n")

if __name__ == "__main__":
    worker = CloudWorker()
    try:
        worker.poll_queue()
    except KeyboardInterrupt:
        print("\n[CLOUD] Worker shutting down.")