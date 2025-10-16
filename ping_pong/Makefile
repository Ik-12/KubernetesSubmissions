ifndef TAG
$(error TAG is not set. Usage: make <target> TAG=x.y)
endif

DOCKER_BUILDER = docker

ping_pong_image := docker.io/iku1/ping_pong:$(TAG)

.PHONY: ping_pong
ping_pong: 
	$(DOCKER_BUILDER) build -t $(ping_pong_image) .
	$(DOCKER_BUILDER) push $(ping_pong_image)

