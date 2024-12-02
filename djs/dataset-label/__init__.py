import os
from pprint import pprint
import random

DIFF_DATA_ROOT = "/shared/project/mondo/bugswarm-data/data/task_diff"
FAILED = "failed.log"
PASSED = "passed.log"


def generate_subdirs_list(*, parent_dir):
    sorted_subdirs = sorted(
        subdir for _root, dirs, _files in os.walk(parent_dir) for subdir in dirs
    )
    abs_paths = list(
        map(lambda subdir: os.path.join(parent_dir, subdir), sorted_subdirs)
    )
    return abs_paths


if __name__ == "__main__":
    subdirs = generate_subdirs_list(parent_dir=DIFF_DATA_ROOT)
    random.seed(6745)
    chosen = random.choices(subdirs, k=10)
    pprint(chosen)
