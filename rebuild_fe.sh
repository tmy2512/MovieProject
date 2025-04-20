#!/bin/bash

sudo docker-compose rm -f frontend
sudo docker system prune -f

# Build lại frontend
echo "Build lại frontend..."
sudo docker-compose up -d --build frontend
