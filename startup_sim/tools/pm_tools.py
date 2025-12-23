from __future__ import annotations

import json
from typing import List

from agents import function_tool


@function_tool
def write_prd(title: str, goals: List[str], non_goals: List[str], acceptance_criteria: List[str]) -> str:
    prd = [
        f"# PRD: {title}",
        "## Goals",
        "\n".join(f"- {g}" for g in goals),
        "## Non-Goals",
        "\n".join(f"- {ng}" for ng in non_goals),
        "## Acceptance Criteria",
        "\n".join(f"- {ac}" for ac in acceptance_criteria),
    ]
    return "\n".join(prd)


@function_tool
def clarify_requirements(question: str) -> str:
    return f"Consideration: {question}\nFollow up with stakeholders for clarity."


@function_tool
def prioritize(items: List[str]) -> List[str]:
    return sorted(items, key=lambda x: x.lower())


# Leader-side utilities


def _team_registry() -> List[str]:
    # Placeholder; real implementation would inspect runtime state
    return ["Lucy", "Priya", "Steve", "Sara"]


@function_tool
def team_status() -> str:
    return "Active team members: " + ", ".join(_team_registry())


@function_tool
def assign_work(assignee: str, task: str) -> str:
    return json.dumps({"assignee": assignee, "task": task, "status": "assigned"})


@function_tool
def review_work(artifact: str, rubric: List[str]) -> str:
    notes = "\n".join(f"- {criterion}: looks good" for criterion in rubric)
    return f"Reviewing {artifact}:\n{notes}"
