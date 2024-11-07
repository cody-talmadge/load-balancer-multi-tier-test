#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/cluster-load-balancer"

# Install required python dependencies
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo -H pip install flask requests gunicorn redis psutil

# Install flask-server and load-balancer-report services
sudo cp flask-server.service /etc/systemd/system/flask-server.service
sudo cp load-balancer-report.service /etc/systemd/system/load-balancer-report.service

# Install Redis service
sudo dnf update
sudo dnf install redis6
sudo cp redis.service /etc/systemd/system/redis.service

# Start services
sudo systemctl daemon-reload
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl enable flask-server.service
sudo systemctl start flask-server.service
sudo systemctl enable load-balancer-report.service
sudo systemctl start load-balancer-report.service