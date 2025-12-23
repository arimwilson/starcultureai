from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

from agents import Agent, Runner

DelegationPlan = Dict[str, Any]
AssignmentOutput = Dict[str, str]
RunRecord = Dict[str, Any]


async def _run_agent(agent: Agent, prompt: str) -> str:
    result = await Runner.run(agent, prompt)
    return getattr(result, "final_output", "")


def _default_plan(user_text: str, team_members: List[str]) -> DelegationPlan:
    pm = next((name for name in team_members if name.lower().startswith("p")), "Priya")
    swe = next((name for name in team_members if name.lower().startswith("s")), "Steve")
    return {
        "objective": user_text,
        "assignments": [
            {"assignee": pm, "task": "Draft a concise PRD", "expected_output": "PRD markdown"},
            {"assignee": swe, "task": "Propose implementation steps", "expected_output": "Engineering plan"},
        ],
        "final_prompt": "Summarize user objective with PRD and engineering plan",
    }


def _parse_plan(plan_text: str, user_text: str, team_members: List[str]) -> DelegationPlan:
    try:
        plan = json.loads(plan_text)
        if not isinstance(plan, dict):
            raise ValueError
        return plan
    except Exception:
        return _default_plan(user_text, team_members)


async def orchestrate(
    leader: Agent,
    others: Dict[str, Agent],
    user_text: str,
) -> Tuple[str, RunRecord]:
    roster = ", ".join(others.keys())
    planning_prompt = (
        "You are the leader. Return a JSON delegation plan with keys 'objective', 'assignments', and 'final_prompt'.\n"
        "Assignments must include assignee, task, expected_output.\n"
        f"Team: {roster}\n"
        "Tag your output with DELEGATION_PLAN for tracing."
    )
    leader_plan_text = await _run_agent(leader, f"DELEGATION_PLAN\nUser: {user_text}\n{planning_prompt}")
    plan = _parse_plan(leader_plan_text, user_text, list(others.keys()))

    assignment_results: List[AssignmentOutput] = []
    for assignment in plan.get("assignments", []):
        assignee = assignment.get("assignee")
        task = assignment.get("task", "")
        if assignee not in others:
            continue
        output = await _run_agent(others[assignee], task)
        assignment_results.append({"assignee": assignee, "output": output})

    synthesis_prompt_lines = [
        "FINAL_SYNTHESIS",
        f"User request: {user_text}",
        "Assignment outputs:",
    ]
    for result in assignment_results:
        synthesis_prompt_lines.append(f"- {result['assignee']}: {result['output']}")
    synthesis_prompt_lines.append(f"Final instructions: {plan.get('final_prompt', '')}")
    synthesis_prompt = "\n".join(synthesis_prompt_lines)
    final_output = await _run_agent(leader, synthesis_prompt)

    team_line = f"Team: {leader.name}, " + ", ".join(others.keys())
    combined_output = f"{final_output}\n\n{team_line}"

    run_record: RunRecord = {
        "plan": plan,
        "assignments": assignment_results,
        "final_output": combined_output,
    }
    return combined_output, run_record
