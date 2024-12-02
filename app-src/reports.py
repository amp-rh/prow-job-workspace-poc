import os
from pathlib import Path
import re
import json
import csv

prow_jobs_json_path = Path(os.environ["PROW_JOBS_JSON_PATH"])
job_name_filter_regex = os.environ["JOB_NAME_FILTER_REGEX"]
output_reports_dir = Path(os.environ["CONTAINER_REPORTS_DIR"])

output_reports_dir.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    with prow_jobs_json_path.open() as fo:
        jobs_iter = filter(
            lambda x: re.match(job_name_filter_regex, x["spec"]["job"]),
            (_ for _ in json.load(fo)["items"]),
        )

        with output_reports_dir.joinpath("latest.csv").open("a") as csv_fo:
            csv_writer = csv.DictWriter(
                f=csv_fo,
                fieldnames=["build_id", "job_name", "job_url", "job_state"]
            )
            csv_writer.writeheader()

            for j in jobs_iter:
                job_spec = j["spec"]
                job_type = job_spec["type"]
                job_status = j["status"]
                job_name = job_spec["job"]
                job_url = job_status["url"]
                job_state = job_status["state"]

                try:
                    job_build_id = job_status["build_id"]
                except KeyError:
                    print("skipping job without build_id")
                    continue

                csv_writer.writerow(
                    {
                        "build_id": job_build_id,
                        "job_name": job_name,
                        "job_url": job_url,
                        "job_state": job_state,
                    }
                )
