import os
import json

DIFF_DATA_ROOT = "/shared/project/mondo/bugswarm-data/data/task_diff"


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def generate_data(*, diff=False, context_size=0):
    category = f"diff_{context_size}" if diff else None

    if category is None:
        raise NotImplementedError(f"Only supports diff logs currently")

    output_filepath = get_relative_path(f"{category}_training.jsonl")

    input_files = [
        os.path.join(root, subdir, f"{category}.log")
        for root, dirs, files in os.walk(DIFF_DATA_ROOT)
        for subdir in dirs
    ]

    ## open output file in append mode
    with open(output_filepath, "a") as output_file:
        for index, input_filepath in enumerate(input_files):
            print(f"{index}/{len(input_files)}")
            with open(input_filepath, "r") as input_file:
                output_file.write(json.dumps({"text": input_file.read()}) + "\n")


if __name__ == "__main__":
    generate_data(diff=True)
