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
DEVICE_INDEX = 3  # Ensure the device index is set as requested

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

# Initialize the plot for vertical bars
fig, ax = plt.subplots()
x = np.arange(1, CHANNELS + 1)  # Channel numbers as x-axis
bars = ax.bar(x, np.zeros(CHANNELS), align='center', alpha=0.5)  # Initialize bars with zero height
ax.set_ylim(0, 100)  # Example range, adjust based on actual signal power

def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        rms_values = [np.sqrt(np.mean(np.square(data[i::CHANNELS]))) for i in range(CHANNELS)]
        max_rms = np.max(rms_values) if np.max(rms_values) != 0 else 1  # Avoid division by zero
        normalized_rms_values = [rms / max_rms * 100 for rms in rms_values]  # Normalize to 0-100 scale

        for bar, rms_value in zip(bars, normalized_rms_values):
            bar.set_height(rms_value)  # Update the height of the bar

            # Update the color based on the range
            if rms_value < 33.33:
                bar.set_color('green')
            elif rms_value < 66.66:
                bar.set_color('yellow')
            else:
                bar.set_color('red')

    return bars

ani = FuncAnimation(fig, update_bars, blit=False, interval=20)

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
