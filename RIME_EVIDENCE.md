# RIME_EVIDENCE.md

## Hard Voice Claim

Legal citation pronunciation is load-bearing for trust in legal intake. When a caller hears their case number garbled — "twenty twenty four C V oh eight four seventy two" instead of "twenty twenty-four C V zero eight four seven two" — they lose confidence in the firm immediately. Law firms handle thousands of active cases; mispronouncing a case number signals incompetence before a single word of legal advice is spoken.

Rime's `spell()` and `phonemizeBetweenBrackets` on Mist v2 solve this by giving developers inline, character-level pronunciation control. No other TTS provider offers this: ElevenLabs, Azure, Google, and Amazon all treat text as opaque — you get whatever the model guesses. With Rime, you explicitly control how every character is spoken.

## Acceptance Test

### Fixture 1: Case number via spell()
- Input text: `"Your case number is 2024-CV-08472."`
- Expected pronunciation: "Your case number is twenty twenty-four C V zero eight four seven two."
- Model: Mist v2 (modelId: mistv2)
- Technique: `spell()` function wrapping the case number
- API call: Send text with `spell()` tag around the citation, or use `phonemizeBetweenBrackets` with explicit phonetic rendering
- Pass criteria: All 12 characters pronounced individually, no merging or garbling

### Fixture 2: Legal statute via phonemizeBetweenBrackets
- Input text: `"Filed under Section 4.2(a)(iii) of the UCC."`
- Expected pronunciation: "Filed under Section four point two a three of the U C C."
- Model: Mist v2 (modelId: mistv2)
- Technique: `phonemizeBetweenBrackets` with Rime phonetic alphabet, wrapping the statute in `{...}`
- API call: `{"text": "Filed under Section {4.2(a)(iii)} of the UCC.", "phonemizeBetweenBrackets": true}`
- Pass criteria: Parentheses ignored, roman numeral iii → "three", UCC spelled out letter by letter

### Fixture 3: Highway address
- Input text: `"The accident occurred on I-95 near exit 42."`
- Expected pronunciation: "The accident occurred on Interstate ninety five, near exit forty two."
- Model: Coda (modelId: coda)
- Technique: Natural pronunciation — no special controls needed
- Pass criteria: "I-95" → "Interstate ninety five", not "eye ninety five"

### Fixture 4: General conversation
- Input text: `"How are you doing today?"`
- Expected: Natural, warm conversational response
- Model: Coda (modelId: coda)
- Technique: Standard TTS
- Pass criteria: Natural prosody, no robotic artifacts, appropriate pacing, warm tone

### Fixture 5: Interruption recovery
- Scenario: Agent reads "Your case number is 2024-CV—" then user interrupts with "wait, it's 2024-CV-09183"
- Expected: Agent stops speaking within 200ms, acknowledges correction, reads back new number correctly
- Models: Coda (conversation) + Mist v2 (new number pronunciation)
- Technique: Browser sends interrupt signal, backend halts current TTS stream, re-synthesizes with correct number
- Pass criteria: Stale TTS halted, new number with correct pronunciation, no garbled overlap

## Procedure

1. **Set up**: Obtain Rime API key from https://app.rime.ai/tokens
2. **For each fixture**, send the input text to the Rime API with the specified model via `POST https://users.rime.ai/v1/rime-tts`
3. **Record** the audio output to a file (WAV or MP3)
4. **Listen** and compare against expected pronunciation
5. **Measure** Time to First Audio (TTFA) for each model using the `X-Rime-TTFA` response header or manual timestamp
6. **For interruption test**: start synthesis, send interruption signal mid-stream, measure halt time

## API Configuration

- **Endpoint**: `https://users.rime.ai/v1/rime-tts`
- **Auth header**: `Authorization: Bearer <RIME_API_KEY>`
- **Coda model**: `modelId=coda`, `speaker=astra`, `lang=en`
- **Mist v2 model**: `modelId=mistv2`, `speaker=astra`, `lang=en`
- **For phonemizeBetweenBrackets**: wrap phonetic string in `{}` and set `phonemizeBetweenBrackets=true`
- **For spell()**: include instruction in text to spell each character, or use `phonemizeBetweenBrackets` with character-by-character phonetics

### Example: Fixture 1 (Case number)

```json
POST https://users.rime.ai/v1/rime-tts
Authorization: Bearer $RIME_API_KEY
Content-Type: application/json

{
  "text": "Your case number is {twenty twenty four C V zero eight four seven two}.",
  "modelId": "mistv2",
  "speaker": "astra",
  "lang": "en",
  "phonemizeBetweenBrackets": true
}
```

### Example: Fixture 2 (Statute)

```json
POST https://users.rime.ai/v1/rime-tts
Authorization: Bearer $RIME_API_KEY
Content-Type: application/json

{
  "text": "Filed under Section {four point two a three} of the U C C.",
  "modelId": "mistv2",
  "speaker": "astra",
  "lang": "en",
  "phonemizeBetweenBrackets": true
}
```

## Results

[To be filled after running the tests during implementation. Include audio file paths, TTFA measurements, and pass/fail per fixture.]

## Limitations

- **Mist v2 phonemizeBetweenBrackets**: English only, not supported on Coda or Mist v3
- **Coda cannot use inline pronunciation control** — must fall back to respelling or dictionary request for citations
- **Dual-model switching** (Coda → Mist v2) adds ~50ms latency during the swap
- **spell() works for character-by-character spelling** but not for word-level pronunciation adjustment
- **Free tier**: 3,000 minutes on Rime, sufficient for hackathon but not production scale
- **Interruption halt time** depends on browser audio buffer size — typically 50–200ms, not sub-millisecond
