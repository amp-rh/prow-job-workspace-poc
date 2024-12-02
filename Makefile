DEFAULT_IMG_TAG=prow-jobs
DEFAULT_STAGE=unpack_prow_jobs

CONSOLE_IMG_TAG=prow-jobs-run
CONSOLE_STAGE=run

REPORTS_IMG_TAG=prow-jobs-reports
REPORTS_STAGE=reports
REPORTS_CONTAINER_NAME=prow-jobs-reports

CONTAINER_REPORTS_DIR=/tmp/reports

export GANGWAY_TOKEN
export GANGWAY_URL

all: build

build: build-default-img

build-default-img:
	podman build --rm --no-cache -t $(DEFAULT_IMG_TAG) --target $(DEFAULT_STAGE) --squash .

build-console-img:
	podman build --rm --no-cache -t $(CONSOLE_IMG_TAG) --target $(CONSOLE_STAGE) --squash .

build-reports-img:
	podman build --rm --no-cache -t $(REPORTS_IMG_TAG) --target $(REPORTS_STAGE) --squash .

reports: build-reports-img
	podman container create --replace --rm --name=$(REPORTS_CONTAINER_NAME) $(REPORTS_IMG_TAG)
	podman cp --overwrite $(REPORTS_CONTAINER_NAME):$(CONTAINER_REPORTS_DIR) ./

console: build-console-img
	podman run -it -e GANGWAY_TOKEN -e GANGWAY_URL $(CONSOLE_IMG_TAG)
