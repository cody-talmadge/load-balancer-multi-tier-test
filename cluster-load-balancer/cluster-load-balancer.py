from flask import Flask, request, Response, jsonify
import requests
import random
import time
import redis
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Endpoint for load balancing requests
@app.route('/')
def load_balance():

    # Choose the target server randomly - this logic will be changed to
    # the actual load balancer log
    server_ips = [ip for ip in r.keys("*")]
    if len(server_ips) > 0:
        target_ip = pick_server(server_ips)
        target_url = "http://" + target_ip
    else:
        return Response("No connected servers", 503)
    print("Target: " + target_url)
    r.hincrby(target_ip, 'active_requests')
    r.hincrby(target_ip, 'req_curr_5')
    try:
        print("Target: " + target_url)
        resp = requests.get(target_url)
        r.hincrby(target_ip, 'active_requests', -1)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except:
        r.hincrby(target_ip, 'active_requests', -1)
        return Response("Server error", status=503)
    

# Endpoint for receiving server load status from servers
@app.route('/server_status', methods=['POST'])
def receive_server_status():
    data = request.get_json()
    try:
        server_name = data.get('server_ip')
        r.hset(server_name, 'cpu_usage', data.get('average_cpu_usage'))
        r.hset(server_name, 'last_updated', time.time())
        req_last_5 = r.hget(server_name, 'req_curr_5')
        if req_last_5 is None:
            req_last_5 = 0
        r.hset(server_name, 'req_curr_5' , 0)
        r.hset(server_name, 'req_last_5', req_last_5)

        # Expire servers after 15 seconds of not seeing them (they should report
        # status every 5 seconds)
        r.expire(server_name, 15)
        return Response(status=200)
    except:
        return Response("Request error", status=400)

# Endpoint for reporting server load status for all connected servers
@app.route('/all_server_status', methods=['GET'])
def report_all_server_status():
    server_info = []
    server_names = [name for name in r.keys("*")]
    for name in server_names:
        server_data = r.hgetall(name)
        decoded_data = {key: value for key, value in server_data.items()}
        server_info.append({name: decoded_data})
    return jsonify(server_info)

def pick_server(server_ips):
    if len(server_ips) == 1:
        return server_ips[0]
    d_choice_1 = random.choice(server_ips)
    d_choice_2 = None
    while d_choice_1 == d_choice_2 or d_choice_2 is None:
        d_choice_2 = random.choice(server_ips)

    d_choice_1_active_requests = r.hget(d_choice_1,'active_requests')
    if d_choice_1_active_requests is None:
        d_choice_1_active_requests = 0
    else:
        d_choice_1_active_requests = int(d_choice_1_active_requests)
    d_choice_2_active_requests = r.hget(d_choice_2,'active_requests')
    if d_choice_2_active_requests is None:
        d_choice_2_active_requests = 0
    else:
        d_choice_2_active_requests = int(d_choice_2_active_requests)
    if d_choice_1_active_requests > d_choice_2_active_requests:
        return d_choice_2
    else:
        return d_choice_1

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)