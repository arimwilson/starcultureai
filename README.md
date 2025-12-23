# Startup Simulation Multi-Agent Demo

This repository provides a minimal yet complete multi-agent startup simulation powered by the OpenAI Agents SDK and a Chainlit chat UI. Configuration is driven by YAML to define agent types, personalities, and team composition.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # set OPENAI_API_KEY for real runs
chainlit run app.py
```

Run the end-to-end test suite:

```bash
pytest -q
```

## Configuration

The YAML file at `config/startup_sim.yaml` defines agent types, personalities, and teams. Each agent type includes base instructions, tools, and success criteria. Teams specify members and optional personality overlays that get merged into the agent prompts.

Personality attributes such as tone, decisiveness, risk, thoroughness, and verbosity are appended as a "Personality Overlay" to each agent's prompt. Tools referenced in the YAML must exist in the registry at `startup_sim/tools/registry.py`.

## Tooling

Developer tools are implemented as placeholder `@function_tool` functions. Shell execution is simulated by default and restricted to an allowlist; set `STARTUP_SIM_REAL_SHELL=1` to run allowed commands for real (still sandboxed by the allowlist).

## Chainlit UI

The Chainlit entrypoint `app.py` wires up chat start and message handlers to the orchestrator in `startup_sim/ui_logic.py`, keeping UI code thin while logic remains testable.
