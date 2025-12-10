ifndef TAG
$(error TAG is not set. Usage: make <target> TAG=x.y)
endif

DOCKER_BUILDER = docker

greeter_image := docker.io/iku1/greeter:$(TAG)

.PHONY: greeter
greeter: 
	$(DOCKER_BUILDER) build --platform linux/amd64 -t $(greeter_image) .
	$(DOCKER_BUILDER) push $(greeter_image)

