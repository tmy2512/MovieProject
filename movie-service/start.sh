#!/bin/bash

until pg_isready -h movie-db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

python manage.py makemigrations movies
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")" | python manage.py shell

# Set PGPASSWORD environment variable
export PGPASSWORD=postgres
psql -h movie-db -U postgres -d movie_db -f /app/init_data.sql

python manage.py runserver 0.0.0.0:8000 