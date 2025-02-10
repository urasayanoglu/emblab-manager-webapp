# Use official Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKERIZED 1  

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Replace SQLite with PostgreSQL settings
RUN sed -i 's/django.db.backends.sqlite3/django.db.backends.postgresql_psycopg2/' emblab/settings.py && \
    sed -i 's/NAME:.*db.sqlite3/NAME: emblab/' emblab/settings.py && \
    sed -i '/USER:/c\\        "USER": "emblab_admin",' emblab/settings.py && \
    sed -i '/PASSWORD:/c\\        "PASSWORD": "your_password_here",' emblab/settings.py && \
    sed -i '/HOST:/c\\        "HOST": "db",' emblab/settings.py && \
    sed -i '/PORT:/c\\        "PORT": "5432",' emblab/settings.py

# Run collectstatic to gather static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start the server
CMD ["gunicorn", "emblab.wsgi:application", "--bind", "0.0.0.0:8000"]
