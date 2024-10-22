#!/bin/bash

git reset --hard
git pull
sudo systemctl restart load-balancer.service