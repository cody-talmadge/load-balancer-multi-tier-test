#!/bin/bash

# Download get-pip.py if it doesn't already exist
if [ ! -f "get-pip.py" ]; then
    echo "Downloading get-pip.py..."
    curl -O https://bootstrap.pypa.io/get-pip.py
else
    echo "get-pip.py already exists. Skipping download."
fi

# Install pip if it doesn't exist
if ! command -v pip &> /dev/null; then
    echo "pip not found. Installing pip..."
    sudo python3 get-pip.py
else
    echo "pip is already installed. Skipping pip installation."
fi

# Install required Python dependencies if they are not already installed
REQUIRED_MODULES=("flask" "requests" "gunicorn" "redis" "psutil" "flask_cors")
for MODULE in "${REQUIRED_MODULES[@]}"; do
    if ! python3 -c "import ${MODULE}" &> /dev/null; then
        echo "${MODULE} not found. Installing ${MODULE}..."
        sudo -H pip install ${MODULE}
    else
        echo "${MODULE} is already installed. Skipping installation."
    fi
done

# Verify installations
echo "Verifying installations..."
python3 -c "import flask, requests, gunicorn, random, time, psutil" && echo "All dependencies are successfully installed."

# Create services
sudo cp flask-server.service /etc/systemd/system/flask-server.service
sudo cp load-balancer-report.service /etc/systemd/system/load-balancer-report.service
sudo cp redis.service /etc/systemd/system/redis.service


# Install Redis service
sudo dnf update
sudo dnf install --assumeyes redis6
sudo systemctl enable redis
sudo systemctl start redis

# Reload systemd, enable and start load-balancer service
sudo systemctl daemon-reload
sudo systemctl enable flask-server.service
sudo systemctl start flask-server.service
sudo systemctl enable load-balancer-report.service
sudo systemctl start load-balancer-report.service