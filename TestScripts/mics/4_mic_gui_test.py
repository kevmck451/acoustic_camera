import customtkinter as ctk
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Ensure TkAgg is used
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyaudio
import queue

# Configuration
CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3
THRESHOLD = 4000

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for audio data
audio_queue = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
    return (None, pyaudio.paContinue)

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                stream_callback=audio_callback)

# Create customTkinter application window
app = ctk.CTk()
app.geometry("800x600")

# Create a Matplotlib figure and axes
fig = Figure(figsize=(5, 5))
axs = fig.subplots(CHANNELS, 1)
lines = []

for ax in axs:
    x = np.arange(0, CHUNK)
    y = np.zeros(CHUNK)
    line, = ax.plot(x, y, color='blue')
    ax.set_ylim(-8192, 8192)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    lines.append(line)

fig.tight_layout(pad=1)

# Embed the Matplotlib figure in the customTkinter window
canvas = FigureCanvasTkAgg(fig, master=app)  # master specifies the Tkinter widget
canvas.draw()
canvas.get_tk_widget().pack(fill="both", expand=True)

def update_plot(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            if np.any(np.abs(channel_data) > THRESHOLD):
                lines[i].set_color('red')
            else:
                lines[i].set_color('blue')
            lines[i].set_ydata(channel_data)
    return lines

ani = FuncAnimation(fig, update_plot, blit=True, interval=20)

# Start the audio stream
stream.start_stream()

# Run the customTkinter application
try:
    app.mainloop()
except KeyboardInterrupt:
    pass

# Cleanup on exit
stream.stop_stream()
stream.close()
p.terminate()
