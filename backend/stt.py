import httpx

from config import settings
from logger import get_logger

logger = get_logger("stt")

GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


async def transcribe(audio_bytes: bytes) -> str:
    """Send raw PCM audio (16kHz mono 16-bit) to Groq Whisper and return transcript."""
    if not audio_bytes:
        return ""

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Wrap raw PCM in a WAV header so Groq can parse it
        wav = _pcm_to_wav(audio_bytes, sample_rate=16000, channels=1, sample_width=2)
        files = {"file": ("audio.wav", wav, "audio/wav")}
        data = {"model": "whisper-large-v3-turbo", "response_format": "text"}

        resp = await client.post(
            GROQ_STT_URL,
            headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}"},
            files=files,
            data=data,
        )
        resp.raise_for_status()
        text = resp.text.strip()
        logger.info("STT result: %s", text[:120])
        return text


def _pcm_to_wav(pcm: bytes, sample_rate: int, channels: int, sample_width: int) -> bytes:
    """Wrap raw PCM bytes in a WAV header."""
    import struct

    data_size = len(pcm)
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        36 + data_size,
        b"WAVE",
        b"fmt ",
        16,
        1,  # PCM format
        channels,
        sample_rate,
        sample_rate * channels * sample_width,
        channels * sample_width,
        sample_width * 8,
        b"data",
        data_size,
    )
    return header + pcm
