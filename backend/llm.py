from collections.abc import AsyncIterator

import httpx

from config import settings
from logger import get_logger

logger = get_logger("llm")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


async def chat_stream(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> AsyncIterator[str]:
    """Stream LLM response chunks. Returns text tokens via SSE."""
    body: dict = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "temperature": 0.4,
        "max_tokens": 1024,
    }
    if tools:
        body["tools"] = tools

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", GROQ_CHAT_URL, json=body, headers=headers) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if not line.startswith("data: "):
                    continue
                payload = line[len("data: "):]
                if payload.strip() == "[DONE]":
                    break
                import json
                chunk = json.loads(payload)
                delta = chunk["choices"][0].get("delta", {})
                if "content" in delta and delta["content"]:
                    yield delta["content"]


async def chat_once(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    """Non-streaming chat that returns the full response (text or tool_call)."""
    body: dict = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "temperature": 0.4,
        "max_tokens": 1024,
    }
    if tools:
        body["tools"] = tools

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            GROQ_CHAT_URL,
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json=body,
        )
        resp.raise_for_status()
        choice = resp.json()["choices"][0]
        msg = choice["message"]

        if msg.get("tool_calls"):
            tc = msg["tool_calls"][0]
            import json as _json
            return {
                "type": "tool_call",
                "tool": tc["function"]["name"],
                "arguments": _json.loads(tc["function"]["arguments"]),
            }
        return {"type": "text", "content": msg.get("content", "")}
