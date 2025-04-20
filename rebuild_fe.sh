#!/bin/bash

sudo docker-compose rm -f frontend
# sudo docker system prune -f

# Build lại frontend
echo "Build lại frontend..."
sudo docker-compose up -d --build frontend

# Dừng các service backend
# echo "Dừng các service backend..."
# sudo docker-compose down -v movie-service 
# # Build lại backend
# echo "Build lại backend..."
# sudo docker-compose up -d --build movie-service
# # sudo docker-compose up -d --build booking-service
# sudo docker-compose up -d --build payment-service
# sudo docker-compose up -d --build report-service
# sudo docker-compose up -d --build showtime-service
# sudo docker-compose up -d --build user-service 