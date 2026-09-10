import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getCalls, getCases } from "../api.ts";
import type { Call, Case } from "../api.ts";
import CallCard from "../components/CallCard.tsx";

export default function Dashboard() {
  const [calls, setCalls] = useState<Call[]>([]);
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([getCalls(), getCases()])
      .then(([c, cs]) => {
        setCalls(c);
        setCases(cs);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <button className="btn btn-primary" onClick={() => navigate("/call")}>
          + New Call
        </button>
      </div>

      <section className="dashboard-section">
        <h2>Recent Calls</h2>
        {calls.length === 0 ? (
          <p className="empty-state">No calls yet.</p>
        ) : (
          <div className="card-grid">
            {calls.map((call) => (
              <CallCard key={call.id} call={call} />
            ))}
          </div>
        )}
      </section>

      <section className="dashboard-section">
        <h2>Cases</h2>
        {cases.length === 0 ? (
          <p className="empty-state">No cases yet.</p>
        ) : (
          <div className="case-list">
            {cases.map((c) => (
              <div
                key={c.id}
                className="case-row"
                onClick={() => navigate(`/case/${c.id}`)}
              >
                <div className="case-row-main">
                  <span className="case-name">{c.caller_name || "Unknown"}</span>
                  <span className="case-type">{c.incident_type || "—"}</span>
                </div>
                <div className="case-row-meta">
                  <span
                    className={`urgency-badge urgency-${c.urgency}`}
                  >
                    {c.urgency}
                  </span>
                  <span className="case-date">
                    {new Date(c.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
