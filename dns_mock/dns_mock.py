from flask import Flask, Response
import requests
import random

app = Flask(__name__)
server_list = ['172.31.1.1', '172.31.2.1']

# Endpoint for load balancing requests
@app.route('/')
def load_balance():
    target_url = "http://" + random.choice(server_list)
    try:
        resp = requests.get(target_url)
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except:
        return Response("Request error", status=400) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)