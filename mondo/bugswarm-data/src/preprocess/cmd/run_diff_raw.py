from collections import defaultdict
from datetime import datetime
import json
import os
import shutil
from typing import Generator
from types import SimpleNamespace
from difflib import unified_diff

import downloader.typing.bugswarm as typ_bugswarm
from consts import (
    ARTIFACTS_JSON_PATH,
    LOG_DIR,
    DIFF_DIR,
    PASSED_LOG_NAME,
    FAILED_LOG_NAME,
    DIFF_NO_CTX_NAME,
)


class Task:
    id: str  # image tag
    passed_log_id: str
    failed_log_id: str

    def save_diff(self, loaddir: str, savedir: str, ctxs: list[int] = [0]):
        cwd = os.path.join(savedir, self.id)

        passed_path = os.path.join(cwd, PASSED_LOG_NAME)
        failed_path = os.path.join(cwd, FAILED_LOG_NAME)

        src_passed = os.path.join(loaddir, self.passed_log_id + ".log")
        src_failed = os.path.join(loaddir, self.failed_log_id + ".log")

        if not os.path.exists(src_passed):
            print(f"[{self.id}] Missing passed log")
            return False
        if not os.path.exists(src_failed):
            print(f"[{self.id}] Missing failed log")
            return False
        os.makedirs(cwd, exist_ok=True)

        # copy from
        shutil.copyfile(src_passed, passed_path)
        shutil.copyfile(src_failed, failed_path)

        print(f"[{self.id}] Saving diff")

        passed_lines = []
        with open(passed_path) as f:
            passed_lines = f.readlines()
        failed_lines = []
        with open(failed_path) as f:
            failed_lines = f.readlines()

        # TODO: do we need to save a pure or object style diff?
        for ctx in ctxs:
            diff_path = os.path.join(cwd, f"diff_{ctx}.log")
            # regen everytime
            # if os.path.exists(diff_path):
            #     continue
            diff_with_context_lines = list(
                unified_diff(
                    failed_lines,
                    passed_lines,
                    PASSED_LOG_NAME,
                    FAILED_LOG_NAME,
                    n=ctx,
                )
            )
            with open(diff_path, "w") as f:
                f.writelines(diff_with_context_lines)
        return True


def load_artifact(artifacts_json_path: str):
    artifacts = []  # type: list[typ_bugswarm.Entry]
    with open(artifacts_json_path) as f:
        artifacts = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    tasks = defaultdict(Task)
    for artifact in artifacts:
        i = tasks[artifact.image_tag]
        i.id = artifact.image_tag
        i.passed_log_id = str(artifact.passed_job.job_id)
        i.failed_log_id = str(artifact.failed_job.job_id)
    return tasks


def compute_diffs(savedir: str, log_dir: str, artifacts_json_path: str):
    os.makedirs(savedir, exist_ok=True)

    tasks = load_artifact(artifacts_json_path)

    assert len(tasks) > 0, "No tasks loaded"
    success_count = 0
    fail_count = 0
    miss_count = 0

    for tasks in tasks.values():
        try:
            # TODO: will context window length of diffs affect our results?
            done = tasks.save_diff(log_dir, savedir, [0, 2, 4, 8])
            if done:
                success_count += 1
            else:
                miss_count += 1
        except Exception as e:
            print(f"Failed to save diff for {tasks.id}: ", {e})
            fail_count += 1
            continue
    print(f"Success: {success_count}, Fail: {fail_count}, Miss: {miss_count}")


def main():
    print("Diff started")
    os.makedirs(DIFF_DIR, exist_ok=True)
    art_path = os.path.join(os.getcwd(), ARTIFACTS_JSON_PATH)
    compute_diffs(DIFF_DIR, LOG_DIR, art_path)


if __name__ == "__main__":
    main()
