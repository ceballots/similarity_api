.DEFAULT_GOAL := init
.EXPORT_ALL_VARIABLES:

APP_VERSION = 1.0.0
PROJECT_NAME = similarity-api

image := $(PROJECT_NAME):$(app.version)

clean: clean-build clean-py

clean-build:
	rm -fr dist/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


prepare-build: clean 

build: prepare-build docker-build

docker-build-local:
	docker build --rm -t "$(PROJECT_NAME)" -f "deploy/docker/Dockerfile" .

docker-build:
	docker build --rm \
		-t "$(image)" \
		-f "deploy/docker/Dockerfile" .


run: docker-build-local
	./deploy/scripts/run_app.sh
