#!/bin/bash

cd "/home/ec2-user/load-balancer-multi-tier-test/dns_mock/"
sudo ./update.sh
sudo systemctl stop dns_mock.service
sudo systemctl daemon-reload
sudo systemctl start dns_mock.service