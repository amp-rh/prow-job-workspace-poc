import json
from pathlib import Path
import os
import re

if __name__ == "__main__":
    prow_jobs_json_path = Path(os.environ["PROW_JOBS_JSON_PATH"])
    app_root = Path(os.environ["UNPACKED_PROW_DIR"])
    job_name_filter_regex = os.environ["JOB_NAME_FILTER_REGEX"]

    jobs_root = app_root.joinpath("jobs")

    for d in (
        (jobs_by_build_id_path := jobs_root.joinpath("by-build-id")),
        (jobs_by_name_path := jobs_root.joinpath("by-job-name")),
        (jobs_by_type_path := jobs_root.joinpath("by-job-type")),
        (jobs_by_state_path := jobs_root.joinpath("by-job-state")),
        (jobs_by_refs_path := jobs_root.joinpath("by-refs")),
    ):
        d.mkdir(exist_ok=False, parents=True)

    with prow_jobs_json_path.open() as fo:
        jobs_iter = filter(
            lambda x: re.match(job_name_filter_regex, x["spec"]["job"]),
            (_ for _ in json.load(fo)["items"]),
        )
        for j in jobs_iter:
            job_spec = j["spec"]
            job_type = job_spec["type"]
            job_status = j["status"]
            job_name = job_spec["job"]

            try:
                job_build_id = job_status["build_id"]
            except KeyError:
                print("skipping job without build_id")
                continue

            job_dir = jobs_by_build_id_path.joinpath(job_build_id)
            job_refs_dir = job_dir.joinpath("refs")

            job_dir.mkdir()
            job_refs_dir.mkdir()

            job_dir.joinpath("raw").write_text(json.dumps(j))

            if job_url := job_status.get("url"):
                job_dir.joinpath("url").write_text(job_url)

            if job_start_time := job_status.get("startTime"):
                job_dir.joinpath("start_time").write_text(job_start_time)

            if job_pending_time := job_status.get("pendingTime"):
                job_dir.joinpath("pending_time").write_text(job_pending_time)

            if completion_time := job_status.get("completionTime"):
                job_dir.joinpath("completion_time").write_text(completion_time)

            if job_state := job_status.get("state"):
                job_dir.joinpath("state").write_text(job_state)
                _p = jobs_by_state_path.joinpath(job_state).joinpath(job_build_id)
                _p.parent.mkdir(exist_ok=True)
                _p.symlink_to(job_dir, target_is_directory=True)

            if job_name := job_spec.get("job"):
                job_dir.joinpath("job").write_text(job_name)
                _p = jobs_by_name_path.joinpath(job_name).joinpath(job_build_id)
                _p.parent.mkdir(exist_ok=True)
                _p.symlink_to(job_dir, target_is_directory=True)

            _refs = job_spec.get("refs")
            job_refs = [_refs] if _refs else []
            job_refs.extend(job_spec.get("extra_refs", []))

            if job_refs:
                job_refs_dir.joinpath("raw").write_text(json.dumps(job_refs))

                for ref in job_refs:
                    ref_org = ref["org"]
                    ref_repo = ref["repo"]
                    base_ref = ref["base_ref"]

                    _p = (
                        jobs_by_refs_path.joinpath(ref_org)
                        .joinpath(ref_repo)
                        .joinpath(base_ref)
                        .joinpath(job_name)
                    )
                    _p.parent.mkdir(exist_ok=True, parents=True)
                    _p.symlink_to(jobs_by_name_path.joinpath(job_name), target_is_directory=True)

            if job_type := job_spec.get("type"):
                job_dir.joinpath("type").write_text(job_type)
                _p = jobs_by_type_path.joinpath(job_type).joinpath(job_build_id)
                _p.parent.mkdir(exist_ok=True)
                _p.symlink_to(job_dir, target_is_directory=True)