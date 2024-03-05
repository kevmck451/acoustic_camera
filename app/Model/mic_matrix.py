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
