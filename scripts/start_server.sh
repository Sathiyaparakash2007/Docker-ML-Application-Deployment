```bash
#!/bin/bash
set -Eeuo pipefail

APP_DIR="/opt/docker-ml-app"
IMAGE_NAME="docker-ml-app:latest"
CONTAINER_NAME="docker-ml-app"

cd "$APP_DIR"

echo "Building Docker image..."

docker build --pull -t "$IMAGE_NAME" .

echo "Removing previous container if it exists..."

if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
    docker rm -f "$CONTAINER_NAME"
fi

echo "Starting new container..."

docker run -d \
    --name "$CONTAINER_NAME" \
    --restart unless-stopped \
    -p 80:5000 \
    "$IMAGE_NAME"

echo "Container started successfully."

docker ps --filter "name=$CONTAINER_NAME"
```
