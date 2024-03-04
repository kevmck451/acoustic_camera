import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 16384  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 8  # Number of audio channels
RATE = 48000  # Sample rate (samples per second)
DEVICE_INDEX = 3  # Audio input device index
THRESHOLD = 800  # Threshold value for visual indication
SECONDS_TO_DISPLAY = 10  # Length of the audio data to display in seconds

# Calculate the number of samples needed to display 10 seconds of audio per channel
total_samples_per_channel = RATE * SECONDS_TO_DISPLAY

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

# Initialize the rolling window buffer
rolling_window = np.zeros((CHANNELS, total_samples_per_channel), dtype=np.int16)

# Prepare the plots
fig, axs = plt.subplots(CHANNELS, 1, figsize=(10, 5))
lines = []

# Set up the initial plot with correct dimensions
for ax in axs:
    line, = ax.plot(np.zeros(total_samples_per_channel // CHANNELS), color='blue')
    ax.set_ylim(-3000, 3000)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    lines.append(line)

fig.tight_layout(pad=1)

def update_plot(frame):
    global rolling_window
    while not audio_queue.empty():
        data = audio_queue.get()
        reshaped_data = data.reshape(-1, CHANNELS).T
        # Update rolling window: shift left and append new data
        rolling_window = np.roll(rolling_window, -reshaped_data.shape[1], axis=1)
        rolling_window[:, -reshaped_data.shape[1]:] = reshaped_data

    # Update plot lines for each channel
    for i in range(CHANNELS):
        channel_data = rolling_window[i, :]
        lines[i].set_ydata(channel_data)
        if np.any(np.abs(channel_data) > THRESHOLD):
            lines[i].set_color('red')
        else:
            lines[i].set_color('blue')

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
