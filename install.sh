#!/bin/bash
# Installation script for Garage Door Controller

echo "Installing packages for Garage Door Controller..."
sudo apt-get update
sudo apt-get install -y python3-pip

echo "Installing required Python packages..."
pip3 install -r requirements.txt

echo "Setting up permissions..."
# Make sure the script can access GPIO
sudo usermod -a -G gpio $USER

echo "Installation complete!"
echo "Run the application with: python3 web.py"
echo "Then access your garage door securely at: https://YOUR_PI_IP:5000"
