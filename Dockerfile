FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY fetcher_regional.py .
COPY gunicorn.conf.py .

# Environment variables (override these in deployment)
ENV REGION_ID=fetcher-region-1
ENV PORT=8080

# Run with Gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "fetcher_regional:app"]
