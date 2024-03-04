import pyaudio
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg or another backend that works on your system
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3  # Assuming this is your desired input device index

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

# Prepare the plot for updating
fig, ax = plt.subplots()
x = np.arange(0, CHUNK)
y = np.zeros(CHUNK)
line, = ax.plot(x, y)
ax.set_ylim(-32768, 32767)

def update_plot(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        # Assuming you want to visualize only the first channel for simplicity
        line.set_ydata(data[::CHANNELS])
    return line,

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
