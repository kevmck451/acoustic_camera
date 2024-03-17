import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 4096  # Adjust based on experimentation
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
DEVICE_INDEX = 3
THRESHOLD = 800
DISPLAY_SECONDS = 2  # Display last 2 seconds of data

# Calculate total samples to display for 2-second window
total_samples = RATE * DISPLAY_SECONDS

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for transferring data from audio callback to main thread
audio_queue = queue.Queue()

# Initialize a rolling buffer
audio_buffer = np.zeros(total_samples, dtype=np.int16)

def callback(in_data, frame_count, time_info, status):
    if status:
        print(f"Error status: {status}")
    audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
    return (None, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                stream_callback=callback)

fig, ax = plt.subplots(1, 1, figsize=(10, 5))
x = np.linspace(0, DISPLAY_SECONDS, total_samples)
line, = ax.plot(x, np.zeros(total_samples), color='blue')
ax.set_ylim(-3000, 3000)
ax.set_xlim(0, DISPLAY_SECONDS)

def update_plot(frame):
    global audio_buffer
    while not audio_queue.empty():
        data = audio_queue.get()
        # Efficiently roll the buffer and append new data
        audio_buffer = np.roll(audio_buffer, -len(data))
        audio_buffer[-len(data):] = data

    # The plot updates with the rolling buffer
    line.set_ydata(audio_buffer)
    return line,

ani = FuncAnimation(fig, update_plot, blit=False, interval=20)

stream.start_stream()

try:
    plt.show()
except KeyboardInterrupt:
    print("Stream stopped")

stream.stop_stream()
stream.close()
p.terminate()
