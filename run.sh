#!/bin/bash
podman build . -t prow_jobs && podman run -it prow_jobs