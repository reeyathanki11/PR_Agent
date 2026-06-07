from typing import TypedDict, List


class PRState(TypedDict):
    pr_number: int

    changed_files: List[str]

    file_contents: str

    review_report: str