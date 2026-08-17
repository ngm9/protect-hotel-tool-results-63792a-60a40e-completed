from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parents[1]
FIXTURE_PATH = BASE_DIR / "fixtures" / "sample_requests.json"

HOTEL_SEARCH_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "search_hotels",
        "description": (
            "Read current hotel prices and availability for one city. "
            "Use this read-only tool only when current hotel facts are needed."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to search",
                    "minLength": 1,
                    "maxLength": 80,
                }
            },
            "required": ["city"],
            "additionalProperties": False,
        },
    },
}


def search_hotels(city: str) -> dict[str, Any]:
    """Read a realistic supplier response from the local travel fixture."""
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        fixture = json.load(fixture_file)

    response = copy.deepcopy(fixture["supplier_response"])
    response["query_city"] = city
    return response
