# 🌊 Smart Aqua: IoT Edge-to-Cloud Monitoring
> **A Cloud-Native Fog Computing System for Real-Time Water Quality Analysis.**

This project implements a complete IoT pipeline—from local sensor simulation to cloud persistence—featuring real-time anomaly detection and automated DevOps.

---

## 🏗️ Technical Architecture
The system is divided into four distinct layers to ensure scalability and fault tolerance:

1.  **Physical Layer:** Simulated sensors (Temperature, pH, Dissolved Oxygen) using Mean Reversion logic.
2.  **Edge/Fog Layer:** Local processing via **Mosquitto MQTT** and **Z-Score Anomaly Detection**.
3.  **Cloud Layer:** Asynchronous data ingestion using **AWS SQS** and an **AWS EC2** worker.
4.  **Presentation Layer:** Real-time visualization via **Grafana**.

---

## PREREQUISITES

- Python 3.8+
- Mosquitto MQTT Broker (installed locally)
- AWS Account (SQS Queue and EC2 Instance)
- GitHub Account (for CI/CD pipeline)
---


## 🚀 Features
- **Intelligent Analytics:** Detects sensor anomalies locally to reduce cloud noise.
- **Asynchronous Architecture:** Uses SQS to decouple the edge from the database, preventing data loss.
- **Automated CI/CD:** Fully automated deployment to AWS using **GitHub Actions** and Native SSH.
- **Professional Dashboard:** Live monitoring with time-series graphs and severity gauges.

---

## 🛠️ Installation & Setup

### 1. Local Node Setup (Edge)

First, clone the repository and install the Python environment:
bash
git clone [https://github.com/Prayas-sharmaa/FogAndEdge.git](https://github.com/Prayas-sharmaa/FogAndEdge.git)
cd FogAndEdge


### 2. pip install -r requirements.txt

### 3. Start Mosquitto Broker:
   (Windows) Run services.msc -> Start 'Mosquitto Broker'
   (Linux) sudo systemctl start mosquitto

### 4. CLOUD SETUP (AWS)
1. Create an SQS Queue in the 'us-east-1' region.
2. Launch an Ubuntu EC2 instance.
3. Configure AWS Credentials on your local machine (~/.aws/credentials) 
   and on the EC2 instance to allow SQS access.

### 5. CI/CD CONFIGURATION
1. In your GitHub Repo, go to Settings > Secrets and Variables > Actions.
2. Add the following repository secrets:
   - EC2_HOST: (Your EC2 Public IP)
   - EC2_USER: ubuntu
   - EC2_SSH_KEY: (The content of your .pem private key)

### 6. RUNNING THE SYSTEM

1. Start the Cloud Worker (on EC2):
   The GitHub Action handles this automatically on push, or run:
   $ python3 lambda_worker.py

2. Start the Fog Node (Local):
   $ python3 fog_node.py

3. Start the Sensor Simulator (Local):
   $ python3 sensor_sim.py

### 7. MONITORING

- Logs: View 'worker.log' on the EC2 instance for ingestion status.
- Dashboard: Access your Grafana URL (Port 3000) to view real-time 
  analytics and anomaly gauges.