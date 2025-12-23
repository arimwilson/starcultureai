from __future__ import annotations

import yaml
from pathlib import Path
from typing import Optional

from startup_sim.config_schema import Config


def load_config(path: Optional[str] = None) -> Config:
    config_path = Path(path or "config/startup_sim.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    data = yaml.safe_load(config_path.read_text())
    return Config.model_validate(data)
