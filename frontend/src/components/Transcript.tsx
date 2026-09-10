interface TranscriptLine {
  role: "user" | "agent";
  text: string;
  timestamp: string;
}

interface TranscriptProps {
  lines: TranscriptLine[];
}

export default function Transcript({ lines }: TranscriptProps) {
  return (
    <div className="transcript">
      <h3 className="transcript-title">Live Transcript</h3>
      <div className="transcript-body">
        {lines.length === 0 && (
          <p className="transcript-empty">
            No messages yet. Start a call to begin.
          </p>
        )}
        {lines.map((line, i) => (
          <div
            key={i}
            className={`transcript-line transcript-${line.role}`}
          >
            <div className="transcript-role">
              {line.role === "agent" ? "Agent" : "Caller"}
            </div>
            <div className="transcript-bubble">{line.text}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
