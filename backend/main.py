from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

import database as db
from health import health_check
from logger import get_logger
from schemas import CallRecord, CaseRecord, HealthResponse, TranscriptRecord
from websocket_handler import websocket_endpoint

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    logger.info("CaseVoice backend started")
    yield
    await db.close_db()
    logger.info("CaseVoice backend stopped")


app = FastAPI(title="CaseVoice", lifespan=lifespan)

allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── WebSocket ──────────────────────────────────────────────────────────
@app.websocket("/ws/call")
async def ws_call(ws: WebSocket):
    await websocket_endpoint(ws)


# ── REST endpoints ─────────────────────────────────────────────────────
@app.get("/health", response_model=HealthResponse)
async def health():
    return await health_check()


@app.get("/api/calls", response_model=list[CallRecord])
async def list_calls():
    return await db.get_calls()


@app.get("/api/cases", response_model=list[CaseRecord])
async def list_cases():
    return await db.get_cases()


@app.get("/api/cases/{case_id}", response_model=CaseRecord)
async def get_case(case_id: str):
    case = await db.get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/api/calls/{call_id}/transcripts", response_model=list[TranscriptRecord])
async def list_transcripts(call_id: str):
    return await db.get_call_transcripts(call_id)
