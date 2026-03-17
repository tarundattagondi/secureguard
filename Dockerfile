FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy app code
COPY . .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Set Flask app
ENV FLASK_APP=run.py

# Expose port
EXPOSE 5001

# Run entrypoint
CMD ["./docker-entrypoint.sh"]