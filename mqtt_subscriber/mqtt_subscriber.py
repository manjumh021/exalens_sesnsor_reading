import paho.mqtt.client as mqtt
import json
import pymongo
import redis

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe("sensors/temperature")
    client.subscribe("sensors/humidity")  # Subscribe to the humidity topic as well

def update_redis(payload, topic):
    sensor_id = payload["sensor_id"]
    redis_key = f"{topic}:{sensor_id}"  # Create a Redis key using the topic and sensor_id
    redis_client.lpush(redis_key, json.dumps(payload, default=str))
    redis_client.ltrim(redis_key, 0, 9)

def store_in_mongodb(payload, topic):
    client = pymongo.MongoClient("mongodb://mongodb-container:27017/")  # Use the container name of MongoDB
    db = client["sensor_db"]
    # Use the topic as the collection name
    collection = db[topic]  
    collection.insert_one(payload)

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    topic = msg.topic  # Get the topic from the MQTT message
    topic = topic.replace("/", "_")
    store_in_mongodb(payload, topic)
    update_redis(payload, topic)

client.on_connect = on_connect
client.on_message = on_message

# Initialize Redis client
redis_client = redis.Redis(host='redis-container', port=6379, db=0)

client.connect("mqtt-broker-container", 1883, 60)  # Use the IP address of the MQTT broker
client.loop_forever()
