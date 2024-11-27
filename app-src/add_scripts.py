from pathlib import Path
import os

if __name__ == "__main__":
    job_scripts_dir = Path(os.environ["JOB_SCRIPTS_DIR"])
    build_scripts_dir = Path(os.environ["BUILD_SCRIPTS_DIR"])

    assert job_scripts_dir.is_dir()
    assert build_scripts_dir.is_dir()

    app_root = Path(os.environ["UNPACKED_PROW_DIR"])
    jobs_root = app_root.joinpath("jobs")
    jobs_dir = jobs_root.joinpath("by-job-name")

    for jd in jobs_dir.iterdir():
        for js in job_scripts_dir.iterdir():
            jd.joinpath(js.stem).symlink_to(js)

    