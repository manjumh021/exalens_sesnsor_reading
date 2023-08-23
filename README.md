# Sensor Monitoring System

This project simulates the behavior of sensors, monitors their readings, and provides APIs to retrieve data based on specific criteria.

## Setup Instructions

1. Clone this repository:
    ```bash
    git clone https://github.com/manjumh021/sensor_reading.git
    cd sensor_reading
    ```
2. Install Docker and Docker Compose if not already installed.
3. Run the system using Docker Compose:
    ```bash
    docker-compose up
    ```
4. Access the FastAPI endpoints:
- Sensor Readings API: [http://localhost:8000/sensor_readings?topic=<topic_name>&start=<start_time>&end=<end_time>]([http://localhost:8000/sensor_readings](http://localhost:8000/sensor_readings?topic=sensors_temperature&start=<start_time>&end=<end_time>))
--> example: http://localhost:8000/sensor_readings?topic=sensors_temperature&start=2022-08-23&end=2024-08-23T04:20:10Z
- Last Ten Readings API: [http://localhost:8000/last_ten_readings?topic=<topic_name>&sensor_id=<sensor_id>](http://localhost:8000/last_ten_readings?topic=<topic_name>&sensor_id=<sensor_id>)
--> example: http://localhost:8000/last_ten_readings?topic=sensors_humidity&sensor_id=12345
- topics are <b>sensors_humidity</b> and <b>sensors_temperature</b>.
5. Stop the system:
    ```bash
    docker-compose down
    ```

# Services Overview

## MQTT Broker (Mosquitto)

The MQTT broker is responsible for facilitating communication between various components of the system using the MQTT protocol. It enables the publisher to send sensor readings to specific topics and allows subscribers to receive and process these readings. The broker ensures efficient and reliable message delivery.

## MQTT Publisher

The MQTT publisher simulates the behavior of sensors by generating random sensor readings for both temperature and humidity. It then publishes these readings to their respective topics, 'sensors/temperature' and 'sensors/humidity'. The publisher establishes a connection to the MQTT broker and uses the Paho MQTT library to interact with the broker.

## MQTT Subscriber

The MQTT subscriber listens to the 'sensors/temperature' and 'sensors/humidity' topics, where sensor readings are published. Upon receiving a new reading, the subscriber extracts the data, stores it in a MongoDB collection for persistent storage, and updates the Redis cache to maintain the latest ten readings. This component also establishes a connection to the MQTT broker and utilizes the Paho MQTT library.

## FastAPI Application

The FastAPI application serves as the interface for interacting with the system. It provides two endpoints:
- 'GET /sensor_readings': Retrieves sensor readings within a specified date range from the MongoDB database.
- 'GET /last_ten_readings': Fetches the last ten readings for a specific sensor from the Redis cache. This endpoint offers quick access to the most recent data without querying the database.

## MongoDB

MongoDB is used as the persistent storage solution for sensor readings. The subscriber stores incoming readings in a MongoDB collection named 'sensor_readings'. MongoDB's flexible document-based model allows efficient storage and retrieval of data.

## Redis

Redis serves as an in-memory cache for maintaining the latest sensor readings. The subscriber utilizes Redis lists to store the readings, with the 'ltrim' operation ensuring that only the last ten readings are retained. This caching mechanism provides fast access to recent data without needing frequent database queries.

# Design Choices and Rationale

The following design choices were made to ensure the system's efficiency and reliability:

- MQTT was chosen as the communication protocol due to its lightweight nature and support for the publish-subscribe model, ideal for sensor data distribution.
- MongoDB was selected as the database for sensor readings due to its scalability, flexibility, and document-oriented architecture, which suits the nature of sensor data.
- Redis was incorporated as an in-memory cache to maintain the latest sensor readings, reducing the need for repeated database queries.

The use of Docker and Docker Compose streamlines deployment by encapsulating each component in a container, ensuring consistent environments across development and deployment stages.

# Challenges and Solutions

During the development of the project, a few challenges were encountered:

1. **Data Processing Efficiency**: Efficiently processing and storing incoming sensor readings in real-time required optimizing database operations. Solution: Leveraging Redis as a cache for quick access to the latest readings while storing historical data in MongoDB.

2. **Container Networking**: Ensuring seamless communication between containers (such as between MQTT broker, MongoDB, and Redis) within the Docker network was a challenge. Solution: Defining appropriate container names and utilizing Docker Compose's networking capabilities.

3. **Data Format Consistency**: Ensuring consistent data formats between publishers, subscribers, and APIs was crucial for data integrity. Solution: Implementing JSON payloads and defining data schemas to maintain consistency across components.

These challenges were addressed through careful architecture design, appropriate technology selection, and iterative testing and refinement.

