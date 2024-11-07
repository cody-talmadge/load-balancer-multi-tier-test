import redis
import requests
import time
import json
import socket
import psutil

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
        average_cpu_usage = psutil.cpu_percent()

        status_data = {
            "server_ip": server_ip,
            "average_cpu_usage": average_cpu_usage
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