# Downloader
DATA_DIR = "data"
ARTIFACTS_JSON_PATH = f"{DATA_DIR}/2024-11-17-02-09-45-artifacts.json"
LOG_DIR = f"{DATA_DIR}/job_logs"
DIFF_DIR = f"{DATA_DIR}/task_diff"

PASSED_LOG_NAME = "passed.log"
FAILED_LOG_NAME = "failed.log"
DIFF_PREFIX = "diff_"
DIFF_NO_CTX_NAME = "diff_no_ctx.log"

BUGSWARM_TOKEN = "OlDzyq3bGuOFodk3l8PLyM6a0a337asUpITo2LMIj2c"
BUGSWARM_QPM = 100

# Merger
MERGED_DIR = f"{DATA_DIR}/merged_job_logs"
LOG_FILTERED_DIR = f"{DATA_DIR}/filtered_job_logs"
DIFF_HUNK_FILTERED_DIR = f"{DATA_DIR}/diff_hunk_filtered"
