import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue

# Configuration and PyAudio initialization code remains the same

# Initialize the plot for vertical bars with the dB scale adjusted
fig, ax = plt.subplots()
x = np.arange(1, CHANNELS + 1)  # Channel numbers as x-axis
bars = ax.bar(x, np.zeros(CHANNELS), align='center', alpha=0.5)  # Initialize bars with zero height
ax.set_ylim(0, 100)  # Adjust y-axis limit to 0 to 100 scale


def update_bars(frame):
    if not audio_queue.empty():
        data = audio_queue.get()
        rms_values = []
        for i in range(CHANNELS):
            channel_data = data[i::CHANNELS]
            # Calculate RMS power for each channel and convert to dB scale
            rms = np.sqrt(np.mean(np.square(channel_data)))
            # Convert RMS to a scale of 0 to 100 (Assuming RMS values are pre-processed for dB conversion)
            # Here you might need to adjust the conversion based on your actual RMS value range
            scaled_rms = np.interp(rms, [min_rms, max_rms], [0, 100])

            rms_values.append(scaled_rms)

        # Update bar heights and colors
        for bar, height in zip(bars, rms_values):
            bar.set_height(height)
            if height <= 40:
                bar.set_color('green')
            elif height <= 60:
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
