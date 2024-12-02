import os
from pathlib import Path

import requests


PROW_BASE_URL = os.environ["PROW_BASE_URL"]
PROW_JOBS_JSON_ENDPOINT = os.environ["PROW_JOBS_JSON_ENDPOINT"]
PROW_JOBS_JSON_PATH = os.environ["PROW_JOBS_JSON_PATH"]


if __name__ == "__main__":
    url = PROW_BASE_URL + PROW_JOBS_JSON_ENDPOINT

    out_path = Path(PROW_JOBS_JSON_PATH)
    out_path.parent.mkdir(exist_ok=True)

    print(f"fetching the latest prow jobs")

    out_path.write_bytes(requests.get(url).content)

    print(f"prow jobs written to {out_path.as_posix()}")
