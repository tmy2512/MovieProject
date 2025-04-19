# Sử dụng Python 3.9 slim làm base image
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Cài đặt các dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code vào container
COPY . .

# Tạo thư mục exports để lưu file Excel
RUN mkdir -p /app/exports

# Expose port 8000
EXPOSE 8000

# Chạy ứng dụng
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"] 