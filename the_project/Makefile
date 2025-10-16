ifndef TAG
$(error TAG is not set. Usage: make <target> TAG=x.y)
endif

DOCKER_BUILDER = docker

todo_app_image := docker.io/iku1/todo_app:$(TAG)

.PHONY: todo_app
todo_app: 
	$(DOCKER_BUILDER) build -t $(todo_app_image) ./todo_app
	$(DOCKER_BUILDER) push $(todo_app_image)
