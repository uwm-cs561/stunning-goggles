from datetime import datetime
import json
from downloader.vendor.bugswarm_database_api import DatabaseAPI


def main():
  print("Start Downloading")
  bugswarmapi = DatabaseAPI()
  res = bugswarmapi.list_artifacts()

  print(res)

  out_name = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}-artifacts.json"
  open(out_name, "w").write(json.dumps(res, indent=2))



if __name__ == "__main__":
  main()