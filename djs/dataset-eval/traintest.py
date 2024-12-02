import os
import random
import json

DATA_ROOT = "/shared/project/mondo/bugswarm-data/data/diff_hunk_filtered"


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


TRAINTEST_FILE_NAME = get_relative_path("train_test.json")


def generate_files_list(*, parent_dir):
    result = []

    sorted_subdirs = sorted(
        subdir for _root, dirs, _files in os.walk(parent_dir) for subdir in dirs
    )
    for subdir in sorted_subdirs:
        path = os.path.join(parent_dir, subdir)
        files = sorted(
            file
            for _root, _dirs, files in os.walk(path)
            for file in files
            if file.startswith("hunk_20")
        )
        largest_seq_num = 0
        for file in files:
            _hunk, _20, sequence_num, _kind_dot_log = file.split("_")
            largest_seq_num = max(largest_seq_num, int(sequence_num))
        for seq_num in range(largest_seq_num + 1):
            result.append(
                {
                    "path": path,
                    "ans": f"hunk_20_{seq_num}_ans.log",
                    "ctx": f"hunk_20_{seq_num}_ctx.log",
                }
            )

    return result


def generate_train_test_split():
    files = generate_files_list(parent_dir=DATA_ROOT)
    random.seed(6745)
    random.shuffle(files)
    split_index = len(files) // 10
    test_split = files[:split_index]
    train_split = files[split_index:]
    with open(TRAINTEST_FILE_NAME, "w") as f:
        json.dump({"test": test_split, "train": train_split}, f, indent=2)


def get_train():
    with open(TRAINTEST_FILE_NAME, "r") as f:
        file_content = json.load(f)
    return file_content["train"]


def get_test():
    with open(TRAINTEST_FILE_NAME, "r") as f:
        file_content = json.load(f)
    return file_content["test"]


def get_ans(file_info):
    filepath = os.path.join(file_info["path"], file_info["ans"])
    with open(filepath, "r") as f:
        file_contents = f.read()
    return file_contents


def get_ctx(file_info):
    filepath = os.path.join(file_info["path"], file_info["ctx"])
    with open(filepath, "r") as f:
        file_contents = f.read()
    return file_contents


if __name__ == "__main__":
    generate_train_test_split()
