FROM python:3.10.14-alpine3.20

# Install requirements for building Python packages
RUN apk update && apk add --no-cache g++ unixodbc-dev gnupg curl mariadb-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creating and setting the working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ! This is causing file permission issues as of now
# TODO: Check if this can be fixed
# Create a non-root user
# RUN adduser -D pythonuser
# USER pythonuser

# Copying the entire source code
COPY . .

CMD ["gunicorn", "QtxDjangoApp.wsgi", "--bind", "0.0.0.0:8000"]
