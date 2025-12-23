from __future__ import annotations

import json
from typing import Any

from agents import function_tool


@function_tool
def github_get_pr(pr_number: int) -> str:
    return json.dumps({
        "number": pr_number,
        "title": f"Placeholder PR #{pr_number}",
        "url": f"https://example.com/pr/{pr_number}",
        "status": "open",
    })


@function_tool
def github_create_pr(title: str, body: str, branch: str = "feature/demo") -> str:
    return json.dumps({
        "title": title,
        "body": body,
        "branch": branch,
        "url": f"https://example.com/{branch}",
        "number": 123,
    })


@function_tool
def github_review_pr(pr_number: int, event: str, body: str) -> str:
    return json.dumps({
        "number": pr_number,
        "event": event,
        "comment": body,
        "status": "recorded",
    })
