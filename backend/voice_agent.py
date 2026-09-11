from __future__ import annotations

import asyncio
import json
import time
import uuid
from collections.abc import AsyncIterator

import database as db
from llm import chat_once
from logger import get_logger
from pronunciation import has_legal_citations, wrap_legal_citations
from prompts import SYSTEM_PROMPT
from stt import transcribe
from tools import TOOL_DEFINITIONS, execute_tool
from tts import synthesize_coda, synthesize_mist

logger = get_logger("voice_agent")

# VAD: silence threshold in seconds
_SILENCE_THRESHOLD_S = 0.5
# Max buffer: 30 seconds of audio
_MAX_BUFFER_BYTES = 16000 * 2 * 30


class VoiceAgent:
    def __init__(self, call_id: str) -> None:
        self.call_id = call_id
        self.messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.state: str = "listening"
        self._audio_buffer = bytearray()
        self._last_voice_time: float = 0.0
        self._speaking = False
        self._interrupt_event = asyncio.Event()

    async def handle_audio_frame(self, pcm_bytes: bytes, send_json, send_binary) -> None:
        """Process incoming PCM frame: buffer, detect speech end, run pipeline."""
        if self._speaking:
            return

        # Enforce buffer limit
        if len(self._audio_buffer) + len(pcm_bytes) > _MAX_BUFFER_BYTES:
            logger.warning("Audio buffer overflow for call %s, discarding", self.call_id)
            self._audio_buffer.clear()
            return

        # Check if frame has actual audio (non-zero samples)
        import array
        samples = array.array("h", pcm_bytes)
        has_voice = any(abs(s) > 500 for s in samples[:len(samples)//2])

        if has_voice:
            self._last_voice_time = time.monotonic()

        self._audio_buffer.extend(pcm_bytes)

        # Process when we have enough audio AND silence detected
        if len(self._audio_buffer) >= 3200:
            elapsed = time.monotonic() - self._last_voice_time
            if elapsed >= _SILENCE_THRESHOLD_S:
                await self._process_speech(send_json, send_binary)

    async def _process_speech(self, send_json, send_binary) -> None:
        """Run the full STT → LLM → TTS pipeline."""
        audio = bytes(self._audio_buffer)
        self._audio_buffer.clear()

        if len(audio) < 1600:  # less than 50ms — skip
            return

        # 1. STT
        await self._set_state("thinking", send_json)
        try:
            transcript = await transcribe(audio)
        except Exception as e:
            logger.error("STT failed: %s", e)
            await send_json({"type": "error", "message": f"STT failed: {e}"})
            await self._set_state("listening", send_json)
            return

        if not transcript.strip():
            await self._set_state("listening", send_json)
            return

        # 2. Add to history
        self.messages.append({"role": "user", "content": transcript})
        await db.add_transcript(self.call_id, "user", transcript)
        await send_json({"type": "transcript", "role": "user", "text": transcript})

        # 3. LLM loop (may call tools multiple times)
        await self._run_llm_loop(send_json, send_binary)

        # 4. Back to listening
        await self._set_state("listening", send_json)

    async def _run_llm_loop(self, send_json, send_binary) -> None:
        """LLM with tool-calling loop."""
        max_iterations = 5
        for _ in range(max_iterations):
            self._interrupt_event.clear()

            result = await chat_once(self.messages, tools=TOOL_DEFINITIONS)

            if result["type"] == "tool_call":
                tool_name = result["tool"]
                tool_args = result["arguments"]
                call_id = f"call_{uuid.uuid4().hex[:12]}"

                # Record tool call in messages
                self.messages.append({
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [{
                        "id": call_id,
                        "type": "function",
                        "function": {"name": tool_name, "arguments": json.dumps(tool_args)},
                    }],
                })

                # Execute
                output = await execute_tool(self.call_id, tool_name, tool_args)
                await send_json({"type": "tool_call", "tool": tool_name, "result": output})

                self.messages.append({
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": output,
                })
                continue

            # Text response — stream TTS
            text = result["content"]
            self.messages.append({"role": "assistant", "content": text})
            await db.add_transcript(self.call_id, "agent", text)
            await send_json({"type": "transcript", "role": "agent", "text": text})

            await self._stream_tts(text, send_json, send_binary)
            return

    async def _stream_tts(self, text: str, send_json, send_binary) -> None:
        """Stream TTS audio back to client."""
        await self._set_state("speaking", send_json)
        self._speaking = True
        self._interrupt_event.clear()

        tts_text = wrap_legal_citations(text) if has_legal_citations(text) else text
        tts_fn = synthesize_mist if has_legal_citations(text) else synthesize_coda

        try:
            async for chunk in tts_fn(tts_text):
                if self._interrupt_event.is_set():
                    logger.info("TTS interrupted for call %s", self.call_id)
                    break
                await send_binary(chunk)
        except Exception as e:
            logger.error("TTS failed: %s", e)
            await send_json({"type": "error", "message": f"TTS failed: {e}"})
        finally:
            self._speaking = False
            await send_json({"type": "done"})

    def interrupt(self) -> None:
        """Handle user interrupt — stop TTS."""
        self._interrupt_event.set()
        self._audio_buffer.clear()

    async def _set_state(self, state: str, send_json) -> None:
        if self.state != state:
            self.state = state
            await send_json({"type": "status", "state": state})
