# Docker Hub username and image names
DOCKER_USERNAME="barun25"
FRONTEND_IMAGE_NAME="todo_react_frontend"
FRONTEND_TAG="latest"
BACKEND_IMAGE_NAME="todo_django_backend"
BACKEND_TAG="latest"

# Create a custom Docker network if it doesn't already exist
if ! sudo docker network ls | grep -q my-app-network; then
  sudo docker network create my-app-network
  echo "Docker network 'my-app-network' created successfully."
else
  echo "Docker network 'my-app-network' already exists."
fi

# Pull and run the backend container on port 8000
sudo docker run -d \
  --network my-app-network \
  --name backend \
  -p 8000:8000 \
  $DOCKER_USERNAME/$BACKEND_IMAGE_NAME:$BACKEND_TAG

# Pull and run the frontend container on port 80
sudo docker run -d \
  --network my-app-network \
  --name frontend \
  -p 80:80 \
  $DOCKER_USERNAME/$FRONTEND_IMAGE_NAME:$FRONTEND_TAG