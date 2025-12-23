from __future__ import annotations

from typing import Callable, Dict, List

from startup_sim.tools.github_tools import github_create_pr, github_get_pr, github_review_pr
from startup_sim.tools.pm_tools import (
    assign_work,
    clarify_requirements,
    prioritize,
    review_work,
    team_status,
    write_prd,
)
from startup_sim.tools.shell_tools import shell_run_safe

TOOL_REGISTRY: Dict[str, Callable] = {
    "github_get_pr": github_get_pr,
    "github_create_pr": github_create_pr,
    "github_review_pr": github_review_pr,
    "shell_run_safe": shell_run_safe,
    "write_prd": write_prd,
    "clarify_requirements": clarify_requirements,
    "prioritize": prioritize,
    "team_status": team_status,
    "assign_work": assign_work,
    "review_work": review_work,
}


def get_tools(tool_names: List[str]) -> List[Callable]:
    tools = []
    for name in tool_names:
        if name not in TOOL_REGISTRY:
            raise ValueError(f"Tool '{name}' not found in registry")
        tools.append(TOOL_REGISTRY[name])
    return tools
