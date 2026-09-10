import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getCase, getCallTranscripts } from "../api.ts";
import type { Case, Transcript } from "../api.ts";
import IntakeBrief from "../components/IntakeBrief.tsx";
import TranscriptDisplay from "../components/Transcript.tsx";

export default function CaseDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [caseData, setCaseData] = useState<Case | null>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getCase(id)
      .then((c) => {
        setCaseData(c);
        return getCallTranscripts(c.call_id);
      })
      .then(setTranscripts)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="loading">Loading...</div>;
  if (!caseData) return <div className="error-state">Case not found.</div>;

  return (
    <div className="case-detail">
      <button className="btn btn-ghost" onClick={() => navigate("/")}>
        ← Back to Dashboard
      </button>

      <IntakeBrief data={caseData} />

      <section className="case-transcript-section">
        <h2>Call Transcript</h2>
        {transcripts.length === 0 ? (
          <p className="empty-state">No transcripts available.</p>
        ) : (
          <TranscriptDisplay
            lines={transcripts.map((t) => ({
              role: t.role,
              text: t.text,
              timestamp: t.timestamp,
            }))}
          />
        )}
      </section>
    </div>
  );
}
