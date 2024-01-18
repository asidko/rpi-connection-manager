#!/bin/bash

# Disable the systemd service
if [ -f "/etc/systemd/system/hotspot.service" ]; then
    sudo systemctl disable hotspot.service
    sudo rm /etc/systemd/system/hotspot.service
    sudo systemctl daemon-reload
fi

# Remove the Python virtual environment
if [ -d "venv" ]; then
    rm -rf venv
fi