from flask import Flask, request, Response, jsonify
import requests
import random
import time
import redis
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_internal_ip():
    try:
        # Create a socket connection to Google's DNS server We're not actually
        # sending any data, just using it to get the local IP of the server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 53))
        internal_ip = s.getsockname()[0]
        s.close()
        return internal_ip
    except Exception as e:
        return f"Error: {e}"
        exit(1)

server_ip = get_internal_ip()

overload_server = '172.31.1.1' if server_ip == '172.31.2.1' else '172.31.2.1'

# Endpoint for load balancing requests
@app.route('/')
def load_balance():

    # Choose the target server randomly - this logic will be changed to
    # the actual load balancer log
    server_status_keys = r.keys("server_status:*")
    server_ips = [key.split(":")[1] for key in server_status_keys]
    if len(server_ips) > 0:
        target_ip = pick_server(server_ips)
        target_url = "http://" + target_ip
    else:
        return Response("No connected servers", 503)

    if target_ip != overload_server:
        r.hincrby(f"server_counts:{target_ip}", 'active_requests')
        r.hincrby(f"server_counts:{target_ip}", 'req_curr_5')
    try:
        print("Target: " + target_url)
        resp = requests.get(target_url)
        if target_ip != overload_server:
            r.hincrby(f"server_counts:{target_ip}", 'active_requests', -1)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except:
        if target_ip != overload_server:
            r.hincrby(f"server_counts:{target_ip}", 'active_requests', -1)
        return Response("Server error", status=503)
    

# Endpoint for receiving server load status from servers
@app.route('/server_status', methods=['POST'])
def receive_server_status():
    data = request.get_json()
    try:
        server_name = data.get('server_ip')
        status_key = f"server_status:{server_name}"
        r.hset(status_key, 'cpu_usage', data.get('average_cpu_usage'))
        r.hset(status_key, 'last_updated', time.time())
        req_last_5 = r.hget(f"server_counts:{server_name}", 'req_curr_5')
        if req_last_5 is None:
            req_last_5 = 0
        r.hset(f"server_counts:{server_name}", 'req_curr_5' , 0)
        r.hset(f"server_counts:{server_name}", 'req_last_5', req_last_5)

        # Expire servers after 15 seconds of not seeing them (they should report
        # status every 5 seconds)
        r.expire(status_key, 15)
        return Response(status=200)
    except:
        return Response("Request error", status=400)

# Endpoint for reporting server load status for all connected servers
@app.route('/all_server_status', methods=['GET'])
def report_all_server_status():
    server_info = []
    server_status_keys = r.keys("server_status:*")
    for status_key in server_status_keys:
        server_ip = status_key.split(":")[1]
        status_data = r.hgetall(status_key)
        counts_data = r.hgetall(f"server_counts:{server_ip}")
        
        decoded_data = {**status_data, **counts_data}
        server_info.append({server_ip: decoded_data})
    return jsonify(server_info)

def pick_server(server_ips):
    if len(server_ips) == 1:
        return server_ips[0]
    
    server_1 = random.choice(server_ips)
    server_2 = None
    while server_2 is None or server_2 == server_1:
        server_2 = random.choice(server_ips)

    active_requests_1 = get_active_requests(server_1)
    active_requests_2 = get_active_requests(server_2)

    lower_server = server_1 if active_requests_1 < active_requests_2 else server_2
    lower_active_requests = min(active_requests_1, active_requests_2)
    cpu_usage = get_cpu_usage(lower_server)

    if lower_active_requests > 5 and cpu_usage > 90:
        return overload_server
    else:
        return lower_server


def get_active_requests(server_ip):
    active_requests = r.hget(f"server_counts:{server_ip}", 'active_requests')
    if active_requests is None:
        return 0
    else:
        return int(active_requests)

def get_cpu_usage(server_ip):
    cpu_usage = r.hget(f"server_status:{server_ip}", 'cpu_usage')
    if cpu_usage is None:
        return 0
    else:
        return float(cpu_usage)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)