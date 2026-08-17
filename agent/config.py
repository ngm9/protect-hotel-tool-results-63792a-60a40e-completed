from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = BASE_DIR / ".env"


@dataclass(frozen=True)
class AgentConfig:
    api_key: str
    base_url: str
    model: str


def load_config() -> AgentConfig:
    load_dotenv(ENV_PATH)
    return AgentConfig(
        api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").strip(),
        model=os.getenv("AGENT_MODEL", "gpt-4o-mini").strip(),
    )
