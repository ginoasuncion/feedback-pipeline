FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Ensure the app listens on all interfaces
ENV PORT=8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

