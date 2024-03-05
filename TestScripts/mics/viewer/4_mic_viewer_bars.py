import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3
MAX_INT16 = np.iinfo(np.int16).max

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for transferring data from audio callback to main thread
audio_queue = queue.Queue()


def callback(in_data, frame_count, time_info, status):
    audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
    return (None, pyaudio.paContinue)


stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                stream_callback=callback)

# Initialize the plot for vertical bars
fig, ax = plt.subplots()
x = np.arange(1, CHANNELS + 1)  # Channel numbers as x-axis
bars = ax.bar(x, np.zeros(CHANNELS), align='center', alpha=0.5)  # Initialize bars with zero height
ax.set_ylim(-80, 0)  # dB range


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            # Calculate RMS and then convert to dB
            rms = np.sqrt(np.mean(np.square(channel_data)))
            rms_db = 20 * np.log10(rms / MAX_INT16 + 1e-10)  # Avoid log(0) by adding a small number

            # Set bar height based on dB value
            bars[i].set_height(rms_db)

            # Set bar color based on intensity thresholds
            if rms_db < -20:
                bars[i].set_color('green')
            elif -20 <= rms_db < -10:
                bars[i].set_color('yellow')
            else:
                bars[i].set_color('red')

    return [bar for bar in bars]


ani = FuncAnimation(fig, update_bars, blit=True, interval=20)

# Start the stream and show the plot
stream.start_stream()

try:
    plt.show()
except KeyboardInterrupt:
    pass

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()
