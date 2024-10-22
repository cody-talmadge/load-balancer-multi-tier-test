from flask import Flask, request, Response, jsonify
import requests
import random
import time
import redis

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)

# Endpoint for load balancing requests
@app.route('/')
def load_balance():

    # Choose the target server randomly
    server_ips = [ip.decode('utf-8') for ip in r.keys("*")]
    if len(server_ips) > 0:
        target_ip = "http://" + random.choice(server_ips)
    else:
        # If no servers are connected
        return Response("No connected servers", 503)
    
    # Forward the request to the chosen target server
    resp = requests.get(target_ip)
    return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))

# Endpoint for receiving server load status from servers
@app.route('/server_status', methods=['POST'])
def receive_server_status():
    data = request.get_json()
    try:
        server_ip = data.get('server_ip')
        r.hset(server_ip, mapping = {
            "average_cpu_usage": data.get("average_cpu_usage"),
            "average_request_duration": data.get("average_request_duration"),
            "last_updated": time.time()
        })
        r.expire(server_ip, 15)
        return Response(status=200)
    except:
        return Response("Invalid request", status=400)

# Endpoint for reporting server load status for all connected servers
@app.route('/all_server_status', methods=['GET'])
def report_all_server_status():
    server_info = []
    server_ips = [ip.decode('utf-8') for ip in r.keys("*")]
    for ip in server_ips:
        server_data = r.hgetall(ip)
        decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in server_data.items()}
        server_info.append({ip: decoded_data})
    return jsonify(server_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)