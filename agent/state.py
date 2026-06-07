# agent/state.py

from typing import TypedDict, Optional


class PRState(TypedDict):
    # PR metadata
    pr_number:          int
    repo_full_name:     str
    pr_title:           str
    pr_author:          str
    base_branch:        str
    head_branch:        str
    pr_description:     str

    # Collected data  ← review.py must read from these, not "file_contents"
    changed_files:      list    # list of file path strings
    git_diff:           str     # unified diff string
    file_contents:      dict    # path -> file content string (optional helper)

    # Review results
    black_issues:       list
    ruff_issues:        list
    bandit_issues:      list
    llm_review_issues:  list
    security_issues:    list

    # Auto-fix
    autofix_applied:    bool
    autofix_log:        list

    # Tests
    generated_tests:    str
    pytest_output:      str
    pytest_passed:      bool
    pytest_retry_count: int

    # Docs
    docs_generated:     str

    # Report
    review_report:      str
    severity_counts:    dict
    confidence_score:   float

    # Decision
    approval_status:    Optional[str]
    block_reason:       Optional[str]
    should_block:       bool
    retry_count:        int