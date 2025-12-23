from __future__ import annotations

from typing import Dict, Tuple

from agents import Agent

from startup_sim.config_schema import AgentType, Config, Member
from startup_sim.tools.registry import get_tools


def _compose_instructions(agent_type: AgentType, personality: str) -> str:
    return (
        f"{agent_type.prompt}\n\nSuccess:\n{agent_type.success}\n\nPersonality Overlay:\n{personality}"
    )


def build_agent(member: Member, agent_type: AgentType, tool_names: list[str]) -> Agent:
    tools = get_tools(tool_names)
    personality_lines = member.personality.formatted_lines() if member.personality else "- default: balanced"
    instructions = _compose_instructions(agent_type, personality_lines)
    agent = Agent(
        name=member.name,
        model=member.model or agent_type.default_model,
        instructions=instructions,
        tools=tools,
    )
    return agent


def build_team(config: Config, team_id: str = "seed_startup") -> Tuple[Agent, Dict[str, Agent]]:
    team = config.get_team(team_id)
    leader_agent: Agent | None = None
    others: Dict[str, Agent] = {}

    for member in team.members:
        agent_type = config.get_agent_type(member.type)
        agent = build_agent(member, agent_type, agent_type.tools)
        if agent_type.letter == "L" or member.type.lower() == "leader":
            if leader_agent is not None:
                raise ValueError("Only one leader allowed per team")
            leader_agent = agent
        else:
            others[agent.name] = agent

    if leader_agent is None:
        raise ValueError("Leader agent not found in team configuration")

    return leader_agent, others
