import type { Case } from "../api";

interface IntakeBriefProps {
  data: Case;
}

const urgencyColors: Record<string, string> = {
  low: "#4ade80",
  medium: "#facc15",
  high: "#FF8A3D",
  urgent: "#E85D5D",
};

export default function IntakeBrief({ data }: IntakeBriefProps) {
  let injuries: string[] = [];
  if (data.injuries) {
    try {
      injuries = typeof data.injuries === "string" ? JSON.parse(data.injuries) : data.injuries;
    } catch {
      injuries = [];
    }
  }

  return (
    <div className="intake-brief">
      <div className="intake-header">
        <h2>{data.caller_name || "Unknown Caller"}</h2>
        <span
          className="urgency-badge"
          style={{ backgroundColor: urgencyColors[data.urgency] || "#666" }}
        >
          {data.urgency}
        </span>
      </div>

      <div className="intake-grid">
        <div className="intake-field">
          <label>Phone</label>
          <span>{data.phone || "—"}</span>
        </div>
        <div className="intake-field">
          <label>Email</label>
          <span>{data.email || "—"}</span>
        </div>
        <div className="intake-field">
          <label>Incident Type</label>
          <span>{data.incident_type || "—"}</span>
        </div>
        <div className="intake-field">
          <label>Incident Date</label>
          <span>{data.incident_date || "—"}</span>
        </div>
        <div className="intake-field">
          <label>Location</label>
          <span>{data.incident_location || "—"}</span>
        </div>
        <div className="intake-field">
          <label>Created</label>
          <span>{new Date(data.created_at).toLocaleString()}</span>
        </div>
      </div>

      {data.description && (
        <div className="intake-section">
          <label>Description</label>
          <p>{data.description}</p>
        </div>
      )}

      {injuries.length > 0 && (
        <div className="intake-section">
          <label>Injuries</label>
          <ul className="injury-list">
            {injuries.map((inj: string, i: number) => (
              <li key={i}>{inj}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="intake-section">
        <label>Consultation</label>
        <p>
          {data.consultation_booked
            ? `Booked${data.consultation_date ? ` for ${new Date(data.consultation_date).toLocaleDateString()}` : ""}`
            : "Not booked"}
        </p>
      </div>
    </div>
  );
}
