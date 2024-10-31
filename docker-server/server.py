# Importing necessary modules
import socket
from flask import Flask, request
import psutil
import redis
import time
import os

# Configure Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Define Redis keys
CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'
TOTAL_REQUESTS_KEY = 'total_requests'

server_name = os.environ["HOSTNAME"]

app = Flask(__name__)

@app.route('/')
def cpu_monitor():
    # Track the start time of the request
    start_time = time.time()

    # Simulate CPU load
    for _ in range(10000000):
        pass
    
    current_cpu_percent = psutil.cpu_percent()
    
    # Store CPU usage in Redis (keep only the last 50 values)
    redis_client.lpush(CPU_USAGE_KEY, current_cpu_percent)
    redis_client.ltrim(CPU_USAGE_KEY, 0, 49)
    
    # Update total requests count in Redis
    redis_client.incr(TOTAL_REQUESTS_KEY)
    total_requests = int(redis_client.get(TOTAL_REQUESTS_KEY))
    
    # Calculate the time taken for the request
    request_duration = time.time() - start_time
    
    # Store request duration in Redis (keep only the last 50 values)
    redis_client.lpush(REQUEST_DURATION_KEY, request_duration)
    redis_client.ltrim(REQUEST_DURATION_KEY, 0, 49)
    
    return (f"Server name: {server_name}. Total requests handled: {total_requests}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
