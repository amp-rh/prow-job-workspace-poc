REMOTE_URL=https://github.com/amp-rh/prow-job-workspace-poc.git 
IMG_TAG=prow-jobs


all: build console

build:
	podman build --rm --no-cache -t $(IMG_TAG) --squash .

console:
	podman run -it $(IMG_TAG)
