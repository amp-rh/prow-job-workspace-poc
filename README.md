# Prow Job Workspace Proof-of-Concept
Deploy an extensible workspace for interacting with Prow Job runs and executing automation tasks.

Requires:
- `podman`
- `make`

Clone repo and `cd`:
```bash
git clone https://github.com/amp-rh/prow-job-workspace-poc.git
cd prow-job-workspace-poc
```
Make reports:
```bash
make reports
```

Start interactive console with injected scripts:
```bash
make console
```