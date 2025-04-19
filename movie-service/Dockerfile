FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . /app/

# Add wait script
RUN echo '#!/bin/bash\n\
until pg_isready -h movie-db -p 5432 -U postgres; do\n\
  echo "Waiting for database..."\n\
  sleep 2\n\
done\n\
python manage.py makemigrations movies\n\
python manage.py migrate\n\
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")" | python manage.py shell\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh && \
chmod +x /app/start.sh

# Run migrations and start server
CMD ["/app/start.sh"] 