class CaptureProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._buffer = new Float32Array(0);
  }

  process(inputs) {
    const input = inputs[0];
    if (!input || !input[0]) return true;

    const channelData = input[0];

    // Downsample from 48kHz to 16kHz (take every 3rd sample)
    const downsampled = new Float32Array(Math.floor(channelData.length / 3));
    for (let i = 0; i < downsampled.length; i++) {
      downsampled[i] = channelData[i * 3];
    }

    // Convert Float32 [-1, 1] to Int16 PCM
    const pcm = new Int16Array(downsampled.length);
    for (let i = 0; i < downsampled.length; i++) {
      const s = Math.max(-1, Math.min(1, downsampled[i]));
      pcm[i] = s < 0 ? s * 0x8000 : s * 0x7fff;
    }

    this.port.postMessage(pcm.buffer, [pcm.buffer]);
    return true;
  }
}

registerProcessor("capture-processor", CaptureProcessor);
