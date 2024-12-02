#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/dns_mock"

# Install required python dependencies
curl -O https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo -H pip install flask requests gunicorn

# Allow the service to update the git repo
sudo git config --global --add safe.directory /home/ec2-user/load-balancer-multi-tier-test

# Install load-balancer.service for gunicorn
sudo cp dns_mock.service /etc/systemd/system/dns_mock.service

# Start services
sudo systemctl daemon-reload
sudo systemctl enable dns_mock.service
sudo systemctl start dns_mock.service