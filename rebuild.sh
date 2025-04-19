#!/bin/bash

# Xóa tất cả các container, images và volumes
echo "Xóa tất cả các container, images và volumes..."
sudo docker-compose down -v
# sudo docker system prune -f

# Xóa tất cả các volumes
echo "Xóa tất cả các volumes..."
# sudo docker volume rm $(sudo docker volume ls -q)

# Xóa tất cả các images
echo "Xóa tất cả các images..."
# sudo docker rmi $(sudo docker images -q)

# Xóa tất cả các networks
echo "Xóa tất cả các networks..."
# sudo docker network rm $(sudo docker network ls -q)

# Build lại các service
echo "Build lại các service..."
# sudo docker-compose build

# Khởi động lại các service
echo "Khởi động lại các service..."
sudo docker-compose up -d --build

