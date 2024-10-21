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
REQUIRED_MODULES=("flask" "requests" "gunicorn" "redis")
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
python3 -c "import flask, requests, gunicorn, random, time" && echo "All dependencies are successfully installed."

# Create load-balancer.service for gunicorn
cat <<EOL | sudo tee /etc/systemd/system/load-balancer.service
[Unit]
Description=Gunicorn instance to serve the load balancer
After=network.target

[Service]
User=root
WorkingDirectory=/home/ec2-user/load-balancer-multi-tier-test/cluster-load-balancer
ExecStart=/usr/local/bin/gunicorn --workers 4 --threads 10 --bind 0.0.0.0:80 cluster-load-balancer:app
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Install Redis service
sudo dnf update
sudo dnf install redis6
sudo systemctl enable redis

# Reload systemd, enable and start load-balancer service
sudo systemctl daemon-reload
sudo systemctl enable load-balancer.service
sudo systemctl start load-balancer.service

