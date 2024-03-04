import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

# Audio Configuration
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000

# Initialize PyAudio
p = pyaudio.PyAudio()

# Initialize Plot
fig, axs = plt.subplots(CHANNELS, 1, figsize=(10, 20))
lines = [ax.plot(np.arange(0, CHUNK), np.zeros((CHUNK,)))[0] for ax in axs]

# Function to update each channel in the plot
def update_plot(frame):
    data_int = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    for i in range(CHANNELS):
        # Extract and plot data for each channel
        data = np.array(data_int[i::CHANNELS])
        lines[i].set_ydata(data)
    return lines

def stream_audio():
    global stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=3)  # Specify the device index here
    ani = FuncAnimation(fig, update_plot, blit=True, interval=50)
    for ax in axs:
        ax.set_ylim(-32768, 32767)
        ax.set_xlim(0, CHUNK)
    plt.show()

# Run streaming in a separate thread to prevent blocking
thread = threading.Thread(target=stream_audio)
thread.start()
