from __future__ import annotations

from startup_sim.agent_factory import build_team
from startup_sim.loader import load_config
from startup_sim import orchestrator


async def handle_message(user_text: str, team_id: str = "seed_startup") -> str:
    config = load_config()
    leader, others = build_team(config, team_id)
    final_output, _ = await orchestrator.orchestrate(leader, others, user_text)
    return final_output
