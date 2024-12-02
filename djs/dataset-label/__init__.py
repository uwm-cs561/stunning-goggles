import os
import random
import json

DATA_ROOT = "/shared/project/mondo/bugswarm-data/data/filtered_job_logs"
FAILED = "failed.log"
PASSED = "passed.log"
CONTEXT_WINDOW = 4


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def generate_subdirs_list(*, parent_dir):
    sorted_subdirs = sorted(
        subdir for _root, dirs, _files in os.walk(parent_dir) for subdir in dirs
    )
    abs_paths = [os.path.join(parent_dir, subdir, FAILED) for subdir in sorted_subdirs]
    return abs_paths


def generate_logfiles_list(*, parent_dir):
    sorted_filenames = sorted(
        file for _root, _dirs, files in os.walk(parent_dir) for file in files
    )
    abs_paths = [os.path.join(parent_dir, filename) for filename in sorted_filenames]
    return abs_paths


def process(*, abs_paths, output_abs_path):

    with open(output_abs_path, "a") as out_file:
        # open file from random choices
        for input_abs_path in abs_paths:
            with open(input_abs_path, "r") as in_file:
                lines = in_file.readlines()
            # choose random lines
            start_line = random.randint(0, len(lines) - CONTEXT_WINDOW)
            chosen_lines = "".join(lines[start_line : start_line + CONTEXT_WINDOW])
            print()
            print(chosen_lines)
            y_or_n = input("Lines contain error? (y/N) ")
            result = False
            if y_or_n in ["y", "Y"]:
                result = True
            elif y_or_n in ["", "n", "N"]:
                pass
            else:
                raise ValueError(f"Unrecognized input")
            out_file.write(
                json.dumps(
                    {"id": input_abs_path, "text": chosen_lines, "label": result}
                )
            )


if __name__ == "__main__":
    subdirs = generate_logfiles_list(parent_dir=DATA_ROOT)
    random.seed(6745)
    chosen = random.choices(subdirs, k=10)
    process(abs_paths=chosen, output_abs_path=get_relative_path("output.jsonl"))
