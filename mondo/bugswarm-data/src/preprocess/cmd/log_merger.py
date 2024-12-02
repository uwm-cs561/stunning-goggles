import os
import re

from consts import ARTIFACTS_JSON_PATH, LOG_DIR, LOG_FILTERED_DIR
from downloader.cmd.download_logs import load_artifact_job_ids

BLACK_LIST = [
    r"^\033\[[0-9]?K",
    r"\033\[[0-9]?K$",
    r"\d+%\s*\(\d+/\d+\)",
]
merged = f"({'|'.join([e for e in BLACK_LIST])})"
REGEX_PROGRESS_LINE = re.compile(merged)


def merge_progress_lines(log_content: str):
    lines = log_content.splitlines()
    res = []

    # no list comprehension for debug
    for line in lines:
        mat = REGEX_PROGRESS_LINE.findall(line)
        if mat:
            continue
        res.append(line)
    return res


def main():
    art_path = os.path.join(os.getcwd(), ARTIFACTS_JSON_PATH)
    job_ids = load_artifact_job_ids(art_path)
    os.makedirs(LOG_FILTERED_DIR, exist_ok=True)

    for job_id in job_ids:
        log_path = os.path.join(os.getcwd(), f"{LOG_DIR}/{job_id}.log")
        if not os.path.exists(log_path):
            print(f"Log not found for {job_id}")
            continue
        with open(log_path, "r") as f:
            log_content = f.read()
        new_log_content = merge_progress_lines(log_content)

        print(
            f"Filtered {job_id}: {len(log_content.splitlines())} -> {len(new_log_content)}"
        )
        new_log_path = os.path.join(os.getcwd(), f"{LOG_FILTERED_DIR}/{job_id}.log")
        with open(new_log_path, "w") as f:
            f.write("\n".join(new_log_content))


if __name__ == "__main__":
    main()
