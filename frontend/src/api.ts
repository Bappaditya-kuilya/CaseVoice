export interface Call {
  id: string;
  started_at: string;
  ended_at: string | null;
  status: "active" | "completed";
}

export interface Case {
  id: string;
  call_id: string;
  caller_name: string;
  phone: string;
  email: string;
  incident_type: string;
  incident_date: string;
  incident_location: string;
  description: string;
  injuries: string[];
  urgency: "low" | "medium" | "high" | "urgent";
  consultation_booked: boolean;
  consultation_date: string;
  created_at: string;
}

export interface Transcript {
  id: string;
  call_id: string;
  role: "user" | "agent";
  text: string;
  timestamp: string;
}

const BASE = import.meta.env.VITE_API_URL || "/api";

async function fetchJSON<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export function getCalls(): Promise<Call[]> {
  return fetchJSON<Call[]>("/calls");
}

export function getCases(): Promise<Case[]> {
  return fetchJSON<Case[]>("/cases");
}

export function getCase(id: string): Promise<Case> {
  return fetchJSON<Case>(`/cases/${id}`);
}

export function getCallTranscripts(callId: string): Promise<Transcript[]> {
  return fetchJSON<Transcript[]>(`/calls/${callId}/transcripts`);
}
