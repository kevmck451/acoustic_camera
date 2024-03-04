import pyaudio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Specify the backend
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3
THRESHOLD = 4000  # Define your threshold value here

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

# Prepare the plots for updating
fig, axs = plt.subplots(CHANNELS, 1, figsize=(5, 10))
lines = []
for ax in axs:
    x = np.arange(0, CHUNK)
    y = np.zeros(CHUNK)
    line, = ax.plot(x, y, color='blue')  # Set the default color to blue
    ax.set_ylim(-8192, 8192)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    lines.append(line)

fig.tight_layout(pad=1)

def update_plot(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            # Check if any value in channel_data exceeds the threshold
            if np.any(np.abs(channel_data) > THRESHOLD):
                lines[i].set_color('red')  # Change color to red if threshold is exceeded
            else:
                lines[i].set_color('blue')  # Reset to default color otherwise
            lines[i].set_ydata(channel_data)
    return lines

ani = FuncAnimation(fig, update_plot, blit=True, interval=20)

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
