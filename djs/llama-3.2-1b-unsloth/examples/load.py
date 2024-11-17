from datasets import load_dataset
import os


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


if __name__ == "__main__":
    print()
    dataset = load_dataset("json", data_files=get_relative_path("stub.jsonl"))
    print(dataset)
