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
ax.set_ylim(0, 10)  # Set a suitable y-axis limit


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        rms_values = []
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            # Calculate RMS power for each channel
            rms = np.sqrt(np.mean(np.square(channel_data)))
            rms_values.append(rms)

        # Normalize or scale RMS values to fit within the plot's y-axis limits if necessary
        # For this example, we assume RMS values are already suitable or you can apply scaling

        # Update bar heights
        for bar, height in zip(bars, rms_values):
            bar.set_height(height)

    return bars


ani = FuncAnimation(fig, update_bars, blit=False, interval=20)

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
