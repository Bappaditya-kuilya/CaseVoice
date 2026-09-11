import type { Call } from "../api";

interface CallCardProps {
  call: Call;
  onClick?: () => void;
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString();
}

function formatDuration(start: string, end: string | null): string {
  const ms = (end ? new Date(end) : new Date()).getTime() - new Date(start).getTime();
  const secs = Math.max(0, Math.floor(ms / 1000));
  const m = Math.floor(secs / 60);
  const s = secs % 60;
  return `${m}m ${s}s`;
}

export default function CallCard({ call, onClick }: CallCardProps) {
  return (
    <div className="call-card" onClick={onClick}>
      <div className="call-card-header">
        <span className={`badge badge-${call.status}`}>{call.status}</span>
        <span className="call-card-date">{formatDate(call.started_at)}</span>
      </div>
      <div className="call-card-duration">
        {formatDuration(call.started_at, call.ended_at)}
      </div>
    </div>
  );
}
