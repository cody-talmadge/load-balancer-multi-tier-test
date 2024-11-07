import socket
from flask import Flask, request
import psutil
import redis
import time
import math
import random
import os

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'
TOTAL_REQUESTS_KEY = 'total_requests'

LOAD_BALANCER_INTERNAL_IP = "172.31.1.1"

def get_internal_ip():
    try:
        # Create a socket connection to the load balancer. We're not actually
        # sending any data, just using it to get the local IP of the server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((LOAD_BALANCER_INTERNAL_IP, 80))
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception as e:
        return f"Error: {e}"
        exit(1)

server_ip = get_internal_ip()

app = Flask(__name__)

@app.route('/')
def handle_request():
    start_time = time.time()

    # Simulate CPU load, will be replaced by a better function later
    # Used to determine how slow the average response will be (note: not linear)
    prime_limit_avg = 100000
    # Used to set the standard deviation for response time (note: not linear)
    std_dev = 0.5
    prime_limit = int(random.gauss(prime_limit_avg, prime_limit_avg * std_dev))
    prime_list = primes_up_to_n(prime_limit)
    
    # Update total requests count in Redis
    redis_client.incr(TOTAL_REQUESTS_KEY)
    total_requests = int(redis_client.get(TOTAL_REQUESTS_KEY))
    
    request_duration = time.time() - start_time
    
    return (f"Server IP: {server_ip}<br>Total requests handled: {total_requests}<br>Duration: {request_duration}<br>Prime limit: {prime_limit}<br>Prime list: {prime_list}")

# Used to simulate CPU load (and network load by generating data to return)
def primes_up_to_n(n):
    prime_list = []
    for num in range(2, n):
        prime = True
        for check_num in range(2, int(math.sqrt(num)) + 1):
            if num % check_num == 0:
                prime = False
                break
        if prime:
            prime_list.append(num)
    return prime_list

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
