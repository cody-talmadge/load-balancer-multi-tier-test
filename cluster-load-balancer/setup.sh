#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/cluster-load-balancer"

# Install required python dependencies
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo -H pip install flask requests gunicorn redis

# Allow the service to update the git repo
sudo git config --global --add safe.directory /home/ec2-user/load-balancer-multi-tier-test

# Install load-balancer.service for gunicorn
sudo cp load-balancer.service /etc/systemd/system/load-balancer.service

# Install Redis service
sudo dnf update
sudo dnf install -y redis6
sudo cp redis.service /etc/systemd/system/redis.service

# Start services
sudo systemctl daemon-reload
sudo systemctl enable redis
sudo systemctl start redis
sudo systemctl enable load-balancer.service
sudo systemctl start load-balancer.service