IMG_TAG=prow-jobs

export GANGWAY_TOKEN
export GANGWAY_URL

all: build console

build:
	podman build --rm --no-cache -t $(IMG_TAG) --squash .

console:
	podman run -it -e GANGWAY_TOKEN -e GANGWAY_URL $(IMG_TAG)
