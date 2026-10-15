```bash
#!/bin/bash
set -Eeuo pipefail

echo "Installing Docker and curl..."

dnf install -y docker curl

systemctl enable --now docker

docker --version
systemctl is-active --quiet docker

echo "Docker is installed and running."
```
