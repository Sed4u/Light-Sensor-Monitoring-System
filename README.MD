# Light Sensor Monitoring System

This project is a **full-stack application** for monitoring, analyzing, and visualizing ambient light (lux) data in real time. It allows users to register, log in, view live and historical lux data, set custom warning thresholds, and receive alerts when light levels are outside the desired range.

## Features

- **User authentication** (register/login)
- **Real-time lux data visualization** (via Grafana dashboards)
- **Custom warning thresholds** for lux levels (per user)
- **Live alerts** when lux is too high or too low
- **Average lux calculation** over a selected interval
- **Simulated sensor data** (for demo/testing)
- **Modern, responsive web interface**

## Technologies Used

- **Python 3.9** (Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS)
- **PostgreSQL** (user data, thresholds)
- **InfluxDB 2.x** (time-series lux data)
- **Grafana** (data visualization)
- **Mosquitto** (MQTT broker)
- **paho-mqtt** (sensor data simulation)
- **Docker & Docker Compose** (multi-container orchestration)
- **HTML/CSS/JavaScript** (frontend)

## Architecture Overview

- **Flask backend**: Handles user management, threshold logic, API endpoints.
- **PostgreSQL**: Stores user accounts and threshold settings.
- **InfluxDB**: Stores time-series lux readings.
- **Grafana**: Visualizes lux data and warnings.
- **Mosquitto**: MQTT broker for sensor data ingestion.
- **Light simulator**: Python script that simulates sensor data and publishes it to MQTT.

## How to Run the Application

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/) installed on your system.

### Steps

1. **Clone the repository**
    ```sh
    git clone <your-repo-url>
    cd light-sensor-project
    ```

2. **Start all services with Docker Compose**
    ```sh
    docker-compose up --build
    ```
    This will build and start all containers: Flask backend, PostgreSQL, InfluxDB, Grafana, Mosquitto, and the data simulator.

3. **Access the application**
    - **Web interface:**  
      Open [http://localhost:5000](http://localhost:5000) in your browser.
    - **Grafana dashboards:**  
      Open [http://localhost:3000](http://localhost:3000)  
      (Default login: `admin` / `grafana123`)

4. **Register a new user**  
   Use the web interface to register and log in.

5. **Explore features**
    - View live lux data and graphs.
    - Set warning thresholds.
    - See live alerts and calculate average lux.

### Notes

- All configuration (database, tokens, ports) is handled via environment variables and Docker Compose.
- The application is fully containerized; **no local Python or database setup is required**. If you want to see the user data itself, you can use pgAdmin 4 and connect to the database hosted with docker.
- The light simulator will generate fake lux data for all users in the database.

## Stopping the Application

To stop all containers, press `Ctrl+C` in the terminal where Docker Compose is running, then:
```sh
docker-compose down
```

## Troubleshooting

- Make sure ports `5000`, `3000`, `8086`, and `1883` are free on your machine.
- If you encounter issues, try rebuilding with `docker-compose up --build`.

---
