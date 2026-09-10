from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class CallRecord(BaseModel):
    id: str
    started_at: str
    ended_at: Optional[str] = None
    status: str = "active"


class CaseRecord(BaseModel):
    id: str
    call_id: str
    caller_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    incident_type: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    description: Optional[str] = None
    injuries: list[str] = []
    urgency: str = "low"
    consultation_booked: bool = False
    consultation_date: Optional[str] = None
    created_at: str


class TranscriptRecord(BaseModel):
    id: str
    call_id: str
    role: str
    text: str
    timestamp: str


class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "casevoice-backend"
