import redis
import requests
import time
import json
import socket

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'

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

def report_status():
    while True:
        # Recent CPU values from Redis
        recent_cpu_values = [float(value) for value in redis_client.lrange(CPU_USAGE_KEY, 0, 49)]
        average_cpu_usage = sum(recent_cpu_values) / len(recent_cpu_values) if recent_cpu_values else 0

        # Recent request durations from Redis
        recent_request_durations = [float(value) for value in redis_client.lrange(REQUEST_DURATION_KEY, 0, 49)]
        average_request_duration = sum(recent_request_durations) / len(recent_request_durations) if recent_request_durations else 0

        status_data = {
            "server_ip": server_ip,
            "average_cpu_usage": average_cpu_usage,
            "average_request_duration": average_request_duration,
            "current_time": time.time()
        }

        try:
            requests.post("http://" + LOAD_BALANCER_INTERNAL_IP + "/server_status", json=status_data)
            print("Sent status: " + str(status_data))
        except requests.exceptions.RequestException as e:
            print(f"Error reporting status: {e}")

        # Wait for 5 seconds between reports
        time.sleep(5)

if __name__ == '__main__':
    report_status()