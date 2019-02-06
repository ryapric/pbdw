# Name of package
PKGNAME := $$(grep 'name = ' setup.py | sed -r 's/name = '"'"'(.*)'"'"',/\1/')

# Need to adjust shell used, for `source` command
SHELL = /usr/bin/env bash

# Set venv activation, since make runs each recipe in its own shell instance
venv-act = source venv/bin/activate


all: venv dev-pkgs install_venv test clean

# Dummy FORCE target dep to make things always run
FORCE:

venv: FORCE
	@python3 -m venv --clear venv

dev-pkgs: venv
	@$(venv-act); \
	pip3 install wheel; \
	pip3 install setuptools pytest pytest-flask

test: clean venv dev-pkgs install_venv
	@$(venv-act); \
	python3 -m pytest -v; \
	make -s clean

build: venv dev-pkgs
	@$(venv-act); \
	python3 setup.py sdist bdist_wheel

install_venv: venv
	@$(venv-act); \
	pip3 install .

clean: FORCE
	@find . -type d -regextype posix-extended -regex ".*\.egg-info|.*cache.*" -exec rm -rf {} +
	@find . -type f -regextype posix-extended -regex ".*\.pyc" -exec rm {} +
	@find . -name "test.db" -exec rm {} +

# Install to system library
install: FORCE
ifeq ($(`whoami`), 'root')
	pip3 install .
else
	pip3 install --user .
endif

doc: FORCE
	@pandoc -o README.html README.md
	@echo "Created README.html"

uninstall: FORCE
	pip3 uninstall -y $(PKGNAME)


# Docker deployment
IMAGE = fredcast
TAG = latest
REPO = docker.io/ryapric

# Cumulative deps on each other; Make can't determine if something is out of
# date, but Docker is smart enough to not redo anything it's already done
docker-build:
	@docker build -t $(IMAGE):$(TAG) .

docker-push: docker-build
	@docker tag $(IMAGE):$(TAG) $(REPO)/$(IMAGE):$(TAG)
	@docker push $(REPO)/$(IMAGE):$(TAG)

gcloud-instance-create: docker-push
	@gcloud compute instances create-with-container $(IMAGE) \
	--container-image $(REPO)/$(IMAGE):$(TAG) \
	--machine-type "f1-micro" \
	--tags=http-server,https-server

gcloud-instance-update: docker-push
	@gcloud compute instances update-container $(IMAGE) \
	--container-image $(REPO)/$(IMAGE):$(TAG)
