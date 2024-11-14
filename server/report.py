import redis
import requests
import time
import json
import socket
import psutil
import os

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

CPU_USAGE_KEY = 'recent_cpu_load'
REQUEST_DURATION_KEY = 'recent_request_durations'

with open("/home/ec2-user/ip.info", "r") as file:
    LOAD_BALANCER_INTERNAL_IP = file.readline().strip()

def get_internal_ip():
    ip_success = False

    while ip_success == False:
        # Try to get the internal IP address of the server
        try:
            # Create a socket connection to Google's DNS server. We're not actually
            # sending any data, just using it to get the local IP of the server
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect("8.8.8.8")
            internal_ip = s.getsockname()[0]
            s.close()
            ip_success = True
            print("Server IP: ", internal_ip)
            return internal_ip
        except Exception as e:
            time.sleep(10)
            print("IP Error")

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