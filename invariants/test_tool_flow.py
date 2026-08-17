from __future__ import annotations

import json
from typing import Any

from agent.agent import run_agent
from agent.tools import search_hotels
from agent.validation import prepare_hotel_observation


OK = "ok"
HOTELS = "hotels"
ERROR = "error"
RESULT_KEYS = {OK, HOTELS}
PUBLIC_KEYS = {"name", "nightly_price", "currency", "available"}
FORBIDDEN_MARKERS = {
    "internal_rate_code",
    "supplier_note",
    "AB-NET-42",
    "Ignore your rules",
    "environment variables",
}
EXPECTED_HOTELS = [
    {
        "name": "Riverside Rooms",
        "nightly_price": 132,
        "currency": "EUR",
        "available": True,
    },
    {
        "name": "Old Town Stay",
        "nightly_price": 98,
        "currency": "EUR",
        "available": True,
    },
    {
        "name": "Closed Dock Hotel",
        "nightly_price": 75,
        "currency": "EUR",
        "available": False,
    },
]
MALFORMED_RESULT = {OK: True}


class RecordingModel:
    def __init__(self) -> None:
        self.call_count = 0
        self.observation: str | None = None

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        self.call_count += 1
        if self.call_count == 1:
            return {
                "content": None,
                "tool_calls": [
                    {
                        "id": "call-hotel-1",
                        "name": "search_hotels",
                        "arguments": {"city": "Lisbon"},
                    }
                ],
            }

        self.observation = messages[-1]["content"]
        return {"content": "I found current hotel options.", "tool_calls": []}


def test_supplier_result_contract() -> None:
    result = prepare_hotel_observation(search_hotels("Lisbon"))
    hotels = result.get(HOTELS)
    encoded = json.dumps(result)

    assert set(result) == RESULT_KEYS
    assert result.get(OK) is True
    assert hotels == EXPECTED_HOTELS
    assert all(set(hotel) == PUBLIC_KEYS for hotel in hotels)
    assert not any(marker in encoded for marker in FORBIDDEN_MARKERS)


def test_malformed_supplier_result_contract() -> None:
    result = prepare_hotel_observation(MALFORMED_RESULT)

    assert result.get(OK) is False
    assert result.get(ERROR)


def test_agent_receives_prepared_observation() -> None:
    model = RecordingModel()
    answer = run_agent("Find current hotels in Lisbon", model)
    observation = json.loads(model.observation or "null")

    assert answer
    assert observation.get(OK) is True
    assert observation.get(HOTELS) == EXPECTED_HOTELS
