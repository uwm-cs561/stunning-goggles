from datetime import datetime
import json
import os
from typing import Generator
from downloader.vendor.bugswarm_database_api import DatabaseAPI
from ratelimit import limits, sleep_and_retry


bugswarmapi = DatabaseAPI()


@sleep_and_retry
@limits(calls=6, period=60)
def list_artifacts_limited(
    iter: Generator[tuple[list, Exception | None], None, tuple[None, None]]
):
    return next(iter)


def list_artifacts():
    iter = bugswarmapi.list_artifacts_gen()
    while True:
        yield list_artifacts_limited(iter)


def main():
    print("Start Downloading")
    dir_name = f"data"
    os.makedirs(dir_name, exist_ok=True)
    out_name = f"{dir_name}/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-artifacts.json"

    with open(out_name, "w") as f:
        all = []
        page_num = 1
        try:
            for i, res in enumerate(list_artifacts()):
                print(f"page: {page_num}, res: {res}")
                page, err = res
                if err:
                    print(f"Error: {err}, continue")
                    continue
                page_num += 1
                print(f"Downloaded {len(page)} artifacts")
                all += page
                open(out_name, "w").write(json.dumps(all, indent=2))
        except Exception as e:
            print("Error:", e)
            pass

        print(f"Downloaded {len(all)} artifacts in total")
        open(out_name, "w").write(json.dumps(all, indent=2))


if __name__ == "__main__":
    main()
