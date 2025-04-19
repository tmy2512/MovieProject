#!/bin/bash

# Dừng tất cả các container đang chạy
echo "Dừng tất cả các container..."
sudo docker-compose down

# Khởi động lại các service
echo "Khởi động lại các service..."
sudo docker-compose up -d

# Kiểm tra trạng thái các service
echo "Kiểm tra trạng thái các service..."
sudo docker-compose ps

# Hiển thị logs của movie-service
echo "Hiển thị logs của movie-service..."
# sudo docker-compose logs -f movie-service 