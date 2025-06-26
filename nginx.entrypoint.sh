#!/bin/sh

# Wait until backend is reachable on port 7575
echo "Waiting for backend to start..."

while ! nc -z backend 7575; do
  echo "Backend is not ready yet..."
  sleep 2
done

echo "Backend is up. Starting Nginx..."

# Start Nginx in the foreground
nginx -g "daemon off;"
