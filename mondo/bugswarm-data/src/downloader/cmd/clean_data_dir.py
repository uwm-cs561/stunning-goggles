
import os


def delete_empty_dirs(path):
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        if not dirnames and not filenames:
            print(f"Removing empty dir: {dirpath}")
            os.rmdir(dirpath)

def main():
  delete_empty_dirs('data/task_diff')

if __name__ == '__main__':
  main()