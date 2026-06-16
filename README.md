# AI-Driven Self-Healing Network Monitoring Framework

## Overview

The AI-Driven Self-Healing Network Monitoring Framework is a Django-based network management system designed to improve network reliability, availability, and operational efficiency through continuous monitoring, fault detection, congestion analysis, and automated recovery recommendations.

The system provides administrators with a centralized dashboard to monitor network health, identify anomalies, detect overloaded servers, analyze traffic patterns, and receive intelligent recovery suggestions. By incorporating self-healing networking principles, the framework minimizes downtime and reduces the need for manual intervention.

---

## Features

### Network Monitoring
- Real-time monitoring of network devices and connected clients.
- Tracks active connections and network activity.
- Displays network performance metrics.

### Client Monitoring
- Monitor connected clients with:
  - Username
  - IP Address
  - Connection Timestamp
  - Connection Status

### Fault Detection
- Detects:
  - Network congestion
  - Server overload
  - Communication failures
  - Node outages
  - Network instability

### Traffic Analysis
- Analyzes traffic patterns and bandwidth usage.
- Identifies abnormal network behavior.
- Supports proactive network management.

### Self-Healing Recommendations
- Provides intelligent recovery suggestions.
- Recommends load balancing actions.
- Helps administrators restore network performance quickly.

### Administrative Dashboard
- Centralized monitoring interface.
- Displays:
  - Active Clients
  - Active Connections
  - Network Events
  - Network Health Status
- Access to all management modules.

### User Management
- Django Admin integration.
- User authentication and authorization.
- User account management.
- Role-based access control.

---

## System Architecture

```text
Network Monitoring
        ↓
Data Collection & Processing
        ↓
Fault Detection
        ↓
AI-Based Prediction
        ↓
Self-Healing Recovery
```

### Workflow

1. Monitor network activities continuously.
2. Collect and preprocess network data.
3. Detect faults and abnormal conditions.
4. Predict potential failures using AI techniques.
5. Trigger recovery recommendations and corrective actions.

---

## Technology Stack

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Database
- SQLite

### Networking
- Socket Programming
- Network Traffic Monitoring
- Traffic Analysis

### AI Concepts
- Fault Detection
- Failure Prediction
- Congestion Analysis
- Self-Healing Mechanisms

---

## Modules

### 1. Admin Dashboard
Provides a complete overview of network status and system statistics.

### 2. Client Monitoring Module
Tracks all connected clients and their activities.

### 3. Network Status Summary
Displays:
- Congestion Status
- Active Connections
- Node Health

### 4. Network Issue Detection
Identifies:
- Server Overload
- Congestion Events
- Network Performance Degradation

### 5. User Management Module
Allows administrators to:
- Add Users
- Edit Users
- Delete Users
- Manage Permissions

---

## Project Structure

```text
self-healing-network/
│
├── manage.py
├── requirements.txt
│
├── network_monitor/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── utils.py
│
├── templates/
│   ├── dashboard.html
│   ├── clients.html
│   ├── network_status.html
│   └── alerts.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── logs/
│
└── README.md
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/self-healing-network.git
cd self-healing-network
```

### Create a Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

### Run the Server

```bash
python manage.py runserver
```

Open the application:

```text
http://127.0.0.1:8000/
```

Admin Panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Expected Outcomes

- Early fault detection.
- Improved network visibility.
- Faster issue resolution.
- Reduced network downtime.
- Enhanced service availability.
- Improved operational efficiency.
- Scalable network management.

---

## Future Enhancements

- Machine Learning-based fault prediction.
- Deep Learning anomaly detection.
- Automated traffic rerouting.
- Cloud deployment support.
- IoT network integration.
- Reinforcement Learning for autonomous recovery.
- Large Language Model (LLM) integration.
- Email and SMS alert notifications.

---

## Results

The implemented system successfully:

- Monitored active network clients.
- Detected network congestion.
- Identified overloaded servers.
- Generated recovery recommendations.
- Supported centralized network administration.
- Improved network management efficiency.

---

## Conclusion

The AI-Driven Self-Healing Network Monitoring Framework provides an intelligent solution for modern network management by combining real-time monitoring, fault detection, congestion analysis, and recovery recommendations. The framework enhances network reliability, reduces downtime, and supports proactive network administration, making it suitable for future intelligent networking environments.

---

## Authors

- Chandrashekar G
- Deepthi Reddy S
- Devika R
- Harshitha D
- Gouri Mahesh Tuppad

Department of Computer Science and Engineering  
Dayananda Sagar Academy of Technology and Management  
Bangalore, India

---

## License

This project is developed for academic and research purposes. Feel free to use, modify, and extend it for educational and non-commercial applications.
