ifndef TAG
$(error TAG is not set. Usage: make <target> TAG=x.y)
endif

DOCKER_BUILDER = docker

log_writer_image := docker.io/iku1/log_output_writer:$(TAG)

.PHONY: log_writer
log_writer: 
	$(DOCKER_BUILDER) build -t $(log_writer_image) .
	$(DOCKER_BUILDER) push $(log_writer_image)

