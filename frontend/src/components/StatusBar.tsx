interface StatusBarProps {
  state: string;
}

const labels: Record<string, string> = {
  listening: "Listening",
  thinking: "Thinking",
  speaking: "Speaking",
};

export default function StatusBar({ state }: StatusBarProps) {
  const dotClass = `status-dot status-${state}`;
  return (
    <div className="status-bar">
      <span className={dotClass} />
      <span className="status-label">{labels[state] || state}</span>
    </div>
  );
}
