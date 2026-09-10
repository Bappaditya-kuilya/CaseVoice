# CaseVoice — Build Plan

## What

Voice-native legal client intake agent. Browser-based voice agent — no LiveKit, no Twilio, no phone infrastructure. Just browser mic → WebSocket → FastAPI backend → Groq STT/LLM → Rime TTS → audio back to browser. Real production project.

## Why

- 195M calls unanswered/year at US law firms, $109B lost revenue
- 67% of callers don't leave voicemail — they call the next firm
- Only 40% of firms answer phone calls
- Existing solutions are text chatbots — none are voice-native

---

## Goals

1. **Browser voice agent** — mic input → real-time conversation → speaker output, no plugins
2. **Legal citation pronunciation** — case numbers, statutes via Rime `spell()` + `phonemizeBetweenBrackets`
3. **Interruption recovery** — caller corrects mid-sentence, agent stops, updates
4. **Structured data extraction** — name, phone, incident, injuries, urgency from messy speech
5. **Consultation booking** — mock attorney calendar
6. **Dashboard** — live transcripts, case briefs
7. **Zero cost** — Rime free tier + Groq free tier
8. **Docker deployment** — one command

## Non-Goals

1. Phone/SIP telephony — browser-only for hackathon
2. Real database — SQLite
3. User auth — no login
4. Real calendar — mock
5. Multilingual — English only
6. Audio recording — live only
7. CI/CD — local Docker

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                     Browser                          │
│                                                      │
│  ┌─────────┐    ┌──────────┐    ┌─────────────────┐  │
│  │ Mic     │───▶│ AudioWork│───▶│ WebSocket       │  │
│  │ Capture │    │ let      │    │ (raw PCM 16kHz) │  │
│  └─────────┘    └──────────┘    └────────┬────────┘  │
│                                          │           │
│  ┌─────────┐    ┌──────────┐    ┌────────▼────────┐  │
│  │ Speaker │◀───│ Audio    │◀───│ WebSocket       │  │
│  │ Playback│    │ Worklet  │    │ (raw PCM 24kHz) │  │
│  └─────────┘    └──────────┘    └────────▲────────┘  │
│                                          │           │
│  ┌──────────────────────────────────────┐│           │
│  │ Dashboard (React)                    ││           │
│  │ - Live transcript                    ││           │
│  │ - Case data                          ││           │
│  │ - Call status                        ││           │
│  └──────────────────────────────────────┘│           │
└──────────────────────────────────────────┼───────────┘
                                           │
                                    WebSocket
                                           │
┌──────────────────────────────────────────▼───────────┐
│                FastAPI Backend                        │
│                                                      │
│  ┌─────────────────────────────────────────────────┐ │
│  │ WebSocket Handler                               │ │
│  │ - Receives PCM audio from browser               │ │
│  │ - Buffers until end-of-speech                   │ │
│  │ - Sends audio chunks back for playback          │ │
│  └───────┬─────────────────────────────┬───────────┘ │
│          │                             │             │
│  ┌───────▼──────────┐        ┌────────▼──────────┐  │
│  │ Groq Whisper STT │        │ Rime TTS          │  │
│  │ (free tier)      │        │ (free tier)       │  │
│  │ audio → text     │        │ text → audio      │  │
│  └───────┬──────────┘        └────────▲──────────┘  │
│          │                            │             │
│  ┌───────▼────────────────────────────▼───────────┐  │
│  │ Groq Llama 3.3 LLM                            │  │
│  │ (free tier)                                    │  │
│  │ transcript → response text + tool calls        │  │
│  │ streams tokens to Rime as generated            │  │
│  └───────┬────────────────────────────┬───────────┘  │
│          │                            │             │
│  ┌───────▼──────────┐        ┌───────▼──────────┐   │
│  │ Tool Router      │        │ Rime Mist v2     │   │
│  │ - extract_case() │        │ (pronunciation)  │   │
│  │ - book_consult() │        │ case numbers,    │   │
│  │ - read_citation()│        │ statutes         │   │
│  └───────┬──────────┘        └──────────────────┘   │
│          │                                          │
│  ┌───────▼──────────────────────────────────────┐   │
│  │ SQLite Database                               │   │
│  │ - calls, cases, transcripts                   │   │
│  └───────────────────────────────────────────────┘  │
│                                                      │
│  ┌───────────────────────────────────────────────┐   │
│  │ REST API                                      │   │
│  │ GET /api/calls, GET /api/cases, etc.          │   │
│  └───────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

### Audio Pipeline

```
Browser mic (48kHz stereo)
    │ AudioWorklet: downsample to 16kHz mono PCM
    ▼
WebSocket (binary frames, 16kHz PCM)
    │ Backend buffers PCM chunks
    ▼
Groq Whisper STT → transcript
    │
    ▼
Groq Llama 3.3 → response text (streaming tokens)
    │
    ├─ If legal citation detected → Rime Mist v2 (pronunciation)
    │   ▼
    │   WebSocket binary frames (24kHz PCM) → Browser AudioWorklet → Speaker
    │
    └─ If normal conversation → Rime Coda (streaming)
        ▼
        WebSocket binary frames (24kHz PCM) → Browser AudioWorklet → Speaker
```

### Dual-Model TTS

| Situation | Model | Why |
|---|---|---|
| General conversation | **Coda** | Best quality, sub-100ms TTFA, word timestamps |
| Legal citations, case numbers | **Mist v2** | Only model with `phonemizeBetweenBrackets` |

Both via Rime direct API. Switch detected by LLM tool call.

---

## Zero-Cost Stack

| Component | Choice | Free tier |
|---|---|---|
| **TTS** | Rime (direct API) | 3,000 min on signup, no CC |
| **STT** | Groq Whisper (direct API) | 20 RPM, 2K RPD, no CC |
| **LLM** | Groq Llama 3.3 (direct API) | 30 RPM, 8K TPM, no CC |
| **Backend** | FastAPI + Python | Open source |
| **Frontend** | React + Vite | Open source |
| **Database** | SQLite | Open source |
| **Docker** | docker-compose | Open source |

**Cost: $0.00**

---

## File Structure

```
casevoice/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entrypoint (REST + WebSocket)
│   ├── websocket_handler.py    # WebSocket audio processing
│   ├── voice_agent.py          # Voice pipeline orchestration
│   ├── stt.py                  # Groq Whisper adapter
│   ├── llm.py                  # Groq Llama 3.3 adapter (streaming)
│   ├── tts.py                  # Rime TTS adapter (Coda + Mist v2)
│   ├── pronunciation.py        # Legal citation pronunciation
│   ├── tools.py                # LLM tool functions
│   ├── prompts.py              # System prompts
│   ├── database.py             # SQLite
│   ├── schemas.py              # Pydantic models
│   ├── config.py               # Env-based settings
│   ├── calendar_mock.py        # Mock calendar
│   ├── logger.py               # Structured logging
│   ├── health.py               # Health endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── audio/
│   │   │   ├── capture.ts      # Mic → PCM 16kHz via AudioWorklet
│   │   │   ├── playback.ts     # PCM 24kHz → Speaker via AudioWorklet
│   │   │   └── worklets/
│   │   │       ├── capture-processor.js   # AudioWorklet: downsample mono
│   │   │       └── playback-processor.js  # AudioWorklet: buffer + play
│   │   ├── ws/
│   │   │   └── client.ts       # WebSocket client (binary + JSON)
│   │   ├── api.ts              # REST API client
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── LiveCall.tsx
│   │   │   └── CaseDetail.tsx
│   │   └── components/
│   │       ├── CallCard.tsx
│   │       ├── IntakeBrief.tsx
│   │       ├── Transcript.tsx
│   │       └── StatusBar.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── index.html
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
├── README.md
└── RIME_EVIDENCE.md
```

---

## Implementation Order (8 hours)

### Phase 1: Audio Pipeline (hours 0-3)

**Exit criteria:** Browser mic → WebSocket → Groq STT → Groq LLM → Rime TTS → browser speaker. Full loop.

| Step | What | Time |
|------|------|------|
| 1.1 | Sign up: Rime + Groq (get API keys) | 10min |
| 1.2 | Project scaffold + FastAPI with WebSocket endpoint | 20min |
| 1.3 | Browser AudioWorklet: mic → 16kHz PCM → WebSocket | 30min |
| 1.4 | Backend: receive PCM → Groq Whisper STT → transcript | 30min |
| 1.5 | Backend: Groq Llama 3.3 → streaming response | 20min |
| 1.6 | Backend: Rime Coda TTS → stream audio back via WebSocket | 30min |
| 1.7 | Browser: receive PCM → AudioWorklet → speaker playback | 20min |
| 1.8 | Full loop test | 10min |

### Phase 2: Legal Intake + Pronunciation (hours 3-5)

**Exit criteria:** Agent collects data, handles interruptions, reads legal citations.

| Step | What | Time |
|------|------|------|
| 2.1 | System prompt with intake flow | 20min |
| 2.2 | Tool: extract_case_data (Pydantic + SQLite) | 30min |
| 2.3 | Tool: book_consultation (mock calendar) | 20min |
| 2.4 | Interruption handling (stop TTS on new speech) | 30min |
| 2.5 | Dual-model: Mist v2 for legal citations | 30min |
| 2.6 | Pronunciation fixtures | 15min |
| 2.7 | Test 5 scenarios | 15min |

### Phase 3: Dashboard + Backend (hours 5-7)

**Exit criteria:** Attorneys see live transcripts and case data.

| Step | What | Time |
|------|------|------|
| 3.1 | REST API endpoints (calls, cases, transcripts) | 30min |
| 3.2 | WebSocket: stream transcript events to dashboard | 20min |
| 3.3 | React scaffold + routing | 20min |
| 3.4 | Dashboard page: calls + cases | 30min |
| 3.5 | LiveCall page: real-time transcript | 30min |
| 3.6 | CaseDetail page: intake brief | 30min |

### Phase 4: Evidence + Docker + Polish (hours 7-8)

| Step | What | Time |
|------|------|------|
| 4.1 | RIME_EVIDENCE.md | 20min |
| 4.2 | Latency measurement | 10min |
| 4.3 | Docker setup | 15min |
| 4.4 | README | 10min |
| 4.5 | Demo rehearsal | 5min |

---

## WebSocket Protocol

### Browser → Backend

| Type | Format | When |
|---|---|---|
| `audio` | Binary (16kHz mono PCM, 16-bit) | Continuous while mic is on |
| `start` | JSON `{"type": "start"}` | Begin new call |
| `stop` | JSON `{"type": "stop"}` | End call |
| `interrupt` | JSON `{"type": "interrupt"}` | User interrupts agent |

### Backend → Browser

| Type | Format | When |
|---|---|---|
| `audio` | Binary (24kHz mono PCM, 16-bit) | Agent speech chunks |
| `transcript` | JSON `{"role": "user"|"agent", "text": "..."}` | Each utterance |
| `tool_call` | JSON `{"tool": "...", "result": "..."}` | Tool execution |
| `status` | JSON `{"state": "listening"|"thinking"|"speaking"}` | State changes |
| `done` | JSON `{"type": "done"}` | Agent finished speaking |

---

## Demo Script (5 minutes)

**0:00-0:30** — Problem
"195 million calls go unanswered at law firms every year. $109 billion lost."

**0:30-1:30** — Live call: Normal intake
Caller describes car accident. Agent extracts facts, asks questions, books consultation.

**1:30-2:30** — Stress case: Interruption
Caller corrects date mid-sentence. Agent stops, updates, confirms.

**2:30-3:30** — Pronunciation demo
Agent reads back: "Your case number is 2024-CV-08472, filed under Section 4.2(a)(iii) of the UCC."

**3:30-4:30** — Dashboard reveal
Attorney sees structured brief: date, location, injuries, urgency, booked consultation.

**4:30-5:00** — Numbers
"35% of calls go unanswered. This answers 100%. Cost: two cents. 24/7."

---

## RIME_EVIDENCE.md

```markdown
# RIME_EVIDENCE.md

## Hard Voice Claim
Legal citation pronunciation is load-bearing for trust.
Rime's `spell()` and `phonemizeBetweenBrackets` on Mist v2 solve this.
No other TTS provider offers inline pronunciation control.

## Acceptance Test

### Fixture 1: Case number
- Input: "2024-CV-08472"
- Expected: "twenty twenty-four C V zero eight four seven two"
- Model: Mist v2 + spell()

### Fixture 2: Legal statute
- Input: "Section 4.2(a)(iii) of the UCC"
- Expected: "Section four point two a three of the U C C"
- Model: Mist v2 + phonemizeBetweenBrackets

### Fixture 3: Address
- Input: "I-95 near exit 42"
- Expected: "Interstate ninety five, near exit forty two"
- Model: Coda

### Fixture 4: General conversation
- Input: "How are you doing today?"
- Expected: Natural response
- Model: Coda

### Fixture 5: Interruption
- Input: "My case number is 2024-CV—" → correction "wait, it's 2024-CV-09183"
- Expected: Stop, acknowledge, read new number correctly

## Results
[Fill after implementation]

## Limitations
- Mist v2 phonemizeBetweenBrackets: English only
- Coda cannot use phonemizeBetweenBrackets
- Dual-model switch adds ~50ms
```

---

## PRD Alignment

| PRD Requirement | Coverage |
|---|---|
| **Problem & necessity of voice (25%)** | ✅ $109B market, voice IS the channel |
| **Hard voice engineering (25%)** | ✅ Legal pronunciation (Mist v2), interruption (word timestamps), chaotic extraction |
| **Rime integration (20%)** | ✅ Dual-model Coda + Mist v2, `spell()` + `phonemizeBetweenBrackets` load-bearing |
| **Evidence & reproducibility (20%)** | ✅ RIME_EVIDENCE.md with 5 fixtures |
| **Demo clarity (10%)** | ✅ 5-min script |
| **Rime as primary spoken output** | ✅ All speech through Rime |
| **Configuration hygiene** | ✅ .env.example, no secrets |

---

## Risks

| Risk | Mitigation |
|---|---|
| Groq rate limit | Cache responses, batch where possible |
| Rime free tier exhausted | Direct API has 3,000 min — enough for hackathon |
| Browser audio issues | Test Chrome/Edge, fallback to Text-to-Speech API |
| WebSocket disconnects | Auto-reconnect, resume state |
