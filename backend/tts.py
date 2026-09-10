from collections.abc import AsyncIterator

import httpx

from config import settings
from logger import get_logger

logger = get_logger("tts")

RIME_TTS_URL = "https://users.rime.ai/v1/rime-tts"


async def synthesize_coda(text: str) -> AsyncIterator[bytes]:
    """Synthesize speech using Coda (general conversation). Yields raw PCM chunks (24kHz mono 16-bit)."""
    body = {
        "modelId": "coda",
        "speaker": "astra",
        "lang": "en",
        "text": text,
    }
    headers = {
        "Authorization": f"Bearer {settings.RIME_API_KEY}",
        "Accept": "audio/pcm",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream("POST", RIME_TTS_URL, json=body, headers=headers) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes(chunk_size=960):
                if chunk:
                    yield chunk


async def synthesize_mist(text: str) -> AsyncIterator[bytes]:
    """Synthesize speech using Mist v2 (pronunciation for legal terms). Yields raw PCM chunks."""
    body = {
        "modelId": "mistv2",
        "speaker": "astra",
        "lang": "en",
        "text": text,
        "phonemizeBetweenBrackets": True,
    }
    headers = {
        "Authorization": f"Bearer {settings.RIME_API_KEY}",
        "Accept": "audio/pcm",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        async with client.stream("POST", RIME_TTS_URL, json=body, headers=headers) as resp:
            resp.raise_for_status()
            async for chunk in resp.aiter_bytes(chunk_size=960):
                if chunk:
                    yield chunk
