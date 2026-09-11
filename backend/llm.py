import json

import httpx

from config import settings
from logger import get_logger

logger = get_logger("llm")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"


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
            return {
                "type": "tool_call",
                "tool": tc["function"]["name"],
                "arguments": json.loads(tc["function"]["arguments"]),
            }
        return {"type": "text", "content": msg.get("content", "")}
