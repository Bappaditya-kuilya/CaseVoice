from __future__ import annotations

import json

from fastapi import WebSocket, WebSocketDisconnect

import database as db
from logger import get_logger
from voice_agent import VoiceAgent

logger = get_logger("websocket")


async def websocket_endpoint(ws: WebSocket) -> None:
    """Handle a voice call WebSocket connection."""
    await ws.accept()
    call_id = await db.create_call()
    agent = VoiceAgent(call_id)

    async def send_json(data: dict) -> None:
        await ws.send_text(json.dumps(data))

    async def send_binary(data: bytes) -> None:
        await ws.send_bytes(data)

    logger.info("WebSocket connected, call_id=%s", call_id)
    await send_json({"type": "status", "state": "listening"})

    try:
        while True:
            message = await ws.receive()

            if message["type"] == "websocket.disconnect":
                break

            # JSON control messages
            if "text" in message and message["text"]:
                try:
                    data = json.loads(message["text"])
                except json.JSONDecodeError:
                    await send_json({"type": "error", "message": "Invalid JSON"})
                    continue

                msg_type = data.get("type")

                if msg_type == "start":
                    await send_json({"type": "status", "state": "listening"})

                elif msg_type == "interrupt":
                    agent.interrupt()

                elif msg_type == "stop":
                    break

            # Binary audio frames
            if "bytes" in message and message["bytes"]:
                await agent.handle_audio_frame(message["bytes"], send_json, send_binary)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected, call_id=%s", call_id)
    except Exception as e:
        logger.error("WebSocket error for call %s: %s", call_id, e)
        try:
            await send_json({"type": "error", "message": str(e)})
        except Exception:
            pass
    finally:
        await db.end_call(call_id)
        logger.info("Call %s ended", call_id)
