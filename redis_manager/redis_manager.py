import redis
import json

redis_client = redis.Redis(host='redis-container', port=6379, db=0)  # Use the container name of Redis

def update_redis(payload):
    sensor_id = payload["sensor_id"]
    redis_client.lpush(sensor_id, json.dumps(payload))
    redis_client.ltrim(sensor_id, 0, 9)
