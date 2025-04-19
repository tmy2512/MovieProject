# Hệ Thống Quản Lý Rạp Chiếu Phim

Hệ thống quản lý rạp chiếu phim được xây dựng theo kiến trúc microservice, bao gồm các service sau:

## Các Service

1. **Movie Service** (Port 8001)
   - Quản lý thông tin phim
   - API endpoints:
     - GET /api/movies/
     - POST /api/movies/
     - GET /api/movies/{id}/
     - PUT /api/movies/{id}/
     - DELETE /api/movies/{id}/

2. **Showtime Service** (Port 8002)
   - Quản lý suất chiếu
   - API endpoints:
     - GET /api/showtimes/
     - POST /api/showtimes/
     - GET /api/showtimes/{id}/
     - PUT /api/showtimes/{id}/
     - DELETE /api/showtimes/{id}/

3. **Booking Service** (Port 8003)
   - Quản lý đặt vé
   - API endpoints:
     - GET /api/bookings/
     - POST /api/bookings/
     - GET /api/bookings/{id}/
     - PUT /api/bookings/{id}/
     - DELETE /api/bookings/{id}/

4. **Payment Service** (Port 8004)
   - Quản lý thanh toán
   - API endpoints:
     - GET /api/payments/
     - POST /api/payments/
     - GET /api/payments/{id}/
     - PUT /api/payments/{id}/
     - DELETE /api/payments/{id}/

5. **User Service** (Port 8005)
   - Quản lý người dùng
   - API endpoints:
     - GET /api/users/
     - POST /api/users/
     - GET /api/users/{id}/
     - PUT /api/users/{id}/
     - DELETE /api/users/{id}/
     - POST /api/users/login/
     - POST /api/token/refresh/

6. **Report Service** (Port 8006)
   - Quản lý báo cáo
   - API endpoints:
     - GET /api/reports/
     - POST /api/reports/
     - GET /api/reports/{id}/
     - POST /api/reports/{id}/export/
     - GET /api/reports/{id}/download/
     - GET /api/reports/summary/

## Cài Đặt và Chạy

1. Cài đặt Docker và Docker Compose

2. Clone repository:
```bash
git clone <repository-url>
cd <project-directory>
```

3. Tạo file .env:
```bash
cp .env.example .env
```

4. Chỉnh sửa file .env với các giá trị phù hợp:
```
POSTGRES_DB=movie_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
SECRET_KEY=your-secret-key
```

5. Build và chạy các service:
```bash
docker-compose up --build
```

6. Truy cập các service:
- Movie Service: http://localhost:8001
- Showtime Service: http://localhost:8002
- Booking Service: http://localhost:8003
- Payment Service: http://localhost:8004
- User Service: http://localhost:8005
- Report Service: http://localhost:8006

## Cấu Trúc Project

```
.
├── movie-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── showtime-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── booking-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── payment-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── user-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── report-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── ...
├── docker-compose.yml
├── .env
└── README.md
```

## Công Nghệ Sử Dụng

- Python 3.9
- Django 4.2
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose

## Tác Giả

- [Tên tác giả]

## Giấy Phép

MIT 