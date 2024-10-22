#!/bin/bash

git reset --hard
git pull
sudo systemctl restart load-balancer-report.service
sudo systemctl restart flask-server.service