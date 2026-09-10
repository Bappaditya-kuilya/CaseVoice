# CaseVoice

Voice-native legal client intake agent. Browser mic → real-time conversation → structured case data. 195M calls go unanswered at US law firms every year, costing $109B. CaseVoice answers every call, 24/7, for pennies.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       Browser                           │
│  Mic ──▶ AudioWorklet ──▶ WebSocket (16kHz PCM)        │
│  Speaker ◀── AudioWorklet ◀── WebSocket (24kHz PCM)    │
│  Dashboard (React): transcript, case data, call status  │
└────────────────────────┬────────────────────────────────┘
                         │ WebSocket
┌────────────────────────▼────────────────────────────────┐
│                  FastAPI Backend                         │
│                                                         │
│  WebSocket Handler                                      │
│    ├── Groq Whisper STT (free)   → transcript           │
│    ├── Groq Llama 3.3 LLM (free)→ response text        │
│    ├── Rime Coda TTS (free)      → general speech       │
│    ├── Rime Mist v2 TTS (free)   → legal citations      │
│    ├── Tool Router               → extract, book, read  │
│    └── SQLite                    → cases, calls, logs   │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology | Free Tier |
|-----------|-----------|-----------|
| TTS | Rime (Coda + Mist v2) | 3,000 min |
| STT | Groq Whisper | 20 RPM |
| LLM | Groq Llama 3.3 | 30 RPM |
| Backend | Python 3.12 + FastAPI | — |
| Frontend | React + TypeScript + Vite | — |
| Database | SQLite | — |
| Deploy | Docker Compose | — |

**Total cost: $0.00**

## Prerequisites

- Python 3.12+
- Node.js 20+
- Docker + Docker Compose (optional)
- Rime API key ([sign up](https://app.rime.ai/tokens))
- Groq API key ([sign up](https://console.groq.com/keys))

## Quick Start

```bash
# 1. Clone
git clone https://github.com/your-org/casevoice.git
cd casevoice

# 2. Configure
cp .env.example .env
# Edit .env — add your RIME_API_KEY and GROQ_API_KEY

# 3. Run (pick one)
# Option A: Docker
docker-compose up

# Option B: Manual
cd backend && pip install -r requirements.txt && uvicorn main:app --port 8000 &
cd frontend && npm install && npm run dev
```

**Docker**: open http://localhost:3000
**Manual**: open http://localhost:5173

## How to Use

1. Click **Start Call**
2. Speak — describe your legal situation (car accident, injury, dispute, etc.)
3. The agent asks follow-up questions, extracts case data, and books a consultation
4. Watch the live transcript and structured case brief update in real time
5. Try interrupting mid-sentence — the agent stops, listens, and adapts

## Rime Integration

CaseVoice uses two Rime models, switching dynamically per utterance:

| Model | Use Case | Key Feature |
|-------|----------|-------------|
| **Coda** | General conversation | Fast TTFA, natural prosody, word timestamps |
| **Mist v2** | Legal citations, case numbers | `phonemizeBetweenBrackets` for precise pronunciation |

**Pronunciation examples:**
- Case number `2024-CV-08472` → "twenty twenty-four C V zero eight four seven two"
- Statute `Section 4.2(a)(iii)` → "Section four point two a three"
- Highway `I-95` → "Interstate ninety five"

Both models use the `astra` speaker with English language setting.

**Endpoint:** `https://users.rime.ai/v1/rime-tts`

## Known Limitations

- Browser-only — no phone/SIP telephony (hackathon scope)
- English only
- SQLite only — no production database
- Mock calendar — no real attorney scheduling
- Rime free tier: 3,000 minutes (sufficient for hackathon)
- Groq rate limits: 20 RPM STT, 30 RPM LLM (sufficient for demo)
- No authentication or user accounts

## License

MIT — see [LICENSE](LICENSE).
