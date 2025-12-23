import json
from types import SimpleNamespace

import pytest

from startup_sim import ui_logic


@pytest.mark.asyncio
async def test_end_to_end(monkeypatch):
    outputs = {
        "delegation": json.dumps(
            {
                "objective": "Build a hello-world feature",
                "assignments": [
                    {"assignee": "Priya", "task": "Write PRD", "expected_output": "PRD markdown"},
                    {"assignee": "Steve", "task": "Plan implementation", "expected_output": "Engineering plan"},
                ],
                "final_prompt": "Combine PRD and engineering plan",
            }
        ),
    }

    async def fake_run(agent, input_text):
        if agent.name == "Lucy" and "DELEGATION_PLAN" in input_text:
            return SimpleNamespace(final_output=outputs["delegation"])
        if agent.name == "Lucy" and "FINAL_SYNTHESIS" in input_text:
            return SimpleNamespace(final_output="PRD:\n ...\nENGINEERING:\n Done")
        if agent.name == "Priya":
            return SimpleNamespace(final_output="PRD: sample")
        if agent.name in {"Steve", "Sara"}:
            return SimpleNamespace(final_output="ENGINEERING: plan including github_create_pr and shell_run_safe")
        return SimpleNamespace(final_output="Unhandled")

    monkeypatch.setattr(ui_logic.orchestrator.Runner, "run", fake_run)

    output = await ui_logic.handle_message("Build a hello-world feature")

    assert "PRD:" in output
    assert "ENGINEERING:" in output
    assert "Lucy" in output or "Lucy" in outputs["delegation"]
    assert "Priya" in output or "Priya" in outputs["delegation"]
    assert "Steve" in output or "Steve" in outputs["delegation"]
