export class AudioPlayback {
  private ctx: AudioContext | null = null;
  private node: AudioWorkletNode | null = null;

  async start(): Promise<void> {
    this.ctx = new AudioContext({ sampleRate: 24000 });
    await this.ctx.audioWorklet.addModule("/worklets/playback-processor.js");
    this.node = new AudioWorkletNode(this.ctx, "playback-processor");
    this.node.connect(this.ctx.destination);
  }

  pushPCM(pcm: Int16Array): void {
    if (!this.node) return;
    this.node.port.postMessage(pcm.buffer, [pcm.buffer]);
  }

  stop(): void {
    this.node?.disconnect();
    this.ctx?.close();
    this.node = null;
    this.ctx = null;
  }
}
