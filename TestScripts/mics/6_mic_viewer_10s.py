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

# Configuration for 10 seconds of data
samples_per_channel_10s = RATE * SECONDS_TO_DISPLAY // CHANNELS

# Initialize the plots with the correct dimensions
fig, axs = plt.subplots(CHANNELS, 1, figsize=(10, 5))
lines = []
x = np.linspace(0, SECONDS_TO_DISPLAY, samples_per_channel_10s)

for ax in axs:
    # Initial y-data has the same shape as x but filled with zeros
    y = np.zeros_like(x)
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
        # Assuming audio_buffer update logic is implemented here

        # Loop through each channel to update the plot
        for i in range(CHANNELS):
            # Extract the current channel's data from the buffer
            channel_data = audio_buffer[i, :samples_per_channel_10s]

            # Update the plot color based on threshold
            if np.any(np.abs(channel_data) > THRESHOLD):
                lines[i].set_color('red')
            else:
                lines[i].set_color('blue')

            # Update the y-data of the plot
            lines[i].set_ydata(channel_data)  # Ensure channel_data shape matches x-axis

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
