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
THRESHOLD = 800
SECONDS_TO_DISPLAY = 10

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for transferring data
audio_queue = queue.Queue()

# Calculate total samples to display for 10-second window per channel
samples_per_channel = RATE * SECONDS_TO_DISPLAY
# Initialize a buffer to store the audio data
audio_buffer = np.zeros((CHANNELS, samples_per_channel), dtype=np.int16)


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

# Prepare the plots
fig, axs = plt.subplots(CHANNELS, 1, figsize=(10, 5))
lines = []

# Set up the initial plot
x = np.arange(0, samples_per_channel // CHANNELS)
for ax in axs:
    y = np.zeros(samples_per_channel // CHANNELS)
    line, = ax.plot(x, y, color='blue')
    ax.set_ylim(-3000, 3000)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    lines.append(line)

fig.tight_layout(pad=1)


def update_plot(frame):
    global audio_buffer
    if not audio_queue.empty():
        data = audio_queue.get()
        # Reshape data and append to the buffer, remove oldest data
        reshaped_data = data.reshape(-1, CHANNELS).T
        audio_buffer = np.hstack((audio_buffer[:, reshaped_data.shape[1]:], reshaped_data))

        for i in range(CHANNELS):
            channel_data = audio_buffer[i, :]
            # Update line data
            if np.any(np.abs(channel_data) > THRESHOLD):
                lines[i].set_color('red')
            else:
                lines[i].set_color('blue')
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
