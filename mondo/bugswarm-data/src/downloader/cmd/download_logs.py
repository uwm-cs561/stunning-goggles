from datetime import datetime
import json
import os
from typing import Generator
from types import SimpleNamespace
from ratelimit import limits, sleep_and_retry

from downloader.vendor.bugswarm_database_api import DatabaseAPI
import downloader.typing.bugswarm as typ_bugswarm

ARTIFACTS_JSON_PATH = "data/2024-11-17-02-09-45-artifacts.json"

bugswarmapi = DatabaseAPI()


@sleep_and_retry
@limits(calls=6, period=60)
def get_log(job_id: int):
    return bugswarmapi.get_build_log_raw_resp(str(job_id), error_if_not_found=False)


def load_artifact_job_ids(artifacts_json_path: str):
    artifacts = []  # type: list[typ_bugswarm.Entry]
    with open(artifacts_json_path) as f:
        artifacts = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    job_ids = set()
    for artifact in artifacts:
        passed_job_id = artifact.passed_job.job_id
        failed_job_id = artifact.failed_job.job_id
        job_ids.update([passed_job_id, failed_job_id])
    return job_ids


def load_existed_job_ids(savedir: str):
    job_ids = set()
    for filename in os.listdir(savedir):
        if filename.endswith(".log"):
            size = os.path.getsize(os.path.join(savedir, filename))
            if size == 0:
                continue
            job_id = int(filename.split(".")[0])
            job_ids.add(job_id)
    return job_ids


def get_logs(savedir: str, artifacts_json_path: str):
    os.makedirs(savedir, exist_ok=True)

    full_job_ids = load_artifact_job_ids(artifacts_json_path)
    existed_job_ids = load_existed_job_ids(savedir)

    job_ids = full_job_ids - existed_job_ids
    assert len(job_ids) > 0, "No new job ids to download logs"
    print(
        f"Total: {len(full_job_ids)}, Finished: {len(existed_job_ids)}, Wait: {len(job_ids)}"
    )

    def get_next_job_id():
        try:
            return job_ids.pop()
        except KeyError:
            return None

    job_id = get_next_job_id()

    while True:
        if job_id is None:
            break
        try:
            resp = get_log(job_id)
            if resp.status_code == 404:
                # continue if not found
                print(f"Logs not found for {job_id}")
                job_id = get_next_job_id()
                continue
            resp_json = resp.json()
            logs = resp_json["build_log"]
            if logs:
                with open(os.path.join(savedir, f"{job_id}.log"), "w") as f:
                    f.write(logs)
                print(f"Downloaded logs for {job_id}")
            job_id = get_next_job_id()
        except Exception as e:
            print(f"Failed to download logs for {job_id}: ", e)
            continue


def main():
    print("Start Downloading")
    dir_name = f"data/job_logs"
    os.makedirs(dir_name, exist_ok=True)
    art_path = os.path.join(os.getcwd(), ARTIFACTS_JSON_PATH)
    get_logs(dir_name, art_path)


if __name__ == "__main__":
    main()
