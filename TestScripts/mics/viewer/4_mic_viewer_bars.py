import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import queue
import pyaudio

# Configuration
CHUNK = 16384
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3

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
ax.set_ylim(0, 100)  # Adjusted for the new dB scale range


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        for i, bar in enumerate(bars):
            channel_data = data[i::CHANNELS]
            rms = np.sqrt(np.mean(np.square(channel_data)))

            # Convert RMS to a dB scale (simulated conversion for demonstration)
            db_value = 20 * np.log10(rms / np.max(np.abs(data))) + 100  # Adjusting formula to fit the scale

            # Ensure db_value falls within the 0 to 100 range
            db_value = np.clip(db_value, 0, 100)

            # Update bar height
            bar.set_height(db_value)

            # Update bar color based on intensity
            if db_value <= 40:
                bar.set_color('green')
            elif db_value <= 60:
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
