#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/server/"
sudo ./update.sh
sudo systemctl stop load-balancer-report.service
sudo systemctl stop flask-server.service
sudo systemctl daemon-reload
sudo systemctl start flask-server.service
sudo systemctl start load-balancer-report.service