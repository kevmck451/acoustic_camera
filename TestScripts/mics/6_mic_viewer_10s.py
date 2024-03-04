import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 1024  # Smaller chunk size for more frequent updates
FORMAT = pyaudio.paInt16
CHANNELS = 1  # Simplified to 1 channel for clarity
RATE = 48000
DEVICE_INDEX = None  # None for default device
THRESHOLD = 800
DISPLAY_SECONDS = 10  # Display last 10 seconds of data

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for transferring data from audio callback to main thread
audio_queue = queue.Queue()

# Calculate total samples to display for 10-second window
total_samples = RATE * DISPLAY_SECONDS

# Initialize an empty buffer
audio_buffer = np.empty(0, dtype=np.int16)


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

# Prepare the plot
fig, ax = plt.subplots(1, 1, figsize=(10, 5))
x = np.linspace(0, DISPLAY_SECONDS, total_samples)
line, = ax.plot(x, np.zeros(total_samples), color='blue')
ax.set_ylim(-3000, 3000)
ax.set_xlim(0, DISPLAY_SECONDS)


def update_plot(frame):
    global audio_buffer
    while not audio_queue.empty():
        data = audio_queue.get()
        audio_buffer = np.append(audio_buffer, data)
        # Keep only the last 10 seconds of data
        if len(audio_buffer) > total_samples:
            audio_buffer = audio_buffer[-total_samples:]

    # Update plot
    current_length = len(audio_buffer)
    x_data = np.linspace(0, DISPLAY_SECONDS * current_length / total_samples, current_length)
    line.set_data(x_data, audio_buffer)
    ax.set_xlim(0, max(x_data[-1], 1))  # Update xlim to show up to 10 seconds
    return line,


ani = FuncAnimation(fig, update_plot, blit=False, interval=20)

# Start the stream and show the plot
stream.start_stream()

try:
    plt.show()
except KeyboardInterrupt:
    print("Stream stopped")

# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()
