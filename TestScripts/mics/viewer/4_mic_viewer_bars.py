import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyaudio
import queue

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
    # Put the incoming data into the queue
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

# Prepare the plot for displaying the audio signal power
fig, ax = plt.subplots()
x = np.arange(1, CHANNELS + 1)
bars = ax.bar(x, np.zeros(CHANNELS))
ax.set_ylim(0, 100)  # Example range, adjust based on actual signal power


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        # Calculate the RMS values, handling cases where data might lead to invalid operations
        rms_values = [np.sqrt(np.mean(np.square(data[i::CHANNELS]))) if np.any(data[i::CHANNELS]) else 0 for i in
                      range(CHANNELS)]
        # Normalize or scale RMS values here if necessary

        # Determine the color based on the intensity (lower 1/3 green, middle 1/3 yellow, top 1/3 red)
        for bar, rms in zip(bars, rms_values):
            bar_height = rms  # This should be scaled appropriately
            bar.set_height(bar_height)
            if bar_height < 33.33:
                bar.set_color('green')
            elif bar_height < 66.67:
                bar.set_color('yellow')
            else:
                bar.set_color('red')

    return bars


ani = FuncAnimation(fig, update_bars, blit=False, interval=50)

# Start the audio stream and display the plot
stream.start_stream()

try:
    plt.show()
except KeyboardInterrupt:
    print("Stream stopped by user.")

# Cleanup on exit
stream.stop_stream()
stream.close()
p.terminate()
