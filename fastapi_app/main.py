from fastapi import FastAPI, HTTPException
import pymongo
import redis
import json
from datetime import datetime

app = FastAPI()

@app.get("/sensor_readings")
def get_sensor_readings(start: str, end: str):
    client = pymongo.MongoClient("mongodb://mongo-container:27017/")  # Use the container name of MongoDB
    db = client["sensor_db"]
    collection = db["sensor_readings"]
    
    start_time = parse_datetime(start)
    end_time = parse_datetime(end)
    
    readings = collection.find({
        "timestamp": {
            "$gte": start_time,
            "$lte": end_time
        }
    })
    
    return [reading for reading in readings]

@app.get("/last_ten_readings")
def get_last_ten_readings(sensor_id: str):
    redis_client = redis.Redis(host='redis-container', port=6379, db=0)  # Use the container name of Redis
    readings = redis_client.lrange(sensor_id, 0, -1)
    return [json.loads(reading) for reading in readings]

def parse_datetime(datetime_str):
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        raise ValueError("Invalid datetime format. Expected ISO8601 format: 'YYYY-MM-DDTHH:MM:SSZ'")
