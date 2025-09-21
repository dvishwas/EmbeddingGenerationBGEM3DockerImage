#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./push-to-dockerhub.sh <your-dockerhub-username>"
    echo "Example: ./push-to-dockerhub.sh myusername"
    exit 1
fi

DOCKERHUB_USERNAME=$1
IMAGE_NAME="bge-m3-api"
FULL_NAME="$DOCKERHUB_USERNAME/$IMAGE_NAME:latest"

echo "Tagging image as $FULL_NAME..."
docker tag $IMAGE_NAME $FULL_NAME

echo "Pushing to Docker Hub..."
docker push $FULL_NAME

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to Docker Hub!"
    echo "Image available at: https://hub.docker.com/r/$DOCKERHUB_USERNAME/$IMAGE_NAME"
    echo ""
    echo "To use in RunPod:"
    echo "Container Image: $FULL_NAME"
    echo "Expose Port: 5000"
else
    echo "❌ Push failed. Make sure you're logged in with 'docker login'"
fi
