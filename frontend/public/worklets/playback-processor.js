class PlaybackProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._buffer = new Float32Array(0);
    this._readPos = 0;
    this.port.onmessage = (e) => {
      const int16 = new Int16Array(e.data);
      const float32 = new Float32Array(int16.length);
      for (let i = 0; i < int16.length; i++) {
        float32[i] = int16[i] / (int16[i] < 0 ? 0x8000 : 0x7fff);
      }
      // Append to buffer
      const newBuf = new Float32Array(this._buffer.length + float32.length);
      newBuf.set(this._buffer, 0);
      newBuf.set(float32, this._buffer.length);
      this._buffer = newBuf;
    };
  }

  process(inputs, outputs) {
    const output = outputs[0];
    if (!output || !output[0]) return true;
    const channel = output[0];

    for (let i = 0; i < channel.length; i++) {
      if (this._readPos < this._buffer.length) {
        channel[i] = this._buffer[this._readPos++];
      } else {
        channel[i] = 0;
      }
    }

    // Trim consumed buffer to prevent unbounded growth
    if (this._readPos > 4800) {
      this._buffer = this._buffer.slice(this._readPos);
      this._readPos = 0;
    }

    return true;
  }
}

registerProcessor("playback-processor", PlaybackProcessor);
