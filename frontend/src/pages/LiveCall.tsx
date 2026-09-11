import { useEffect, useRef, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { VoiceClient } from "../ws/client.ts";
import { AudioCapture } from "../audio/capture.ts";
import { AudioPlayback } from "../audio/playback.ts";
import Transcript from "../components/Transcript.tsx";
import StatusBar from "../components/StatusBar.tsx";

interface TranscriptLine {
  role: "user" | "agent";
  text: string;
  timestamp: string;
}

export default function LiveCall() {
  const navigate = useNavigate();
  const [active, setActive] = useState(false);
  const [agentState, setAgentState] = useState("listening");
  const [transcript, setTranscript] = useState<TranscriptLine[]>([]);
  const [error, setError] = useState("");
  const [reconnecting, setReconnecting] = useState(false);

  const clientRef = useRef<VoiceClient | null>(null);
  const captureRef = useRef<AudioCapture | null>(null);
  const playbackRef = useRef<AudioPlayback | null>(null);
  const transcriptEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    transcriptEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [transcript]);

  const addLine = useCallback((role: "user" | "agent", text: string) => {
    setTranscript((prev) => [
      ...prev,
      { role, text, timestamp: new Date().toISOString() },
    ]);
  }, []);

  const startCall = useCallback(async () => {
    setError("");
    setTranscript([]);
    setAgentState("listening");

    const playback = new AudioPlayback();
    playbackRef.current = playback;
    await playback.start();

    const client = new VoiceClient({
      onTranscript: (role, text) => addLine(role, text),
      onStatus: (state) => setAgentState(state),
      onToolCall: (_tool, result) => addLine("agent", `[System] ${result}`),
      onDone: () => setAgentState("listening"),
      onError: (msg) => setError(msg),
      onAudio: (pcm) => playback.pushPCM(pcm),
      onReconnecting: () => setReconnecting(true),
    });
    clientRef.current = client;
    client.start();
    setReconnecting(false);

    const capture = new AudioCapture((pcm) => client.sendAudio(pcm));
    captureRef.current = capture;
    await capture.start();

    setActive(true);
  }, [addLine]);

  const stopCall = useCallback(() => {
    captureRef.current?.stop();
    clientRef.current?.stop();
    playbackRef.current?.stop();
    captureRef.current = null;
    clientRef.current = null;
    playbackRef.current = null;
    setActive(false);
    navigate("/");
  }, [navigate]);

  const sendInterrupt = useCallback(() => {
    clientRef.current?.interrupt();
  }, []);

  useEffect(() => {
    return () => {
      captureRef.current?.stop();
      clientRef.current?.stop();
      playbackRef.current?.stop();
    };
  }, []);

  return (
    <div className="live-call">
      <div className="live-call-controls">
        <div className="call-control-panel">
          <h2>Call Controls</h2>
          <StatusBar state={agentState} />

          {error && <div className="call-error">{error}</div>}

          <div className="call-buttons">
            {!active ? (
              <button className="btn btn-primary btn-large" onClick={startCall}>
                Start Call
              </button>
            ) : (
              <>
                <button
                  className="btn btn-secondary"
                  onClick={sendInterrupt}
                >
                  Interrupt
                </button>
                <button className="btn btn-danger" onClick={stopCall}>
                  End Call
                </button>
              </>
            )}
          </div>

          <div className="call-info">
            <p>
              {active
                ? "Call in progress. Speak naturally."
                : 'Press "Start Call" to begin.'}
            </p>
          </div>
        </div>
      </div>

      <div className="live-call-transcript">
        <Transcript lines={transcript} />
        <div ref={transcriptEndRef} />
      </div>
    </div>
  );
}
