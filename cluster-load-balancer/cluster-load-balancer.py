from flask import Flask, request, Response, jsonify
import requests
import random
import time

app = Flask(__name__)

server_load_status = {}

# Endpoint for load balancing requests
@app.route('/')
def load_balance():
    delete_stale_servers()

    # Choose the target server randomly
    if server_load_status:
        target_ip = "http://" + random.choice(list(server_load_status.keys()))
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
        server_load_status[server_ip] = {
            "average_cpu_usage": data.get("average_cpu_usage"),
            "average_request_duration": data.get("average_request_duration"),
            "last_updated": time.time()
        }
        return Response(status=200)
    except:
        return Response("Invalid request", status=400)

# Endpoint for reporting server load status for all connected servers
@app.route('/all_server_status', methods=['GET'])
def report_all_server_status():
    return jsonify(server_load_status)

def delete_stale_servers():
    current_time = time.time()
    stale_servers = []
    for server_ip, server_data in server_load_status.items():
        # Remove the server from the list if it hasn't been updated in the last 15 seconds
        if server_data.last_updated + 15 < current_time:
            stale_servers.append(server_ip)
    
    for server_ip in stale_servers:
        del server_load_status[server_ip]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)