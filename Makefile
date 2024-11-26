DOCKER_USERNAME = barun25

FRONTEND_IMAGE_NAME = todo_react_frontend
FRONTEND_TAG = latest

BACKEND_IMAGE_NAME = todo_django_backend
BACKEND_TAG = latest


# Build, tag, and push frontend image
build-frontend:
	docker build -t $(FRONTEND_IMAGE_NAME):$(FRONTEND_TAG) ./frontend

tag-frontend:
	docker tag $(FRONTEND_IMAGE_NAME):$(FRONTEND_TAG) $(DOCKER_USERNAME)/$(FRONTEND_IMAGE_NAME):$(FRONTEND_TAG)

push-frontend:
	docker push $(DOCKER_USERNAME)/$(FRONTEND_IMAGE_NAME):$(FRONTEND_TAG)

all-frontend:	build-frontend tag-frontend push-frontend


run-frontend:
	docker run -p 80:80 $(DOCKER_USERNAME)/$(FRONTEND_IMAGE_NAME):$(FRONTEND_TAG)


# Build, tag, and push backend image
build-backend:
	docker build -t $(BACKEND_IMAGE_NAME):$(BACKEND_TAG) ./backend

tag-backend:
	docker tag $(BACKEND_IMAGE_NAME):$(BACKEND_TAG) $(DOCKER_USERNAME)/$(BACKEND_IMAGE_NAME):$(BACKEND_TAG)

push-backend:
	docker push $(DOCKER_USERNAME)/$(BACKEND_IMAGE_NAME):$(BACKEND_TAG)

all-backend:	build-backend tag-backend push-backend


run-backend:
	docker run -p 8000:8000 $(DOCKER_USERNAME)/$(BACKEND_IMAGE_NAME):$(BACKEND_TAG)

