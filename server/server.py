# Importing necessary modules
import socket
from flask import Flask, request
import psutil
import redis
import time

# Configure Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Define Redis keys
CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'
TOTAL_REQUESTS_KEY = 'total_requests'

LOAD_BALANCER_INTERNAL_IP = "172.31.19.117"

# Get the server's internal IP address
def get_internal_ip():
    try:
        # Create a socket connection to a public DNS server
        # (we're not actually sending any data, just using it to get the local IP)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((LOAD_BALANCER_INTERNAL_IP, 80))
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception as e:
        return f"Error: {e}"

server_ip = get_internal_ip()

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
    
    return (f"Server IP: {server_ip}. Total requests handled: {total_requests}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
