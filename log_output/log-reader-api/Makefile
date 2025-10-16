ifndef TAG
$(error TAG is not set. Usage: make <target> TAG=x.y)
endif

DOCKER_BUILDER = docker

log_reader_api_image := docker.io/iku1/log_output_reader_api:$(TAG)

.PHONY: log_reader_api
log_reader_api: 
	$(DOCKER_BUILDER) build -t $(log_reader_api_image) .
	$(DOCKER_BUILDER) push $(log_reader_api_image)
