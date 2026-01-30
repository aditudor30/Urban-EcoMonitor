# Urban EcoMonitor  
**IoT-Based Smart Building Management System**

## Overview

**Urban EcoMonitor** is a software-defined Smart Building Management System designed to monitor, analyze, and simulate active control of indoor office environments. The platform focuses on optimizing energy consumption and improving indoor air quality by correlating **occupancy**, **environmental conditions**, and **power usage**.

Instead of relying on physical IoT hardware, Urban EcoMonitor uses a **Python-based virtual sensor gateway** that replays real-world environmental data. This approach allows validation of the full IoT software architecture—data ingestion, storage, analytics, and visualization—without deploying physical sensors.

Commercial buildings are estimated to waste up to **30% of energy** due to inefficient lighting, ventilation, and HVAC usage in unoccupied or naturally lit spaces. Urban EcoMonitor addresses this issue through simulated automation strategies such as daylight harvesting and demand-driven ventilation.

---

## System Architecture

Urban EcoMonitor follows a containerized, microservice-oriented architecture.

```
Simulator (Python)
        |
        v
Flask REST API
        |
        v
TimescaleDB (PostgreSQL)
        |
        v
Vue.js Dashboard
```

### Data Flow

1. **Simulator (Edge Layer)**  
   A Python script replays time-series data from a real indoor environment dataset and sends measurements to the backend.

2. **Backend (Control & API Layer)**  
   A Flask-based REST API ingests sensor data, applies control logic, and exposes aggregated metrics.

3. **Database (Persistence Layer)**  
   TimescaleDB stores high-frequency time-series data such as CO₂ levels, lighting intensity, occupancy, and power consumption.

4. **Frontend (Visualization Layer)**  
   A Vue.js dashboard provides real-time monitoring, historical analysis, and simulated automation feedback.

---

## Key Features

### Daylight Harvesting Control

Artificial lighting intensity is dynamically adjusted based on ambient natural light levels.

- Inverse relationship between natural light (Lux) and artificial lighting output  
- Reduction of unnecessary electrical lighting during daylight hours  
- Simulation of smart dimming strategies used in modern green buildings  

### Active Ventilation Control

Ventilation behavior is driven by indoor air quality metrics.

- CO₂ concentration increases proportionally with occupancy  
- Fan speed increases when CO₂ thresholds are exceeded  
- Simulation of demand-controlled ventilation strategies  

### Real-Time Financial Analytics

Energy consumption is translated into actionable financial insights.

- Conversion of power usage (Watts) into estimated cost (USD / RON)  
- Calculation of an efficiency-based **Eco-Score**  
- Correlation between energy usage and occupancy efficiency  

---

## Dataset Methodology

Urban EcoMonitor does **not** rely on synthetic or random data generation.

The system uses the **Intelligent Indoor Environment Dataset**, sourced from Kaggle. This dataset contains real measurements collected from monitored indoor spaces.

### Processed Dataset Columns

- `room_CO2`  
- `lighting_intensity` (Lux)  
- `power_consumption`  
- `occupancy`  
- `air_quality_control`  

### Playback Strategy

The dataset is replayed sequentially by the simulator, emulating a live sensor gateway. This allows:

- Validation of ingestion pipelines  
- Testing of control logic  
- End-to-end evaluation of the platform without physical IoT devices  

---

## Tech Stack

### Infrastructure
- Docker  
- Docker Compose  

### Backend
- Python 3.9+  
- Flask (REST API)  

### Database
- TimescaleDB (PostgreSQL time-series extension)  

### Frontend
- Vue.js 3  
- Tailwind CSS (Dark Mode, Glassmorphism UI)  

### Edge / Simulation
- Python-based virtual sensor gateway  

---

## Prerequisites

- Docker Desktop  
- Python 3.9 or newer  
- Git  

---

## Installation and Usage

### Clone the Repository

```
git clone https://github.com/aditudor30/Urban-EcoMonitor.git
cd Urban-EcoMonitor
```

### Step 1: Start Infrastructure Containers

```
docker-compose up -d
```

### Step 2: Initialize the Database

```
python setup_db.py
```

### Step 3: Start the Backend API

```
python app.py
```

### Step 4: Start the Simulator

```
python simulator.py
```

### Step 5: Launch the Frontend

Open the `index.html` file in a web browser.

---

## API Endpoints

| Endpoint        | Method | Description                               |
|-----------------|--------|-------------------------------------------|
| `/api/ingest`   | POST   | Ingest sensor data from the simulator     |
| `/api/status`   | GET    | Retrieve current system state and metrics |
| `/api/history` | GET    | Query historical time-series data         |

---

## Use Cases

- Smart office energy optimization  
- Indoor air quality monitoring  
- IoT system prototyping without hardware  
- Academic research and teaching in smart buildings and IoT  

---

## License

MIT License

---

## Author

Developed as an academic and engineering project focused on smart buildings, IoT software architectures, and energy efficiency.
