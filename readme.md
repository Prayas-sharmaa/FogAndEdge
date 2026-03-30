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

## 🚀 Features
- **Intelligent Analytics:** Detects sensor anomalies locally to reduce cloud noise.
- **Asynchronous Architecture:** Uses SQS to decouple the edge from the database, preventing data loss.
- **Automated CI/CD:** Fully automated deployment to AWS using **GitHub Actions** and Native SSH.
- **Professional Dashboard:** Live monitoring with time-series graphs and severity gauges.

---

## 🛠️ Installation & Setup

### 1. Local Node Setup (Edge)
First, clone the repository and install the Python environment:
```bash
git clone [https://github.com/Prayas-sharmaa/FogAndEdge.git](https://github.com/Prayas-sharmaa/FogAndEdge.git)
cd FogAndEdge
pip install -r requirements.txt