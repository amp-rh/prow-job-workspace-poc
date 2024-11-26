REMOTE_URL=https://github.com/amp-rh/prow-job-workspace-poc.git 
IMG_TAG=prow-jobs

build:
	podman build --rm -t $(IMG_TAG) --force-rm --squash $(REMOTE_URL)

build-local:
	podman build --rm -t $(IMG_TAG) --force-rm --squash .

console:
	podman run -it $(IMG_TAG)
