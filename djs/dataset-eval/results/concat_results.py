import os
from pprint import pprint


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def concat_files(outfile_name, infile_name_list):
    with open(outfile_name, "w") as outfile:
        for filename in infile_name_list:
            with open(get_relative_path(filename), "r") as infile:
                lines = infile.readlines()
                outfile.writelines(lines)


if __name__ == "__main__":
    local_dir = get_relative_path("")
    ((_, __, filenames),) = os.walk(local_dir)

    base_files = []
    finetune_files = []
    for filename in filenames:
        if not filename.endswith(".jsonl"):
            continue

        if filename.startswith("finetune"):
            finetune_files.append(filename)
        else:
            base_files.append(filename)

    base_files.sort(key=lambda x: int(x.split("-")[1]))
    finetune_files.sort(key=lambda x: int(x.split("-")[1]))

    concat_files(get_relative_path("_base.jsonl"), base_files)
    concat_files(get_relative_path("_finetune.jsonl"), finetune_files)
