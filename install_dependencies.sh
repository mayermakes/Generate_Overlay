#!/bin/bash

# Install Git
sudo apt-get update
sudo apt-get install -y git

# Install pip (if not already installed)
sudo apt-get install -y python3-pip

# Install Python packages
pip3 install ezdxf reportlab

echo "Dependencies installed successfully."

