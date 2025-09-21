#!/bin/bash

IMAGE_NAME="bge-m3-api"
DOCKER_USERNAME=${1:-"your-username"}

echo "Building BGE-M3 Docker image..."
docker build --platform linux/amd64 -t $IMAGE_NAME .

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "To push to Docker Hub:"
    echo "1. docker tag $IMAGE_NAME $DOCKER_USERNAME/$IMAGE_NAME:latest"
    echo "2. docker push $DOCKER_USERNAME/$IMAGE_NAME:latest"
    echo ""
    echo "To run locally:"
    echo "docker run -p 5000:5000 $IMAGE_NAME"
else
    echo "Build failed!"
    exit 1
fi
