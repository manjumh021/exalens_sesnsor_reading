import paho.mqtt.client as mqtt
import json
import time
import random

client = mqtt.Client()
client.connect("mqtt-broker-container", 1883, 60)  # Use the container name of the MQTT broker

while True:
    sensor_id = "unique_sensor_id"
    value = random.uniform(0, 100)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    payload = {
        "sensor_id": sensor_id,
        "value": value,
        "timestamp": timestamp
    }
    client.publish("sensors/temperature", json.dumps(payload))
    time.sleep(5)
