import customtkinter as ctk
import numpy as np
import matplotlib

matplotlib.use('TkAgg')  # Ensure TkAgg is used
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pyaudio
import queue
import threading

# Your original audio configuration
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

# CustomTkinter application window
app = ctk.CTk()
app.geometry("800x600")

# Matplotlib figure and axes for each channel
fig = Figure(figsize=(5, 5), dpi=100)
axs = fig.subplots(CHANNELS, 1)
lines = []

for i, ax in enumerate(axs):
    ax.set_ylim(-8192, 8192)
    ax.set_xlim(0, CHUNK / CHANNELS)
    line, = ax.plot([], [], lw=1)
    lines.append(line)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()

# Embed the Matplotlib figure in the customTkinter window
canvas = FigureCanvasTkAgg(fig, master=app)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)


def update_plot():
    if not audio_queue.empty():
        data = audio_queue.get()
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            if np.any(np.abs(channel_data) > THRESHOLD):
                lines[i].set_color('red')
            else:
                lines[i].set_color('blue')
            lines[i].set_ydata(channel_data)
            lines[i].set_xdata(np.arange(len(channel_data)))
        canvas.draw()

    # Schedule the next update
    app.after(1, update_plot)


def start_stream_and_update():
    stream.start_stream()
    update_plot()


# Button functionality to open Matplotlib window
def plot_audio_window():
    # Fetch the latest chunk of audio data for each channel
    if not audio_queue.empty():
        data = audio_queue.get()
        plt.figure(figsize=(10, 8))

        for i in range(CHANNELS):
            plt.subplot(CHANNELS, 1, i + 1)
            channel_data = data[i::CHANNELS]
            plt.plot(np.arange(len(channel_data)), channel_data)
            if np.any(np.abs(channel_data) > THRESHOLD):
                plt.title(f"Channel {i + 1} - Over Threshold", color='red')
            else:
                plt.title(f"Channel {i + 1}", color='blue')
            plt.ylim(-8192, 8192)

        plt.tight_layout()
        plt.show()


# Adding button to the GUI
plot_button = ctk.CTkButton(app, text="Plot Audio in New Window", command=plot_audio_window)
plot_button.pack(pady=20)

# Use threading to prevent audio stream from blocking GUI
thread = threading.Thread(target=start_stream_and_update, daemon=True)
thread.start()

# Run the customTkinter application
app.mainloop()

# Cleanup on exit
stream.stop_stream()
stream.close()
p.terminate()
