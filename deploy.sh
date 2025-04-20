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

# Hiển thị logs của booking-service
# echo "Hiển thị logs của booking-service..."
# sudo docker-compose logs -f booking-service

# # Hiển thị logs của payment-service
# echo "Hiển thị logs của payment-service..."
# sudo docker-compose logs -f payment-service

# # Hiển thị logs của report-service
# echo "Hiển thị logs của report-service..."
# sudo docker-compose logs -f report-service

# # Hiển thị logs của showtime-service
# echo "Hiển thị logs của showtime-service..."
# sudo docker-compose logs -f showtime-service

# # Hiển thị logs của user-service
# echo "Hiển thị logs của user-service..."
# sudo docker-compose logs -f user-service

