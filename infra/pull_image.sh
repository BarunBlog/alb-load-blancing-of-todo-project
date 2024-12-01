# Docker Hub username and image names
DOCKER_USERNAME="barun25"
FRONTEND_IMAGE_NAME="todo_react_frontend"
FRONTEND_TAG="latest"
BACKEND_IMAGE_NAME="todo_django_backend"
BACKEND_TAG="latest"

# Pull and run the backend container on port 8000
sudo docker run -d -p 8000:8000 barun25/todo_django_backend:latest

# Pull and run the frontend container on port 80
sudo docker run -d -p 80:80 barun25/todo_react_frontend:latest