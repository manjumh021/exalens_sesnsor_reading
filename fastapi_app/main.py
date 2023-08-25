from fastapi import FastAPI, HTTPException
import pymongo
import redis
import json
from datetime import datetime, timezone

app = FastAPI()

@app.get("/sensor_readings")
def get_sensor_readings(sensor_id: str, topic: str, start: str, end: str):
    if topic == "sensors_temperature" or topic == "sensors_humidity":
        client = pymongo.MongoClient("mongodb://mongodb-container:27017/")
        db = client["sensor_db"]
        collection = db[topic]
        
        start_time = convert_to_custom_format(start)
        end_time = convert_to_custom_format(end)
        
        readings = collection.find({
            "sensor_id": sensor_id,
            "timestamp": {
                "$gte": start_time,
                "$lte": end_time
            }
        })
        
        # Convert ObjectId to string for JSON serialization
        readings_list = []
        for reading in readings:
            reading_dict = dict(reading)
            reading_dict["_id"] = str(reading["_id"])
            readings_list.append(reading_dict)
        
        return readings_list
    else:
        raise HTTPException(status_code=400, detail="Invalid topic chosen.")


@app.get("/last_ten_readings")
def get_last_ten_readings(topic: str, sensor_id: str):
    if topic == "sensors_temperature" or topic == "sensors_humidity":
        redis_key = f"{topic}:{sensor_id}"  # Create the Redis key for the topic and sensor ID
        redis_client = redis.Redis(host='redis-container', port=6379, db=0)
        readings = redis_client.lrange(redis_key, 0, -1)
        return [json.loads(reading) for reading in readings]
    else:
        raise HTTPException(status_code=400, detail="Invalid topic for last_ten_readings")

def convert_to_custom_format(datetime_str):
    try:
        input_formats = [
            "%Y-%m-%d %H:%M:%S%z",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%SZ"
        ]
        
        dt = None
        for format_str in input_formats:
            try:
                dt = datetime.strptime(datetime_str, format_str)
                break
            except ValueError:
                pass
        
        if dt is None:
            raise ValueError("Invalid datetime format")
        
        formatted_dt = dt.replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return formatted_dt
    except ValueError as e:
        return str(e)