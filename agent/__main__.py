from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.agent import run_agent
from agent.config import load_config
from agent.llm_client import OpenAIModelClient
from agent.tools import HOTEL_SEARCH_TOOL


BASE_DIR = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BASE_DIR / "fixtures" / "sample_requests.json"


def run_selfcheck() -> int:
    config = load_config()

    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)

    requests = fixture.get("requests")
    supplier_response = fixture.get("supplier_response")
    function = HOTEL_SEARCH_TOOL.get("function", {})

    if not isinstance(requests, list) or not requests:
        print("selfcheck failed: sample requests are missing")
        return 2
    if not isinstance(supplier_response, dict):
        print("selfcheck failed: supplier response is missing")
        return 2
    if function.get("name") != "search_hotels":
        print("selfcheck failed: hotel tool registration is invalid")
        return 2
    if function.get("parameters", {}).get("type") != "object":
        print("selfcheck failed: hotel tool schema is invalid")
        return 2

    print(f"selfcheck: loaded {len(requests)} sample requests")
    print(f"selfcheck: configured model is {config.model}")

    if config.api_key:
        try:
            reply = OpenAIModelClient(config).ping()
        except Exception as exc:
            print(f"selfcheck failed: provider ping failed: {exc}")
            return 2
        print(f"selfcheck: provider replied with {reply!r}")
    else:
        print("selfcheck: no provider key found, skipping provider ping")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local hotel search agent")
    parser.add_argument("message", nargs="*", help="Travel question for the agent")
    parser.add_argument("--selfcheck", action="store_true")
    args = parser.parse_args()

    if args.selfcheck:
        return run_selfcheck()

    question = " ".join(args.message).strip()
    if not question:
        parser.error("provide a travel question or use --selfcheck")

    config = load_config()
    if not config.api_key:
        print("OPENAI_API_KEY is missing. Add it to .env in the project root for an end-to-end run.")
        return 2

    model = OpenAIModelClient(config)
    print(run_agent(question, model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
