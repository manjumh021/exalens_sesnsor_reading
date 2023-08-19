# Sensor Monitoring System

This project simulates the behavior of sensors, monitors their readings, and provides APIs to retrieve data based on specific criteria.

## Setup Instructions

1. Clone this repository:
    ```bash
    git clone https://github.com/manjumh021/exalens_sesnsor_reading.git
    cd exalens_sesnsor_reading
    ```
2. Install Docker and Docker Compose if not already installed.
3. Run the system using Docker Compose:
    ```bash
    docker-compose up
    ```
4. Access the FastAPI endpoints:
# API Endpoints
- Sensor Readings API: [http://localhost:8000/sensor_readings](http://localhost:8000/sensor_readings)
- Last Ten Readings API: [http://localhost:8000/last_ten_readings](http://localhost:8000/last_ten_readings)

Stop the system:
    ```bash
    docker-compose down
    ```
