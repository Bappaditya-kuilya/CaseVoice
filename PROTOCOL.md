# WebSocket Protocol Contract

Both backend and frontend agents MUST implement this exact protocol.

## Connection

```
ws://localhost:8000/ws/call
```

## Browser → Backend (JSON messages)

### Start a call
```json
{"type": "start"}
```

### Audio chunk (binary)
Raw PCM: 16kHz, mono, 16-bit signed LE.
Each binary frame = ~20ms of audio (640 bytes = 320 samples × 2 bytes).

### Interrupt agent
```json
{"type": "interrupt"}
```

### Stop call
```json
{"type": "stop"}
```

## Backend → Browser (JSON messages)

### Agent state change
```json
{"type": "status", "state": "listening|thinking|speaking"}
```

### Transcript
```json
{"type": "transcript", "role": "user|agent", "text": "the text"}
```

### Tool call result
```json
{"type": "tool_call", "tool": "extract_case_data|book_consultation|read_legal_citation", "result": "..."}
```

### Agent done speaking
```json
{"type": "done"}
```

### Error
```json
{"type": "error", "message": "description"}
```

### Audio chunk (binary)
Raw PCM: 24kHz, mono, 16-bit signed LE.
Each binary frame = ~20ms of audio (960 bytes = 480 samples × 2 bytes).

## REST API Endpoints

### GET /api/calls
```json
[
  {
    "id": "uuid",
    "started_at": "ISO8601",
    "ended_at": "ISO8601|null",
    "status": "active|completed"
  }
]
```

### GET /api/cases
```json
[
  {
    "id": "uuid",
    "call_id": "uuid",
    "caller_name": "string",
    "incident_type": "string",
    "incident_date": "string",
    "incident_location": "string",
    "injuries": ["string"],
    "urgency": "low|medium|high|urgent",
    "consultation_booked": true,
    "created_at": "ISO8601"
  }
]
```

### GET /api/cases/{id}
Full case object with all fields.

### GET /api/calls/{id}/transcripts
```json
[
  {
    "id": "uuid",
    "role": "user|agent",
    "text": "string",
    "timestamp": "ISO8601"
  }
]
```

## Database Schema (SQLite)

```sql
CREATE TABLE calls (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    status TEXT DEFAULT 'active'
);

CREATE TABLE cases (
    id TEXT PRIMARY KEY,
    call_id TEXT REFERENCES calls(id),
    caller_name TEXT,
    phone TEXT,
    email TEXT,
    incident_type TEXT,
    incident_date TEXT,
    incident_location TEXT,
    description TEXT,
    injuries TEXT,  -- JSON array
    urgency TEXT DEFAULT 'low',
    consultation_booked INTEGER DEFAULT 0,
    consultation_date TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE transcripts (
    id TEXT PRIMARY KEY,
    call_id TEXT REFERENCES calls(id),
    role TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
```

## Config (.env.example)

```
RIME_API_KEY=your_rime_key
GROQ_API_KEY=your_groq_key
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DATABASE_PATH=./casevoice.db
```
