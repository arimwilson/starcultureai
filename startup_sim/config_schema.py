from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, field_validator, model_validator


class AgentType(BaseModel):
    letter: str
    names: List[str]
    default_model: str
    tools: List[str]
    prompt: str
    success: str

    @field_validator("letter")
    @classmethod
    def validate_letter(cls, value: str) -> str:
        if len(value) != 1 or not value.isupper():
            raise ValueError("letter must be a single uppercase character")
        return value


class Personality(BaseModel):
    tone: Optional[str] = None
    decisiveness: Optional[str] = None
    risk: Optional[str] = None
    thoroughness: Optional[str] = None
    verbosity: Optional[str] = None

    def formatted_lines(self) -> str:
        entries = {
            "tone": self.tone,
            "decisiveness": self.decisiveness,
            "risk": self.risk,
            "thoroughness": self.thoroughness,
            "verbosity": self.verbosity,
        }
        return "\n".join(f"- {key}: {value}" for key, value in entries.items() if value)


class Member(BaseModel):
    type: str
    name: str
    model: Optional[str] = None
    personality: Optional[Personality] = None


class Team(BaseModel):
    description: str
    members: List[Member]

    @model_validator(mode="after")
    def ensure_unique_names(self) -> "Team":
        names = [m.name for m in self.members]
        if len(names) != len(set(names)):
            raise ValueError("Team member names must be unique")
        return self


class Config(BaseModel):
    agent_types: Dict[str, AgentType]
    teams: Dict[str, Team]

    def get_agent_type(self, name: str) -> AgentType:
        if name not in self.agent_types:
            raise KeyError(f"Unknown agent type: {name}")
        return self.agent_types[name]

    def get_team(self, team_id: str) -> Team:
        if team_id not in self.teams:
            raise KeyError(f"Unknown team id: {team_id}")
        return self.teams[team_id]
