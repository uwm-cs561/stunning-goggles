import os
import re

from consts import ARTIFACTS_JSON_PATH, LOG_DIR, LOG_FILTERED_DIR
from downloader.cmd.download_logs import load_artifact_job_ids

BLACK_LIST = [
    r"^\033\[\d?K",
    r"\033\[\d?K$",
    # r"\d+%\s*\(\d+/\d+\)",
    r"\d+/\d+",
    r"\d+%",
    r"Downloading",
    r"Downloaded",
    r"\.{8}",
    r"\[new branch\]",
    r"\[new tag\]",
    r"\d+ .?B",
]
merged = f"({'|'.join([e for e in BLACK_LIST])})"
print(merged)
REGEX_PROGRESS_LINE = re.compile(merged)


def merge_progress_lines(log_content: str):
    lines = log_content.splitlines()
    res = []

    # no list comprehension for debug
    for line in lines:
        striped = line.strip()
        if len(striped) == 0:
            continue
        mat = REGEX_PROGRESS_LINE.findall(line)
        if len(mat) > 0:
            continue
        res.append(striped)
    return res


LINE_THRESHOLD = 1000


def main():
    art_path = os.path.join(os.getcwd(), ARTIFACTS_JSON_PATH)
    job_ids = load_artifact_job_ids(art_path)
    os.makedirs(LOG_FILTERED_DIR, exist_ok=True)

    need_inspection = []

    for job_id in job_ids:
        log_path = os.path.join(os.getcwd(), f"{LOG_DIR}/{job_id}.log")
        if not os.path.exists(log_path):
            print(f"Log not found for {job_id}")
            continue
        with open(log_path, "r") as f:
            log_content = f.read()
        new_log_content = merge_progress_lines(log_content)

        before = len(log_content.splitlines())
        after = len(new_log_content)
        delta = before - after
        if after > LINE_THRESHOLD or delta / before < 0.5:
            need_inspection.append(job_id)

        print(f"Filtered {job_id}: {before} -> {after}")
        new_log_path = os.path.join(os.getcwd(), f"{LOG_FILTERED_DIR}/{job_id}.log")
        with open(new_log_path, "w") as f:
            f.write("\n".join(new_log_content))

    print(f"Inspection needed for {(need_inspection)}")


if __name__ == "__main__":
    main()
