import zipfile
import os
import json
from pprint import pprint

ZIP_FILE_PATH = '/u/d/j/djsmedema/public/stunning-goggles-data/data.zip'
LOCAL_PREFIX = "/shared/project/mondo/bugswarm-data/data/"


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


TRAINTEST_FILE_NAME = get_relative_path("train_test.json")


def get_test():
    with open(TRAINTEST_FILE_NAME, "r") as f:
        file_content = json.load(f)
    return [{**obj, "path": obj["path"].replace(LOCAL_PREFIX, "") } for obj in file_content["test"]]


def print_zip_file_tree(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        file_list = zip_file.namelist()
        dir_set = {f.split("/")[0] for f in file_list if "/" in f}
        for dir in dir_set:
            print(dir)

def load_zip_file(filepath: str):
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as z:
        with z.open(filepath, 'r') as f:
            return f.read().decode()
        
def get_ans(file_info):
    filepath = os.path.join(file_info["path"], file_info["ans"])
    return load_zip_file(filepath)


def get_ctx(file_info):
    filepath = os.path.join(file_info["path"], file_info["ctx"])
    return load_zip_file(filepath)

if __name__ == "__main__":
    print()
    test_split = get_test()
    print(get_ans(test_split[0]))
