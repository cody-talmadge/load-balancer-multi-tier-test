#!/bin/bash

cd "/home/cody_talmadge/load-balancer-multi-tier-test/server/gce"

# Install required python dependencies
sudo apt-get install -y pip
sudo -H pip install flask requests gunicorn redis psutil --break-system-packages

# Allow the service to update the git repo
sudo git config --global --add safe.directory /home/cody_talmadge/load-balancer-multi-tier-test/

# Install flask-server and load-balancer-report services
sudo cp flask-server.service /etc/systemd/system/flask-server.service
sudo cp load-balancer-report.service /etc/systemd/system/load-balancer-report.service

# Install Redis service
sudo apt-get install -y redis
sudo cp redis.service /etc/systemd/system/redis.service

# Start services
sudo systemctl daemon-reload
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl enable flask-server.service
sudo systemctl start flask-server.service
sudo systemctl enable load-balancer-report.service
sudo systemctl start load-balancer-report.service