#!/bin/python3.12

import os
import requests
import dotenv
from requests.exceptions import JSONDecodeError
import json

assert dotenv.load_dotenv()

GANGWAY_URL = os.getenv("GANGWAY_URL", "NOT_SET")
GANGWAY_TOKEN = os.getenv("GANGWAY_TOKEN", "NOT_SET")

JOB_NAME = os.environ["JOB_NAME"]


def main():
    print(f"retriggering job: {JOB_NAME}")

    resp = requests.post(
        url=f"{GANGWAY_URL}/v1/executions/{JOB_NAME}",
        headers={"Authorization": f"Bearer {GANGWAY_TOKEN}"},
        data=json.dumps({"job_execution_type": "1"}),
    )

    try:
        print(resp.json())
    except JSONDecodeError:
        print(resp.status_code)
        print(resp.reason)
        print (resp.content)        

if __name__ == "__main__":
    main()
