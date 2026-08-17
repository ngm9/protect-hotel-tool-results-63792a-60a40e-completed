from __future__ import annotations

import json
from typing import Any, Protocol

from openai import OpenAI

from agent.config import AgentConfig


class ModelClient(Protocol):
    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Return assistant content and any requested tool calls."""


class OpenAIModelClient:
    """Real OpenAI-compatible model client used by the production agent path."""

    def __init__(self, config: AgentConfig) -> None:
        self._model = config.model
        self._client = OpenAI(api_key=config.api_key, base_url=config.base_url)

    def complete(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
        }
        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

        response = self._client.chat.completions.create(**request)
        message = response.choices[0].message
        tool_calls: list[dict[str, Any]] = []

        for call in message.tool_calls or []:
            try:
                arguments = json.loads(call.function.arguments)
            except (json.JSONDecodeError, TypeError):
                arguments = None
            tool_calls.append(
                {
                    "id": call.id,
                    "name": call.function.name,
                    "arguments": arguments,
                }
            )

        return {
            "content": message.content,
            "tool_calls": tool_calls,
        }

    def ping(self) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": "Reply with OK."}],
            max_tokens=5,
        )
        return response.choices[0].message.content or ""
