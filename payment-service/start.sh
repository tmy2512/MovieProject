#!/bin/bash

until pg_isready -h payment-db -p 5432 -U postgres; do
  echo "Waiting for database..."
  sleep 2
done

python manage.py makemigrations payments
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")" | python manage.py shell
python manage.py runserver 0.0.0.0:8000 