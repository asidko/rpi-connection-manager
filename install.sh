#!/bin/bash

# Install venv in current directory if not installed
if [ ! -d "venv" ]; then
    python3 -m venv venv
    venv/bin/pip install -r requirements.txt
fi

# Make autostart for main.py and api.py
if [ ! -f "/etc/systemd/system/hotspot.service" ]; then
    sed "s|PROJECT_PATH|$(pwd)|g" hotspot.service | sudo tee /etc/systemd/system/hotspot.service > /dev/null
    sudo systemctl daemon-reload
    sudo systemctl enable hotspot.service
fi