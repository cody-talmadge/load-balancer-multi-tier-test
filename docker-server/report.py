# Importing necessary modules
import redis
import requests
import time
import json
import socket
import os

# Configure Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Define the keys for storing data
CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'

LOAD_BALANCER_INTERNAL_IP = "172.31.19.117"
server_name = os.environ["HOSTNAME"]

# Function to report server status
def report_status():
    while True:
        # Retrieve recent CPU values from Redis
        recent_cpu_values = [float(value) for value in redis_client.lrange(CPU_USAGE_KEY, 0, 49)]
        average_cpu_usage = sum(recent_cpu_values) / len(recent_cpu_values) if recent_cpu_values else 0

        # Retrieve recent request durations from Redis
        recent_request_durations = [float(value) for value in redis_client.lrange(REQUEST_DURATION_KEY, 0, 49)]
        average_request_duration = sum(recent_request_durations) / len(recent_request_durations) if recent_request_durations else 0

        # Prepare the status data
        status_data = {
            "server_name": server_name,
            "average_cpu_usage": average_cpu_usage,
            "average_request_duration": average_request_duration,
            "current_time": time.time()
        }

        # Send the status data to the specified endpoint
        try:
            requests.post("http://" + LOAD_BALANCER_INTERNAL_IP + "/server_status", json=status_data)
        except requests.exceptions.RequestException as e:
            print(f"Error reporting status: {e}")

        # Wait for 5 seconds before the next report
        time.sleep(5)

# Run the status reporting function
if __name__ == '__main__':
    report_status()
