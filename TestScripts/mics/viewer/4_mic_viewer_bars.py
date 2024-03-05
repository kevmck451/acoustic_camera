import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import queue

# Configuration
CHUNK = 1024  # Smaller chunk size to increase responsiveness
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 48000
DEVICE_INDEX = 3  # Ensure this is the correct device index

# Initialize PyAudio
p = pyaudio.PyAudio()

# Queue for transferring data from audio callback to main thread
audio_queue = queue.Queue()


def callback(in_data, frame_count, time_info, status):
    audio_queue.put(np.frombuffer(in_data, dtype=np.int16))
    return (None, pyaudio.paContinue)


# Open the audio stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX,
                stream_callback=callback)

# Initialize the plot for displaying the audio signal power
fig, ax = plt.subplots()
x = np.arange(1, CHANNELS + 1)
bars = ax.bar(x, np.zeros(CHANNELS), color='green')
ax.set_ylim(0, 100)  # Example range


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        # Calculate the RMS values
        rms_values = [10 * np.log10(np.mean(np.square(data[i::CHANNELS]))) if np.any(data[i::CHANNELS]) else 0 for i in
                      range(CHANNELS)]

        # Normalize RMS values to fit the 0-100 scale (assuming dB scale for demonstration)
        max_possible_db = 120.0  # Adjust based on your audio system's maximum dB
        scaled_rms_values = [(value + max_possible_db) / max_possible_db * 100 for value in rms_values]

        # Update bars
        for bar, value in zip(bars, scaled_rms_values):
            bar.set_height(value)
            # Update color based on value
            if value <= 33.33:
                bar.set_color('green')
            elif value <= 66.67:
                bar.set_color('yellow')
            else:
                bar.set_color('red')

    return bars


ani = FuncAnimation(fig, update_bars, blit=False, interval=50)

# Start the audio stream and show the plot
stream.start_stream()

try:
    plt.show()
except KeyboardInterrupt:
    print("Stream stopped by user.")

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
