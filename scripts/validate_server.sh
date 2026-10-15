```bash
#!/bin/bash
set -Eeuo pipefail

URL="http://127.0.0.1/health"
CONTAINER_NAME="docker-ml-app"
ATTEMPTS=30

echo "Checking Docker container..."

docker inspect -f '{{.State.Running}}' "$CONTAINER_NAME" \
    | grep -qx true

echo "Checking application health..."

for attempt in $(seq 1 "$ATTEMPTS"); do
    if response=$(curl --silent --fail --max-time 3 "$URL" 2>/dev/null) \
       && echo "$response" | grep -q '"status"[[:space:]]*:[[:space:]]*"healthy"'; then
        echo "Application is healthy: $response"
        exit 0
    fi

    echo "Attempt $attempt/$ATTEMPTS: waiting..."
    sleep 2
done

echo "Health check failed. Container logs:"
docker logs --tail 100 "$CONTAINER_NAME" || true

exit 1
```
