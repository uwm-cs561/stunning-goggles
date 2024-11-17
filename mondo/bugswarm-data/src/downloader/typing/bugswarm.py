from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List
from datetime import datetime

@dataclass
class Entry(dict):
    _created: datetime
    _deleted: bool
    _etag: str
    _id: str
    _links: Links
    _updated: datetime
    added_version: str
    base_branch: str
    branch: str
    build_system: str
    cached: bool
    ci_service: str
    classification: Classification
    creation_time: float
    current_image_tag: str
    deprecated_version: None
    failed_job: FailedJobOrPassedJob
    filtered_reason: str
    image_tag: str
    is_error_pass: bool
    lang: str
    match: int
    merged_at: None
    metrics: Metrics
    passed_job: FailedJobOrPassedJob
    pr_num: int
    repo: str
    repo_builds: int
    repo_commits: int
    repo_members: int
    repo_mined_version: str
    repo_prs: int
    repo_watchers: int
    reproduce_attempts: int
    reproduce_successes: int
    reproduced: bool
    reproducibility_status: ReproducibilityStatus
    stability: str
    status: str
    test_framework: str

@dataclass
class Links:
    self: Self

@dataclass
class Self:
    href: str
    title: str

@dataclass
class Classification:
    build: str
    code: str
    exceptions: List[Any]
    test: str

@dataclass
class Metrics:
    additions: int
    changes: int
    deletions: int
    num_of_changed_files: int

@dataclass
class FailedJobOrPassedJob:
    base_sha: str
    build_id: int
    build_job: str
    committed_at: datetime
    config: Config
    failed_tests: str
    job_id: int
    message: str
    mismatch_attrs: List[Any]
    num_tests_failed: int
    num_tests_run: int
    patches: Patches
    trigger_sha: str

@dataclass
class Config:
    after_success: List[str]
    cache: Cache
    dist: str
    group: str
    install: bool
    jdk: str
    language: str
    os: str
    script: List[str]
    sudo: bool


@dataclass
class Cache:
    directories: List[str]

@dataclass
class Patches:
    casher: str
    # mvn-tls: str

@dataclass
class ReproducibilityStatus:
    status: str
    time_stamp: str
