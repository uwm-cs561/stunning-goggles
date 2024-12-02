import os
import json

DIFF_DATA_ROOT = "/shared/project/mondo/bugswarm-data/data/task_diff"


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def generate_data(*, output_filepath, input_filenames):
    input_files = [
        os.path.join(root, subdir, input_filenames)
        for root, dirs, files in os.walk(DIFF_DATA_ROOT)
        for subdir in dirs
    ]

    ## open output file in append mode
    with open(output_filepath, "a") as output_file:
        for index, input_filepath in enumerate(input_files):
            print(f"{index}/{len(input_files)}")
            with open(input_filepath, "r") as input_file:
                output_file.write(json.dumps({"text": input_file.read()[:1000]}) + "\n")


if __name__ == "__main__":
    generate_data(
        output_filepath=get_relative_path(f"diff_0_sliced_training.jsonl"),
        input_filenames="diff_0.log",
    )
