#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/cluster-load-balancer/"
sudo ./update.sh
sudo systemctl stop load-balancer.service
sudo systemctl daemon-reload
sudo systemctl start load-balancer.service