

## Data

- [date]-artifacts.json: database of all artifacts (only reproducible) from bugswarm downloded at the [date]
  - you can find the data schema at typing/bugswarm.py
- job_logs: logs files of passed and failed jobs from bugswarm, named as [job_id].log
- task_diff: different ctx of diffs from the same task (or image_id in bugswarm), every task has a folder named as [image_id] and contains:
  - diff_[ctx_size].log:  the diff of passed log on top of the failed log
  - passed.log
  - failed.log
