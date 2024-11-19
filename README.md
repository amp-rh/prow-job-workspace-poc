# Prow Job Workspace Proof-of-Concept
Deploy an extensible workspace for interacting with Prow Job runs and executing automation tasks.

Build and run with Podman:
```bash
podman build https://github.com/amp-rh/prow-job-workspace-poc.git -t prow-jobs-workspace && podman run -it prow-jobs-workspace
```