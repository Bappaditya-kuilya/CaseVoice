import json
import uuid
from datetime import datetime, timezone

import aiosqlite

from config import settings
from logger import get_logger

logger = get_logger("database")

_db: aiosqlite.Connection | None = None

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS calls (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS cases (
    id TEXT PRIMARY KEY,
    call_id TEXT REFERENCES calls(id),
    caller_name TEXT,
    phone TEXT,
    email TEXT,
    incident_type TEXT,
    incident_date TEXT,
    incident_location TEXT,
    description TEXT,
    injuries TEXT,
    urgency TEXT DEFAULT 'low',
    consultation_booked INTEGER DEFAULT 0,
    consultation_date TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transcripts (
    id TEXT PRIMARY KEY,
    call_id TEXT REFERENCES calls(id),
    role TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
"""


async def init_db() -> None:
    global _db
    _db = await aiosqlite.connect(settings.DATABASE_PATH)
    _db.row_factory = aiosqlite.Row
    await _db.executescript(CREATE_TABLES_SQL)
    await _db.commit()
    logger.info("Database initialized at %s", settings.DATABASE_PATH)


async def close_db() -> None:
    global _db
    if _db:
        await _db.close()
        _db = None


def _get_db() -> aiosqlite.Connection:
    assert _db is not None, "Database not initialised. Call init_db() first."
    return _db


async def create_call() -> str:
    call_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    db = _get_db()
    await db.execute("INSERT INTO calls (id, started_at, status) VALUES (?, ?, 'active')", (call_id, now))
    await db.commit()
    logger.info("Created call %s", call_id)
    return call_id


async def end_call(call_id: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    db = _get_db()
    await db.execute("UPDATE calls SET ended_at = ?, status = 'completed' WHERE id = ?", (now, call_id))
    await db.commit()
    logger.info("Ended call %s", call_id)


async def create_case(call_id: str, data: dict) -> str:
    case_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    injuries = json.dumps(data.get("injuries", []))
    db = _get_db()
    await db.execute(
        """INSERT INTO cases
           (id, call_id, caller_name, phone, email, incident_type,
            incident_date, incident_location, description, injuries,
            urgency, consultation_booked, consultation_date, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            case_id,
            call_id,
            data.get("caller_name"),
            data.get("phone"),
            data.get("email"),
            data.get("incident_type"),
            data.get("incident_date"),
            data.get("incident_location"),
            data.get("description"),
            injuries,
            data.get("urgency", "low"),
            1 if data.get("consultation_booked") else 0,
            data.get("consultation_date"),
            now,
        ),
    )
    await db.commit()
    logger.info("Created case %s for call %s", case_id, call_id)
    return case_id


async def update_case(case_id: str, data: dict) -> None:
    db = _get_db()
    fields: list[str] = []
    values: list = []
    for key in (
        "caller_name", "phone", "email", "incident_type", "incident_date",
        "incident_location", "description", "urgency", "consultation_booked",
        "consultation_date",
    ):
        if key in data:
            val = data[key]
            if key == "injuries":
                val = json.dumps(val) if isinstance(val, list) else val
            if key == "consultation_booked":
                val = 1 if val else 0
            fields.append(f"{key} = ?")
            values.append(val)
    if "injuries" in data:
        fields.append("injuries = ?")
        values.append(json.dumps(data["injuries"]) if isinstance(data["injuries"], list) else data["injuries"])
    if not fields:
        return
    values.append(case_id)
    await db.execute(f"UPDATE cases SET {', '.join(fields)} WHERE id = ?", values)
    await db.commit()


async def get_case_for_call(call_id: str) -> dict | None:
    db = _get_db()
    cursor = await db.execute("SELECT * FROM cases WHERE call_id = ? LIMIT 1", (call_id,))
    row = await cursor.fetchone()
    if row is None:
        return None
    return dict(row)


async def get_calls() -> list[dict]:
    db = _get_db()
    cursor = await db.execute("SELECT * FROM calls ORDER BY started_at DESC")
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]


async def get_cases() -> list[dict]:
    db = _get_db()
    cursor = await db.execute("SELECT * FROM cases ORDER BY created_at DESC")
    rows = await cursor.fetchall()
    return [_parse_case(r) for r in rows]


async def get_case(case_id: str) -> dict | None:
    db = _get_db()
    cursor = await db.execute("SELECT * FROM cases WHERE id = ?", (case_id,))
    row = await cursor.fetchone()
    if row is None:
        return None
    return _parse_case(row)


async def get_call_transcripts(call_id: str) -> list[dict]:
    db = _get_db()
    cursor = await db.execute(
        "SELECT * FROM transcripts WHERE call_id = ? ORDER BY timestamp ASC", (call_id,)
    )
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]


async def add_transcript(call_id: str, role: str, text: str) -> None:
    tid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    db = _get_db()
    await db.execute(
        "INSERT INTO transcripts (id, call_id, role, text, timestamp) VALUES (?, ?, ?, ?, ?)",
        (tid, call_id, role, text, now),
    )
    await db.commit()


def _parse_case(row: aiosqlite.Row) -> dict:
    d = dict(row)
    d["injuries"] = json.loads(d["injuries"]) if d.get("injuries") else []
    d["consultation_booked"] = bool(d.get("consultation_booked", 0))
    return d
