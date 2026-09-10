export interface VoiceCallbacks {
  onTranscript: (role: "user" | "agent", text: string) => void;
  onStatus: (state: "listening" | "thinking" | "speaking") => void;
  onToolCall: (tool: string, result: string) => void;
  onDone: () => void;
  onError: (message: string) => void;
  onAudio: (pcm: Int16Array) => void;
}

export class VoiceClient {
  private ws: WebSocket | null = null;
  private callbacks: VoiceCallbacks;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private shouldReconnect = true;

  constructor(callbacks: VoiceCallbacks) {
    this.callbacks = callbacks;
  }

  start(): void {
    this.shouldReconnect = true;
    this.connect();
  }

  private connect(): void {
    const wsBase = import.meta.env.VITE_WS_URL;
    let url: string;
    if (wsBase) {
      url = `${wsBase}/ws/call`;
    } else {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      url = `${protocol}//${window.location.host}/ws/call`;
    }
    this.ws = new WebSocket(url);
    this.ws.binaryType = "arraybuffer";

    this.ws.onopen = () => {
      this.ws?.send(JSON.stringify({ type: "start" }));
    };

    this.ws.onmessage = (event) => {
      if (event.data instanceof ArrayBuffer) {
        this.callbacks.onAudio(new Int16Array(event.data));
        return;
      }

      const msg = JSON.parse(event.data);
      switch (msg.type) {
        case "status":
          this.callbacks.onStatus(msg.state);
          break;
        case "transcript":
          this.callbacks.onTranscript(msg.role, msg.text);
          break;
        case "tool_call":
          this.callbacks.onToolCall(msg.tool, msg.result);
          break;
        case "done":
          this.callbacks.onDone();
          break;
        case "error":
          this.callbacks.onError(msg.message);
          break;
      }
    };

    this.ws.onclose = () => {
      if (this.shouldReconnect) {
        this.reconnectTimer = setTimeout(() => this.connect(), 2000);
      }
    };

    this.ws.onerror = () => {
      this.ws?.close();
    };
  }

  sendAudio(pcm: Int16Array): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(pcm.buffer);
    }
  }

  interrupt(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: "interrupt" }));
    }
  }

  stop(): void {
    this.shouldReconnect = false;
    if (this.reconnectTimer) clearTimeout(this.reconnectTimer);
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({ type: "stop" }));
    }
    this.ws?.close();
    this.ws = null;
  }
}
