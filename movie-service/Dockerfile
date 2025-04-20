FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

# Copy project files
COPY . /app/

# Create and set up start script
RUN echo '#!/bin/bash\n\
until pg_isready -h movie-db -p 5432 -U postgres; do\n\
  echo "Waiting for database..."\n\
  sleep 2\ndone\n\
python manage.py makemigrations movies\n\
python manage.py migrate\n\
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")" | python manage.py shell\n\
psql -h movie-db -U postgres -d movie_db -f /app/init_data.sql\n\
python manage.py runserver 0.0.0.0:8000' > /app/start.sh

# Make start script executable
RUN chmod 755 /app/start.sh

# Run the start script
CMD ["/bin/bash", "/app/start.sh"]