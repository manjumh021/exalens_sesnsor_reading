import paho.mqtt.client as mqtt
import json
import pymongo
import redis

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/temperature")
    client.subscribe("sensors/humidity")  # Subscribe to the humidity topic as well

def update_redis(payload):
    sensor_id = payload["sensor_id"]
    redis_client.lpush(sensor_id, json.dumps(payload))
    redis_client.ltrim(sensor_id, 0, 9)

def store_in_mongodb(payload):
    client = pymongo.MongoClient("mongodb://mongo-container:27017/")  # Use the container name of MongoDB
    db = client["sensor_db"]
    collection = db["sensor_readings"]
    collection.insert_one(payload)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    store_in_mongodb(payload)
    update_redis(payload)

client.on_connect = on_connect
client.on_message = on_message

# Initialize Redis client
redis_client = redis.Redis(host='redis-container', port=6379, db=0)

client.connect("mqtt-broker-container", 1883, 60)  # Use the container name of the MQTT broker
client.loop_forever()
