
import matplotlib
matplotlib.use('TkAgg')  # Specify the backend
import matplotlib.pyplot as plt
import threading
import pyaudio
import numpy as np
import queue


class Matrix_Mics:
    def __init__(self, device_index=3, chunk_size=16384, audio_dtype=pyaudio.paInt16, mic_channels=8,
                 sample_rate=48000):
        self.device_index = device_index
        self.chunk_size = chunk_size
        self.audio_dtype = audio_dtype
        self.mic_channels = mic_channels
        self.sample_rate = sample_rate

        self.audio_queue = queue.Queue()
        self.p = pyaudio.PyAudio()
        self.stream = None

        self.stream_thread = threading.Thread(target=self.start_stream, daemon=True).start()

    def audio_callback(self, in_data, frame_count, time_info, status):
        self.audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
        return (None, pyaudio.paContinue)

    def start_stream(self):
        self.stream = self.p.open(format=self.audio_dtype,
                                  channels=self.mic_channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk_size,
                                  input_device_index=self.device_index,
                                  stream_callback=self.audio_callback)

        self.stream.start_stream()

    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def terminate(self):
        self.p.terminate()

    def get_audio_data(self):
        if not self.audio_queue.empty():
            return self.audio_queue.get()
        else:
            return None

    def ch8_viewer_figure(self):
        fig, axs = plt.subplots(self.mic_channels, 1, figsize=(2, 2), dpi=100)
        lines = []
        for ax in axs:
            x = np.arange(0, self.chunk_size)
            y = np.zeros(self.chunk_size)
            line, = ax.plot(x, y, color='blue')  # Set the default color to blue
            # ax.set_ylim(-8192, 8192)
            ax.set_ylim(-3000, 3000)
            ax.set_yticklabels([])
            ax.set_xticklabels([])
            lines.append(line)

        fig.tight_layout(pad=1)

        return fig