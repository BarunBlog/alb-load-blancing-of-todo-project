#!/bin/bash

# Update package lists and install dependencies
sudo apt update -y

# Install Docker
sudo apt install -y docker.io

# Start Docker service
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Add ec2-user to the docker group
sudo usermod -aG docker $USER

# Restart Docker to apply group changes
sudo systemctl restart docker
