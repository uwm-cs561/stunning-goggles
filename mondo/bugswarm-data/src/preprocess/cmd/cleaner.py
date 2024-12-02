import os
import re

from consts import ARTIFACTS_JSON_PATH, LOG_DIR, LOG_CLEANED_DIR
from downloader.cmd.download_logs import load_artifact_job_ids

BLACK_LIST = [r"^\d{4}-\d{2}-\d{2}.(\d{2}:\d{2})?:?(\d{2}\.\d{1,7})?Z?\s*"]
merged = f"({'|'.join([e for e in BLACK_LIST])})"
REGEX_PROGRESS_LINE = re.compile(merged)


def clean_logs(log_content: str):
    lines = log_content.splitlines()
    res = []

    # no list comprehension for debug
    for line in lines:
        striped = line.strip()
        if len(striped) == 0:
            continue
        mat = REGEX_PROGRESS_LINE.sub("", striped)
        if len(mat) == 0:
            continue
        res.append(mat)
    return res


def main():
    art_path = os.path.join(os.getcwd(), ARTIFACTS_JSON_PATH)
    job_ids = load_artifact_job_ids(art_path)
    os.makedirs(LOG_CLEANED_DIR, exist_ok=True)

    for job_id in job_ids:
        log_path = os.path.join(os.getcwd(), f"{LOG_DIR}/{job_id}.log")
        if not os.path.exists(log_path):
            print(f"Log not found for {job_id}")
            continue
        with open(log_path, "r") as f:
            log_content = f.read()
        new_log_content = clean_logs(log_content)

        print(f"Cleaning {job_id}")
        new_log_path = os.path.join(os.getcwd(), f"{LOG_CLEANED_DIR}/{job_id}.log")
        with open(new_log_path, "w") as f:
            f.write("\n".join(new_log_content))


if __name__ == "__main__":
    main()
